"""
schema.py
"""

from typing import Literal, List, Optional

from pydantic import BaseModel, Field


class DialogueItem(BaseModel):
    """A single dialogue item."""

    speaker: Literal["Host (MotionG Host)", "Guest"]
    text: str
    audio_file_path: Optional[str]


class ShortDialogue(BaseModel):
    """The dialogue between the host and guest."""

    scratchpad: str
    name_of_guest: str
    dialogue: List[DialogueItem] = Field(
        ..., description="A list of dialogue items, typically between 11 to 17 items"
    )


class MediumDialogue(BaseModel):
    """The dialogue between the host and guest."""

    scratchpad: str
    name_of_guest: str
    dialogue: List[DialogueItem] = Field(
        ..., description="A list of dialogue items, typically between 19 to 29 items"
    )

