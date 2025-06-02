import requests
from abc import ABC, abstractmethod

class JobAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_to_api(self, url: str, params: dict):
        """Приватный метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, query):
        """Метод для получения списка вакансий по запросу"""
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API HeadHunter (hh.ru)"""


    def __init__(self):
        self._URL = 'https://api.hh.ru/vacancies'
        self._per_page = 15


    def _connect_to_api(self, url: str, params: dict):
        """Приватный метод подключения к API"""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return None


    def get_vacancies(self, query: str):
        """Получает вакансии с hh.ru по указанному запросу"""
        params = {
            'text': query,  # Ключевое слово для поиска
            'per_page': self._per_page # Количество вакансий на одной странице
        }

        # Используем приватный метод подключения
        response = self._connect_to_api(self._URL, params)

        if response:
            return response.json().get('items', [])
        return []
