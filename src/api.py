from __future__ import annotations

import abc
import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class JobAPI(abc.ABC):
    """Абстрактный интерфейс любого job-API."""

    @abc.abstractmethod
    def get_vacancies(self, query: str, per_page: int = 100) -> list[dict[str, Any]]:
        """Вернуть &laquo;сырые&raquo; вакансии списком словарей."""


class HeadHunterAPI(JobAPI):
    """Адаптер к публичному API hh.ru."""

    _BASE_URL = "https://api.hh.ru/vacancies"

    # ­­­­­­­­­­­­­­­­­­­­­­­­­­ helpers
    def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        resp = requests.get(self._BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    # ­­­­­­­­­­­­­­­­­­­­­­­­­­ public
    def get_vacancies(self, query: str, per_page: int = 100) -> list[dict[str, Any]]:
        params = {"text": query, "per_page": per_page}
        logger.debug("HH-API params: %s", params)
        return self._request(params).get("items", [])
