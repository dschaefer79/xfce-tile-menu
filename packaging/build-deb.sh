#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 dschaefer79
# Written entirely with Claude Code (Anthropic).
# Build xfce-tile-menu as a .deb for Debian 13 (needs dpkg-deb).
#   build-deb.sh SOURCE_TARBALL VERSION OUTDIR
# The tarball is a git archive with the top directory xfce-tile-menu-VERSION.
set -eu
tarball=$1 version=$2 out=$3
name=xfce-tile-menu
revision=1
work=$(mktemp -d)
tar xzf "$tarball" -C "$work"
src=$work/$name-$version
root=$work/root

# The files, where the RPM puts them.
for f in xfce-tile xfce-tile-settings xfce-tile-menu-setup \
         resolution/xfce-resolution-set resolution/xfce-resolution-menu-setup \
         resolution/xfce-resolution-menu-settings; do
    install -Dm 0755 "$src/$f" "$root/usr/bin/${f#resolution/}"
    # Debian wants the shell at /bin/sh.
    sed -i '1s|^#!/usr/bin/sh$|#!/bin/sh|' "$root/usr/bin/${f#resolution/}"
done
install -Dm 0644 "$src/tile.menu" "$root/usr/share/$name/tile.menu"
install -Dm 0644 -t "$root/usr/share/$name/items" "$src"/items/*.desktop
install -Dm 0644 -t "$root/usr/share/icons/hicolor/scalable/actions" "$src"/icons/*.svg
for f in xfce-tile-menu.desktop xfce-tile-settings.desktop \
         resolution/xfce-resolution-menu-settings.desktop resolution/xfce-resolution-menu.desktop; do
    install -Dm 0644 "$src/$f" "$root/usr/share/applications/${f#resolution/}"
done
for f in xfce-tile-menu-setup.desktop xfce-tile-snap.desktop resolution/xfce-resolution-menu-setup.desktop; do
    install -Dm 0644 "$src/$f" "$root/etc/xdg/autostart/${f#resolution/}"
done
install -Dm 0644 "$src/resolution/resolutions" "$root/etc/xfce-resolution-menu/resolutions"

# Documentation, as Debian wants it.
doc=$root/usr/share/doc/$name
install -Dm 0644 "$src/README.md" "$doc/README.md"
cat > "$doc/copyright" <<EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: $name
Upstream-Contact: dschaefer79 <7472357+dschaefer79@users.noreply.github.com>
Source: https://github.com/dschaefer79/$name
Comment: Written entirely with Claude Code, Anthropic's AI coding assistant.

Files: *
Copyright: 2026 dschaefer79
License: GPL-3.0-or-later

License: GPL-3.0-or-later
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 .
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 .
 On Debian systems, the complete text of the GNU General Public License
 version 3 can be found in "/usr/share/common-licenses/GPL-3".
EOF
cat > "$work/changelog" <<EOF
$name ($version-$revision) stable; urgency=medium

  * Package for Debian 13 (trixie), built from
    https://github.com/dschaefer79/$name tag v$version.

 -- dschaefer79 <7472357+dschaefer79@users.noreply.github.com>  $(date -R)
EOF
gzip -9n -c "$work/changelog" > "$doc/changelog.Debian.gz"
chmod 0644 "$doc/changelog.Debian.gz"

# Control files.
mkdir -p "$root/DEBIAN"
size=$(du -sk --exclude=DEBIAN "$root" | cut -f1)
cat > "$root/DEBIAN/control" <<EOF
Package: $name
Version: $version-$revision
Architecture: all
Maintainer: dschaefer79 <7472357+dschaefer79@users.noreply.github.com>
Installed-Size: $size
Depends: python3, python3-gi, gir1.2-gtk-3.0, gir1.2-wnck-3.0, xfce4-panel, xfce4-settings, xfwm4, xfconf, procps, libnotify-bin, x11-xserver-utils
Recommends: xcvt
Section: xfce
Priority: optional
Homepage: https://github.com/dschaefer79/$name
Description: XFCE panel menus for window tiling and screen resolution
 Two XFCE panel menus. Tiling tiles the windows of the current workspace
 into columns, rows or a grid (automatically, 2, 3 or 4 columns, 2 or 3
 rows, a 2 x 2, 3 x 2 or 4 x 2 grid), puts them back with Restore, can tile
 new windows as they open and snap dropped windows into place, with
 keyboard shortcuts for every action. Resolution switches the screen
 resolution with xrandr from a list you edit, adding sizes the screen does
 not offer.
 .
 Both menus are put on the panel at the next login, or right away by
 running xfce-tile-menu-setup and xfce-resolution-menu-setup.
 .
 Written entirely with Claude Code, Anthropic's AI coding assistant.
EOF
cat > "$root/DEBIAN/conffiles" <<EOF
/etc/xdg/autostart/xfce-tile-menu-setup.desktop
/etc/xdg/autostart/xfce-tile-snap.desktop
/etc/xdg/autostart/xfce-resolution-menu-setup.desktop
/etc/xfce-resolution-menu/resolutions
EOF
cat > "$root/DEBIAN/postinst" <<'EOF'
#!/bin/sh
# For users logged in to XFCE, move the panel button to their own menu,
# rebuild both menus and restart the snap daemon, so the new version is used
# without logging out.
set -e
if [ "$1" = configure ]; then
    for pid in $(pgrep -x xfce4-panel 2>/dev/null || :); do
        user=$(id -nu "$(ps -o uid= -p "$pid" | tr -d ' ')" 2>/dev/null) || continue
        env=$(tr '\0' '\n' <"/proc/$pid/environ" 2>/dev/null |
            grep -E '^(DISPLAY|DBUS_SESSION_BUS_ADDRESS|XAUTHORITY|XDG_RUNTIME_DIR|HOME)=') || continue
        pkill -u "$user" -f 'xfce-tile snap-daemon' 2>/dev/null || :
        runuser -u "$user" -- env $env sh -c \
            'xfce-tile-menu-setup --auto >/dev/null 2>&1; xfce-resolution-menu-setup --auto >/dev/null 2>&1; setsid xfce-tile snap-daemon >/dev/null 2>&1 &' || :
    done
fi
exit 0
EOF
chmod 0755 "$root/DEBIAN/postinst"

mkdir -p "$out"
dpkg-deb --root-owner-group --build "$root" "$out/${name}_${version}-${revision}_all.deb"
rm -rf "$work"
