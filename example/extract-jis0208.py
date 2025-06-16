INPUT_FILE = "JIS0208.TXT"  # from: https://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT
OUTPUT_FILE = "jis0208-unicode.txt"

unicode_codes: list[int] = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        unicode_code = int(parts[2], 16)
        unicode_codes.append(unicode_code)

unicode_codes.sort()

# 連続する範囲をまとめる
ranges: list[str] = []
start = unicode_codes[0]
end = start

for i in range(1, len(unicode_codes)):
    if unicode_codes[i] == end + 1:
        end = unicode_codes[i]
    else:
        ranges.append(
            f"0x{start:04X}" if start == end else f"0x{start:04X}-0x{end:04X}"
        )
        start = end = unicode_codes[i]  # 新しい範囲の開始

ranges.append(f"0x{start:04X}" if start == end else f"0x{start:04X}-0x{end:04X}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(",".join(ranges))
