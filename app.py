from workflows.software_team_graph import run_graph
from agents.backend_engineer import generate_backend
from agents.frontend_engineer import generate_frontend
from utils.file_manager import save_output

def main():

    requirement = input("\nEnter Project Idea: ")

    result = run_graph(requirement)

    save_output("prd.md", result["prd"])

    save_output("architecture.md", result["architecture"])

    save_output("backend.md", result["backend_code"])

    save_output("frontend.md", result["frontend_code"])
    
if __name__ == "__main__":
    main()