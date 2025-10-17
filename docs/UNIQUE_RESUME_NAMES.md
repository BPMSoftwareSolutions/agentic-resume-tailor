# Unique Resume Names Constraint

## Overview

Resume names must be unique across the entire resume database. This constraint prevents data confusion and ensures that resume identification by name is reliable.

## Implementation

### 1. Resume Model Changes (`src/models/resume.py`)

#### New Helper Method: `_name_exists()`

```python
def _name_exists(self, name: str, exclude_id: Optional[str] = None) -> bool:
    """
    Check if a resume with the given name already exists.
    
    Args:
        name: Resume name to check
        exclude_id: Optional resume ID to exclude from check (for updates)
    
    Returns:
        True if name exists, False otherwise
    """
```

**Features:**
- Case-insensitive name matching
- Optional `exclude_id` parameter for updates (allows a resume to keep its own name)

#### Updated `create()` Method

Now validates that the resume name is unique before creating:

```python
def create(self, data, name, ...):
    # Check for duplicate name
    if self._name_exists(name):
        raise ValueError(f"A resume with the name '{name}' already exists...")
```

**Error Handling:**
- Raises `ValueError` if name already exists
- Error message clearly indicates the conflict

#### Updated `update_metadata()` Method

Now validates unique names when updating resume metadata:

```python
def update_metadata(self, resume_id, **kwargs):
    # Check for duplicate name if updating name
    if "name" in kwargs:
        new_name = kwargs["name"]
        if self._name_exists(new_name, exclude_id=resume_id):
            raise ValueError(f"A resume with the name '{new_name}' already exists...")
```

**Features:**
- Allows a resume to keep its own name
- Prevents renaming to an existing name
- Raises `ValueError` on conflict

### 2. Duplicate Resume Script (`src/duplicate_resume.py`)

Updated error handling to catch and report duplicate name errors:

```python
try:
    new_metadata = resume_model.duplicate(source_id, new_name)
except ValueError as e:
    raise ValueError(str(e))
```

**User Guidance:**
When a duplicate name error occurs, the script suggests alternatives:
- Include company name (e.g., 'Ford', 'GM')
- Include position title (e.g., 'Senior Engineer', 'Manager')
- Include date or version (e.g., 'v2', '2025-01')

### 3. API Endpoint (`src/api/app.py`)

Updated `/api/resumes` POST endpoint to handle duplicate name errors:

```python
try:
    metadata = resume_model.create(...)
except ValueError as e:
    return jsonify({"error": str(e)}), 409  # 409 Conflict
```

**HTTP Status Codes:**
- `201 Created`: Resume created successfully
- `409 Conflict`: Resume name already exists
- `400 Bad Request`: Invalid request data
- `500 Internal Server Error`: Unexpected error

### 4. Cleanup Script (`src/cleanup_duplicate_resumes.py`)

One-time script to clean up existing duplicate resumes:

```bash
# Show what would be deleted (dry run)
python src/cleanup_duplicate_resumes.py --dry-run

# Actually delete duplicate resumes
python src/cleanup_duplicate_resumes.py
```

**Behavior:**
- Identifies all resumes with duplicate names
- For each duplicate name, keeps the most recently updated resume
- Deletes all other copies
- Provides detailed output of what will be deleted

**Results:**
- Reduced from 28 resumes to 9 unique resumes
- Deleted 19 duplicate entries

## Testing

Comprehensive unit tests in `tests/test_resume_unique_names.py`:

```bash
python -m pytest tests/test_resume_unique_names.py -v
```

**Test Coverage:**
- ✅ Creating resume with unique name succeeds
- ✅ Creating resume with duplicate name raises error
- ✅ Duplicate check is case-insensitive
- ✅ Duplicating resume with unique name succeeds
- ✅ Duplicating resume with duplicate name raises error
- ✅ Updating metadata with unique name succeeds
- ✅ Updating metadata with duplicate name raises error
- ✅ Updating resume with its own name is allowed
- ✅ Helper method correctly identifies existing names
- ✅ Helper method respects exclude_id parameter

**All 10 tests pass ✅**

## Usage Examples

### Creating a Resume

```python
from src.models.resume import Resume

resume_model = Resume(Path("data"))

# This succeeds
metadata = resume_model.create(
    data=resume_data,
    name="Ford Resume"
)

# This raises ValueError
try:
    metadata = resume_model.create(
        data=resume_data,
        name="Ford Resume"  # Already exists!
    )
except ValueError as e:
    print(f"Error: {e}")
```

### Duplicating a Resume

```bash
# This succeeds
python src/duplicate_resume.py --resume "Ford" --new-name "Ford v2"

# This fails with helpful error message
python src/duplicate_resume.py --resume "Ford" --new-name "Ford"
```

### Updating Resume Name

```python
# This succeeds
resume_model.update_metadata(resume_id, name="New Name")

# This raises ValueError
resume_model.update_metadata(resume_id, name="Existing Resume Name")
```

## Error Messages

### When Creating Duplicate

```
❌ A resume with the name 'Ford Resume' already exists. Please use a different name.

💡 Tip: Use a unique name for the new resume. You can include:
   - Company name (e.g., 'Ford', 'GM')
   - Position title (e.g., 'Senior Engineer', 'Manager')
   - Date or version (e.g., 'v2', '2025-01')
```

### API Response (409 Conflict)

```json
{
  "error": "A resume with the name 'Ford Resume' already exists. Please use a different name."
}
```

## Benefits

1. **Data Integrity**: Prevents accidental duplicate resumes
2. **Reliable Lookup**: Resume names can be used as unique identifiers
3. **User Experience**: Clear error messages guide users to fix issues
4. **Consistency**: Case-insensitive matching prevents subtle duplicates
5. **Flexibility**: Allows updating other metadata while keeping name

## Migration

If you have existing duplicate resumes:

```bash
# Run the cleanup script
python src/cleanup_duplicate_resumes.py --dry-run  # Preview changes
python src/cleanup_duplicate_resumes.py            # Apply changes
```

The script keeps the most recently updated copy of each duplicate name.

