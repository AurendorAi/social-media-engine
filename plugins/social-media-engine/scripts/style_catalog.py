"""Offline discovery of the 27 style priorities; the host assesses brand fit."""
import json
from pathlib import Path


def catalogue():
    return json.loads((Path(__file__).resolve().parents[1] / "assets/style-catalog.json").read_text(encoding="utf-8"))
