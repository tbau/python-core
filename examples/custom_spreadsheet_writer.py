"""Custom spreadsheet writer example."""

from pathlib import Path

from python_core.files.excel_workbook_writer import ExcelWorkbookWriter
from python_core.files.spreadsheet_column import SpreadsheetColumn
from python_core.files.spreadsheet_sheet import SpreadsheetSheet
from python_core.files.spreadsheet_style import SpreadsheetStyle
from python_core.files.spreadsheet_workbook import SpreadsheetWorkbook


def build_orders_workbook() -> SpreadsheetWorkbook:
    """Build a workbook model before handing it to the Excel adapter."""
    money = SpreadsheetStyle(number_format='"$"#,##0.00')
    return SpreadsheetWorkbook(
        styles={"money": money},
        sheets=(
            SpreadsheetSheet(
                name="Orders",
                tab_color="4F81BD",
                columns=(
                    SpreadsheetColumn("order_id", header="Order ID", width=18),
                    SpreadsheetColumn("amount", header="Amount", width=14, style_key="money"),
                    SpreadsheetColumn("status", header="Status", width=14),
                ),
                rows=(
                    {"order_id": "A001", "amount": 125.5, "status": "paid"},
                    {"order_id": "A002", "amount": 42, "status": "pending"},
                ),
            ),
        ),
    )


def write_orders_workbook(path: Path) -> None:
    """Write the example workbook to disk."""
    ExcelWorkbookWriter().write(build_orders_workbook(), path)


if __name__ == "__main__":
    write_orders_workbook(Path("orders.xlsx"))
