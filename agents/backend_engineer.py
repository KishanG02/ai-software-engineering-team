from llm import llm

def generate_backend(architecture: str):
    
    with open(
        "prompts/backend.txt",
        "r",
        encoding = "utf-8"
    ) as f :
        prompt_template = f.read()

    prompt = prompt_template.replace(
        "<<ARCHITECTURE>>",
        architecture
    )

    response = llm.invoke(prompt)

    return response.content