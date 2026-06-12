from agents.product_manager import generate_prd
from utils.file_manager import save_outputs

def main():

    requirement = input(
        "\nEnter Project Idea: "
    )

    print(
        "\nGenerating PRD...\n"
    )

    prd = generate_prd(
        requirement
    )

    save_outputs(
        "prd.md",
        prd
    )

    print(prd)

    print(
        "\nPRD saved to output/prd.md"
    )

if __name__ == "__main__":
    main()