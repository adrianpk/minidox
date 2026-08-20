#!/usr/bin/env python3
"""Generate the MiniDox layer reference SVG files from the QMK keymap."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KEYMAP_PATH = (
    ROOT
    / "keyboards"
    / "maple_computing"
    / "minidox"
    / "rev1"
    / "keymaps"
    / "adrianpk"
    / "keymap.json"
)
OUTPUT_DIR = ROOT / "assets" / "img" / "layers"

LAYER_METADATA = {
    0: {
        "slug": "qwerty",
        "title": "QWERTY",
        "summary": "QWERTY typing layer",
        "legend": [
            ("primary", "Letters"),
            ("symbol", "Punctuation"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("layer", "Layer access"),
        ],
    },
    1: {
        "slug": "numbers-symbols",
        "title": "NUMBERS & SYMBOLS",
        "summary": "Numbers and symbols layer",
        "legend": [
            ("primary", "Numbers"),
            ("symbol", "Symbols"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("layer", "Layer access"),
        ],
    },
    2: {
        "slug": "function-numpad",
        "title": "FUNCTION & NUMPAD",
        "summary": "Function and numpad layer",
        "legend": [
            ("primary", "Function keys"),
            ("secondary", "Numpad"),
            ("action", "System keys"),
            ("modifier", "Modifiers"),
            ("layer", "Layer access"),
        ],
    },
    3: {
        "slug": "media-navigation",
        "title": "MEDIA & NAVIGATION",
        "summary": "Media, navigation, and programming symbols layer",
        "legend": [
            ("secondary", "Media"),
            ("action", "Navigation"),
            ("symbol", "Programming symbols"),
            ("modifier", "Modifiers"),
            ("layer", "Layer access"),
        ],
    },
    4: {
        "slug": "layer-selector",
        "title": "LAYER SELECTOR",
        "summary": "Default layer selector",
        "legend": [
            ("layer", "Layer selection"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("empty", "Unassigned"),
        ],
    },
    5: {
        "slug": "colemak",
        "title": "COLEMAK",
        "summary": "Colemak typing layer",
        "legend": [
            ("primary", "Letters"),
            ("symbol", "Punctuation"),
            ("modifier", "Modifiers"),
            ("action", "Editing"),
            ("layer", "Layer access"),
        ],
    },
}

COLORS = {
    "primary": "#d1d5db",
    "symbol": "#c4b5d4",
    "modifier": "#aeb0ec",
    "action": "#acd0ed",
    "layer": "#fcf7a8",
    "secondary": "#b9dfc5",
    "empty": "#f3f4f6",
}

SIMPLE_LABELS = {
    "KC_0": "0",
    "KC_1": "1",
    "KC_2": "2",
    "KC_3": "3",
    "KC_4": "4",
    "KC_5": "5",
    "KC_6": "6",
    "KC_7": "7",
    "KC_8": "8",
    "KC_9": "9",
    "KC_EXLM": "!",
    "KC_AT": "@",
    "KC_HASH": "#",
    "KC_DLR": "$",
    "KC_PERC": "%",
    "KC_CIRC": "^",
    "KC_AMPR": "&",
    "KC_ASTR": "*",
    "KC_LPRN": "(",
    "KC_RPRN": ")",
    "KC_MINS": "−",
    "KC_EQL": "=",
    "KC_LBRC": "[",
    "KC_RBRC": "]",
    "KC_LCBR": "{",
    "KC_RCBR": "}",
    "KC_GRV": "\u0060",
    "KC_TILD": "~",
    "KC_BSLS": "\\",
    "KC_SLSH": "/",
    "KC_SCLN": ";",
    "KC_COMM": ",",
    "KC_DOT": ".",
    "KC_INS": "Ins",
    "KC_DEL": "Del",
    "KC_HOME": "Home",
    "KC_END": "End",
    "KC_PGUP": "PgUp",
    "KC_PGDN": "PgDn",
    "KC_PSCR": "PrtSc",
    "KC_SLCK": "ScrLk",
    "KC_MUTE": "Mute",
    "KC_VOLD": "Vol −",
    "KC_VOLU": "Vol +",
    "KC_BRID": "Bright −",
    "KC_BRIU": "Bright +",
    "KC_NUBS": "< >",
}

THUMB_KEYS = {
    "KC_LSFT": ("Shift", "", "modifier"),
    "KC_LCTL": ("Ctrl", "", "modifier"),
    "KC_SPC": ("Space", "", "action"),
    "KC_BSPC": ("Bksp", "", "action"),
    "KC_ENT": ("Enter", "", "action"),
    "LT(4,KC_ESC)": ("Esc", "HOLD L4", "layer"),
}

LATAM_SYMBOLS = {
    "LSFT(KC_8)": "(",
    "LSFT(KC_9)": ")",
    "RALT(KC_8)": "[",
    "RALT(KC_9)": "]",
    "RALT(KC_7)": "{",
    "RALT(KC_0)": "}",
    "KC_NUBS": "< >",
    "LSFT(KC_7)": "/",
    "RALT(KC_MINS)": "\\",
    "RALT(KC_1)": "|",
    "RALT(KC_4)": "~",
    "KC_GRV": "|",
    "KC_LBRC": "´",
    "RALT(KC_6)": "¬",
}

KEY_WIDTH = 58
KEY_HEIGHT = 54
COLUMN_STEP = 68
ROW_STEP = 64
LEFT_X = 70
RIGHT_X = 710
TOP_Y = 120
LEFT_COLUMN_OFFSETS = (24, 10, 0, 8, 22)
RIGHT_COLUMN_OFFSETS = (22, 8, 0, 10, 24)


def describe_keycode(keycode: str, layer: int) -> tuple[str, str, str]:
    if keycode in THUMB_KEYS:
        return THUMB_KEYS[keycode]

    default_layer = re.fullmatch(r"DF\((\d+)\)", keycode)
    if default_layer:
        return f"L{default_layer.group(1)}", "SELECT", "layer"

    if keycode == "KC_NO":
        return "—", "", "empty"

    letter = re.fullmatch(r"KC_([A-Z])", keycode)
    if letter:
        return letter.group(1), "", "primary"

    function_key = re.fullmatch(r"KC_F(\d+)", keycode)
    if function_key:
        return f"F{function_key.group(1)}", "", "primary"

    numpad_digit = re.fullmatch(r"KC_P(\d)", keycode)
    if numpad_digit:
        return numpad_digit.group(1), "NUM", "secondary"

    numpad_labels = {
        "KC_PSLS": "/",
        "KC_PAST": "*",
        "KC_PMNS": "−",
        "KC_PPLS": "+",
        "KC_PEQL": "=",
    }
    if keycode in numpad_labels:
        return numpad_labels[keycode], "NUM", "secondary"

    if layer == 3 and keycode in LATAM_SYMBOLS:
        return LATAM_SYMBOLS[keycode], "", "symbol"

    if keycode in {"KC_MUTE", "KC_VOLD", "KC_VOLU", "KC_BRID", "KC_BRIU"}:
        return SIMPLE_LABELS[keycode], "", "secondary"

    if keycode in {
        "KC_INS",
        "KC_DEL",
        "KC_HOME",
        "KC_END",
        "KC_PGUP",
        "KC_PGDN",
        "KC_PSCR",
        "KC_SLCK",
    }:
        return SIMPLE_LABELS[keycode], "", "action"

    if keycode in SIMPLE_LABELS:
        category = "primary" if keycode.startswith("KC_") and keycode[3:].isdigit() else "symbol"
        return SIMPLE_LABELS[keycode], "", category

    return keycode.removeprefix("KC_"), "", "primary"


def key_svg(
    x: int,
    y: int,
    keycode: str,
    layer: int,
    *,
    key_width: int = KEY_WIDTH,
    key_height: int = KEY_HEIGHT,
) -> str:
    label, sublabel, category = describe_keycode(keycode, layer)
    fill = COLORS[category]
    label_size = 17 if len(label) <= 5 else 12
    label_y = y + key_height / 2 + (-4 if sublabel else 1)
    parts = [
        (
            f'<rect x="{x}" y="{y}" width="{key_width}" height="{key_height}" '
            f'rx="8" fill="{fill}" stroke="#8b8f97" stroke-width="1.2"/>'
        ),
        (
            f'<text x="{x + key_width / 2}" y="{label_y}" class="key-label" '
            f'font-size="{label_size}">{escape(label)}</text>'
        ),
    ]
    if sublabel:
        parts.append(
            f'<text x="{x + key_width / 2}" y="{y + key_height / 2 + 13}" '
            f'class="key-sub">{escape(sublabel)}</text>'
        )
    return "\n".join(parts)


def legend_svg(items: list[tuple[str, str]]) -> str:
    item_widths = [32 + len(label) * 7 for _, label in items]
    total_width = sum(item_widths) + 18 * (len(items) - 1)
    cursor = (1120 - total_width) / 2
    parts: list[str] = []

    for (category, label), width in zip(items, item_widths, strict=True):
        parts.append(
            f'<rect x="{cursor:.1f}" y="480" width="12" height="12" rx="3" '
            f'fill="{COLORS[category]}" stroke="#8b8f97" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{cursor + 19:.1f}" y="490" class="legend-label">{escape(label)}</text>'
        )
        cursor += width + 18

    return "\n".join(parts)


def generate_svg(layer_number: int, keys: list[str]) -> str:
    metadata = LAYER_METADATA[layer_number]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 520" role="img"',
        f'  aria-labelledby="layer-{layer_number}-title layer-{layer_number}-description">',
        f'  <title id="layer-{layer_number}-title">MiniDox layer {layer_number}: {escape(metadata["title"])}</title>',
        f'  <desc id="layer-{layer_number}-description">{escape(metadata["summary"])}</desc>',
        "  <style>",
        "    text { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif; fill: #111827; }",
        "    .kicker { font-size: 12px; font-weight: 600; letter-spacing: 2px; text-anchor: middle; fill: #718096; }",
        "    .title { font-size: 27px; font-weight: 600; text-anchor: middle; }",
        "    .key-label { font-weight: 500; text-anchor: middle; dominant-baseline: middle; }",
        "    .key-sub { font-size: 8px; font-weight: 600; letter-spacing: 0.4px; text-anchor: middle; fill: #667085; }",
        "    .half-label { font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-anchor: middle; fill: #718096; }",
        "    .legend-label { font-size: 11px; fill: #667085; }",
        "  </style>",
        '  <text x="560" y="28" class="kicker">MINIDOX · 3×5+3</text>',
        f'  <text x="560" y="66" class="title">LAYER {layer_number} · {escape(metadata["title"])}</text>',
    ]

    for row in range(3):
        for column in range(5):
            left_index = row * 10 + column
            right_index = row * 10 + 5 + column
            left_y = TOP_Y + LEFT_COLUMN_OFFSETS[column] + row * ROW_STEP
            right_y = TOP_Y + RIGHT_COLUMN_OFFSETS[column] + row * ROW_STEP
            parts.append(
                "  "
                + key_svg(
                    LEFT_X + column * COLUMN_STEP,
                    left_y,
                    keys[left_index],
                    layer_number,
                )
            )
            parts.append(
                "  "
                + key_svg(
                    RIGHT_X + column * COLUMN_STEP,
                    right_y,
                    keys[right_index],
                    layer_number,
                )
            )

    left_thumb_x = (206, 274, 342)
    right_thumb_x = (710, 778, 846)
    for offset, x in enumerate(left_thumb_x):
        parts.append("  " + key_svg(x, 348, keys[30 + offset], layer_number))
    for offset, x in enumerate(right_thumb_x):
        parts.append("  " + key_svg(x, 348, keys[33 + offset], layer_number))

    parts.extend(
        [
            '  <text x="274" y="440" class="half-label">LEFT HALF</text>',
            '  <text x="778" y="440" class="half-label">RIGHT HALF</text>',
            "  " + legend_svg(metadata["legend"]),
            "</svg>",
            "",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    keymap = json.loads(KEYMAP_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for layer_number, metadata in LAYER_METADATA.items():
        output_path = OUTPUT_DIR / f"layer-{layer_number}-{metadata['slug']}.svg"
        output_path.write_text(
            generate_svg(layer_number, keymap["layers"][layer_number]),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
