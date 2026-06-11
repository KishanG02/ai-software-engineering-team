from typing import TypedDict


class ProjectState(TypedDict):
    requirement: str
    prd: str
    architecture: str
    backend_code: str
    frontend_code: str
    tests: str
    deployment: str
    review: str