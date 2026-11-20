def analyse_requirements(data):
    """
    Analyse questions identified by the AI.

    Returns a summary of unclear requirements.
    """

    questions = data.get("questions", [])

    if not isinstance(questions, list):
        return {
            "complete": False,
            "question_count": 0,
            "questions": [],
            "error": "'questions' must be a list."
        }

    return {
        "complete": len(questions) == 0,
        "question_count": len(questions),
        "questions": questions
    }