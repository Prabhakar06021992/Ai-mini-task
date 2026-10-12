
import re
from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError


class UserProfile(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=18, le=120)
    email: EmailStr
    pan: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValueError("Name must contain letters and spaces only")

        return value

    @field_validator("age", mode="before")
    @classmethod
    def validate_age(cls, value):
        if isinstance(value, bool):
            raise ValueError("Age must be an integer")

        if isinstance(value, str) and not re.fullmatch(r"\d+", value.strip()):
            raise ValueError("Age must contain digits only")

        return value

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, value: str) -> str:
        value = value.strip().upper()

        # Format: 5 letters, 4 digits, 1 letter
        if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", value):
            raise ValueError("Invalid PAN format")

        return value


def test_valid_profile():
    print("=== VALID PROFILE TEST ===")

    try:
        user = UserProfile(
            name="Prabhakar",
            age=33,
            email="vvprabhakars@gmail.com",
            pan="ABCDE1234F",
        )

        print("Validation successful!")
        print(user.model_dump(mode="json"))

    except ValidationError as error:
        print("Validation failed:")
        print(error)


def test_invalid_profile():
    print("\n=== INVALID PROFILE TEST ===")

    try:
        UserProfile(
            name="P",
            age=15,
            email="invalid-email",
            pan="123INVALID",
        )

    except ValidationError as error:
        print("Invalid data rejected successfully!")
        print(f"Number of validation errors: {error.error_count()}")
        print(error)


if __name__ == "__main__":
    test_valid_profile()
    test_invalid_profile()
