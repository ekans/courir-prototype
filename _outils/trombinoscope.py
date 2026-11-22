# /// script
# requires-python = ">=3.11"
# dependencies = ["olefile", "xlrd", "pillow"]
# ///
"""Met à jour le trombinoscope depuis le classeur Excel du club.

    uv run _outils/trombinoscope.py "Trombino Courir Fonsegrives 2026-2027 V6.xls"

Écrit les photos dans photos/membres/ et la liste `membres:` de
_rubriques/membres.md. Le reste de membres.md (titre, textes) est gardé.
"""
import io
import re
import shutil
import struct
import sys
import unicodedata
from pathlib import Path

import olefile
import xlrd
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
PHOTOS = REPO / "photos" / "membres"
RUBRIQUE = REPO / "_rubriques" / "membres.md"

# The sheet is BIFF8, but its pictures are BIFF5-style: an OBJ record anchors
# each one to a cell, and the IMDATA record that follows holds the image,
# either a raw 24-bit bitmap (cf 9) or a metafile wrapping one (cf 2).
OBJ, IMDATA, CONTINUE = 0x005D, 0x007F, 0x003C


def records(book):
    i = 0
    while i + 4 <= len(book):
        kind, size = struct.unpack_from("<HH", book, i)
        yield kind, book[i + 4 : i + 4 + size]
        i += 4 + size


def bitmap(raw):
    header, w, h, _, bpp = struct.unpack_from("<IHHHH", raw, 0)
    assert header == 12 and bpp == 24, (header, bpp)
    stride = (w * 3 + 3) & ~3
    return Image.frombuffer("RGB", (w, h), raw[12 : 12 + stride * h], "raw", "BGR", stride, -1)


def metafile_bitmap(wmf):
    i = struct.unpack_from("<H", wmf, 2)[0] * 2
    while i + 6 <= len(wmf):
        size, function = struct.unpack_from("<IH", wmf, i)
        if function == 0x0B41:  # META_DIBSTRETCHBLT
            dib = wmf[i + 26 : i + size * 2]
            header, bpp, colors = struct.unpack_from("<I", dib, 0)[0], struct.unpack_from("<H", dib, 14)[0], struct.unpack_from("<I", dib, 32)[0]
            palette = (colors or (1 << bpp if bpp <= 8 else 0)) * 4
            file_header = b"BM" + struct.pack("<IHHI", 14 + len(dib), 0, 0, 14 + header + palette)
            return Image.open(io.BytesIO(file_header + dib)).convert("RGB")
        i += size * 2
    raise ValueError("métafichier sans image")


def photos_by_cell(book):
    recs = list(records(book))
    found, anchor = {}, None
    for k, (kind, body) in enumerate(recs):
        if kind == OBJ and struct.unpack_from("<H", body, 4)[0] == 8:
            col, _, row = struct.unpack_from("<3H", body, 10)
            anchor = (row, col)
        elif kind == IMDATA:
            cf, _, size = struct.unpack_from("<HHI", body, 0)
            data = bytearray(body[8:])
            j = k + 1
            while len(data) < size and recs[j][0] == CONTINUE:
                data += recs[j][1]
                j += 1
            found[anchor] = metafile_bitmap(bytes(data[8:])) if cf == 2 else bitmap(bytes(data))
            anchor = None
    return found


def title_case(s):
    return " ".join("-".join(p[:1].upper() + p[1:].lower() for p in w.split("-")) for w in s.split())


def slug(s):
    ascii_ = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_.lower()).strip("-")


def members(path):
    photos = photos_by_cell(olefile.OleFileIO(path).openstream("Book").read())
    sheet = xlrd.open_workbook(path).sheet_by_index(0)
    out = []
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            words = str(sheet.cell_value(row, col)).split()
            # A member cell reads "Prénom NOM": the surname is the run of
            # upper-case words after the first name.
            cut = next((i for i, w in enumerate(words) if i > 0 and w.isupper() and len(w) > 1), None)
            if cut is None or not words[0][:1].isupper() or words[0].isupper():
                continue
            prenom, nom = " ".join(words[:cut]), title_case(" ".join(words[cut:]))
            out.append((prenom, nom, photos.get((row, col))))
    return sorted(out, key=lambda m: (slug(m[1]), slug(m[0])))


def main(path):
    found = members(path)
    shutil.rmtree(PHOTOS, ignore_errors=True)
    PHOTOS.mkdir(parents=True)
    lines = ["membres:"]
    for prenom, nom, image in found:
        lines += [f'  - prenom: "{prenom}"', f'    nom: "{nom}"']
        if image:
            name = f"{slug(prenom + ' ' + nom)}.jpg"
            image.thumbnail((360, 480))
            image.save(PHOTOS / name, quality=82, optimize=True)
            lines.append(f'    photo: "photos/membres/{name}"')
    head, sep, rest = RUBRIQUE.read_text().partition("\nmembres:\n")
    assert sep, f"{RUBRIQUE} doit finir son en-tête par une ligne « membres: »"
    RUBRIQUE.write_text(head + "\n" + "\n".join(lines) + "\n" + rest[rest.index("---\n"):])
    with_photo = sum(1 for m in found if m[2])
    print(f"{len(found)} membres, {with_photo} avec photo, {len(found) - with_photo} sans.")


if __name__ == "__main__":
    main(sys.argv[1])
