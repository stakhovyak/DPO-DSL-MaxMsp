from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import hypernetx as hnx
import traceback, logging
from src.api.models import EvolveRequest, EvolveResponse, Edge

from src.dpo import apply_dpo_rule, DPORewritingRule, clean_hypergraph

app = FastAPI()
logger = logging.getLogger("uvicorn.error")


def edge_list_to_dict(edges: List[Edge]) -> dict:
    return {f"e{i}": edge.vertices for i, edge in enumerate(edges)}


@app.post("/evolve", response_model=EvolveResponse)
async def evolve(request: EvolveRequest):
    try:
        L = hnx.Hypergraph(edge_list_to_dict(request.rule.L))
        I = hnx.Hypergraph(edge_list_to_dict(request.rule.I))
        R = hnx.Hypergraph(edge_list_to_dict(request.rule.R))
        rule = DPORewritingRule(L, I, R)

        H = hnx.Hypergraph(edge_list_to_dict(request.hypergraph))

        logger.info(f"steps: {request.steps}")

        for step in range(request.steps):
            ## TODO ! clean hypergraph doesn't work!!
            current = clean_hypergraph(H) if request.clean == True else H

            res = apply_dpo_rule(current, rule)
            logger.info(step)
            if not res:
                break
            _, H = res[0]

        out = [Edge(vertices=list(H.edges[e].elements)) for e in H.edges]

        return EvolveResponse(hypergraph=out)

    except Exception as exc:
        tb = traceback.format_exc()
        logger.error(f"Error in /evolve:\n{tb}")
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "trace": tb.splitlines()[-1]},
        )
