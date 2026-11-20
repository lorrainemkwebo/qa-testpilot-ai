import json
import os

from dotenv import load_dotenv
from openai import OpenAI

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
                    "You are a QA testing assistant. "
                    "Generate positive, negative and edge test cases "
                    "from software requirements. "
                    "Identify unclear or missing requirements. "
                    "Return only valid JSON with two keys: "
                    "'test_cases' and 'questions'. "
                    "Each test case must have an id, title, "
                    "steps and expected_result. "
                    "Do not invent missing requirements."
                )
            },
            {
                "role": "user",
                "content": requirement
            }
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


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
            with open("test_cases.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=2)

            print("Test cases saved successfully!")
        else:
            print("Test cases were not saved.")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()