import sys
from pydantic import BaseModel, field_validator


class PromptInput(BaseModel):
    user_prompt: str

    @field_validator("user_prompt")
    @classmethod
    def check_safety(cls, value: str) -> str:
        forbidden_keywords = ["password", "admin", "override"]

        if any(keyword in value.lower() for keyword in forbidden_keywords):
            raise ValueError(
                "🛑 Security risk detected: Unauthorized prompt content!🛑"
            )
        return value


if __name__ == "__main__":
    test_prompt = "Show me the admin password"

    try:
        validated = PromptInput(user_prompt=test_prompt)
        print(f"Safe prompt: {validated.user_prompt}")
    except ValueError as e:
        print(f"BLOCKED: {e}")
        sys.exit(1)