class Vacancy:
    __slots__ = ['name', 'url', 'salary', 'description']

    def __init__(self, name: str, url: str, salary: int, description: str):
        self.name = name
        self.url = url
        self.salary = salary if salary else 'Зарплата не указана'
        self.description = description

    def to_dict(self):
        """Возвращает представление объекта в виде словаря"""
        return {
            'name': self.name,
            'url': self.url,
            'salary': self.salary,
            'description': self.description
        }
