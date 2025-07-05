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


class ScrollToBottomAction(BaseModel):
    type: Literal["scroll_to_bottom"]


class ScrollToTopAction(BaseModel):
    type: Literal["scroll_to_top"]


class HoverAction(BaseModel):
    type: Literal["hover"]
    selector: str


class SelectAction(BaseModel):
    type: Literal["select"]
    selector: str
    value: str


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
    ScrollToBottomAction,
    ScrollToTopAction,
    HoverAction,
    SelectAction,
    DoneAction,
]


class ActionItem(BaseModel):
    thought: str = Field(..., description="Brief reasoning for this action")
    action: Action


class NextActions(BaseModel):
    actions: List[ActionItem]
