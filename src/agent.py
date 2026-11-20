import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.tools.test_case_validator import validate_test_cases

load_dotenv(override=True)


def generate_test_cases(requirement):
    # Connect to GroqCloud
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

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

    # Convert AI response from JSON text into a Python dictionary
    return json.loads(response.choices[0].message.content)


def main():
    print("Welcome to QA TestPilot AI!")

    # STEP 1: Get software requirement from user
    requirement = input("\nEnter a software requirement: ")

    if not requirement.strip():
        print("Please enter a requirement.")
        return

    try:
        # STEP 2: Generate test cases using Groq AI
        print("\nGenerating test cases...")

        result = generate_test_cases(requirement)

        # STEP 3: Validate generated test cases
        validation = validate_test_cases(result)

        if not validation["valid"]:
            print("\n❌ Validation failed!")

            for error in validation["errors"]:
                print(f"- {error}")

            return

        print("\n✅ Validation passed!")

        # STEP 4: Display generated test cases
        print("\nGenerated test cases:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # STEP 5: Ask for human approval
        approval = input(
            "\nDo you want to save these test cases? (yes/no): "
        ).strip().lower()

        # STEP 6: Save approved test cases
        if approval == "yes":
            with open(
                "test_cases.json",
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    result,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            print("\n✅ Test cases saved successfully!")
        else:
            print("\nTest cases were not saved.")

    except json.JSONDecodeError:
        print("\n❌ Error: AI returned invalid JSON.")

    except Exception as error:
        print(f"\n❌ Error: {error}")


if __name__ == "__main__":
    main()