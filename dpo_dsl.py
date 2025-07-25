import hypernetx as hnx
from .dpo import DPORewritingRule


class GraphModule:
    """Hypergraph generation or storage"""

    def __init__(self, edges: dict[str, list[str]], name: str):
        self.graph = hnx.Hypergraph(data=edges, name=name)

    def grow(self, rule, steps=1):
        """Apply the rule to itself several times"""
        pass

    def subgraph(self, nodes: set[str]):
        pass


class RuleBuilder:
    """Constructs a rule from modules L, I, R."""

    def __init__(self):
        self.L = {}
        self.I = {}
        self.R = {}

    def from_modules(
        self, modL: GraphModule, modI: GraphModule, modR: GraphModule
    ):
        pass

    def merge(self, other: "RuleBuilder"):
        """Combines the rule with others, merging L, I, R."""
        pass


class Experiment:
    """Interface for controlling the operations"""

    def __init__(self):
        self.modules = {}
        self.rules = {}
        self.states = {}

    def add_module(self, name: str, edges: dict):
        pass

    def grow_module(self, name: str, rule_name: str, steps: int = 1):
        pass

    def combine_rule(self, name: str, *rule_names):
        pass

    def set_rule(self, name: str, rule: DPORewritingRule):
        pass

    def apply(self, state_name: str, rule_name: str, steps: int = 1):
        pass

    def show(self, state_name: str):
        pass
