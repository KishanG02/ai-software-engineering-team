from llm import llm

def generate_prd(requirement: str):
    
    with open(
        "prompts/product_manager.txt",
        "r",
        encoding="utf-8"
     ) as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        requirement = requirement
    )

    response = llm.invoke(prompt)

    return response.content