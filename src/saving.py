import json

class JSONSaver:
    def __init__(self, file_name='vacancies.json'):
        self._file_name = file_name

    def add_vacancy(self, vacancy):
        """Добавляет вакансию в JSON-файл"""
        data = self.get_vacancies()
        data.append(vacancy.to_dict())
        self._save_vacancies(data)

    def get_vacancies(self):
        """Загружает вакансии из JSON-файла и возвращает их как список словарей"""
        try:
            with open(self._file_name, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_vacancies(self, data):
        """Публичный метод для сохранения вакансий"""
        self._save_vacancies(data)  # Вызов приватного метода

    def _save_vacancies(self, data):
        """Приватный метод для записи вакансий в JSON-файл"""
        with open(self._file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy_name):
        pass