from langgraph.graph import StateGraph, END
from workflows.state import ProjectState

from agents.product_manager import generate_prd
from agents.architect import generate_architecture
from agents.backend_engineer import generate_backend
from agents.frontend_engineer import generate_frontend

def pm_node(state):

    prd = generate_prd(
        state["requirement"]
    )

    return {
        "prd": prd
    }

def architect_node(state):

    architecture = generate_architecture(
        state["prd"]
    )

    print(
        f"Architecture Length in Architect Node: "
        f"{len(architecture)}"
    )

    return {
        "architecture": architecture
    }

def backend_node(state):

    backend = generate_backend(
        state["architecture"]
    )

    return {
        "backend_code": backend
    }

def frontend_node(state):

    print("\n===== FRONTEND STATE =====")
    print(state.keys())
    print("==========================\n")

    print(
        f"Architecture Length in Frontend Node: "
        f"{len(state['architecture'])}"
    )

    frontend = generate_frontend(
        state["architecture"]
    )

    return {
        "frontend_code": frontend
    }

builder = StateGraph(ProjectState)

builder.add_node(
    "pm",
    pm_node
)

builder.add_node(
    "architect",
    architect_node
)

builder.add_node(
    "backend",
    backend_node
)

builder.add_node(
    "frontend",
    frontend_node
)

builder.set_entry_point("pm")

builder.add_edge(
    "pm",
    "architect"
)

builder.add_edge(
    "architect",
    "backend"
)

builder.add_edge(
    "backend",
    "frontend"
)

builder.add_edge(
    "frontend",
    END
)

graph = builder.compile()

def run_graph(requirement: str):
    result = graph.invoke(
        {
            "requirement" : requirement
        }
    )

    return result