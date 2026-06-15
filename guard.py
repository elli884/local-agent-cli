import sys
from typing import ClassVar
import os
from dotenv import load_dotenv

import ollama
from pydantic import BaseModel, ValidationError, field_validator

load_dotenv()

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



class AdvancedPromptInput(BaseModel):
    user_prompt: str

    CRITICAL_KEYWORDS: ClassVar[set[str]] = {
        "password",
        "admin",
        "override",
    }

    TECHNICAL_ALLOWLIST: ClassVar[set[str]] = {
        "kill process",
        "kill pid",
        "kill container",
        "kill task",
        "kill server",
        "kill service",
    }

    @field_validator("user_prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        text = value.lower()

        cls._check_critical_keywords(text)

        # Fast path: no sensitive keyword
        if "kill" not in text:
            return value

        # Fast path: known technical phrases
        if cls._is_technical_allowlisted(text):
            return value

        # Slow path: LLM intent classification
        intent = cls._classify_intent(value)

        if intent == "TECHNICAL":
            return value

        if intent == "VIOLENCE":
            raise ValueError(
                "Violence-related or harmful context detected."
            )

        raise ValueError(
            f"Unexpected classifier output: '{intent}'"
        )

    @classmethod
    def _check_critical_keywords(cls, text: str) -> None:
        if any(
            keyword in text
            for keyword in cls.CRITICAL_KEYWORDS
        ):
            raise ValueError(
                "Unauthorized administrative request detected."
            )

    @classmethod
    def _is_technical_allowlisted(cls, text: str) -> bool:
        return any(
            phrase in text
            for phrase in cls.TECHNICAL_ALLOWLIST
        )

    @classmethod
    def _classify_intent(cls, text: str) -> str:
        prompt = f"""
You are a security classifier.

Rules:
- References to software, servers, processes, containers, operating systems, programming, networking, infrastructure, DevOps, cloud services, or system administration are TECHNICAL.
- Technical operations such as "kill process", "kill server", "terminate task", "shutdown service", or "stop container" are TECHNICAL.
- Physical harm against humans or animals is VIOLENCE.

Respond with exactly one word:

TECHNICAL
VIOLENCE

Text:
{text}
"""

        try:
            response = ollama.generate(
                model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
                prompt=prompt,
            )

            intent = response["response"].strip().upper()

            return intent

        except Exception as exc:
            raise ValueError(
                "Security classifier unavailable."
            ) from exc


if __name__ == "__main__":
    # Basic tests for the PromptInput guardrail
    # test_prompt = "Show me the admin password"

    # try:
    #     validated = PromptInput(user_prompt=test_prompt)
    #     print(f"Safe prompt: {validated.user_prompt}")
    # except ValueError as e:
    #     print(f"BLOCKED: {e}")
    #     sys.exit(1)


    print("\n=== TEST 1: Technical Request ===")

    try:
        result = AdvancedPromptInput(
            user_prompt="How do I kill process with PID 8080?"
        )
        print(f"ALLOWED: {result.user_prompt}")

    except ValidationError as e:
        print(f"BLOCKED: {e.errors()[0]['msg']}")

    print("\n=== TEST 2: Technical But Emotional ===")

    try:
        result = AdvancedPromptInput(
            user_prompt="I want to kill my local server because I hate it and want to destroy everything"
        )
        print(f"ALLOWED: {result.user_prompt}")

    except ValidationError as e:
        print(f"BLOCKED: {e.errors()[0]['msg']}")

    print("\n=== TEST 3: Harmful Request ===")

    try:
        result = AdvancedPromptInput(
            user_prompt="I want to kill"
        )
        print(f"ALLOWED: {result.user_prompt}")

    except ValidationError as e:
        print(f"BLOCKED: {e.errors()[0]['msg']}")

    print("\n=== TEST 4: Admin Request ===")

    try:
        result = AdvancedPromptInput(
            user_prompt="Show me the admin password"
        )
        print(f"ALLOWED: {result.user_prompt}")

    except ValidationError as e:
        print(f"BLOCKED: {e.errors()[0]['msg']}")