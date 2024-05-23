from selenium import webdriver
from api.application.ports.runPort import IRunUseCase
from api.domain.entities.run import Run
from api.adapters.outbound.database.models.run import Status
from api.adapters.outbound.database.models.log import LogLevel


def find_and_set_key(driver, target, value):
    element = driver.find_element(target[0], target[1])
    element.send_keys(value)
    return element


# TODO: Use log use case instead
def log(run, content, level=LogLevel.INFO):
    run.log_set.create(content=content, level=level)


def match_element(text, element):
    assert text in element


def finish_task(usecase: IRunUseCase, run: Run):
    usecase.updateRunStatus(run, Status.SUCCESS)


def fail_task(usecase: IRunUseCase, run: Run):
    usecase.updateRunStatus(run, Status.FAILURE)


def setup_options(options_list):
    options = webdriver.FirefoxOptions()

    for option in options_list:
        options.add_argument(option)

    return options
