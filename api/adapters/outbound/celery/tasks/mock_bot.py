from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from api.adapters.outbound.database.repositories.RunRepository import RunRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository
from api.application.usecases.runUseCase import RunUseCase
from api.adapters.outbound.database.models.log import LogLevel
from api.adapters.outbound.celery.utils import (
    find_and_set_key,
    match_element,
    log,
    finish_task,
    fail_task,
    setup_options,
)
import csv
import time
import os


def handle_login(run, driver, wait, name, password):
    target = os.environ.get("BOT_LOGIN_PAGE")

    log(run, "Acessando a página de login")

    driver.get(target)

    wait.until(EC.url_to_be(target))
    match_element("Log in | Django site admin", driver.title)

    wait.until(EC.visibility_of_element_located((By.ID, "site-name")))
    match_element(
        "Django administration",
        driver.find_element(By.ID, "site-name").find_element(By.TAG_NAME, "a").text,
    )

    log(run, "Inserindo credenciais")

    find_and_set_key(driver, (By.ID, "id_username"), name)
    find_and_set_key(driver, (By.ID, "id_password"), password).send_keys(Keys.RETURN)

    time.sleep(1)
    if len(driver.find_elements(By.CLASS_NAME, "errornote")) == 1:
        raise RuntimeError("Credenciais invalidas")

    wait.until(EC.visibility_of_element_located((By.ID, "user-tools")))
    match_element(
        "WELCOME",
        driver.find_element(By.ID, "user-tools").text,
    )

    log(run, "Logado com sucesso")


@shared_task()
def execute_mock_bot(file_path, run_id, name, password):
    run_repository = RunRepository()
    robot_repositoty = RobotRepository()
    run_usecase = RunUseCase(run_repository, robot_repositoty)
    run = run_repository.runToSchema(run_repository.findById(run_id))

    try:
        driver = webdriver.Firefox(options=setup_options(["--headless"]))

        wait = WebDriverWait(driver, 30)

        handle_login(run, driver, wait, name, password)

        with open(file_path) as file:
            counter = 0

            csv_reader = csv.reader(file)

            for row in csv_reader:
                counter += 1

                target = os.environ.get("BOT_ADD_PAGE")
                driver.get(target)

                wait.until(EC.url_to_be(target))
                match_element(
                    "Add usuario | Django site admin",
                    driver.title,
                )

                wait.until(EC.visibility_of_element_located((By.ID, "content")))
                match_element(
                    "Add usuario",
                    driver.find_element(By.ID, "content")
                    .find_element(By.TAG_NAME, "h1")
                    .text,
                )

                find_and_set_key(driver, (By.ID, "id_nome"), row[0])
                find_and_set_key(driver, (By.ID, "id_email"), row[1])
                find_and_set_key(driver, (By.ID, "id_telefone"), row[2]).send_keys(
                    Keys.RETURN
                )

                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success")))
                match_element(
                    "was added successfully",
                    driver.find_element(By.CLASS_NAME, "success").text,
                )

                log(run, f"Usuário {counter} inserido com sucesso")

        driver.close()

        log(run, "Bot executado com sucesso")
        finish_task(run_usecase, run)

    except RuntimeError as error:
        driver.close()
        log(run, f"Bot falhou com erro {error.args[0]}", LogLevel.ERROR)
        fail_task(run_usecase, run)
