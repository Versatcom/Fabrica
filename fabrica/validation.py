from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class ValidationErrorDetail:
    row_number: int
    field: str
    message: str
    value: Optional[str] = None


@dataclass(frozen=True)
class ValidationResult:
    valid_rows: List[Dict[str, str]]
    errors: List[ValidationErrorDetail]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


def is_non_empty(value: str) -> bool:
    return value.strip() != ""


def is_positive_number(value: str) -> bool:
    try:
        return float(value) > 0
    except ValueError:
        return False


def is_email(value: str) -> bool:
    if value.strip() == "":
        return True
    return "@" in value and "." in value


def is_optional_phone(value: str) -> bool:
    if value.strip() == "":
        return True
    allowed = set("+0123456789 -()")
    return all(char in allowed for char in value)


def validate_rows(template, rows: Iterable[Dict[str, str]]) -> ValidationResult:
    valid_rows: List[Dict[str, str]] = []
    errors: List[ValidationErrorDetail] = []
    for index, row in enumerate(rows, start=2):
        row_errors = _validate_row(template, row, index)
        if row_errors:
            errors.extend(row_errors)
        else:
            valid_rows.append(row)
    return ValidationResult(valid_rows=valid_rows, errors=errors)


def _validate_row(template, row: Dict[str, str], row_number: int) -> List[ValidationErrorDetail]:
    issues: List[ValidationErrorDetail] = []
    for field in template.fields:
        raw_value = row.get(field.name, "")
        value = str(raw_value).strip()
        if field.required and value == "":
            issues.append(
                ValidationErrorDetail(
                    row_number=row_number,
                    field=field.name,
                    message="Campo obligatorio vacío",
                    value=value,
                )
            )
            continue
        if field.validator and not field.validator(value):
            issues.append(
                ValidationErrorDetail(
                    row_number=row_number,
                    field=field.name,
                    message="Formato inválido",
                    value=value,
                )
            )
    return issues
