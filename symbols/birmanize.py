r"""
Полуавтоматический бирманизатор раскладки. Выводом надо заменить все строки, начинающиеся на `key <`.

Проверен на `ru(winkeys)` и дефолтной `us`.

Если используешь вариант какой-то раскладки (например, `ru(winkeys)` или `us(dvorak)`,
делай `include` основной раскладки (в данном случае `ru(common)` и `us`) руками -
копируй и вставляй тело импортируемой секции.

Бирманизатор *полу*автоматический, все за тебя не сделает.

На выходе получается модифицированная раскладка Бирмана:
- на Alt+G вернулась гривна
- на Alt+\ ломаная вертикальная черта (¦)
- на Alt+Q интерпункт (·). Он отличается от знака умножения по смыслу и иногда толщиной
- на Shift+Alt+<пробел> тонкий пробел (1/5 или 1/6 круглой шпации). В оригинале, также как и на Alt+<пробел>, висит неразрывный

Все остальное без изменений.
"""

FILENAME = "us"

import re
line_dict = dict()

lines = None
with open(FILENAME, "r") as src:
    lines = src.read().splitlines()

space = r"\s*"

for line in lines:
    line = line.split("//")[0] # remove all comments
    key = None
    try:
        key = re.search(fr"key{space}<(.+)>", line).group(1)
    except:
        continue

    line_dict[key] = [char.strip() for char in re.search(r"\[(.+)\]", line).group(1).split(',')]
    for i in range(4 - len(line_dict[key])): line_dict[key].append("NoSymbol")

if "SPCE" not in line_dict:
    line_dict["SPCE"] = ["space", "space", "nobreakspace", "thinspace"]

# "@" - символ отсутствует. Сделано для удобства.
# Настоящая собачка - "at".

birmanized = {
    "TLDE": ("´", "dead_grave"),
    "AE": ("¹¡", "²½", "³⅓", ("dollar", "¼"), "‰@", ("↑", "dead_circumflex"), "@¿", "∞@", "←‹", "→›", "—–", "≠±"),
    "AD": (("·", "dead_breve"), "✓⌃", "€⌥", ("®", "dead_abovering"), "™@", "ѣѢ", "ѵѴ", "іІ", "ѳѲ", "′″", ("bracketleft", "braceleft"), ("bracketright", "braceright")),
    "AC": ("≈⌘", "§⇧", "°⌀", "£@", "₴", ("₽", "dead_doubleacute"), "„@", "“‘", "”’", ("‘", "dead_diaeresis"), "’@"),
    "BKSL": ("¦", "dead_grave"),
    "AB": (("@", "dead_cedilla"), "×·", "©¢", ("↓", "dead_caron"), "ßẞ", ("@", "dead_tilde"), "−•", "«„", "»“", ("…", "dead_acute")),
    "SPCE": ("nobreakspace", "thinspace"),
}

for key in ("AE","AD","AC","AB"):
    for i in range(len(birmanized[key])):
        nk = f"{key}{i+1:02}"
        birmanized[nk] = list(birmanized[key][i])
    del birmanized[key]


for key in birmanized:
    birmanized[key] = line_dict[key][0:2] + list(birmanized[key])
    if not birmanized[key][3].isascii():
        birmanized[key][3] = f"U{ord(birmanized[key][3]):04X}"
    elif birmanized[key][3] == "@":
        birmanized[key][3] = "NoSymbol"
    
    if not birmanized[key][2].isascii():
        birmanized[key][2] = f"U{ord(birmanized[key][2]):04X}"
    elif birmanized[key][2] == "@":
        birmanized[key][2] = "NoSymbol"


for key in birmanized:
    print(f"    key <{key}>", "{[", ", ".join(birmanized[key]), "]};")

print('    include "level3(ralt_switch)"')
