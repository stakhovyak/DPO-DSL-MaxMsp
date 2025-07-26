from fastapi import FastAPI
from src.api.models import EvolveResponse, EvolveRequest, Edge
from src.dpo import apply_dpo_rule, DPORewritingRule, clean_hypergraph
import hypernetx as hnx

app = FastAPI()


@app.post("/evolve", response_model=EvolveResponse)
async def evolve(request: EvolveRequest):
    L = hnx.Hypergraph(request.rule.L)
    I = hnx.Hypergraph(request.rule.I)
    R = hnx.Hypergraph(request.rule.R)

    rule = DPORewritingRule(L, I, R)

    H = hnx.Hypergraph(request.hypergraph)

    hypergraph_form = lambda H: clean_hypergraph(H) if request.clean else H

    for _ in range(request.steps):
        res = apply_dpo_rule(hypergraph_form(H), rule)

        if not res:
            break

        _, H = res[0]

    return EvolveResponse(
        graph=[Edge(vertices=list(H.edges[e])) for e in H.edges]
    )
