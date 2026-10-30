"""
FastAPI app — Cho-Han dice game.

Run: python -m uvicorn main:app --reload --reload-dir .. --port 3034
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from cho_han_core import (  # noqa: E402
    dice_labels,
    initial_state,
    make_guess,
    place_bet,
    reset_purse,
    state_for_client,
)

app = FastAPI(title="Cho-Han")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class StateBody(BaseModel):
    state: dict[str, Any]


class BetBody(StateBody):
    amount: int = Field(..., ge=1)


class GuessBody(StateBody):
    guess: Literal["CHO", "HAN", "cho", "han"]


def _respond(state: dict[str, Any]) -> JSONResponse:
    payload = state_for_client(state)
    if state.get("dice1") is not None and state.get("dice2") is not None:
        if state["phase"] in ("reveal", "broke"):
            payload.update(dice_labels(int(state["dice1"]), int(state["dice2"])))
    return JSONResponse(payload)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "help.html")


@app.post("/api/reset")
async def api_reset() -> JSONResponse:
    return _respond(reset_purse(initial_state()))


@app.post("/api/bet")
async def api_bet(body: BetBody) -> JSONResponse:
    try:
        return _respond(place_bet(body.state, body.amount))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/guess")
async def api_guess(body: GuessBody) -> JSONResponse:
    try:
        return _respond(make_guess(body.state, body.guess))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
