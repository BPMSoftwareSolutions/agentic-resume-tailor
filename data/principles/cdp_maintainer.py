from typing import Dict, Any, List, Optional, Tuple
def ensure_top_tech_stacks(obj: Dict[str, Any]) -> int:
    """
    Ensures every best practice has a 'top_tech_stacks' node (empty list if missing).
    Returns count of practices updated.
    """
    updated = 0
    for a in get_pipeline(obj).get("aspects", []):
        for k in a.get("key_activities", []):
            for p in k.get("best_practices", []):
                if "top_tech_stacks" not in p:
                    p["top_tech_stacks"] = []
                    updated += 1
    return updated
def cmd_ensure_top_tech_stacks(args):
    data = read_json(args.json)
    count = ensure_top_tech_stacks(data)
    if args.save:
        backup_file(args.json)
        write_json(args.json, data)
        print(f"🛠️ Ensured top_tech_stacks for {count} best practices and saved.")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))
#!/usr/bin/env python3
from typing import Dict, Any, List, Optional, Tuple
from typing import Dict, Any, List, Optional, Tuple
"""
CDP Maintainer
--------------
Maintain and evolve a SAFe Continuous Delivery Pipeline (CDP) hierarchical JSON.

Hierarchy:
  Pipeline -> Aspects -> Key Activities -> Best Practices

Features:
- Load/validate/save JSON
- List structure (tree view)
- Add/update aspects, activities, best practices
- Attach "top_tech_stacks" at aspect/activity/best-practice levels
- Generate stable IDs (slug-based) and ensure uniqueness
- Trim long descriptions
- Export minified (app-friendly) JSON (optionally drop metadata/long text)
- Optional: initialize from CSV (same columns used earlier)

Usage examples:
  # List the tree (compact)
  python cdp_maintainer.py list cdp_tree.json

  # Add a stack to a best-practice under Continuous Deployment -> Stage -> Blue/Green deployment
  python cdp_maintainer.py add-stack cdp_tree.json \
    --aspect "Continuous Deployment" \
    --activity "Stage" \
    --practice "Blue/Green deployment" \
    --stack "Kubernetes + Argo Rollouts + NGINX/ALB" \
    --context "Blue/green via Service/Ingress switch or target group shift."

  # Generate IDs for all nodes
  python cdp_maintainer.py gen-ids cdp_tree.json --save

  # Trim descriptions to 240 chars for app display
  python cdp_maintainer.py trim-descriptions cdp_tree.json --max 240 --save

  # Export a minified app JSON without metadata
  python cdp_maintainer.py export-min cdp_tree.json --out app_cdp.json --drop-metadata

"""

import argparse
from typing import Dict, Any, List, Optional, Tuple

import copy
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------
# Utilities
# ----------------------------

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[\s/_]+", "-", s)
    s = re.sub(r"[^a-z0-9-]+", "", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def ensure_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]

def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: str, data: Dict[str, Any], indent: int = 2) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def backup_file(path: str) -> str:
    base, ext = os.path.splitext(path)
    backup = f"{base}.bak{ext}"
    if os.path.exists(path):
        with open(path, "rb") as src, open(backup, "wb") as dst:
            dst.write(src.read())
    return backup

# ----------------------------
# Navigation helpers
# ----------------------------

def get_pipeline(obj: Dict[str, Any]) -> Dict[str, Any]:
    if "pipeline" not in obj:
        obj["pipeline"] = {"name": "Continuous Delivery Pipeline", "aspects": []}
    return obj["pipeline"]

def find_aspect(obj: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    pl = get_pipeline(obj)
    for a in pl.get("aspects", []):
        if a.get("name") == name:
            return a
    return None

def ensure_aspect(obj: Dict[str, Any], name: str, index: Optional[int]=None) -> Dict[str, Any]:
    a = find_aspect(obj, name)
    if a is None:
        a = {"name": name, "key_activities": []}
        if index is not None: a["index"] = index
        get_pipeline(obj)["aspects"].append(a)
    return a

def find_activity(aspect: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    for k in aspect.get("key_activities", []):
        if k.get("name") == name:
            return k
    return None

def ensure_activity(aspect: Dict[str, Any], name: str, index: Optional[int]=None) -> Dict[str, Any]:
    k = find_activity(aspect, name)
    if k is None:
        k = {"name": name, "best_practices": []}
        if index is not None: k["index"] = index
        aspect.setdefault("key_activities", []).append(k)
    return k

def find_practice(activity: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    for p in activity.get("best_practices", []):
        if p.get("name") == name:
            return p
    return None

def ensure_practice(activity: Dict[str, Any], name: str, label: Optional[str]=None, description: Optional[str]=None) -> Dict[str, Any]:
    p = find_practice(activity, name)
    if p is None:
        p = {"name": name}
        if label: p["label"] = label
        if description: p["description"] = description
        activity.setdefault("best_practices", []).append(p)
    else:
        if label: p.setdefault("label", label)
        if description: p.setdefault("description", description)
    return p

# ----------------------------
# Validation
# ----------------------------

def validate_tree(obj: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    pipeline = obj.get("pipeline")
    if not pipeline:
        errors.append("Missing 'pipeline' root.")
        return errors

    aspects = pipeline.get("aspects", [])
    if not isinstance(aspects, list):
        errors.append("'pipeline.aspects' must be a list.")
        return errors

    seen_aspect_names = set()
    for ai, a in enumerate(aspects):
        name = a.get("name")
        if not name:
            errors.append(f"Aspect at index {ai} missing 'name'.")
        elif name in seen_aspect_names:
            errors.append(f"Duplicate aspect name: {name}")
        seen_aspect_names.add(name)

        activities = a.get("key_activities", [])
        if not isinstance(activities, list):
            errors.append(f"Aspect '{name}' key_activities must be a list.")
            continue

        seen_activity_names = set()
        for ki, k in enumerate(activities):
            kname = k.get("name")
            if not kname:
                errors.append(f"Activity at index {ki} under aspect '{name}' missing 'name'.")
            elif kname in seen_activity_names:
                errors.append(f"Duplicate activity name under aspect '{name}': {kname}")
            seen_activity_names.add(kname)

            practices = k.get("best_practices", [])
            if not isinstance(practices, list):
                errors.append(f"Activity '{kname}' best_practices must be a list.")
                continue

            seen_practice_names = set()
            for pi, p in enumerate(practices):
                pname = p.get("name")
                if not pname:
                    errors.append(f"Best practice at index {pi} under activity '{kname}' missing 'name'.")
                elif pname in seen_practice_names:
                    errors.append(f"Duplicate best practice name under activity '{kname}': {pname}")
                seen_practice_names.add(pname)

                # Optional: validate top_tech_stacks shape
                stacks = p.get("top_tech_stacks", [])
                if stacks and not isinstance(stacks, list):
                    errors.append(f"'top_tech_stacks' on practice '{pname}' must be a list.")
                for si, s in enumerate(stacks or []):
                    if "stack" not in s:
                        errors.append(f"Stack entry #{si} on practice '{pname}' missing 'stack'.")
    return errors

# ----------------------------
# ID Generation
# ----------------------------

def gen_ids(obj: Dict[str, Any], prefix: str = "cdp") -> None:
    """
    Adds stable 'id' fields:
      aspect:   cdp.<aspect>
      activity: cdp.<aspect>.<activity>
      practice: cdp.<aspect>.<activity>.<practice>
    """
    pipeline = get_pipeline(obj)
    for a in pipeline.get("aspects", []):
        a_id = f"{prefix}.{slugify(a['name'])}"
        a["id"] = a_id
        for k in a.get("key_activities", []):
            k_id = f"{a_id}.{slugify(k['name'])}"
            k["id"] = k_id
            for p in k.get("best_practices", []):
                p_id = f"{k_id}.{slugify(p['name'])}"
                p["id"] = p_id

# ----------------------------
# Mutations
# ----------------------------

def add_stack(obj: Dict[str, Any], aspect_name: str, activity_name: Optional[str], practice_name: Optional[str], stack: str, context: Optional[str]=None, level: str="practice") -> Dict[str, Any]:
    """
    level: 'aspect' | 'activity' | 'practice'
    """
    aspect = ensure_aspect(obj, aspect_name)
    if level == "aspect":
        aspect.setdefault("top_tech_stacks", [])
        aspect["top_tech_stacks"].append({"stack": stack, "context": context} if context else {"stack": stack})
        return obj

    activity = ensure_activity(aspect, activity_name or "Activity")
    if level == "activity":
        activity.setdefault("top_tech_stacks", [])
        activity["top_tech_stacks"].append({"stack": stack, "context": context} if context else {"stack": stack})
        return obj

    # practice level
    practice = ensure_practice(activity, practice_name or "Best Practice")
    practice.setdefault("top_tech_stacks", [])
    practice["top_tech_stacks"].append({"stack": stack, "context": context} if context else {"stack": stack})
    return obj

def set_top5(obj: Dict[str, Any], aspect: str, activity: Optional[str], practice: Optional[str], stacks: List[Tuple[str, Optional[str]]], level: str="practice") -> Dict[str, Any]:
    """
    Replace top_tech_stacks with up to 5 items.
    stacks: list of (stack, context)
    """
    def pack(ss):
        out = []
        for s, c in ss[:5]:
            out.append({"stack": s, **({"context": c} if c else {})})
        return out

    a = ensure_aspect(obj, aspect)
    if level == "aspect":
        a["top_tech_stacks"] = pack(stacks)
        return obj
    k = ensure_activity(a, activity or "Activity")
    if level == "activity":
        k["top_tech_stacks"] = pack(stacks)
        return obj
    p = ensure_practice(k, practice or "Best Practice")
    p["top_tech_stacks"] = pack(stacks)
    return obj

def trim_descriptions(obj: Dict[str, Any], max_len: int) -> int:
    """
    Trims descriptions on best practices to max_len (adds ellipsis).
    Returns count of trimmed items.
    """
    trimmed = 0
    for a in get_pipeline(obj).get("aspects", []):
        for k in a.get("key_activities", []):
            for p in k.get("best_practices", []):
                desc = p.get("description")
                if isinstance(desc, str) and len(desc) > max_len:
                    p["description_short"] = desc[:max_len].rstrip() + "…"
                    trimmed += 1
    return trimmed

# ----------------------------
# CSV initialization (optional)
# ----------------------------

def init_from_csv(csv_path: str) -> Dict[str, Any]:
    try:
        import pandas as pd  # optional dependency
    except Exception as e:
        raise SystemExit("pandas is required for init-from-csv. pip install pandas") from e

    df = pd.read_csv(csv_path)
    cols = {c.strip().lower().replace(" ", "_") for c in df.columns}
    def col(*names):
        for n in names:
            nn = n.lower().replace(" ", "_")
            if nn in cols: return nn
        return None

    # normalize
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    aspect_col = col("aspect", "stage", "phase")
    aspect_idx_col = col("aspect_index", "aspect_order")
    activity_col = col("key_activity", "activity")
    activity_idx_col = col("key_activity_index", "activity_index")
    bp_col = col("best_practice", "practice")
    bp_label_col = col("best_practice_label", "label")
    desc_col = col("description", "desc")

    obj = {"pipeline": {"name": "Continuous Delivery Pipeline", "aspects": []}, "metadata": {
        "generated_at": now_iso(),
        "source_file": csv_path,
        "model_type": "hierarchical_tree"}}

    aspect_map = {}
    for _, row in df.iterrows():
        a_name = str(row.get(aspect_col)) if aspect_col else "Aspect"
        a_idx  = row.get(aspect_idx_col) if aspect_idx_col else None
        k_name = str(row.get(activity_col)) if activity_col else "Activity"
        k_idx  = row.get(activity_idx_col) if activity_idx_col else None
        p_name = str(row.get(bp_col)) if bp_col else None
        p_label= str(row.get(bp_label_col)) if bp_label_col else None
        p_desc = str(row.get(desc_col)) if desc_col else None

        a = ensure_aspect(obj, a_name, int(a_idx) if pd.notna(a_idx) else None)
        k = ensure_activity(a, k_name, int(k_idx) if pd.notna(k_idx) else None)
        if p_name and p_name != "nan":
            ensure_practice(k, p_name, p_label if p_label!="nan" else None, p_desc if p_desc!="nan" else None)

    return obj

# ----------------------------
# CLI
# ----------------------------

def cmd_list(args):
    data = read_json(args.json)
    pipeline = get_pipeline(data)
    for a in pipeline.get("aspects", []):
        a_idx = f" [{a.get('index')}]" if 'index' in a else ""
        print(f"- Aspect: {a['name']}{a_idx}")
        for k in a.get("key_activities", []):
            k_idx = f" [{k.get('index')}]" if 'index' in k else ""
            print(f"  - Activity: {k['name']}{k_idx}")
            for p in k.get("best_practices", []):
                print(f"    - Practice: {p.get('name')}")

def cmd_validate(args):
    data = read_json(args.json)
    errors = validate_tree(data)
    if errors:
        print("❌ Validation failed:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("✅ JSON is valid.")

def cmd_gen_ids(args):
    data = read_json(args.json)
    gen_ids(data, prefix=args.prefix)
    if args.save:
        backup_file(args.json)
        write_json(args.json, data)
        print("💾 IDs generated and saved.")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def cmd_add_stack(args):
    data = read_json(args.json)
    level = args.level
    if level not in ("aspect", "activity", "practice"):
        raise SystemExit("--level must be aspect|activity|practice")

    add_stack(
        data,
        aspect_name=args.aspect,
        activity_name=args.activity,
        practice_name=args.practice,
        stack=args.stack,
        context=args.context,
        level=level,
    )
    if args.save:
        backup_file(args.json)
        write_json(args.json, data)
        print("✅ Stack added and file saved.")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def cmd_set_top5(args):
    data = read_json(args.json)
    pairs: List[Tuple[str, Optional[str]]] = []
    for item in args.stacks:
        # accept "stack::context" or just "stack"
        if "::" in item:
            s, c = item.split("::", 1)
            pairs.append((s.strip(), c.strip()))
        else:
            pairs.append((item.strip(), None))
    set_top5(data, args.aspect, args.activity, args.practice, pairs, level=args.level)
    if args.save:
        backup_file(args.json)
        write_json(args.json, data)
        print("✅ Top 5 stacks set and file saved.")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def cmd_trim(args):
    data = read_json(args.json)
    count = trim_descriptions(data, max_len=args.max)
    if args.save:
        backup_file(args.json)
        write_json(args.json, data)
        print(f"✂️ Trimmed {count} descriptions and saved.")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def cmd_export_min(args):
    data = read_json(args.json)
    out = copy.deepcopy(data)
    if args.drop_metadata and "metadata" in out:
        del out["metadata"]
    if args.drop_long_text:
        # drop description, keep description_short if present
        for a in get_pipeline(out).get("aspects", []):
            for k in a.get("key_activities", []):
                for p in k.get("best_practices", []):
                    if "description_short" in p:
                        p.pop("description", None)
                    elif "description" in p and len(str(p["description"])) > args.long_text_max:
                        p["description_short"] = str(p["description"])[:args.long_text_max].rstrip() + "…"
                        p.pop("description", None)
    write_json(args.out, out, indent=None if args.minify else 2)
    print(f"📦 Exported to {args.out}")

def cmd_init_from_csv(args):
    data = init_from_csv(args.csv)
    write_json(args.out, data, indent=2)
    print(f"🌱 Initialized JSON from CSV -> {args.out}")

def build_parser():
    p = argparse.ArgumentParser(description="Maintain and evolve CDP hierarchical JSON.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("ensure-top-tech-stacks", help="Ensure every best practice has a top_tech_stacks node")
    sp.add_argument("json", help="Path to JSON")
    sp.add_argument("--save", action="store_true", help="Persist changes")
    sp.set_defaults(func=cmd_ensure_top_tech_stacks)

    sp = sub.add_parser("list", help="List a tree summary")
    sp.add_argument("json", help="Path to JSON")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("validate", help="Validate JSON structure")
    sp.add_argument("json", help="Path to JSON")
    sp.set_defaults(func=cmd_validate)

    sp = sub.add_parser("gen-ids", help="Generate stable IDs")
    sp.add_argument("json", help="Path to JSON")
    sp.add_argument("--prefix", default="cdp", help="ID prefix")
    sp.add_argument("--save", action="store_true", help="Persist changes")
    sp.set_defaults(func=cmd_gen_ids)

    sp = sub.add_parser("add-stack", help="Add a tech stack at aspect/activity/practice level")
    sp.add_argument("json", help="Path to JSON")
    sp.add_argument("--level", choices=["aspect", "activity", "practice"], default="practice")
    sp.add_argument("--aspect", required=True)
    sp.add_argument("--activity", help="Required for level activity/practice")
    sp.add_argument("--practice", help="Required for level practice")
    sp.add_argument("--stack", required=True, help="Stack label, e.g. 'Python + FastAPI + GitHub Actions'")
    sp.add_argument("--context", help="Optional context/notes")
    sp.add_argument("--save", action="store_true", help="Persist changes")
    sp.set_defaults(func=cmd_add_stack)

    sp = sub.add_parser("set-top5", help="Replace top_tech_stacks with up to 5 entries")
    sp.add_argument("json", help="Path to JSON")
    sp.add_argument("--level", choices=["aspect", "activity", "practice"], default="practice")
    sp.add_argument("--aspect", required=True)
    sp.add_argument("--activity")
    sp.add_argument("--practice")
    sp.add_argument("--stacks", nargs="+", required=True, help="Provide up to 5 items, 'stack::context' or 'stack'")
    sp.add_argument("--save", action="store_true", help="Persist changes")
    sp.set_defaults(func=cmd_set_top5)

    sp = sub.add_parser("trim-descriptions", help="Create description_short when long")
    sp.add_argument("json", help="Path to JSON")
    sp.add_argument("--max", type=int, default=240, help="Max length")
    sp.add_argument("--save", action="store_true", help="Persist changes")
    sp.set_defaults(func=cmd_trim)

    sp = sub.add_parser("export-min", help="Export minified app JSON")
    sp.add_argument("json", help="Path to input JSON")
    sp.add_argument("--out", required=True, help="Output path")
    sp.add_argument("--minify", action="store_true", help="No whitespace")
    sp.add_argument("--drop-metadata", action="store_true", help="Remove metadata block")
    sp.add_argument("--drop-long-text", action="store_true", help="Drop long 'description', keep 'description_short'")
    sp.add_argument("--long-text-max", type=int, default=240)
    sp.set_defaults(func=cmd_export_min)

    sp = sub.add_parser("init-from-csv", help="Initialize hierarchical JSON from a CSV")
    sp.add_argument("csv", help="Path to CSV")
    sp.add_argument("--out", required=True, help="Output JSON path")
    sp.set_defaults(func=cmd_init_from_csv)

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
