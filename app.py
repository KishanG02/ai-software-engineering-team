from workflows.phase3_workflow import run_phase_3
from agents.backend_engineer import generate_backend
from agents.frontend_engineer import generate_frontend
from utils.file_manager import save_output

def main():

    requirement = input("\nEnter Project Idea: ")

    result = run_phase_3(requirement)

    save_output("prd.md", result["prd"])

    save_output("architecture.md", result["architecture"])

    print("\nGenerating Backend...\n")

    backend_code = generate_backend(result["architecture"])

    save_output("backend.md",backend_code)

    print("\nFiles saved successfully!")

    frontend_code = generate_frontend(result["architecture"])

    save_output("frontend.md", frontend_code)

    print("\nFiles saved successfully")

if __name__ == "__main__":
    main()