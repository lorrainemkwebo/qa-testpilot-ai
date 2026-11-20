import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.tools.test_case_validator import validate_test_cases
from src.tools.requirement_analyser import analyse_requirements


# Load environment variables
load_dotenv(override=True)


def generate_test_cases(requirement):
    """
    Generate software test cases using GroqCloud AI.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    # Connect to GroqCloud
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    # Send software requirements to the AI model
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced QA testing assistant. "
                    "Generate positive, negative and edge test cases "
                    "from software requirements. "
                    "Identify unclear or missing requirements. "
                    "Return ONLY valid JSON. "
                    "The JSON must contain exactly two keys: "
                    "'test_cases' and 'questions'. "
                    "'test_cases' must be an array of objects. "
                    "Each test case must contain: "
                    "'id' (string), "
                    "'title' (string), "
                    "'steps' (array of strings), "
                    "'expected_result' (string). "
                    "IMPORTANT: 'steps' must ALWAYS be a JSON array, "
                    "never a string. "
                    "'questions' must be an array of strings. "
                    "Generate meaningful positive, negative and edge cases "
                    "when supported by the requirements. "
                    "Do not invent missing requirements. "
                    "If expected behaviour is unclear, add a question "
                    "instead of assuming how the application works."
                )
            },
            {
                "role": "user",
                "content": requirement
            }
        ],
        response_format={"type": "json_object"}
    )

    # Convert the AI response into a Python dictionary
    content = response.choices[0].message.content

    if not content:
        raise ValueError("AI returned an empty response.")

    return json.loads(content)


def main():
    """
    Run the QA TestPilot AI application.
    """

    print("Welcome to QA TestPilot AI!")

    # STEP 1: Get software requirements
    requirement = input("\nEnter a software requirement: ").strip()

    if not requirement:
        print("Please enter a requirement.")
        return

    try:
        # STEP 2: Generate test cases
        print("\nGenerating test cases...")

        result = generate_test_cases(requirement)

        # STEP 3: Validate the generated test cases
        print("\nValidating generated test cases...")

        validation = validate_test_cases(result)

        if not validation["valid"]:
            print("\nValidation failed!")

            for error in validation["errors"]:
                print(f"- {error}")

            return

        print("\nValidation passed!")

        # STEP 4: Analyse unclear requirements
        analysis = analyse_requirements(result)

        print("\nRequirement Analysis")
        print("--------------------")

        if "error" in analysis:
            print(f"Analysis error: {analysis['error']}")
            return

        print(f"Questions identified: {analysis['question_count']}")

        if analysis["complete"]:
            print("No unclear requirements were identified.")
        else:
            for question in analysis["questions"]:
                print(f"- {question}")

        # STEP 5: Display generated test cases
        print("\nGenerated Test Cases")
        print("--------------------")

        for test_case in result["test_cases"]:
            print(f"\nTest Case ID: {test_case['id']}")
            print(f"Title: {test_case['title']}")

            print("Steps:")
            for index, step in enumerate(test_case["steps"], start=1):
                print(f"  {index}. {step}")

            print(f"Expected Result: {test_case['expected_result']}")

        # STEP 6: Ask for human approval
        print("\nHuman Review")
        print("------------")

        approval = input(
            "Do you want to save these test cases? (yes/no): "
        ).strip().lower()

        # STEP 7: Save approved test cases
        if approval == "yes":

            filename = "test_cases.json"

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    result,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            print(f"\nTest cases saved successfully to {filename}.")

        else:
            print("\nTest cases were not saved.")

    except json.JSONDecodeError:
        print("\nError: AI returned invalid JSON.")

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()