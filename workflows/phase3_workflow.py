from agents.product_manager import generate_prd
from agents.architect import generate_architecture


def run_phase_3(requirement):

    prd = generate_prd(requirement)

    architecture = generate_architecture(prd)

    return {
        "prd": prd,
        "architecture": architecture
    }