from __future__ import annotations

import abc
import json
from pathlib import Path
from typing import List

from .models import Vacancy


class VacancyStorage(abc.ABC):
    """Общее хранилище вакансий (файл, БД, …)."""

    @abc.abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None: ...

    @abc.abstractmethod
    def get_vacancies(self) -> List[Vacancy]: ...

    @abc.abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None: ...


class JSONSaver(VacancyStorage):
    """Простое файловое хранилище в JSON."""

    def __init__(self, filename: str | Path = "vacancies.json") -> None:
        self._file = Path(filename)

    # ­­­­­­­­­­­­­­­­­­­­­­­­­­ I/O helpers
    def _read(self) -> list[dict]:
        if self._file.exists():
            return json.loads(self._file.read_text(encoding="utf-8"))
        return []

    def _write(self, data: list[dict]) -> None:
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ­­­­­­­­­­­­­­­­­­­­­­­­­­ API
    def add_vacancy(self, vacancy: Vacancy) -> None:
        store = self._read()
        v_dict = vacancy.to_dict()
        if v_dict not in store:
            store.append(v_dict)
            self._write(store)

    def get_vacancies(self) -> list[Vacancy]:
        return [Vacancy(**raw) for raw in self._read()]

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        store = self._read()
        try:
            store.remove(vacancy.to_dict())
        except ValueError:
            return
        self._write(store)
