"""Example Excel profile for custom parsing and writing."""

from pathlib import Path

from python_core.files.excel_profile import ExcelProfile
from python_core.files.excel_reader import ExcelReader
from python_core.files.excel_writer import ExcelWriter

profile = ExcelProfile(
    sheet_name="Orders",
    required_columns={"order_id", "amount"},
    output_columns=("order_id", "amount", "status"),
)

rows = ExcelReader(profile).parse(Path("orders.xlsx"))
ExcelWriter(profile).write(rows, Path("orders-out.xlsx"))
