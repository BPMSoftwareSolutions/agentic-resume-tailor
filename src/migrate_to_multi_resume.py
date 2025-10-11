"""
Migration script to convert existing master_resume.json to multi-resume structure.

This script:
1. Reads the existing master_resume.json
2. Creates it as the master resume in the new structure
3. Preserves all existing data
4. Creates backup of original file

Related to GitHub Issue #6
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from models.resume import Resume


def migrate_master_resume(data_dir: Path, dry_run: bool = False):
    """
    Migrate existing master_resume.json to new multi-resume structure.
    
    Args:
        data_dir: Data directory path
        dry_run: If True, only show what would be done without making changes
    """
    master_resume_path = data_dir / "master_resume.json"
    
    # Check if master resume exists
    if not master_resume_path.exists():
        print(f"❌ Master resume not found at {master_resume_path}")
        return False
    
    print(f"📄 Found master resume at {master_resume_path}")
    
    # Load master resume data
    try:
        with open(master_resume_path, 'r', encoding='utf-8') as f:
            master_data = json.load(f)
        print(f"✅ Loaded master resume data")
    except Exception as e:
        print(f"❌ Failed to load master resume: {e}")
        return False
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")
        print(f"Would create master resume in data/resumes/")
        print(f"Would backup original to master_resume_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        return True
    
    # Create backup
    backup_path = data_dir / f"master_resume_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        shutil.copy2(master_resume_path, backup_path)
        print(f"✅ Created backup at {backup_path}")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return False
    
    # Initialize Resume model
    resume_model = Resume(data_dir)
    
    # Check if master resume already exists in new structure
    existing_master = resume_model.get_master_metadata()
    if existing_master:
        print(f"⚠️  Master resume already exists in new structure: {existing_master.name}")
        response = input("Do you want to overwrite it? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return False
        # Delete existing master
        resume_model.delete(existing_master.id)
        print(f"✅ Deleted existing master resume")
    
    # Create master resume in new structure
    try:
        metadata = resume_model.create(
            data=master_data,
            name="Master Resume",
            is_master=True,
            description="Primary resume containing all experience and skills"
        )
        print(f"✅ Created master resume in new structure")
        print(f"   ID: {metadata.id}")
        print(f"   Name: {metadata.name}")
        print(f"   Created: {metadata.created_at}")
    except Exception as e:
        print(f"❌ Failed to create master resume in new structure: {e}")
        return False
    
    print("\n✅ Migration completed successfully!")
    print(f"   - Master resume saved to: data/resumes/{metadata.id}.json")
    print(f"   - Original backed up to: {backup_path.name}")
    print(f"   - Index created at: data/resumes/index.json")
    
    return True


def main():
    """Main migration function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate master_resume.json to multi-resume structure"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).parent.parent / "data",
        help="Data directory path (default: ../data)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Master Resume Migration Tool")
    print("=" * 60)
    print()
    
    success = migrate_master_resume(args.data_dir, args.dry_run)
    
    if success:
        print("\n✅ Migration successful!")
        if not args.dry_run:
            print("\nNext steps:")
            print("1. Verify the migrated data in data/resumes/")
            print("2. Test the new API endpoints")
            print("3. Update the web interface to use multi-resume support")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

