# Excel Agent

Use this guide when adding spreadsheet parsing or writing.

## Checklist

- Keep parsing rules in a dedicated `ExcelProfile`.
- Validate required sheets and columns.
- Normalize headers before mapping rows.
- Keep formulas, formatting, and output layout customizable.
- Use temporary files in tests.

## Design Rule

Parsing should produce typed rows or dictionaries. Writing should accept an
explicit workbook model instead of relying on hidden global formatting.
