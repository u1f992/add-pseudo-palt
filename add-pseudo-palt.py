import argparse

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables


def add_pseudo_palt(
    font_path: str, output_path: str, factor: float, codepoints: list[int]
) -> None:
    font = TTFont(font_path)

    # Create codepoint to glyph name mapping from cmap
    best_cmap: dict[int, str] = {}
    for table in font["cmap"].tables:
        if table.isUnicode():
            best_cmap.update(table.cmap)

    # Process only glyphs corresponding to specified codepoints
    glyphs_to_process = [best_cmap[cp] for cp in codepoints if cp in best_cmap]
    if not glyphs_to_process:
        raise ValueError("Specified codepoints not found in font cmap")

    # Create new GPOS table if it doesn't exist
    # if "GPOS" not in font:
    #     font["GPOS"] = TTFont.newTable("GPOS")
    #     gpos = font["GPOS"].table = otTables.GPOS()
    #     gpos.Version = 0x00010000
    #     gpos.ScriptList = otTables.ScriptList()
    #     gpos.FeatureList = otTables.FeatureList()
    #     gpos.LookupList = otTables.LookupList()
    #     gpos.ScriptList.ScriptCount = 0
    #     gpos.FeatureList.FeatureCount = 0
    #     gpos.LookupList.LookupCount = 0
    gpos_table = font["GPOS"].table

    # Prepare Lookup/SubTable for single adjustment
    lookup = otTables.Lookup()
    lookup.LookupType = 1  # Single Adjustment
    lookup.LookupFlag = 0

    # Buffer pairs of Coverage / ValueRecord
    glyf_table = font["glyf"]
    hmtx = font["hmtx"].metrics
    entries: list[tuple[str, otTables.ValueRecord]] = []
    for glyph_name in glyphs_to_process:
        lsb = hmtx[glyph_name][1]
        aw = hmtx[glyph_name][0]
        glyph = glyf_table[glyph_name]
        xMin = getattr(glyph, "xMin", 0)
        xMax = getattr(glyph, "xMax", 0)
        shape_width = xMax - xMin
        rsb = aw - lsb - shape_width

        # Adjustment values
        xPlacement = -lsb * factor
        xAdvance = -(lsb + rsb) * factor

        vr = otTables.ValueRecord()
        vr.XPlacement = int(round(xPlacement))
        vr.YPlacement = 0
        vr.XAdvance = int(round(xAdvance))
        vr.YAdvance = 0

        entries.append((glyph_name, vr))

    # Create a map to sort by glyph ID
    glyph_order = font.getGlyphOrder()
    glyph_index = {name: idx for idx, name in enumerate(glyph_order)}
    entries.sort(key=lambda e: glyph_index.get(e[0], 0))

    # Set Coverage and Value in subtable
    subtable = otTables.SinglePos()
    subtable.Format = 2
    # Coverage
    coverage = otTables.Coverage()
    coverage.glyphs = [gn for gn, _ in entries]
    subtable.Coverage = coverage
    # Required: Specify fields to use (XPlacement + XAdvance)
    subtable.ValueFormat = 0x0001 | 0x0004
    subtable.Value = [vr for _, vr in entries]
    subtable.ValueCount = len(entries)

    lookup.SubTable = [subtable]
    lookup.SubTableCount = 1

    # Add to LookupList
    gpos_table.LookupList.Lookup.append(lookup)
    gpos_table.LookupList.LookupCount += 1
    lookup_index = gpos_table.LookupList.LookupCount - 1

    # Create palt Feature
    feature = otTables.Feature()
    feature.LookupCount = 1
    feature.LookupListIndex = [lookup_index]
    fr = otTables.FeatureRecord()
    fr.FeatureTag = "palt"
    fr.Feature = feature
    gpos_table.FeatureList.FeatureRecord.append(fr)
    gpos_table.FeatureList.FeatureCount += 1
    feat_index = gpos_table.FeatureList.FeatureCount - 1

    # Register to all scripts
    for script_record in gpos_table.ScriptList.ScriptRecord:
        langsys = script_record.Script.DefaultLangSys
        langsys.FeatureIndex.append(feat_index)
        langsys.FeatureCount += 1

    font.save(output_path)


def parse_codepoints(s: str) -> list[int]:
    cps: set[int] = set()
    for part in s.split(","):
        part = part.strip()
        if not part:
            raise ValueError("empty part")
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start = int(start_str, 0)
            end = int(end_str, 0)
            if start > end:
                raise ValueError(f"start > end: {start=},{end=}")
            for cp in range(start, end + 1):
                cps.add(cp)
        else:
            cps.add(int(part, 0))
    return sorted(cps)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("factor", type=float)
    parser.add_argument("codepoints")
    args = parser.parse_args()

    with open(args.codepoints) as f:
        cps = parse_codepoints(f.read())
    add_pseudo_palt(args.input, args.output, args.factor, cps)


if __name__ == "__main__":
    main()
