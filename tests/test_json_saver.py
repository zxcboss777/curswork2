from pathlib import Path
from src.models import Vacancy
from src.storage import JSONSaver


def test_add_and_get(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    saver = JSONSaver(filename=path)

    v = Vacancy(name="Dev", url="u1", salary_from=100, salary_to=0, requirement="")
    saver.add_vacancy(v)

    vacs = saver.get_vacancies()
    assert len(vacs) == 1
    assert vacs[0].url == "u1"
