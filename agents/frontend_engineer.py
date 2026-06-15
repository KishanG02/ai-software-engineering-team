from llm import llm

def generate_frontend(architecture: str):
    
    with open(
        "prompts/frontend.txt",
        "r",
        encoding = "utf-8"
    ) as f:
        prompt_template = f.read()

    prompt = prompt_template.replace(
        "<<ARCHITECTURE>>",
        architecture
    )

    print("Genereating Frontend Code...")

    response = llm.invoke(prompt)

    return response.content