# CI Test Fixes

## Overview

Fixed 8 failing tests in the CI pipeline that were caused by:
1. Updated Claude default model version
2. Resume name conflicts due to unique name constraint

## Issues Fixed

### 1. Claude Model Version Test Failure

**File**: `tests/test_llm_provider.py`  
**Test**: `TestModelRegistry::test_get_default_model_claude`  
**Issue**: Test expected old Claude model `claude-3-5-sonnet-20241022` but system now uses `claude-sonnet-4-5-20250929`

**Fix**:
```python
# Before
assert model == "claude-3-5-sonnet-20241022"

# After
assert model == "claude-sonnet-4-5-20250929"
```

### 2. Resume Name Conflicts in API Tests

**File**: `tests/test_multi_resume_api.py`  
**Tests**:
- `TestResumeAPI::test_create_resume`
- `TestResumeAPI::test_get_resume`
- `TestResumeAPI::test_update_resume`
- `TestResumeAPI::test_delete_resume`

**Issue**: Tests were trying to create resumes with name "Test Resume" which already exists in the system due to unique name constraint

**Fix**: Updated each test to use unique names:
- `test_create_resume` → `"Test Resume API Create"`
- `test_get_resume` → `"Test Resume API Get"`
- `test_update_resume` → `"Test Resume API Update"` (with updated name `"Updated Resume API"`)
- `test_delete_resume` → `"Test Resume API Delete"`

### 3. Resume Name Conflicts in DOCX Export Tests

**File**: `tests/test_docx_export.py`  
**Tests**:
- `TestDocxExport::test_export_specific_resume_post`
- `TestDocxExportIntegration::test_create_and_export_resume`
- `TestDocxExportIntegration::test_tailor_and_export_resume`

**Issue**: Tests were creating resumes with hardcoded names that conflicted with existing resumes

**Fix**:
1. Added `unique_resume_name` fixture that generates timestamp-based unique names
2. Updated all three tests to use the fixture
3. Ensures no name conflicts even if tests run multiple times

```python
@pytest.fixture
def unique_resume_name():
    """Generate a unique resume name using timestamp."""
    return f"Test_Resume_{int(time.time() * 1000)}"
```

## Test Results

### Before Fixes
```
FAILED tests/test_docx_export.py::TestDocxExport::test_export_specific_resume_post
FAILED tests/test_docx_export.py::TestDocxExportIntegration::test_create_and_export_resume
FAILED tests/test_docx_export.py::TestDocxExportIntegration::test_tailor_and_export_resume
FAILED tests/test_llm_provider.py::TestModelRegistry::test_get_default_model_claude
FAILED tests/test_multi_resume_api.py::TestResumeAPI::test_create_resume
FAILED tests/test_multi_resume_api.py::TestResumeAPI::test_get_resume
FAILED tests/test_multi_resume_api.py::TestResumeAPI::test_update_resume
FAILED tests/test_multi_resume_api.py::TestResumeAPI::test_delete_resume

8 failed, 393 passed
```

### After Fixes
```
============================== 401 passed, 3 warnings in 16.38s ==============================
```

## Files Modified

1. `tests/test_llm_provider.py` - Updated Claude model version assertion
2. `tests/test_multi_resume_api.py` - Updated resume names to be unique
3. `tests/test_docx_export.py` - Added unique_resume_name fixture and updated tests

## Root Cause Analysis

### Why Tests Failed

1. **Claude Model Test**: The system was updated to use `claude-sonnet-4-5-20250929` as the default Claude model, but the test still expected the old model version.

2. **Resume Name Conflicts**: The unique resume name constraint (implemented in Issue #19) prevents creating multiple resumes with the same name. Tests were using hardcoded names like "Test Resume" which already existed in the system, causing 409 CONFLICT errors.

### Why Unique Names Fix Works

By using timestamp-based unique names (`Test_Resume_{timestamp}`), each test run generates a different name, preventing conflicts even if:
- Tests run multiple times
- Tests run in parallel
- Previous test data persists

## Verification

All 401 tests now pass:
```bash
python -m pytest --tb=short -q
# Result: 401 passed, 3 warnings in 16.38s
```

## Related Issues

- Issue #30: Claude multi-provider support
- Issue #38: Agent output truncation
- Issue #19: Duplicate resume names

## Future Improvements

1. Consider using a test database fixture to isolate test data
2. Add test cleanup fixtures to remove created resumes after each test
3. Use factory patterns for test data generation

