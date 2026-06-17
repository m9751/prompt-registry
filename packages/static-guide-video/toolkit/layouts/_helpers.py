"""Shared helpers for scene layout renderers."""
from __future__ import annotations


def img_src(path: str) -> str:
    if not path:
        return ""
    if path.startswith("../screenshots"):
        return "../../screenshots/" + path.split("/", 2)[-1]
    if path.startswith("../"):
        return path
    return f"../{path}"


def scene_image(scene: dict) -> str:
    return img_src(scene.get("image", ""))


def scene_image2(scene: dict) -> str:
    return img_src(scene.get("image2", ""))