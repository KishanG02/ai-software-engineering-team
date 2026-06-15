from llm import llm

def generate_architecture(prd: str):
    with open(
        "prompts/architect.txt",
        "r",
        encoding = "utf-8"
    ) as f:
        prompt_template = f.read()

    prompt = prompt_template.replace(
        "<<prd>>",
        prd
    )

    response = llm.invoke(prompt)

    return response.content