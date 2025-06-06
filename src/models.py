from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import total_ordering
from typing import Any

__all__ = ["Vacancy"]


@total_ordering
@dataclass(slots=True)
class Vacancy:
    """Домашняя модель вакансии."""

    name: str
    url: str
    salary_from: int | None
    salary_to: int | None
    requirement: str

    # ──────────────────────────────────────────────
    # ▸ Валидация и нормализация ▸
    # ──────────────────────────────────────────────
    def __post_init__(self) -> None:
        self.salary_from = self._norm(self.salary_from)
        self.salary_to = self._norm(self.salary_to)

    @staticmethod
    def _norm(value: int | None) -> int | None:
        return int(value) if isinstance(value, (int, float)) and value > 0 else None

    # ──────────────────────────────────────────────
    # ▸ Сериализация ▸
    # ──────────────────────────────────────────────
    def to_dict(self) -> dict[str, Any]:  # noqa: D401 – простая обёртка
        """Return a JSON-ready representation."""
        return asdict(self)

    # ──────────────────────────────────────────────
    # ▸ Сравнение по &laquo;salary_from&raquo; ▸
    # ──────────────────────────────────────────────
    def _cmp_value(self) -> int:
        return self.salary_from or 0

    def __eq__(self, other: Any) -> bool:  # type: ignore[override] – mypy OK
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._cmp_value() == other._cmp_value()

    def __lt__(self, other: Any) -> bool:  # type: ignore[override]
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._cmp_value() < other._cmp_value()
