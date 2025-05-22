from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv
import time

# Importa as funções do arquivo alimentacao_planilha
from subdiretorio.alimentacao_planilha import encontrar_ultimo_arquivo_swwweb, processar_arquivo_swwweb

# Caminho para a pasta de downloads desejada
download_folder = os.path.expanduser('I:\\.shortcut-targets-by-id\\1BbEijfOOPBwgJuz8LJhqn9OtOIAaEdeO\\Logdi\\Relatório e Dashboards\\02.Gestão de Fretes\\downloads relatórios')

# Caminho onde a planilha destino será salva
planilha_folder = os.path.expanduser('I:\\.shortcut-targets-by-id\\1BbEijfOOPBwgJuz8LJhqn9OtOIAaEdeO\\Logdi\\Relatório e Dashboards\\02.Gestão de Fretes')

# Caminho para a planilha de destino
planilha_destino = os.path.join(planilha_folder, "DB_COTACAO_FRETES.xlsx")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv("credenciais.env")

def realizar_login(driver):
    # Navega até a página do formulário
    driver.get("https://sistema.ssw.inf.br/bin/ssw0422")  # Substitua pela URL do seu formulário

    # Atraso para garantir que a página carregue completamente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "f1")))

    # Preenche os campos de login
    driver.find_element(By.NAME, "f1").send_keys((os.getenv("SSW_EMPRESA")))
    driver.find_element(By.NAME, "f2").send_keys(os.getenv("SSW_CNPJ"))
    driver.find_element(By.NAME, "f3").send_keys((os.getenv("SSW_USUARIO")))
    driver.find_element(By.NAME, "f4").send_keys(os.getenv("SSW_SENHA"))

    # Clica no botão de login diretamente
    login_button = driver.find_element(By.ID, "5")
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(5)

def preencher_formulario(driver):
    # Preenche os campos de Unidade e Opção
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "f2")))
    driver.find_element(By.NAME, "f3").send_keys("002")

    time.sleep(1)
    abas = driver.window_handles  # Lista o número de abas abertas.
    driver.switch_to.window(abas[-1])  # Muda o foco para a última aba (a nova aba)
    

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "6")))
    driver.find_element(By.ID, "6").clear()
    driver.find_element(By.ID, "6").send_keys("e")
    login_button = driver.find_element(By.ID, "19")
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(10)

def main():
    # Configurações do Edge
    edge_options = Options()
    edge_prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    edge_options.use_chromium = True
    edge_options.add_experimental_option("prefs", edge_prefs)

    # Inicializa o WebDriver apenas quando a função é chamada
    service = Service()
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        realizar_login(driver)
        preencher_formulario(driver)

        time.sleep(10)  # Atraso para garantir que o download seja iniciado

        processar_arquivo_swwweb(download_folder, planilha_destino, planilha_folder)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        # Fecha o navegador
        driver.quit()


if __name__ == "__main__":
    main()