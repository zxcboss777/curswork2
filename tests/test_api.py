import unittest
from unittest.mock import patch
import requests
from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.api = HeadHunterAPI()

    @patch('src.api.requests.get')
    def test_successful_response(self, mock_get):
        """Проверяет корректную обработку успешного ответа API hh.ru."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'items': [
                {
                    'name': 'Python Developer',
                    'url': 'https://hh.ru/vacancy/123456',
                    'salary': {'from': 100000, 'to': 150000},
                    'snippet': {'requirement': 'Опыт работы с Python'}
                },
                {
                    'name': 'Data Scientist',
                    'url': 'https://hh.ru/vacancy/654321',
                    'salary': {'from': 120000, 'to': 180000},
                    'snippet': {'requirement': 'Знание ML и Data Analysis'}
                }
            ]
        }

        vacancies = self.api.get_vacancies('Python')

        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]['name'], 'Python Developer')
        self.assertEqual(vacancies[0]['url'], 'https://hh.ru/vacancy/123456')
        self.assertEqual(vacancies[1]['name'], 'Data Scientist')

    @patch('src.api.requests.get')
    def test_empty_response(self, mock_get):
        """Проверяет обработку пустого ответа API."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'items': []}

        vacancies = self.api.get_vacancies('NonexistentJob')

        self.assertListEqual(vacancies, [])

    @patch('src.api.requests.get')
    def test_network_exception_handling(self, mock_get):
        """Проверяет обработку исключения RequestException."""
        mock_get.side_effect = requests.RequestException("Ошибка сети")

        vacancies = self.api.get_vacancies('Python')

        self.assertListEqual(vacancies, [])

    @patch('src.api.requests.get')
    def test_invalid_status_code(self, mock_get):
        """Проверяет обработку некорректного статус-кода."""
        mock_get.return_value.status_code = 404

        vacancies = self.api.get_vacancies('Python')

        self.assertListEqual(vacancies, [])


if __name__ == '__main__':
    unittest.main()
