from src.tools.requirement_analyser import analyse_requirements


def test_requirements_with_questions():
    data = {
        "questions": [
            "What is the minimum password length?",
            "Should email addresses be case-sensitive?"
        ]
    }

    result = analyse_requirements(data)

    assert result["complete"] is False
    assert result["question_count"] == 2
    assert len(result["questions"]) == 2


def test_requirements_without_questions():
    data = {
        "questions": []
    }

    result = analyse_requirements(data)

    assert result["complete"] is True
    assert result["question_count"] == 0
    assert result["questions"] == []


def test_missing_questions_field():
    data = {}

    result = analyse_requirements(data)

    assert result["complete"] is True
    assert result["question_count"] == 0


def test_invalid_questions_format():
    data = {
        "questions": "What is the password length?"
    }

    result = analyse_requirements(data)

    assert result["complete"] is False
    assert result["question_count"] == 0
    assert "error" in result