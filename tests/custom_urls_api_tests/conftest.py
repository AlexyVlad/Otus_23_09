import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="URL для проверки",
    )
    parser.addoption(
        "--status_code",
        action="store",
        type=int,
        default=200,
        help="Ожидаемый статус-код",
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")