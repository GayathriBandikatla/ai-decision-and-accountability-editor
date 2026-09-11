# Patchamomma Testing Guide

Complete guide for running and understanding the test suite.

## 📋 Overview

The test suite covers:
- ✅ **Unit Tests**: Individual components (validators, agents)
- ✅ **Integration Tests**: Multiple components working together
- ✅ **API Tests**: FastAPI endpoints and error handling
- ✅ **Validation Tests**: Decision and action item validation

## 🚀 Quick Start

### 1. Install Testing Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
pytest -v
```

### 3. Run Specific Test File

```bash
# Test validators only
pytest tests/test_validators.py -v

# Test API only
pytest tests/test_api.py -v
```

### 4. Run Tests with Coverage

```bash
pytest --cov=. --cov-report=html
# Opens htmlcov/index.html to see coverage report
```

## 📊 Test Structure

### test_validators.py (40+ tests)

Tests for deterministic validation logic.

#### TestDecisionValidator
- `test_validate_empty_decisions()` - Empty input handling
- `test_validate_single_decision()` - Single valid decision
- `test_duplicate_detection()` - Fuzzy matching of duplicates
- `test_low_confidence_flag()` - Low confidence detection
- `test_missing_evidence()` - Missing evidence detection
- `test_vague_decision()` - Vague decision detection
- `test_confidence_average()` - Confidence score calculation

#### TestActionValidator
- `test_validate_empty_actions()` - Empty input handling
- `test_missing_owner()` - Unassigned owner detection
- `test_ambiguous_owner()` - Ambiguous owner detection
- `test_high_priority_missing_deadline()` - Critical deadlines
- `test_valid_action_item()` - Valid action item validation
- `test_owned_actions_count()` - Owner counting

#### TestConflictDetector
- `test_no_conflicts()` - Clean data handling
- `test_contradictory_decisions()` - Opposite decisions detection
- `test_unowned_critical_task()` - Unowned critical tasks
- `test_ambiguous_responsibility()` - Unclear responsibility

#### TestValidatorIntegration
- `test_full_validation_pipeline()` - Running all validators together

### test_api.py (20+ tests)

Tests for FastAPI endpoints.

#### TestHealthCheck
- `test_health_check_success()` - `/health` endpoint
- `test_root_endpoint()` - `/` endpoint

#### TestAnalyzeEndpoint
- `test_analyze_success()` - Successful analysis
- `test_analyze_short_transcript()` - Short transcript rejection
- `test_analyze_empty_transcript()` - Empty input handling
- `test_analyze_whitespace_only()` - Whitespace-only handling
- `test_analyze_long_transcript()` - Long transcript handling
- `test_analyze_response_structure()` - Response format validation
- `test_analyze_validation_present()` - Validation results included
- `test_analyze_conflicts_present()` - Conflict detection included
- `test_analyze_missing_body()` - Missing request body
- `test_analyze_invalid_json()` - Invalid JSON handling

#### TestContentNegotiation
- `test_json_response_content_type()` - JSON content type
- `test_request_with_json_content_type()` - Request headers

#### TestErrorHandling
- `test_422_for_invalid_request()` - Invalid request handling
- `test_error_response_format()` - Error response format
- `test_500_error_handling()` - Server error handling

#### TestCORS
- `test_cors_headers_present()` - CORS support
- `test_cors_allow_origin()` - CORS headers

#### TestMetadata
- `test_openapi_schema()` - OpenAPI schema availability
- `test_docs_endpoint()` - Swagger docs endpoint

#### TestConcurrency
- `test_multiple_sequential_requests()` - Sequential requests

## 🏃 Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test Class

```bash
pytest tests/test_validators.py::TestDecisionValidator -v
```

### Run Specific Test

```bash
pytest tests/test_validators.py::TestDecisionValidator::test_duplicate_detection -v
```

### Run Tests Matching Pattern

```bash
pytest -k "confidence" -v
```

### Run Tests with Output Capture

```bash
pytest -s  # Show print statements
```

### Run Tests and Stop on First Failure

```bash
pytest -x
```

### Run Last Failed Tests

```bash
pytest --lf
```

### Run Tests with Markers

```bash
# Run only unit tests
pytest -m unit -v

# Run only API tests
pytest -m api -v

# Run validators tests
pytest -m validators -v
```

## 📈 Coverage Reports

### Generate Coverage

```bash
pytest --cov=. --cov-report=html
```

### View Coverage Report

```bash
# Open in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html # Linux
```

### Coverage Goals

- **Validators**: 95%+ (critical logic)
- **API**: 90%+ (endpoint testing)
- **Overall**: 85%+

## 🧪 Test Examples

### Example 1: Test Decision Validation

```bash
pytest tests/test_validators.py::TestDecisionValidator -v
```

Expected output:
```
test_validate_empty_decisions PASSED
test_validate_single_decision PASSED
test_duplicate_detection PASSED
test_low_confidence_flag PASSED
test_missing_evidence PASSED
test_vague_decision PASSED
test_confidence_average PASSED
```

### Example 2: Test API Endpoints

```bash
pytest tests/test_api.py::TestAnalyzeEndpoint::test_analyze_success -v
```

This test:
1. Sends a valid transcript
2. Checks response status is 200
3. Validates response structure
4. Verifies all expected fields are present

### Example 3: Run Tests with Coverage

```bash
pytest --cov=validators --cov=api --cov-report=term-missing
```

Shows which lines aren't covered by tests.

## 🔧 Debugging Tests

### Add Debug Output

```python
def test_something():
    result = function_call()
    print(f"Result: {result}")  # Will show with pytest -s
    assert result == expected
```

### Use pdb Breakpoint

```python
def test_something():
    result = function_call()
    breakpoint()  # Debugger will pause here
    assert result == expected
```

Run with: `pytest tests/test_file.py -s --pdb`

### Print Request/Response

```python
def test_analyze_success():
    response = client.post("/analyze", json={"transcript_text": "..."})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
```

## 📝 Test Best Practices

### ✅ Do

- Test one thing per test
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Use fixtures for reusable data

### ❌ Don't

- Test implementation details
- Create tests that depend on other tests
- Use `sleep()` in tests
- Make network calls in unit tests
- Test third-party libraries

## 🐛 Common Issues

### Issue: "ModuleNotFoundError: No module named 'config'"

**Solution**: Make sure you're running pytest from project root:
```bash
cd patchamomma/
pytest
```

### Issue: "Tests pass locally but fail in CI"

**Solution**: Check environment variables:
```bash
# Ensure .env is set up for tests
cp .env.example .env
```

### Issue: "CORS test failing"

**Solution**: The test client may not include CORS headers. This is normal. Verify in actual browser.

## 📚 Test Data

### Sample Transcripts

Located in `tests/fixtures/sample_transcripts/`

- `PRJ001.json` - Complete project meeting
- `PRJ002.json` - Infrastructure discussion
- `PRJ003.json` - API design review
- `PRJ004.json` - Security planning
- `PRJ005.json` - Final checkpoint

### Generated Test Data

Tests generate their own data inline for isolation:

```python
VALID_TRANSCRIPT = """
Project Manager: Welcome to the meeting...
"""

SHORT_TRANSCRIPT = "Let's use React."
LONG_TRANSCRIPT = VALID_TRANSCRIPT * 5
```

## 🔄 Continuous Testing

### Watch Mode (Auto-rerun on file changes)

```bash
pytest-watch tests/
```

Or use pytest-dev:
```bash
pip install pytest-watch
ptw
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
pytest tests/ || exit 1
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## 📊 Test Metrics

### Expected Test Results

```
tests/test_validators.py .......... (20 tests)
tests/test_api.py ................ (20 tests)

Total: 40+ tests
Expected: ~5-10 seconds to run
```

### Performance Targets

- Each test: < 1 second
- Full suite: < 30 seconds
- Coverage: > 85%

## 🎯 Next Steps

1. ✅ Run all tests: `pytest -v`
2. ✅ Check coverage: `pytest --cov`
3. ✅ Add new tests as you add features
4. ✅ Keep tests passing in CI/CD

## 📞 Help

### Run Tests with Help

```bash
pytest --help
```

### Common Flags

```
-v          Verbose output
-s          Show print statements
-k KEYWORD  Run tests matching keyword
-m MARKER   Run tests with marker
--lf        Run last failed tests
-x          Stop on first failure
--pdb       Drop to debugger on failure
--cov       Show coverage
```

### Example: Comprehensive Test Run

```bash
pytest -v --cov=. --cov-report=html -k "not slow"
```

This runs all tests except slow ones, with coverage report.

---

**Happy testing!** 🚀

For questions, check DEVELOPMENT_GUIDE.md or README.md.
