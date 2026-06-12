import os

def save_outputs(   
    filename : str,
    content : str
):
    os.makedirs(
        "output", 
        exist_ok= True
    )

    filepath = os.path.join(
        "output",
        filename
    )

    with open(
        f"output/{filename}", 
        "w", 
        encoding="utf-8"
    ) as f:
        f.write(content)

    return filepath