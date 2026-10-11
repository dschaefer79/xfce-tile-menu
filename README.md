# xfce-tile-menu

Two menus for the XFCE panel: **Tiling** arranges the windows of the current
workspace, and **Resolution** switches the screen resolution with xrandr.

This project was written entirely with
[Claude Code](https://claude.com/claude-code), Anthropic's AI coding
assistant: all code, packaging and documentation.

## Tiling

- **Layouts:** tile automatically, or into 4, 3 or 2 columns, 3 or 2 rows, or a
  2 × 2, 3 × 2 or 4 × 2 grid. "Automatically" picks the number of columns and
  rows from the screen size (3 columns from 5120 pixels wide, otherwise 2, by
  default).
- **All windows are tiled:** the most recently used windows fill the layout,
  and the others go into the cell under their middle, behind them.
- **Restore windows** puts every window back where it was.
- **Tile new windows:** each window that opens is tiled with the others, in
  the layout last used on its screen.
- **Snapping:** a window dragged with the mouse and dropped fills the column,
  row or grid cell under the pointer. Optionally only with Shift held, or with
  Shift swapping columns and rows.
- **Resize neighbouring windows together:** dragging the edge of a window also
  moves the edge of the window beside it.
- **Gap** between windows, in pixels or millimetres.
- **Window effects:** turns XFCE's compositor (shadows, transparency, fading)
  on or off, like "Enable display compositing" in Window Manager Tweaks.
- **Keyboard shortcuts** for every action, as XFCE application shortcuts, shown
  in the menu. Default keys: Super+Alt+A (auto), Super+Alt+2/3/4 (columns),
  Super+Ctrl+Alt+2/3 (rows), Super+Ctrl+2/3/4 (grids), Super+Alt+0 (restore),
  only where XFCE does not already use the key.
- **Disable tiling** turns all tiling and snapping off; Restore still works.

## Resolution

- Switches to the resolutions in your list (1920 × 1080, 1900 × 1000 and
  5120 × 1440 by default). Sizes the screen does not offer are added to it with
  xrandr, when picked or right away.
- Edit the list in its settings: add, remove, edit and reorder.

## Settings and menus

- **Settings Manager** has "Window Tiling" (Personal) and "Resolution Menu"
  (Hardware). Tiling settings take effect with **Apply**.
- **Show … menu on the panel** in each settings window puts that menu on the
  panel or takes it off.
- **Save settings to file… / Load settings from file…** keep a copy of the
  settings of both menus and the shortcuts, or move them to another computer.
- **Quit** at the bottom of each menu takes it off the panel. "Window Tiling
  Menu" and "Resolution Menu" in the applications menu put them back.

## Command line

`xfce-tile auto|4|3|2|rows-3|rows-2|grid-2x2|grid-3x2|grid-4x2|restore` tiles;
`xfce-tile toggle snap|tile-new|disabled|vertical|horizontal`, `xfce-tile menu`,
`xfce-tile export FILE` and `xfce-tile import FILE`. `xfce-resolution-set
WIDTHxHEIGHT` switches the resolution. `xfce-tile-menu-setup` and
`xfce-resolution-menu-setup` put the menus on the panel (`--remove` takes them
off, `--status` says whether they are there).

## Building the RPM

```
git archive --prefix=xfce-tile-menu-2.17/ -o ~/rpmbuild/SOURCES/xfce-tile-menu-2.17.tar.gz HEAD
rpmbuild -ba xfce-tile-menu.spec
```

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
Copyright (C) 2026 dschaefer79.
