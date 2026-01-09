from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from openpyxl import Workbook

from fabrica.templates import get_template


def export_template_to_csv(template_key: str, path: str | Path) -> None:
    template = get_template(template_key)
    resolved = Path(path)
    with resolved.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(template.header())


def export_template_to_excel(template_key: str, path: str | Path) -> None:
    template = get_template(template_key)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(template.header())
    workbook.save(Path(path))


def export_listing_to_csv(records: Iterable[Mapping[str, str]], path: str | Path) -> None:
    resolved = Path(path)
    records_list = list(records)
    headers = _infer_headers(records_list)
    with resolved.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records_list)


def export_listing_to_excel(records: Iterable[Mapping[str, str]], path: str | Path) -> None:
    records_list = list(records)
    headers = _infer_headers(records_list)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(headers)
    for record in records_list:
        worksheet.append([record.get(header, "") for header in headers])
    workbook.save(Path(path))


def _infer_headers(records: Sequence[Mapping[str, str]]) -> list[str]:
    headers: list[str] = []
    for record in records:
        for key in record.keys():
            if key not in headers:
                headers.append(key)
    return headers
