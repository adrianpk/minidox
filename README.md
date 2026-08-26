# MiniDox QWERTY–Colemak Keymap

![MiniDox Layer 0 — QWERTY](assets/img/layers/layer-0-qwerty.svg)

[View the complete layer reference](assets/img/layers/index.md).

This repository contains a reusable QMK Userspace keymap for a 36-key split
ergonomic keyboard with a 3x5+3 layout: three rows of five column-staggered
keys per half, plus three thumb keys per side.

It belongs to the same compact 36-key split category as a 5-column Corne,
while using a MiniDox-compatible layout.

The firmware uses the QMK keyboard target
`maple_computing/minidox/rev1` and the `LAYOUT_split_3x5_3` layout.

## What you get

The default typing layer is QWERTY, with Colemak available as an alternative.
Dedicated layers provide numbers and symbols, function and numpad keys, media
and navigation controls, programming symbols, and extended function keys for
host-defined shortcuts.

The thumb keys stay consistent across the typing layers:

```text
Left:  Shift  Control  Space / Layer 6
Right: Backspace  Enter  Esc / Layer 4
```

Tapping the far-right thumb key sends `Escape`. Holding it activates the layer
selector. Tapping `Space` sends a normal space; holding it activates layer 6.

## Layers

| Layer | Purpose | Contents |
|------:|---------|----------|
| 0 | QWERTY | Standard QWERTY letters and punctuation |
| 1 | Numbers and symbols | Digits, shifted symbols, brackets, braces, backtick, tilde, slash, and backslash |
| 2 | Function and numpad | `F1`–`F12`, numpad keys, Insert, and Print Screen |
| 3 | Media and navigation | Mute, volume, brightness, Home, End, Insert, Delete, Page Up, Page Down, Print Screen, Scroll Lock, and programming symbols tuned for a Latin American host layout |
| 4 | Layer selector | Selects layers 0–5 with `DF(0)` through `DF(5)` |
| 5 | Colemak | Standard Colemak letters with the same punctuation and thumb keys as QWERTY |
| 6 | Extended function keys | `F13`–`F24` arranged as a left-hand 3×4 block for host-defined shortcuts |

The two typing layouts are:

```text
QWERTY                    Colemak
Q W E R T   Y U I O P     Q W F P G   J L U Y ;
A S D F G   H J K L ;     A R S T D   H N E I O
Z X C V B   N M , . /     Z X C V B   K M , . /
```

## Switching layers

Hold the far-right `Esc / Layer 4` thumb key, then press one of the first three
keys on the left half:

```text
Top row:   Layer 0  Layer 1  Layer 2
Home row:  Layer 3  Layer 4  Layer 5
```

The same selector is repeated on the three rightmost keys of the right half.
Selecting a layer with `DF(n)` makes it the active default layer. Use the same
sequence to switch again.

Hold the left `Space / Layer 6` thumb key to access the extended function keys:

```text
F13  F14  F15  F16   → host shortcuts 1–4
F17  F18  F19  F20   → host shortcuts 5–8
F21  F22  F23  F24   → host shortcuts 9–12
```

On the configured desktop host, these shortcuts select virtual desktops 1–12.

## Keymap

The complete keymap is stored at:

```text
keyboards/maple_computing/minidox/rev1/keymaps/qwerty_colemak/keymap.json
```

The JSON file can be imported directly into
[QMK Configurator](https://config.qmk.fm/#/maple_computing/minidox/rev1/LAYOUT_split_3x5_3).

## GitHub build

Every push runs the official QMK Userspace build workflow. Successful builds
are published as repository release artifacts.

The configured build target is:

```text
maple_computing/minidox/rev1:qwerty_colemak
```

## Local build

Configure a QMK firmware checkout and this repository as the external
userspace overlay:

```sh
qmk config user.overlay_dir="$(realpath .)"
qmk compile -kb maple_computing/minidox/rev1 -km qwerty_colemak
```

The QMK firmware checkout must be configured separately through
`qmk config user.qmk_home`.
