from pydantic import BaseModel
from typing import List


class Edge:
    vertices: List[str]


class DPORule:
    L: List[Edge]
    I: List[Edge]
    R: List[Edge]


class EvolveRequest(BaseModel):
    hypergraph: List[Edge]
    rule: DPORule
    steps: int
    clean: bool


class EvolveResponse(BaseModel):
    hypergraph: List[Edge]
