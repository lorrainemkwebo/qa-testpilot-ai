def validate_test_cases(data):
    """
    Validate the structure of AI-generated test cases.

    Returns:
        A dictionary containing validation status and errors.
    """

    errors = []

    # Check whether the response is a dictionary
    if not isinstance(data, dict):
        return {
            "valid": False,
            "errors": ["AI response must be a JSON object."]
        }

    # Check whether test_cases exists and is a list
    test_cases = data.get("test_cases")

    if not isinstance(test_cases, list):
        return {
            "valid": False,
            "errors": ["'test_cases' must be a list."]
        }

    if not test_cases:
        errors.append("No test cases were generated.")

    required_fields = [
        "id",
        "title",
        "steps",
        "expected_result"
    ]

    for index, test_case in enumerate(test_cases, start=1):

        if not isinstance(test_case, dict):
            errors.append(
                f"Test case {index} must be a JSON object."
            )
            continue

        for field in required_fields:
            if field not in test_case:
                errors.append(
                    f"Test case {index} is missing '{field}'."
                )
            elif not test_case[field]:
                errors.append(
                    f"Test case {index} has an empty '{field}'."
                )

        # Check that steps is a list
        if "steps" in test_case:
            if not isinstance(test_case["steps"], list):
                errors.append(
                    f"Test case {index}: 'steps' must be a list."
                )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }