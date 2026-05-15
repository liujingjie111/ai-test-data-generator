"""Service layer for data export operations."""

import csv
import io
import json

from openpyxl import Workbook


def export_to_json(data: list[dict]) -> str:
    """Export data to JSON format.

    Args:
        data: List of dictionaries or values to export.

    Returns:
        JSON formatted string.
    """
    return json.dumps(data, ensure_ascii=False, indent=2)


def export_to_csv_bytes(data: list) -> bytes:
    """Export data to CSV format as bytes with UTF-8 BOM.

    Args:
        data: List of dictionaries or values to export.

    Returns:
        CSV file content as bytes with UTF-8 BOM for Windows Excel compatibility.
    """
    if not data:
        return b""

    output = io.StringIO()

    if isinstance(data[0], dict):
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    else:
        writer = csv.writer(output)
        writer.writerow(["value"])
        for item in data:
            writer.writerow([item])

    csv_content = output.getvalue()
    bom = "\ufeff".encode("utf-8")
    return bom + csv_content.encode("utf-8")


def export_to_excel(data: list) -> bytes:
    """Export data to Excel format.

    Args:
        data: List of dictionaries or values to export.

    Returns:
        Excel file content as bytes.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    if data:
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            ws.append(headers)
            for row in data:
                ws.append([row.get(col) for col in headers])
        else:
            ws.append(["value"])
            for item in data:
                ws.append([item])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return output.getvalue()


def export_to_sql(data: list, table_name: str) -> str:
    """Export data to SQL INSERT statements.

    Args:
        data: List of dictionaries or values to export.
        table_name: Name of the SQL table.

    Returns:
        SQL INSERT statements as string.
    """
    if not data:
        return ""

    statements = []

    if isinstance(data[0], dict):
        headers = list(data[0].keys())
        for row in data:
            columns = ", ".join(headers)
            values = []
            for col in headers:
                val = row.get(col)
                if val is None:
                    values.append("NULL")
                elif isinstance(val, (int, float)):
                    values.append(str(val))
                else:
                    escaped = str(val).replace("'", "''")
                    values.append(f"'{escaped}'")
            values_str = ", ".join(values)
            statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values_str});")
    else:
        for item in data:
            if item is None:
                values_str = "NULL"
            elif isinstance(item, (int, float)):
                values_str = str(item)
            else:
                escaped = str(item).replace("'", "''")
                values_str = f"'{escaped}'"
            statements.append(f"INSERT INTO {table_name} (value) VALUES ({values_str});")

    return "\n".join(statements)