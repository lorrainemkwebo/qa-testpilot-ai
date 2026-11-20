# QA TestPilot AI

**An AI-Powered Software Test Case Generator Built with Python and GroqCloud**

## Project Overview

QA TestPilot AI is a Python-based application that uses artificial intelligence to generate software test cases from natural-language requirements.

The application helps Quality Assurance (QA) engineers identify positive, negative, and edge-case testing scenarios while highlighting unclear or missing requirements.

It also validates the structure of AI-generated test cases and requires human approval before saving them.

This project demonstrates the integration of AI technology with software quality assurance practices.

## Key Features

- **AI-Powered Test Case Generation:** Generates software test cases from user requirements using a large language model.
- **Requirement Analysis:** Identifies and displays unclear or missing requirements.
- **Test Case Validation:** Checks generated test cases for required fields and correct data structures.
- **Structured JSON Output:** Generates test cases in a consistent JSON format.
- **Human-in-the-Loop Approval:** Requires user confirmation before saving generated test cases.
- **Automated Unit Testing:** Uses pytest to verify the functionality of the validation and requirement analysis tools.
- **Error Handling:** Handles invalid JSON responses, missing API credentials, and other application errors.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| GroqCloud | Hosted AI model inference |
| GPT-OSS 20B | Large language model for generating test cases |
| OpenAI Python SDK | Communicating with Groq's OpenAI-compatible API |
| python-dotenv | Managing environment variables |
| JSON | Structured test case storage |
| pytest | Automated unit testing |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
qa-testpilot-ai/
├── src/
│   ├── __init__.py
│   ├── agent.py
│   └── tools/
│       ├── __init__.py
│       ├── requirement_analyser.py
│       └── test_case_validator.py
├── tests/
│   ├── __init__.py
│   ├── test_validator.py
│   └── test_requirement_analyser.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── test_cases.json
```

**Note:** The `.env` file contains local configuration and must not be committed to GitHub. The generated `test_cases.json` file is created when the user approves the results.

## How the Application Works

```text
User enters a software requirement
                |
                v
        GroqCloud AI Model
                |
                v
       Generate Test Cases
                |
                v
        Validate Test Cases
                |
                v
       Analyse Requirements
                |
                v
        Display Test Cases
                |
                v
          Human Approval
                |
          +-----+-----+
          |           |
         YES          NO
          |           |
          v           v
      Save JSON     Do Not Save
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd qa-testpilot-ai
```

Replace `<your-repository-url>` with the actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add the following:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Replace `your_groq_api_key_here` with your own Groq API key.

Never share or commit your API key.

### 5. Run the Application

```bash
python3 -m src.agent
```

## Example Usage

### Input Requirement

```text
A user must be able to log in using a valid email address and password. Invalid credentials must display an error message.
```

### Example Generated Test Cases

```json
{
  "test_cases": [
    {
      "id": "TC001",
      "title": "Successful login with valid credentials",
      "steps": [
        "Open the login page",
        "Enter a registered email address",
        "Enter the correct password",
        "Click the Login button"
      ],
      "expected_result": "The user is successfully authenticated"
    },
    {
      "id": "TC002",
      "title": "Login with incorrect password",
      "steps": [
        "Open the login page",
        "Enter a registered email address",
        "Enter an incorrect password",
        "Click the Login button"
      ],
      "expected_result": "An invalid credentials error message is displayed"
    }
  ],
  "questions": [
    "What happens after multiple failed login attempts?",
    "Are email addresses case-sensitive during login?"
  ]
}
```

The actual output may vary depending on the AI model's response.

## Test Case Validation

The application uses a Python validation function to check generated test cases.

The validator checks:

1. The AI response is a dictionary.
2. The response contains a `test_cases` list.
3. The test case list is not empty.
4. Each test case contains the required fields:
   - `id`
   - `title`
   - `steps`
   - `expected_result`
5. Required fields are not empty.
6. The `steps` field is a list.

If validation fails, the application displays the errors and stops before saving the results.

**Limitation:** The validator currently checks data structure, not the completeness or correctness of test coverage.

## Requirement Analysis

The Requirement Analyser processes clarification questions generated by the AI.

It provides:

- The number of identified questions.
- A list of unclear requirements.
- An indication of whether any clarification questions were reported.

This helps QA engineers identify areas that may need further discussion with developers, product owners, or business analysts.

## Automated Testing

The project uses pytest to test the application's Python validation and analysis functions.

### Run All Tests

```bash
python3 -m pytest tests/ -v
```

### Run Validator Tests

```bash
python3 -m pytest tests/test_validator.py -v
```

### Run Requirement Analyser Tests

```bash
python3 -m pytest tests/test_requirement_analyser.py -v
```

The tests cover valid inputs, missing fields, incorrect data types, and empty test case collections.

## Human-in-the-Loop Design

AI-generated test cases are not automatically saved.

The application first:

1. Generates test cases.
2. Validates their structure.
3. Displays the results.
4. Requests human approval.
5. Saves the approved output to `test_cases.json`.

This approach allows a human reviewer to check AI-generated content before accepting it.

## Current Limitations

- Test cases are generated using an external AI API.
- The application requires an internet connection.
- AI-generated test cases may require manual corrections.
- Structural validation does not guarantee complete requirement coverage.
- The application currently uses a fixed workflow rather than autonomous AI tool selection.
- Generated test cases are saved to a local JSON file.

## Future Improvements

Planned enhancements include:

- AI function calling and tool selection.
- Automatic correction of invalid AI-generated outputs.
- Persistent agent memory.
- Retrieval-Augmented Generation (RAG).
- Improved test coverage analysis.
- Exporting test cases to CSV.
- A web-based user interface.
- CI/CD integration using GitHub Actions.

## Skills Demonstrated

This project demonstrates practical experience with:

- Python programming
- AI API integration
- Prompt engineering
- JSON processing
- Software testing principles
- Automated unit testing with pytest
- Input and output validation
- Error handling
- Human-in-the-loop workflows
- Git and GitHub

## Project Purpose

QA TestPilot AI was developed as a practical learning project combining artificial intelligence and software quality assurance.

The goal is to explore how AI can support QA engineers by reducing repetitive test case preparation, identifying unclear requirements, and improving testing workflows.

The project will continue to evolve as additional AI engineering and test automation capabilities are implemented.

## Author

**Lorraine Jettina Mkwebo**

Software Development Student | Quality Assurance | Python | AI Engineering

Developed as a personal portfolio project.