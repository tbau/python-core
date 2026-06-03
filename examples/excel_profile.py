"""Example Excel profile for custom parsing and writing."""

from pathlib import Path

from python_core.files.excel_profile import ExcelProfile
from python_core.files.excel_reader import ExcelReader
from python_core.files.excel_writer import ExcelWriter


def build_orders_profile() -> ExcelProfile:
    """Describe the sheet contract expected by order import/export jobs."""
    return ExcelProfile(
        sheet_name="Orders",
        required_columns={"order_id", "amount"},
        output_columns=("order_id", "amount", "status"),
    )


def parse_and_write_orders(source: Path, destination: Path) -> None:
    """Read validated order rows and write them back with a stable column order."""
    profile = build_orders_profile()
    rows = ExcelReader(profile).parse(source)
    ExcelWriter(profile).write(rows, destination)


if __name__ == "__main__":
    parse_and_write_orders(Path("orders.xlsx"), Path("orders-out.xlsx"))
