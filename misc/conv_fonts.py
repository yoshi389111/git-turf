#!/usr/bin/env python3

import re
from collections import ChainMap
from typing import Dict, List

ZEN_KANA = (
    "。「」、・ヲ"
    "ァィゥェォ"
    "ャュョッー"
    "アイウエオ"
    "カキクケコ"
    "サシスセソ"
    "タチツテト"
    "ナニヌネノ"
    "ハヒフヘホ"
    "マミムメモ"
    "ヤユヨ"
    "ラリルレロ"
    "ワン゛゜"
)
HAN_ZEN_ASCII = {(0x0021 + i): (0xFF01 + i) for i in range(94)}
HAN_ZEN_KANA = {(0xFF61 + i): ord(ZEN_KANA[i]) for i in range(len(ZEN_KANA))}
HAN_ZEN = ChainMap(HAN_ZEN_ASCII, HAN_ZEN_KANA)


def conv_1byte(value: int, charset: str) -> int:
    return ord(bytearray([value]).decode(encoding=charset))


def conv_cp932(value: int) -> int:
    if value <= 0xFF:
        return conv_1byte(value, "cp932")
    ku, ten = divmod(value - 0x2020, 256)
    hi, lo = divmod(ku * 94 + ten - 95, 188)
    hi_byte = hi + (0x81 if hi < 0x1F else 0xC1)
    lo_byte = lo + (0x40 if lo < 0x3F else 0x41)
    return ord(bytearray([hi_byte, lo_byte]).decode(encoding="cp932"))


def conv_code(value: int, charset: str) -> int:
    if charset == "iso10646-1":
        return value
    if charset == "jisx0208.1990-0" or charset == "jisx0201.1976-0":
        return conv_cp932(value)
    if charset == "iso8859-1":
        return conv_1byte(value, "iso-8859-1")
    raise ValueError("unsupported charset " + charset)


def transpose_bitmap(bits: list, width: int) -> str:
    result = bytearray(
        [
            sum([1 << i for i in range(7) if bits[i] & (0x80 >> j)])
            for j in range(width)
        ]
    )
    return result.hex()


def read_bdf_font(file_name: str) -> Dict[int, str]:
    with open(file_name, "r") as font_file:
        # font global
        fonts: Dict[int, str] = {}
        font_ascent = 0
        font_descent = 0
        charset_registry = ""
        charset_encoding = ""

        # for one glyph
        char_code = 0
        dwidth = 0
        bb_height = 0
        offset_x = 0
        offset_y = 0
        bitmap_mode = False
        bitmap_list: List[int] = []

        for line in font_file:
            item = line.split()
            if item[0] == "CHARSET_REGISTRY":
                charset_registry = item[1].replace('"', "").lower()
            elif item[0] == "CHARSET_ENCODING":
                charset_encoding = item[1].replace('"', "").lower()
            elif item[0] == "FONT_ASCENT":
                font_ascent = int(item[1])
            elif item[0] == "FONT_DESCENT":
                font_descent = int(item[1])
            elif item[0] == "ENCODING":
                char_code = int(item[1])
            elif item[0] == "DWIDTH":
                dwidth = int(item[1])
            elif item[0] == "BBX":
                bb_height = int(item[2])
                offset_x = int(item[3])
                offset_y = int(item[4])
            elif item[0] == "ENDCHAR":
                bitmap_list += [0] * (font_descent + offset_y)
                charset_name = charset_registry + "-" + charset_encoding
                code_point = conv_code(char_code, charset_name)
                bitmap_string = transpose_bitmap(bitmap_list, dwidth)
                fonts[code_point] = bitmap_string
                bitmap_mode = False
                bitmap_list = []
            elif bitmap_mode:
                bitmap = int(line.strip(), base=16) >> offset_x
                bitmap_list.append(bitmap)
            elif item[0] == "BITMAP":
                bitmap_mode = True
                bitmap_list = [0] * (font_ascent - bb_height - offset_y)
        return fonts


def conv_full_to_half(fonts):
    new_fonts = {}
    for han, zen in sorted(HAN_ZEN.items()):
        if zen in fonts:
            new_fonts[han] = fonts[zen]
    return new_fonts


def update_proportional(fonts):
    for han in HAN_ZEN.keys():
        bitmap = fonts[han]
        bitmap = re.sub(r"^(00)+", "", bitmap)
        bitmap = re.sub(r"(00)+$", "00", bitmap)
        fonts[han] = bitmap
    fonts[0x20] = "000000"


def main():
    misaki_fonts = read_bdf_font("./misaki_gothic.bdf")
    k6x8_fonts = read_bdf_font("./k6x8.bdf")
    half_fonts = conv_full_to_half(k6x8_fonts)
    misaki_fonts.update(half_fonts)
    update_proportional(misaki_fonts)

    print("from typing import Dict")
    print()
    print()
    print("def create() -> Dict[str, bytes]:")
    print("    fonts = {}")
    for code, bitmap in sorted(misaki_fonts.items()):
        print(
            '    fonts["\\u{:04x}"] = bytes.fromhex("{}")'.format(code, bitmap)
        )
    print("    return fonts")


if __name__ == "__main__":
    main()
