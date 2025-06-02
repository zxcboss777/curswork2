from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.saving import JSONSaver


def user_interaction():
    # Инициализируем объекты для работы с API и файлами

    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    while True:
        print("---Menu---")
        print("1. Найти вакансии по ключевому слову")
        print("2. Показать топ вакансий по зарплате")
        print("3. Найти вакансии по ключевому слову в описании")
        print("4. Удалить вакансию")
        print("5. Выйти")
        choice = input('Выберите действие: ')

        if choice == '1':
            # Поиск вакансий по ключевому слову
            query = input('Введите ключевое слово: ')
            hh_vacancies = hh_api.get_vacancies(query)

            # Преобразование данных в объекты Vacancy и вывод
            vacancies = [
                Vacancy(
                    name = v['name'],
                    url=v['alternate_url'],
                    salary = v['salary']['from'] if v['salary'] and 'from' in v['salary'] else 'Зарплата не указана',
                    description = v['snippet']['requirement'] if v['snippet'] and 'requirement' in v['snippet'] else 'Описание отсутствует'
                )
                for v in hh_vacancies
            ]

            # Сохранение вакансий в JSON-файл
            for vacancy in vacancies:
                json_saver.add_vacancy(vacancy)
            print('Вакансии добавлены в файл')

            # Вывод вакансий
            print('Найденные вакансии')
            for vacancy in vacancies:
                print(f"Название: {vacancy.name}")
                print(f"Ссылка: {vacancy.url}")
                print(f"Зарплата: {vacancy.salary}")
                print(f"Описание: {vacancy.description}\n")
                print('*' * 20)

        elif choice == '2':
            #Показать топ вакансий по зарплате

            try:
                top = int(input("Введите количество вакансий: "))
            except ValueError:
                print('Введите корректное число: ')
                continue

            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print('Нет вакансий')
                continue

            #Сортируем вакансии по зп
            sorted_vacancies = sorted(
                vacancies,
                key=lambda x: x.get('salary', 0) if isinstance(x.get('salary'), (int, float)) else 0,
                reverse=True
            )[:top]

            for vacancy in sorted_vacancies:
                print(f'Название: {vacancy['name']}')
                print(f"Ссылка: {vacancy['url']}")
                print(f"Зарплата: {vacancy['salary']}")
                print(f"Описание: {vacancy['description']}\n")
                print('*' * 20)


        elif choice == "3":
            # Найти вакансии по ключевому слову в описании
            keyword = input("Введите ключевое слово для поиска в описании: ")
            vacancies = json_saver.get_vacancies()
            filtered_vacancies = []
            for v in vacancies:
                try:
                    if keyword.lower() in v['description'].lower():
                        filtered_vacancies.append(v)
                except AttributeError:
                    print(f"Внимание: Описание вакансии отсутствует: {v}")

            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    print(f"Название: {vacancy['name']}")
                    print(f"Ссылка: {vacancy['url']}")
                    print(f"Зарплата: {vacancy['salary']}")
                    print(f"Описание: {vacancy['description']}")
                    print("=" * 40)
            else:
                print("Вакансий с таким ключевым словом в описании не найдено.")


        elif choice == "4":
            # Удалить вакансию по названию
            vacancy_name = input("Введите название вакансии для удаления: ")
            json_saver.delete_vacancy(vacancy_name)
            print("Вакансия удалена.")


        elif choice == "5":
            # Выход из программы
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор, попробуйте снова.")

if __name__ == '__main__':
    user_interaction()


