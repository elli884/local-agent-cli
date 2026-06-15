import time
import logging
import ollama

from dotenv import load_dotenv
import os
load_dotenv()

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [METRICS] - %(message)s"
)


def timed_ai_generation(prompt: str):
    start_time = time.time()

    logging.info(
        f"Pipeline started for prompt length: {len(prompt)} characters."
    )

    try:
        # Simulate the model execution
        response = ollama.generate(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
            prompt=prompt
        )

        duration = time.time() - start_time

        logging.info(
            f"Model response successfully generated in {duration:.2f} seconds."
        )

        return response["response"]

    except Exception as e:
        logging.error(
            f"Error in the local pipeline: {str(e)}"
        )
        raise


if __name__ == "__main__":
    print(
        timed_ai_generation(
            "Give me three prime numbers."
        )
    )