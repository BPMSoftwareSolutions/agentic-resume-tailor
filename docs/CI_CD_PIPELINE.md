# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions to automate testing, code quality checks, and security scanning on every push and pull request. The pipeline ensures that all code changes meet quality standards before being merged.

## Pipeline Architecture

The CI/CD pipeline consists of five main jobs that run in parallel or sequentially:

```
┌─────────────────────────────────────────────────────────┐
│                    Push/Pull Request                     │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   ┌────────┐          ┌──────┐          ┌──────────┐
   │  Test  │          │ Lint │          │ Security │
   └────────┘          └──────┘          └──────────┘
        │
        ▼
┌──────────────────┐
│ Integration Test │
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  Build Status    │
└──────────────────┘
```

## Jobs Description

### 1. Test Job

**Purpose**: Run unit tests across multiple Python versions

**Matrix Strategy**:
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
- Runs tests in parallel for each version

**Steps**:
1. Checkout code
2. Set up Python environment with caching
3. Install dependencies (including pytest-cov and pytest-html)
4. Create required directories (data/backups, out, .logs)
5. Run tests with coverage reporting
6. Upload coverage to Codecov (Python 3.12 only)
7. Upload test results as artifacts
8. Verify coverage threshold (80% minimum for Python 3.12)

**Artifacts**:
- `test-results-{python-version}`: HTML test reports and coverage data
- Coverage reports in XML and HTML formats

**Coverage Threshold**: 80% minimum (enforced on Python 3.12)

### 2. Lint Job

**Purpose**: Ensure code quality and consistency

**Tools**:
- **flake8**: Python syntax and style checking
  - Critical errors (E9, F63, F7, F82) fail the build
  - Other issues are reported but don't fail the build
- **black**: Code formatting verification
- **isort**: Import statement sorting verification

**Note**: Linting issues are reported but don't fail the build (continue-on-error: true)

### 3. Integration Test Job

**Purpose**: Run comprehensive integration and quality tests

**Dependencies**: Requires the Test job to complete successfully

**Test Suites**:
1. Integration tests (`test_integration.py`)
2. Comprehensive quality suite (`test_comprehensive_quality_suite.py`)
3. API tests (`test_api.py`)

### 4. Security Job

**Purpose**: Scan for security vulnerabilities

**Tools**:
- **safety**: Check dependencies for known security vulnerabilities
- **bandit**: Static security analysis of Python code

**Artifacts**:
- `security-reports`: JSON reports from security scans

**Note**: Security issues are reported but don't fail the build (continue-on-error: true)

### 5. Build Status Job

**Purpose**: Aggregate results and determine overall build status

**Dependencies**: Requires all previous jobs to complete

**Logic**:
- ✅ Passes if Test and Integration Test jobs succeed
- ❌ Fails if Test or Integration Test jobs fail
- Lint and Security jobs are informational only

## Triggers

The pipeline runs on:

### Push Events
- `main` branch
- `develop` branch
- `feat/**` branches (all feature branches)

### Pull Request Events
- Targeting `main` branch
- Targeting `develop` branch

## Configuration Files

### `.github/workflows/ci.yml`
Main workflow definition file containing all job configurations.

### `pytest.ini`
Pytest configuration including:
- Test discovery patterns
- Output options
- Coverage settings

### `requirements.txt`
Python dependencies including:
- Core application dependencies
- Testing tools (pytest, pytest-flask)
- Coverage tools (pytest-cov, pytest-html)

## Local Testing

Before pushing, you can run the same checks locally:

### Run Tests
```bash
# All tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=html

# Specific test suite
python -m pytest tests/test_api.py -v

# With coverage threshold check
python -m pytest tests/ --cov=src --cov-fail-under=80
```

### Run Linting
```bash
# Install linting tools
pip install flake8 black isort

# Check syntax errors
flake8 src/ tests/ --select=E9,F63,F7,F82

# Check all style issues
flake8 src/ tests/ --max-complexity=10 --max-line-length=127

# Check formatting
black --check src/ tests/

# Check import sorting
isort --check-only src/ tests/
```

### Run Security Scans
```bash
# Install security tools
pip install safety bandit

# Check dependencies
safety check

# Scan code
bandit -r src/
```

## Viewing Results

### GitHub Actions UI
1. Go to the repository on GitHub
2. Click the "Actions" tab
3. Select a workflow run to view details
4. Click on individual jobs to see logs

### Artifacts
Test results and coverage reports are uploaded as artifacts:
1. Navigate to a completed workflow run
2. Scroll to the "Artifacts" section at the bottom
3. Download artifacts to view locally

### Status Badge
The README includes a status badge showing the current build status:
```markdown
[![CI/CD Pipeline](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/actions/workflows/ci.yml/badge.svg)](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/actions/workflows/ci.yml)
```

## Codecov Integration (Optional)

The pipeline includes Codecov integration for coverage tracking:

### Setup
1. Sign up at [codecov.io](https://codecov.io)
2. Add the repository
3. Get the upload token
4. Add `CODECOV_TOKEN` to repository secrets:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `CODECOV_TOKEN`
   - Value: Your Codecov token

### Without Codecov
If you don't set up Codecov, the pipeline will still work. The coverage upload step will be skipped (fail_ci_if_error: false).

## Troubleshooting

### Tests Failing in CI but Passing Locally

**Possible causes**:
1. **Environment differences**: CI uses a clean environment
2. **Missing dependencies**: Check requirements.txt is complete
3. **File paths**: Use Path objects and relative paths
4. **Python version**: Test locally with multiple Python versions

**Solution**:
```bash
# Test with specific Python version
python3.8 -m pytest tests/ -v
python3.12 -m pytest tests/ -v
```

### Coverage Threshold Failures

**Cause**: Test coverage below 80%

**Solution**:
1. Add tests for uncovered code
2. Remove dead code
3. Adjust threshold in `.github/workflows/ci.yml` if appropriate

### Linting Failures

**Cause**: Code style issues

**Solution**:
```bash
# Auto-fix formatting
black src/ tests/

# Auto-fix imports
isort src/ tests/

# Check remaining issues
flake8 src/ tests/
```

### Security Scan Failures

**Cause**: Vulnerable dependencies or insecure code patterns

**Solution**:
1. Update vulnerable dependencies: `pip install --upgrade <package>`
2. Review bandit findings and fix security issues
3. Add `# nosec` comments for false positives (with justification)

## Best Practices

### Before Committing
1. ✅ Run tests locally: `python -m pytest tests/ -v`
2. ✅ Check coverage: `python -m pytest tests/ --cov=src`
3. ✅ Run linting: `black src/ tests/ && isort src/ tests/`
4. ✅ Review changes: `git diff`

### Writing Tests
1. Follow TDD (Test-Driven Development)
2. Maintain high coverage (>80%)
3. Test edge cases and error conditions
4. Use descriptive test names
5. Keep tests independent and isolated

### Pull Requests
1. Ensure all CI checks pass before requesting review
2. Address any linting or security warnings
3. Update documentation if needed
4. Keep PRs focused and reasonably sized

## Maintenance

### Updating Python Versions
Edit `.github/workflows/ci.yml`:
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13']
```

### Adding New Test Suites
1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Tests will be automatically discovered and run

### Modifying Coverage Threshold
Edit `.github/workflows/ci.yml`:
```yaml
- name: Check test coverage threshold
  run: |
    python -m pytest tests/ --cov=src --cov-fail-under=85  # Change from 80 to 85
```

## Related Documentation

- [Test Suite Summary](QUALITY_TESTS_GREEN_SUMMARY.md)
- [TDD Validation Summary](TDD_VALIDATION_SUMMARY.md)
- [Resume Editor Web Interface](RESUME_EDITOR_WEB_INTERFACE.md)

## Support

For issues with the CI/CD pipeline:
1. Check the [GitHub Actions documentation](https://docs.github.com/en/actions)
2. Review workflow logs for specific error messages
3. Open an issue in the repository with details

