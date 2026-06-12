from llm import llm

response = llm.invoke(
    "Explain what a Product Requirement Document is."
)

print(response.content)