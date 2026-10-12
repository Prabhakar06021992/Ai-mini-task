
import os
import json
import instructor

from groq import Groq
from pydantic import ValidationError
from user_profile import UserProfile


def main():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("Error: GROQ_API_KEY is not configured.")
        return

    # Connect to Groq
    client = Groq(api_key=api_key)

    # Enable Instructor's structured-output handling
    client = instructor.from_groq(
        client,
        mode=instructor.Mode.JSON,
    )

    try:
        # Ask the LLM to generate data matching UserProfile
        user = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            response_model=UserProfile,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate a fictional test user profile. "
                        "Use a name, an age between 18 and 120, "
                        "a reserved example.com email address, and "
                        "a syntactically valid fictional PAN-format "
                        "value. Never use real personal information."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Generate one fictional user profile "
                        "and return data matching the schema."
                    ),
                },
            ],
            max_retries=2,
        )

        print("\nStructured response received!")
        print("\nValidated Python object:")
        print(user)

        print("\nJSON output:")
        print(json.dumps(user.model_dump(mode="json"), indent=2))

        print("\nPydantic validation: PASSED")

    except ValidationError as error:
        print("Pydantic validation failed:")
        print(error)

    except Exception as error:
        print(f"LLM request failed: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
