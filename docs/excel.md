# Excel Guide

## Intent

Excel helpers should support unique workbook formats without hard-coding one
company's spreadsheet assumptions into the library.

## Concepts

- `ExcelProfile`: required sheets, header normalization, and column mapping.
- `ExcelReader`: converts workbook rows into dictionaries.
- `ExcelWriter`: simple row writer for one sheet.
- `SpreadsheetWorkbook`: workbook model with sheets, columns, styles, widths,
  freeze panes, filters, and tab colors.
- `ExcelWorkbookWriter`: customizable openpyxl-backed workbook writer.

## Customization Points

- Header normalization
- Required sheets
- Required columns
- Output column order
- Row filtering
- Type conversion
- Output sheet names and column order
- Column widths
- Header styles
- Cell number formats
- Multiple sheets
- Freeze panes and filters

## Testing

Use temporary files and small workbooks. Test missing sheet, missing column, and
round-trip write/read behavior.
