import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_test_cases(requirement):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=(
            "You are a QA testing assistant. "
            "Generate positive, negative and edge test cases "
            "from software requirements. "
            "Identify unclear or missing requirements. "
            "Return only valid JSON with two keys: "
            "'test_cases' and 'questions'. "
            "Each test case must have an id, title, "
            "steps and expected_result."
        ),
        input=requirement
    )

    return json.loads(response.output_text)


def main():
    print("Welcome to QA TestPilot AI!")

    requirement = input("\nEnter a software requirement: ")

    if not requirement.strip():
        print("Please enter a requirement.")
        return

    try:
        result = generate_test_cases(requirement)

        print("\nGenerated test cases:")
        print(json.dumps(result, indent=2))

        approval = input(
            "\nDo you want to save these test cases? (yes/no): "
        ).strip().lower()

        if approval == "yes":
            with open("test_cases.json", "w") as file:
                json.dump(result, file, indent=2)

            print("Test cases saved successfully!")
        else:
            print("Test cases were not saved.")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()