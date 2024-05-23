from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
import traceback


LOGIN_URL = "https://portalsipec.servidor.gov.br/login"
START_LINE = 2


def handle_login(run, driver, wait, cpf, password):
    log(run, "Acessando a página de login")

    driver.get(LOGIN_URL)

    wait.until(EC.url_to_be(LOGIN_URL))
    match_element("Portal Sipec", driver.title)

    xpath = '//div[@id="auth-logo"]//h2[contains(text(), "Portal de Autenticação")]'
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    log(run, "Página de login acessada com sucesso")
    log(run, "Iniciar login")

    find_and_set_key(driver, (By.NAME, "login[cpf]"), cpf)
    find_and_set_key(driver, (By.NAME, "login[senha]"), password).send_keys(Keys.RETURN)

    time.sleep(1)

    xpath = '//div[@class="modal-dialog"]//button[contains(text(), "PDP")]'
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    log(run, "Logado com sucesso")
    element.click()


def access_pdp(run, driver, wait, year):
    log(run, "Accessando PDP")

    xpath = '//ul[contains(@class, "page-breadcrumb")]//span[contains(text(),"Plano de Desenvolvimento de Pessoas")]'
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    log(run, "PDP Accessado com sucesso")

    log(run, "Filtrar PDP")
    xpath = '//div[contains(@class,"portlet")]//a[contains(text(), "Clique para expandir/ocultar")]'
    element = driver.find_element(By.XPATH, xpath)
    element.click()

    log(run, "Selecionando uma opção")
    xpath = '//*[@id="select2-ano-container"]'
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("$('#ano').select2('open')")

    xpath = '//*[@class="select2-search__field"]'
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    element.send_keys(year)

    xpath = '//*[@id="select2-ano-results"]//li[@role="treeitem"]'
    element = driver.find_element(By.XPATH, xpath)
    element.click()

    xpath = '//button[contains(text(), "Pesquisar")]'
    element = driver.find_element(By.XPATH, xpath)
    element.click()

    log(run, "Aguardando processamento da listagem de PDPs...")
    xpath = '//div[@id="data_table_wrapper"]//div[@id="data_table_processing"]'
    wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    log(run, "Acessando Gerenciar Necessidades")
    xpath = (
        '//*[@id="data_table"]//a[contains(@title, "Gerenciar itens de necessidade")]'
    )
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    element = driver.find_element(By.XPATH, xpath)
    element.click()

    xpath = '//ul[contains(@class, "page-breadcrumb")]//span[contains(text(),"Gerenciar Necessidades")]'
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    log(run, "Gerenciar Necessidades accessado com sucesso")


def fill_out_form_item(run, driver, wait, year, sector, row, row_counter):
    log(run, "Acessando Cadastrar Necessidade")
    element = driver.find_element(By.XPATH, '//button[contains(text(), "Cadastrar")]')
    element.click()

    xpath = '//ul[contains(@class, "page-breadcrumb")]//span[contains(text(), "Cadastrar necessidade")]'
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    log(run, "Cadastrar Necessidade acessado com sucesso")

    log(run, f"Adicionando Necessidade {row_counter + 1}")

    # IFS 0.1
    xpath = '//*[@id="unidades_organizacionais"]'
    find_and_set_key(driver, (By.XPATH, xpath), row[0].strip("\r\n\t ."))

    # IFS 0.2
    find_and_set_key(
        driver, (By.XPATH, '//*[@id="publico_alvo"]'), row[1].strip("\r\n\t .")
    )

    # IFS 0.3
    element = driver.find_element(By.XPATH, '//*[@id="estado_10"]')
    element.click()

    find_and_set_key(
        driver, (By.XPATH, '//*[@id="beneficiado_10"]'), row[2].strip("\r\n\t .")
    )

    # IFS 1
    find_and_set_key(
        driver, (By.XPATH, '//*[@id="necessidade_embassar"]'), row[3].strip("\r\n\t .")
    )

    # IFS 2
    ifs2_ok = False
    if row[4].strip("\r\n\t .") != "":
        elements = driver.find_elements(
            By.XPATH,
            '//input[@name="sugestao_solucao_id"]//ancestor::label[@class="radio-icon"]',
        )
        for element in elements:
            if row[4].strip("\r\n\t .") == element.text.strip("\r\n\t ."):
                elementInput = element.find_element(
                    By.XPATH, './/input[@name="sugestao_solucao_id"]'
                )  # Input radio
                elementInput.click()
                ifs2_ok = True
                break
    if not ifs2_ok:
        log(run, "Erro: IFS 2", LogLevel.WARNING)

    # ifs 3
    ifs3_ok = False
    if row[5].strip("\r\n\t .") != "":
        xpath = '//*[@id="subtematica"]'
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("$('#subtematica').select2('open')")

        xpath = '//*[@class="select2-search__field"]'
        element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.send_keys(row[5].strip("\r\n\t ."))

        xpath = '//*[@id="select2-subtematica-results"]//li[@role="treeitem"]'
        element = driver.find_element(By.XPATH, xpath)
        element.click()

        xpath = '//*[@id="necessidade-desenvolvimento-tema"]/textarea'
        find_and_set_key(driver, (By.XPATH, xpath), row[6].strip("\r\n\t ."))
        ifs3_ok = True

    if not ifs3_ok:
        log(run, "Erro: IFS 3", LogLevel.WARNING)

    # IFS 4
    ifs4_ok = False
    if row[7].strip("\r\n\t .") != "":
        elements = driver.find_elements(
            By.XPATH,
            '//input[@name="nivel_esforco_aprendizagem_id"]//ancestor::label[@class="radio-icon"]',
        )
        for element in elements:
            if row[7].strip("\r\n\t .") == element.text.strip("\r\n\t ."):
                elementInput = element.find_element(
                    By.XPATH, './/input[@name="nivel_esforco_aprendizagem_id"]'
                )  # Input radio
                elementInput.click()
                ifs4_ok = True
                break

    if not ifs4_ok:
        log(run, "Erro: IFS 4", LogLevel.WARNING)

    # IFS 5
    ifs5_ok = False
    if row[8].strip("\r\n\t .") != "":
        elements = driver.find_elements(
            By.XPATH,
            '//input[@name="competencia[]"]//ancestor::label[@class="radio"]',
        )
        for element in elements:
            if row[8].strip("\r\n\t .") == element.text.strip("\r\n\t ."):
                elementInput = element.find_element(
                    By.XPATH, './/input[@name="competencia[]"]'
                )  # Input radio
                elementInput.click()
                ifs5_ok = True
                break
            if "OUTRA COMPETÊNCIA TÉCNICA JÁ MAPEADA PELA ORGANIZAÇÃO" in element.text:
                elementInput = element.find_element(
                    By.XPATH, './/input[@name="competencia[]"]'
                )  # Input radio
                elementInput.click()

                xpath = './/*[@id="competencia_tecnica"]'
                find_and_set_key(driver, (By.XPATH, xpath), row[8].strip("\r\n\t ."))
                ifs5_ok = True
                break

    if not ifs5_ok:
        log(run, "Erro: IFS 5", LogLevel.WARNING)

    # IFS 6
    find_and_set_key(
        driver,
        (By.XPATH, '//textarea[@name="resultado_esperado"]'),
        row[9].strip("\r\n\t ."),
    )

    # Submit
    element = driver.find_element(By.XPATH, '//button[contains(text(), "Salvar")]')
    element.click()


def handle_error_dom_access(driver, run, row_counter):
    log(
        run,
        f"Erro ao cadastrar necessidade {row_counter + 1}",
        LogLevel.WARNING,
    )
    log(run, traceback.format_exc(), LogLevel.WARNING)

    element = driver.find_element(By.XPATH, '//button[contains(text(), "Voltar")]')
    element.click()


def handle_error_1(driver, run, row_counter):
    # Error Area
    xpath = '//div[@id="flashMensager"]//div[contains(@class, "alert-danger")]'
    element = driver.find_element(By.XPATH, xpath)
    # Log error
    log(
        run,
        f"Necessidade {row_counter + 1}"
        + " - Erro: "
        + element.text.replace("\n", "")
        .replace("×", "")
        .replace("Erros:", "")
        .replace("Você precisa especificar a necessidade em ", "")
        .replace('O campo "', "")
        .replace('" não foi preenchido.', "")
        .replace('" é obrigatório', ""),
        LogLevel.WARNING,
    )
    # Voltar
    element = driver.find_element(By.XPATH, '//button[contains(text(), "Voltar")]')
    element.click()


def handle_no_such_element_1(driver, run, row_counter):
    # Error Label
    xpath = '//label[contains(@class, "control-label") and contains(@style, "color: rgb(255, 0, 0)") ] | //div[contains(@class, "form-body") and contains(@class, "has-error")]'
    element = driver.find_element(By.XPATH, xpath)
    # Log error
    log(
        run,
        f"Necessidade {row_counter + 1}"
        + " - Erro: "
        + element.text.replace("\n", "").replace("×", "").replace("*", ""),
        LogLevel.WARNING,
    )
    # Voltar
    element = driver.find_element(By.XPATH, '//button[contains(text(), "Voltar")]')
    element.click()


def handle_no_such_element_2(driver, wait, run, row_counter):
    # Success Area
    xpath = '//div[@id="flashMensager"]//div[contains(@class, "alert-success")]'
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    log(
        run,
        f"Necessidade {row_counter + 1} -"
        + element.text.replace("\n", "").replace("×", ""),
        LogLevel.WARNING,
    )


def handle_timeout(driver, run, row_counter):
    log(
        run,
        f"Necessidade {row_counter + 1} - Erro ao tentar cadastrar",
        LogLevel.WARNING,
    )
    log(traceback.format_exc())
    # Voltar
    element = driver.find_element(By.XPATH, '//button[contains(text(), "Voltar")]')
    element.click()


def fill_out_form(run, driver, wait, file_path, year, sector):
    log(run, "Preencher formulário")

    with open(file_path) as file:
        row_counter = 0

        csv_reader = csv.reader(file)

        for row in csv_reader:
            try:
                if row_counter < START_LINE - 1:
                    row_counter += 1
                    continue

                fill_out_form_item(run, driver, wait, year, sector, row, row_counter)

            except:
                handle_error_dom_access(driver, run, row_counter)

            else:
                try:
                    handle_error_1(driver, run, row_counter)

                except NoSuchElementException:
                    try:
                        handle_no_such_element_1(driver, run, row_counter)
                    except NoSuchElementException:
                        try:
                            handle_no_such_element_2(driver, wait, run, row_counter)
                        except TimeoutException:
                            handle_timeout(driver, run, row_counter)
            row_counter += 1

    log(run, "Formulario preenchido com sucesso")


@shared_task()
def execute_sipec_bot(file_path, run_id, cpf, password, year, sector):
    run_repository = RunRepository()
    robot_repositoty = RobotRepository()
    run_usecase = RunUseCase(run_repository, robot_repositoty)
    run = run_repository.runToSchema(run_repository.findById(run_id))

    try:
        driver = webdriver.Firefox(options=setup_options(["--headless"]))

        wait = WebDriverWait(driver, 30)

        handle_login(run, driver, wait, cpf, password)

        access_pdp(run, driver, wait, year)

        fill_out_form(run, driver, wait, file_path, year, sector)

        driver.close()

        log(run, "Bot executado com sucesso")
        finish_task(run_usecase, run)

    except TimeoutException:
        driver.close()
        log(run, "Bot demorou demais para responder", LogLevel.ERROR)
        fail_task(run_usecase, run)

    except RuntimeError as error:
        driver.close()
        log(run, f"Bot falhou com o erro {error.args[0]}", LogLevel.ERROR)
        fail_task(run_usecase, run)
