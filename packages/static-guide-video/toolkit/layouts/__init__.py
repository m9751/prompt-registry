"""Scene layout library — one module per layout type."""
from __future__ import annotations

from typing import Any, Callable

from . import (
    cta_inguide,
    cta_steps,
    depth_tabs,
    editor_tabs,
    image,
    kinetic_outcomes,
    kinetic_pain,
    proof_highlight,
    split_imagine,
)

LAYOUT_WAITS: dict[str, int] = {
    "kinetic_pain": 1500,
    "kinetic_outcomes": 1200,
    "cta_inguide": 1300,
    "editor_tabs": 1100,
    "proof_highlight": 1400,
    "depth_tabs": 1200,
    "cta_steps": 1200,
}

DARK_LAYOUTS = frozenset({"kinetic_pain", "cta_inguide"})

_RENDERERS: dict[str, Callable[[dict[str, Any]], str]] = {
    "kinetic_pain": kinetic_pain.render,
    "split_imagine": split_imagine.render,
    "kinetic_outcomes": kinetic_outcomes.render,
    "editor_tabs": editor_tabs.render,
    "proof_highlight": proof_highlight.render,
    "depth_tabs": depth_tabs.render,
    "cta_steps": cta_steps.render,
    "cta_inguide": cta_inguide.render,
    "image": image.render,
}


def render_inner(scene: dict[str, Any]) -> str:
    layout = scene.get("layout", "image")
    renderer = _RENDERERS.get(layout, image.render)
    return renderer(scene)


def body_class(scene: dict[str, Any]) -> str:
    layout = scene.get("layout", "image")
    kind = scene.get("kind", "content")
    if kind == "title" or layout in DARK_LAYOUTS:
        return "dark"
    return "light"