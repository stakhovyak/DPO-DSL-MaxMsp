import hypernetx as hnx
from itertools import permutations
import uuid
from collections import defaultdict


class DPORewritingRule:
    def __init__(self, L: hnx.Hypergraph, I: hnx.Hypergraph, R: hnx.Hypergraph):
        """
        :param L: Left hypergraph (pattern)
        :param I: Interface hypergraph
        :param R: Right hypergraph (replacement)
        """
        self.L = L
        self.I = I
        self.R = R


def apply_dpo_rule(H: hnx.Hypergraph, rule: DPORewritingRule):
    """
    Apply DPO rewriting rule to hypergraph H
    Returns list of (mapping, result_hypergraph)
    """
    results = []

    # 1. Find matches (monomorphisms L → H)
    matches = find_matches(H, rule.L)

    for vertex_mapping, edge_mapping in matches:
        # 2. Check dangling condition
        if not check_dangling_condition(H, rule, vertex_mapping, edge_mapping):
            continue

        # 3. Construct pushout complement (D)
        D = construct_pushout_complement(H, rule, vertex_mapping, edge_mapping)

        # 4. Construct pushout (H')
        H_prime = construct_pushout(D, rule, vertex_mapping)

        results.append((vertex_mapping, H_prime))

    return results


def find_matches(H: hnx.Hypergraph, L: hnx.Hypergraph):
    """Find monomorphisms (injective mappings) L → H"""
    matches = []
    L_nodes = sorted(L.nodes)
    H_nodes = sorted(H.nodes)

    for perm in permutations(H_nodes, len(L_nodes)):
        vertex_mapping = dict(zip(L_nodes, perm))

        edge_mapping = {}
        valid = True

        for e in L.edges:
            img_nodes = tuple(vertex_mapping[v] for v in L.edges[e])
            img_set = set(img_nodes)

            found = False
            for he in H.edges:
                target_set = set(H.edges[he])
                if img_set == target_set:
                    if he in edge_mapping.values():
                        valid = False
                        break
                    edge_mapping[e] = he
                    found = True
                    break

            if not found:
                valid = False
                break

        if valid and len(set(edge_mapping.values())) == len(edge_mapping):
            matches.append((vertex_mapping, edge_mapping))

    return matches


def check_dangling_condition(H, rule, vertex_mapping, edge_mapping):
    """
    Check no-dangling-edges condition
    Returns True if condition satisfied
    """
    L_vertices = set(rule.L.nodes)
    I_vertices = set(rule.I.nodes)
    delete_vertices = {vertex_mapping[v] for v in (L_vertices - I_vertices)}

    image_edges = set(edge_mapping.values())

    for v in delete_vertices:
        incident_edges = [he for he in H.edges if v in H.edges[he]]

        for he in incident_edges:
            if he not in image_edges:
                return False

    return True


def construct_pushout_complement(H, rule, vertex_mapping, edge_mapping):
    """
    Construct the pushout complement D
    (Cut graph after removing L\I)
    """
    D_edges = {he: set(H.edges[he]) for he in H.edges}

    D_vertices = set(H.nodes)

    L_vertices = set(rule.L.nodes)
    I_vertices = set(rule.I.nodes)
    L_edges = set(rule.L.edges)
    I_edges = set(rule.I.edges)

    delete_vertices = {vertex_mapping[v] for v in (L_vertices - I_vertices)}
    D_vertices -= delete_vertices

    delete_edges = []
    for e in L_edges:
        if e not in I_edges and e in edge_mapping:
            he = edge_mapping[e]
            if he in D_edges:
                delete_edges.append(he)

    for he in delete_edges:
        if he in D_edges:
            del D_edges[he]

    for he, edge in list(D_edges.items()):
        if any(v in delete_vertices for v in edge):
            del D_edges[he]

    return hnx.Hypergraph(D_edges)


def construct_pushout(D, rule, vertex_mapping):
    """
    Construct pushout of D and R along I
    """
    I_vertices = sorted(rule.I.nodes)
    vertex_map = {}
    for v in I_vertices:
        vertex_map[v] = vertex_mapping[v]

    R_vertices = sorted(rule.R.nodes)
    new_vertices = {}
    for v in R_vertices:
        if v not in rule.I.nodes:
            new_vertices[v] = f"new_{uuid.uuid4().hex[:4]}"

    all_vertices = set(D.nodes) | set(new_vertices.values())

    new_edges = {}

    for he in D.edges:
        new_edges[he] = set(D.edges[he])

    for e in rule.R.edges:
        new_edge = set()
        for v in rule.R.edges[e]:
            if v in rule.I.nodes:
                new_edge.add(vertex_map[v])
            else:
                new_edge.add(new_vertices[v])
        new_edges[f"new_{uuid.uuid4().hex[:4]}"] = new_edge

    return hnx.Hypergraph(new_edges)


def clean_hypergraph(H: hnx.Hypergraph) -> hnx.Hypergraph:
    H_without_singletons = H.remove_singletons()
    H_toplexes = H.toplexes()

    return H_toplexes
