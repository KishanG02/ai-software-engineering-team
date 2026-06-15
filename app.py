from workflows.phase3_workflow import run_phase_3
from utils.file_manager import save_output


def main():

    requirement = input("\nEnter Project Idea: ")

    result = run_phase_3(requirement)

    save_output("prd.md", result["prd"])

    save_output(
        "architecture.md",
        result["architecture"]
    )

    print(result["architecture"])

if __name__ == "__main__":
    main()