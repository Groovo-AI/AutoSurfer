from __future__ import annotations

from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


class GotoAction(BaseModel):
    type: Literal["goto"]
    url: str


class ClickAction(BaseModel):
    type: Literal["click"]
    selector: str


class FillAction(BaseModel):
    type: Literal["fill"]
    selector: str
    value: str


class PressAction(BaseModel):
    type: Literal["press"]
    key: str


class WaitAction(BaseModel):
    type: Literal["wait"]
    seconds: float


class ScrollAction(BaseModel):
    type: Literal["scroll"]
    direction: Literal["up", "down"]
    selector: Optional[str] = None


class DoneAction(BaseModel):
    type: Literal["done"]
    summary: str


Action = Union[
    GotoAction,
    ClickAction,
    FillAction,
    PressAction,
    WaitAction,
    ScrollAction,
    DoneAction,
]


class ActionItem(BaseModel):
    thought: str
    action: Action


class NextActions(BaseModel):
    actions: List[ActionItem] = Field(..., min_items=1, max_items=2)
