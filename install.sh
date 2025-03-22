#!/bin/bash

BASE=$(dirname "$0")

add_layout() {
	OUT="$1"
	IN="$2"
	# remove if layout already installed
	if [ -n "$( grep -e "// BIRMAN_START" "$OUT" )" ]; then
		sudo sed -i '/BIRMAN_START/,/BIRMAN_END/d' "$OUT"
	fi

	sudo bash -c "echo >> \"$OUT\"; \
		      echo '// BIRMAN_START' >> \"$OUT\"; \
		      cat \"$IN\" >> \"$OUT\"; \
		      echo '// BIRMAN_END' >> \"$OUT\"; \
		      echo >> \"$OUT\""
}

add_layout "/usr/share/X11/xkb/symbols/us" "$BASE/symbols/typo-birman-en"
add_layout "/usr/share/X11/xkb/symbols/ru" "$BASE/symbols/typo-birman-ru"

# edit evdev list
sudo sed -i -E 's/\s*birman.*//g' /usr/share/X11/xkb/rules/evdev.lst
sudo sed -i -E 's/(! variant)/\1\n  birman         us: English (Typographic by Ilya Birman)\n  birman         ru: Russian (Typographic by Ilya Birman)/g' /usr/share/X11/xkb/rules/evdev.lst

sudo "$BASE/helper/xmladd.py" /usr/share/X11/xkb/rules/evdev.xml "$BASE/rules/variant_en" "$BASE/rules/variant_ru" /tmp/evdev.xml
sudo rm /usr/share/X11/xkb/rules/evdev.xml
sudo mv /tmp/evdev.xml /usr/share/X11/xkb/rules/evdev.xml

echo -e "\033[0;32mРаскладки успешно установлены!\033[0m"
echo "Не забудьте перезагрузиться."
