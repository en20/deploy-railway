from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse

from api.adapters.outbound.database.repositories.RunRepository import RunRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository
from api.application.usecases.runUseCase import RunUseCase
from api.adapters.outbound.database.models.log import LogLevel
from api.adapters.outbound.celery.utils import (
    log,
    finish_task,
    fail_task,
    setup_options,
)
import time


@shared_task()
def access_url(run_id, target_url):
    run_repository = RunRepository()
    robot_repositoty = RobotRepository()
    run_usecase = RunUseCase(run_repository, robot_repositoty)
    run = run_repository.runToSchema(run_repository.findById(run_id))

    try:
        if not urlparse(target_url).scheme:
            target_url = "https://" + target_url

        if not target_url.endswith("/"):
            target_url += "/"

        driver = webdriver.Firefox(options=setup_options(["--headless"]))

        wait = WebDriverWait(driver, 30)

        log(run, f"Acessando {target_url}")

        driver.get(target_url)

        wait.until(EC.url_to_be(target_url))

        time.sleep(1)

        driver.close()

        log(run, f"{target_url} acessado com sucesso")

        finish_task(run_usecase, run)

    except TimeoutException:
        log(run, "Bot demorou demais para responder", LogLevel.ERROR)
        fail_task(run_usecase, run)

    except RuntimeError as error:
        log(run, f"Bot falhou com erro {error.args[0]}", LogLevel.ERROR)
        fail_task(run_usecase, run)
