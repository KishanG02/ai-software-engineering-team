from llm import llm
import time


def generate_frontend(architecture: str):

    with open(
        "prompts/frontend.txt",
        "r",
        encoding="utf-8"
    ) as f:
        prompt_template = f.read()

    prompt = prompt_template.replace(
        "<<ARCHITECTURE>>",
        architecture
    )

    print("Generating Frontend Code...")
    print(f"Architecture Length: {len(architecture)}")
    print(f"Prompt Length: {len(prompt)}")

    start = time.time()

    response = llm.invoke(prompt)

    end = time.time()

    print(
        f"Frontend generation completed in {end-start:.2f} seconds"
    )

    return response.content