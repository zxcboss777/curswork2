from __future__ import annotations

import argparse
import textwrap

from src.api import HeadHunterAPI
from src.models import Vacancy
from src.storage import JSONSaver


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="CLI-интеграция c hh.ru",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Пример:
              python main.py --query "Python" -top 5
            """
        ),
    )
    parser.add_argument("--query", required=True, help="Поисковая фраза")
    parser.add_argument("--top", type=int, default=10, help="Сколько топ-вакансий вывести")
    args = parser.parse_args()

    api = HeadHunterAPI()
    raw = api.get_vacancies(args.query)
    vacancies = [
        Vacancy(
            name=item["name"],
            url=item["alternate_url"],
            salary_from=(item["salary"] or {}).get("from"),
            salary_to=(item["salary"] or {}).get("to"),
            requirement=item["snippet"]["requirement"] or "",
        )
        for item in raw
    ]

    saver = JSONSaver()
    for v in vacancies:
        saver.add_vacancy(v)

    for idx, v in enumerate(sorted(saver.get_vacancies(), reverse=True)[: args.top], 1):
        salary = (
            f"{v.salary_from}-{v.salary_to}" if v.salary_from or v.salary_to else "не указана"
        )
        print(f"{idx}. {v.name} | {salary} | {v.url}")


if __name__ == "__main__":  # pragma: no cover
    cli()
