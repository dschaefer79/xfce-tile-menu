# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 dschaefer79
# Written entirely with Claude Code (Anthropic).

Name:           xfce-tile-menu
Version:        2.17
Release:        1%{?dist}
Summary:        XFCE panel menus for window tiling and screen resolution
License:        GPL-3.0-or-later
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
Requires:       python3-gobject
Requires:       gtk3
Requires:       libwnck3
Requires:       xfce4-panel
Requires:       xfce4-settings
Requires:       xfwm4
Requires:       xfconf
Requires:       garcon
Requires:       procps-ng
Requires:       libnotify
# The resolution menu
Requires:       xrandr
Recommends:     cvt
# The resolution menu was a package of its own up to 2.0.
Obsoletes:      xfce-resolution-menu < 2.1
Provides:       xfce-resolution-menu = %{version}-%{release}
Requires(posttrans): procps-ng
Requires(posttrans): /usr/sbin/runuser

%description
Two XFCE panel menus, the counterparts of plasma-tile-menu's widgets.

The XFCE counterpart of plasma-tile-menu's Window Tiling widget: a button on
the top XFCE panel with a menu that tiles the windows of the current
workspace into side-by-side columns, rows stacked top to bottom, or a grid
of both: automatically (3 columns on screens at least 5120 pixels wide,
such as 5120x1440, and 2 otherwise; rows follow the same rule by screen
height), or into 4, 3 or 2 columns, 3 or 2 rows, or a 2x2, 3x2 or 4x2 grid
directly, and
puts them back with Restore. New windows can be tiled automatically as they
open, into the layout last used on their screen. The settings window turns
columns and rows on or off, sets the auto rules and the gap between windows
(in pixels or millimetres), and can turn on snapping: a window dragged with
the mouse and dropped fills the column, row or grid cell under the pointer.
Snapping can be limited to drops with Shift held, and Shift can swap
columns and rows. Every action can have a keyboard shortcut, set in the
settings window. The menu shows the entries for the directions that are on
and the switches with their state.

Resolution switches the display resolution with xrandr from a list
(1920x1080, 1900x1000 and 5120x1440 by default). Its settings window,
reachable from the menu and from the XFCE Settings Manager, adds, removes
and reorders resolutions, and adds new ones to the screen right away or at
the press of a button. Missing modes are added automatically, which also
makes it work in TigerVNC sessions.

Both buttons are added to the top panel for each user at their next login,
or right away by running xfce-tile-menu-setup and xfce-resolution-menu-setup.

This project was written entirely with Claude Code, Anthropic's AI coding assistant.

%prep
%autosetup

%build

%install
install -Dpm 0755 xfce-tile %{buildroot}%{_bindir}/xfce-tile
install -Dpm 0644 xfce-tile-menu.desktop %{buildroot}%{_datadir}/applications/xfce-tile-menu.desktop
install -Dpm 0755 xfce-tile-settings %{buildroot}%{_bindir}/xfce-tile-settings
install -Dpm 0755 xfce-tile-menu-setup %{buildroot}%{_bindir}/xfce-tile-menu-setup
install -Dpm 0644 tile.menu %{buildroot}%{_datadir}/%{name}/tile.menu
install -dm 0755 %{buildroot}%{_datadir}/%{name}/items
install -pm 0644 items/*.desktop %{buildroot}%{_datadir}/%{name}/items/
install -dm 0755 %{buildroot}%{_datadir}/icons/hicolor/scalable/actions
install -pm 0644 icons/*.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/actions/
install -Dpm 0644 xfce-tile-settings.desktop %{buildroot}%{_datadir}/applications/xfce-tile-settings.desktop
install -Dpm 0644 xfce-tile-menu-setup.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/xfce-tile-menu-setup.desktop
install -Dpm 0644 xfce-tile-snap.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/xfce-tile-snap.desktop
# The resolution menu
install -Dpm 0755 resolution/xfce-resolution-set %{buildroot}%{_bindir}/xfce-resolution-set
install -Dpm 0755 resolution/xfce-resolution-menu-setup %{buildroot}%{_bindir}/xfce-resolution-menu-setup
install -Dpm 0755 resolution/xfce-resolution-menu-settings %{buildroot}%{_bindir}/xfce-resolution-menu-settings
install -Dpm 0644 resolution/xfce-resolution-menu-settings.desktop %{buildroot}%{_datadir}/applications/xfce-resolution-menu-settings.desktop
install -Dpm 0644 resolution/xfce-resolution-menu.desktop %{buildroot}%{_datadir}/applications/xfce-resolution-menu.desktop
install -Dpm 0644 resolution/resolutions %{buildroot}%{_sysconfdir}/xfce-resolution-menu/resolutions
install -Dpm 0644 resolution/xfce-resolution-menu-setup.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/xfce-resolution-menu-setup.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/%{name}/items/*.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/*.desktop

%posttrans
# For users logged in to XFCE, move the panel button to their own menu,
# rebuild both menus and restart the snap daemon, so the new version is used
# without logging out.
for pid in $(pgrep -x xfce4-panel 2>/dev/null); do
    user=$(id -nu "$(ps -o uid= -p "$pid" | tr -d ' ')" 2>/dev/null) || continue
    env=$(tr '\0' '\n' <"/proc/$pid/environ" 2>/dev/null |
        grep -E '^(DISPLAY|DBUS_SESSION_BUS_ADDRESS|XAUTHORITY|XDG_RUNTIME_DIR|HOME)=') || continue
    pkill -u "$user" -f 'xfce-tile snap-daemon' 2>/dev/null
    runuser -u "$user" -- env $env sh -c \
        'xfce-tile-menu-setup --auto >/dev/null 2>&1; xfce-resolution-menu-setup --auto >/dev/null 2>&1; setsid xfce-tile snap-daemon >/dev/null 2>&1 &' || :
done
:

%files
%license LICENSE
%doc README.md
%{_bindir}/xfce-tile
%{_datadir}/applications/xfce-tile-menu.desktop
%{_bindir}/xfce-tile-settings
%{_bindir}/xfce-tile-menu-setup
%{_datadir}/%{name}/
%{_datadir}/applications/xfce-tile-settings.desktop
%{_datadir}/icons/hicolor/scalable/actions/xfce-tile-columns-*-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/xfce-tile-rows-*-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/xfce-tile-grid-*-symbolic.svg
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfce-tile-menu-setup.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfce-tile-snap.desktop
%{_bindir}/xfce-resolution-set
%{_bindir}/xfce-resolution-menu-setup
%{_bindir}/xfce-resolution-menu-settings
%{_datadir}/applications/xfce-resolution-menu-settings.desktop
%{_datadir}/applications/xfce-resolution-menu.desktop
%dir %{_sysconfdir}/xfce-resolution-menu
%config(noreplace) %{_sysconfdir}/xfce-resolution-menu/resolutions
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfce-resolution-menu-setup.desktop

%changelog
* Sun Oct 11 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.17-1
- License: GPL-3.0-or-later (was MIT), with the license text and a
  header in every source file
- README.md describing all features; the project was written entirely
  with Claude, Anthropic's AI assistant

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.16-1
- Settings Manager: "Window Tiling" has "Show the Tiling menu on the
  panel" (applied with Apply) and "Resolution Menu" "Show the
  Resolution menu on the panel", to put each menu on the panel or take
  it off. New option for both setup commands: --status

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.15-1
- Applications menu (Utilities): "Window Tiling Menu" puts the tiling
  menu on the panel and the new "Resolution Menu" the resolution menu,
  each also after its Quit

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.14-1
- Installing or upgrading also rebuilds the Resolution menu of users
  logged in to XFCE, so new entries such as Quit appear without logging
  out

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.13-1
- Resolution: "Quit" at the end of the menu takes the button off the
  panel; "Window Tiling Menu" in the applications menu now puts both
  menus back. The menu is rebuilt at login, so it has the new entry

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.12-1
- Settings: "Window effects" turns XFCE's compositor (window shadows,
  transparency and fading) off or on when applied, like "Enable display
  compositing" in Window Manager Tweaks; also kept in the settings file

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.11-1
- "Save settings to file…" and "Load settings from file…" in the Window
  Tiling and Resolution Menu settings windows: the settings of the tiling
  and resolution menus and the keyboard shortcuts in one file. New
  commands: xfce-tile export|import FILE

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.10-1
- "Window Tiling Menu" in the applications menu (Utilities) puts the
  tiling menu on the panel, also after Quit

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.9-1
- Window Tiling: "Quit" at the end of the menu takes the button off the panel; tiling
  and its shortcuts keep working. "xfce-tile-menu-setup" puts it back

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.8-1
- Window Tiling: the menu shows the keyboard shortcut of each tiling
  entry and of Restore windows after its name; the menu is
  rebuilt when a shortcut is set in the tiling settings and at login
- Default shortcuts: no longer take a key that one of XFCE's own
  default shortcuts uses

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.7-1
- Window Tiling: default keyboard shortcuts: Super+Alt+A tiles
  automatically, Super+Alt+2, 3 or 4 tiles in 2, 3 or 4 columns,
  Super+Ctrl+Alt+2 or 3 in 2 or 3 rows, Super+Ctrl+2, 3 or 4 in a 2 x 2,
  3 x 2 or 4 x 2 grid, and Super+Alt+0 restores the windows.
  Set once per user at login, only for actions without a shortcut and
  keys nothing else uses

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.6-1
- Window Tiling: layouts keep their columns, rows and cells again (undoing
  the change of 2.5); the windows that do not fit are now tiled too,
  into the cell under their middle, behind the windows in front

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.5-1
- Window Tiling: the menu entries and shortcuts tile all windows on the
  screen, not only as many as the layout has cells; a column with more
  windows than rows splits its height among all of them

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.4-1
- Window Tiling: setting "Resize neighbouring windows together" (off by
  default): dragging the left or right edge of a window also moves the
  edge of the window beside it, keeping the gap, so windows side by side
  stay together

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.3-1
- Resolution menu settings: an Edit button (or a double-click) changes the
  selected resolution

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.2-1
- Include the resolution menu (xfce-resolution-menu 2.0), so one package
  installs both XFCE menus, like plasma-tile-menu; it replaces the
  xfce-resolution-menu package

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.1-1
- Window Tiling: menu entries and shortcuts to tile in 4 columns and in a
  4 x 2 grid
- Update each user's menu at login and after upgrading, so new entries
  appear without changing a setting

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 2.0-1
- Bring the tiling up to plasma-tile-menu 1.12: tile in 3 or 2 columns or
  rows, a 2x2 or 3x2 grid, or automatically; "Tile automatically" can be
  shown in the menu (on for new users, off for users of 1.x)
- Tile only the screen under the pointer, and spread windows over the
  columns as the Plasma widget does
- Tile new windows into the layout last used on their screen (replaces
  snapping new windows into a free column and re-tiling all windows)
- Snapping fills the column, row or grid cell under the pointer; it can be
  limited to drops with Shift held, and Shift can swap columns and rows
  (replaces the choice of which direction needs Shift)
- Rows have their own tall-screen height and counts, like the columns
- The gap between windows can be set in millimetres, from each screen's
  physical size
- The menu is built for each user from the settings: entries for the
  directions that are on, and Automatic tiling, Tile new windows and
  Disable tiling with check boxes showing their state
- Keyboard shortcuts for every action, set on a new page of the settings
  window (stored as XFCE application shortcuts), and a "Keyboard
  shortcuts…" menu entry
- xfce-tile toggle snap|tile-new|disabled|vertical|horizontal and
  xfce-tile get-toggles; the 1.x commands still work
- Settings from 1.x are taken over
- Move the panel button to the new menu and restart the snap daemon for
  logged-in users after upgrading

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 1.2-1
- Turn vertical tiling (columns) or horizontal tiling (rows) on/off, in the
  menu and the settings window: off makes the menu items for that direction
  do nothing, keeps auto from tiling that way, and makes snapping use the
  other direction only; one of the two always stays on
- Automatic tiling can instead tile all windows again, as auto does,
  whenever a window opens (a choice under Tile new windows automatically)
- Settings can turn vertical tiling (columns) and horizontal tiling (rows)
  on or off; with both on, auto tiles into a grid
- Snapping fills the column under the pointer, or the row when Shift is
  held during the drop; the settings window explains this
- Settings option to choose which direction needs Shift when snapping:
  horizontal (rows, the default) or vertical (columns)
- Option to snap new windows automatically into the next free column or
  row (the direction of a drop without Shift)
- Settings window has an Apply button: changes are saved when applied,
  and closing with unapplied changes asks whether to apply them
- Snap columns (vertical) and snap rows (horizontal) counts; Auto uses the
  column and row counts for the screen size
- Add "Tile in 2×2 grid" menu item for 4 windows; xfce-tile CxR tiles into
  any grid of C columns and R rows
- Turn tiling on/off, in the menu and the settings window: off makes the
  tiling menu, snapping and automatic tiling do nothing (Restore still works)
- Turn automatic tiling on/off, in the menu and the settings window; it no
  longer needs drop snapping to be on
- Remove the "Tile automatically" menu item, which was easy to mix up with
  Turn automatic tiling on/off (xfce-tile auto still works)
- Add row counts for wide and other screens, like the column counts
- Add "Tile in 3 rows" and "Tile in 2 rows" menu items next to the columns ones

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 1.1-1
- Add snapping: windows dropped with the mouse fill the column under the
  pointer (left, middle, right); turned on in the settings window

* Sat Oct 10 2026 dschaefer79 <7472357+dschaefer79@users.noreply.github.com> - 1.0-1
- Initial package
