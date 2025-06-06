from src.models import Vacancy


def test_comparison() -> None:
    v1 = Vacancy(name="Dev", url="u1", salary_from=100, salary_to=0, requirement="")
    v2 = Vacancy(name="Dev", url="u2", salary_from=200, salary_to=0, requirement="")
    assert v2 > v1
