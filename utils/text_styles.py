"""
Text style converters
"""

from core.constants import FONTS


def apply_font(text: str, style: str) -> str:
    if style not in FONTS:
        return text
    return text.translate(FONTS[style])


def bold(text: str) -> str:
    return apply_font(text, "bold")


def italic(text: str) -> str:
    return apply_font(text, "italic")


def mono(text: str) -> str:
    return apply_font(text, "monospace")


def bubble(text: str) -> str:
    return apply_font(text, "bubble")
