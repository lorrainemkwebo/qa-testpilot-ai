from src.tools.test_case_validator import validate_test_cases


def test_valid_test_case():
    data = {
        "test_cases": [
            {
                "id": "TC01",
                "title": "Successful login",
                "steps": [
                    "Enter valid email",
                    "Enter valid password",
                    "Click Login"
                ],
                "expected_result": "User logs in successfully"
            }
        ]
    }

    result = validate_test_cases(data)

    assert result["valid"] is True


def test_missing_expected_result():
    data = {
        "test_cases": [
            {
                "id": "TC02",
                "title": "Invalid login",
                "steps": ["Click Login"]
            }
        ]
    }

    result = validate_test_cases(data)

    assert result["valid"] is False
    assert "Test case 1 is missing 'expected_result'." in result["errors"]


def test_steps_as_string():
    data = {
        "test_cases": [
            {
                "id": "TC03",
                "title": "Login test",
                "steps": "Enter email and click Login",
                "expected_result": "User logs in successfully"
            }
        ]
    }

    result = validate_test_cases(data)

    assert result["valid"] is False
    assert "Test case 1: 'steps' must be a list." in result["errors"]


def test_empty_test_cases():
    data = {
        "test_cases": []
    }

    result = validate_test_cases(data)

    assert result["valid"] is False
    assert "No test cases were generated." in result["errors"]