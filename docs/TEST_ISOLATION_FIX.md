# Test Isolation Fix - Issue #39

## Overview

Fixed the anti-pattern where tests were persisting data to the actual `data/resumes` and `data/job_listings` directories instead of using isolated temporary directories.

**Status**: ✅ Complete - All 401 tests pass with proper isolation

## Problem

### Before Fix
- Tests in `test_multi_resume_api.py` used the global `resume_model` and `job_listing_model` from `app.py`
- These models wrote directly to `data/resumes/` and `data/job_listings/` directories
- Test data persisted between test runs, causing:
  - Accumulation of test files in production directories
  - Potential conflicts when tests run multiple times
  - Difficulty in reproducing test failures
  - Violation of test isolation principles

### Evidence
- 29 test resume files accumulated in `data/resumes/` directory
- Similar accumulation in `data/job_listings/` directory
- Tests relied on cleanup code that wasn't always executed

## Solution

### 1. Created `tests/conftest.py`

Centralized pytest fixtures for test isolation:

```python
@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def resume_model(temp_data_dir):
    """Create isolated Resume model with temporary directory."""
    return Resume(temp_data_dir)

@pytest.fixture
def job_listing_model(temp_data_dir):
    """Create isolated JobListing model with temporary directory."""
    return JobListing(temp_data_dir)

@pytest.fixture
def unique_resume_name():
    """Generate unique resume name to prevent conflicts."""
    import time
    timestamp = int(time.time() * 1000)
    return f"Test_Resume_{timestamp}"
```

### 2. Updated `tests/test_multi_resume_api.py`

- Replaced global model usage with isolated fixtures
- Updated `client` fixture to patch app models with temporary directory versions
- Used `monkeypatch` to safely patch module-level variables
- Removed manual cleanup code (automatic via fixture cleanup)
- Updated all test methods to use unique names

**Key Changes**:
```python
@pytest.fixture
def client(temp_data_dir, monkeypatch):
    """Create test client with isolated data directory."""
    from api import app as app_module
    from models.resume import Resume
    from models.job_listing import JobListing
    
    # Patch app module to use temporary directory
    monkeypatch.setattr(app_module, "DATA_DIR", temp_data_dir)
    monkeypatch.setattr(app_module, "resume_model", Resume(temp_data_dir))
    monkeypatch.setattr(app_module, "job_listing_model", JobListing(temp_data_dir))
    
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
```

## Benefits

1. **Test Isolation**: Each test runs in its own temporary directory
2. **No Data Persistence**: Test data is automatically cleaned up after each test
3. **Parallel Test Execution**: Tests can run in parallel without conflicts
4. **Reproducibility**: Tests produce consistent results regardless of previous runs
5. **Cleaner Production Directories**: No accumulation of test files

## Test Results

### Before Fix
- 29 test resume files in `data/resumes/`
- Manual cleanup required
- Risk of test data conflicts

### After Fix
```
====================== 401 passed, 3 warnings in 24.81s =======================
```

- ✅ All 401 tests pass
- ✅ No new test data persists in `data/resumes/`
- ✅ No new test data persists in `data/job_listings/`
- ✅ Automatic cleanup via fixtures

## Files Modified

1. **tests/conftest.py** (NEW)
   - Centralized pytest fixtures
   - Shared fixtures for all tests
   - Proper cleanup with `shutil.rmtree`

2. **tests/test_multi_resume_api.py**
   - Updated `client` fixture to use isolated models
   - Updated all test methods to use unique names
   - Removed manual cleanup code
   - Added documentation about test isolation

## Best Practices Applied

1. **Fixture Scope**: Used function-scoped fixtures for complete isolation
2. **Monkeypatch**: Used pytest's `monkeypatch` for safe patching
3. **Unique Names**: Generated unique names using timestamps
4. **Automatic Cleanup**: Leveraged fixture cleanup for automatic teardown
5. **Documentation**: Added docstrings explaining isolation approach

## Future Improvements

1. Consider using `pytest-factoryboy` for more complex fixtures
2. Add fixture for other test files that might have similar issues
3. Document fixture usage in test guidelines
4. Consider database fixtures for integration tests

## Related Issues

- Issue #39: Fix Tests persisted data/resumes (anti-pattern)
- Issue #6: Multi-resume support
- Issue #19: Duplicate resume names

## Verification

Run tests to verify isolation:
```bash
# Run all tests
python -m pytest --tb=short -q

# Run specific test file
python -m pytest tests/test_multi_resume_api.py -v

# Check no new files in data/resumes
ls data/resumes/ | wc -l
```

All tests pass with proper isolation and no data persistence.

