- [ZenKakuGothicAntique-Regular.ttf](https://github.com/googlefonts/zen-kakugothic/blob/2705757e17e42954f3acbdf921ac0ae24d1270cd/fonts/ttf/ZenKakuGothicAntique-Regular.ttf) (OFL-1.1)
- [JIS0208.TXT](https://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT)

```
PS > docker run --rm --interactive --tty --mount type=bind,source=.,target=/workdir --workdir /workdir registry.gitlab.com/islandoftex/images/texlive:TL2024-historic otfinfo -f ZenKakuGothicAntique-Regular.ttf
aalt    Access All Alternates
case    Case-Sensitive Forms
ccmp    Glyph Composition/Decomposition
frac    Fractions
fwid    Full Widths
hwid    Half Widths
kern    Kerning
mark    Mark Positioning
mkmk    Mark to Mark Positioning
ordn    Ordinals
sups    Superscript
vert    Vertical Writing
vkna    Vertical Kana Alternates
vrt2    Vertical Alternates and Rotation
PS > python ..\add-pseudo-palt.py .\ZenKakuGothicAntique-Regular.ttf palt-0_5.ttf 0.5 .\jis0208-unicode.txt
PS > docker run --rm --interactive --tty --mount type=bind,source=.,target=/workdir --workdir /workdir registry.gitlab.com/islandoftex/images/texlive:TL2024-historic otfinfo -f palt-0_5.ttf                    
aalt    Access All Alternates
case    Case-Sensitive Forms
ccmp    Glyph Composition/Decomposition
frac    Fractions
fwid    Full Widths
hwid    Half Widths
kern    Kerning
mark    Mark Positioning
mkmk    Mark to Mark Positioning
ordn    Ordinals
palt    Proportional Alternate Widths
sups    Superscript
vert    Vertical Writing
vkna    Vertical Kana Alternates
vrt2    Vertical Alternates and Rotation
```
