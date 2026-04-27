import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

# --- LOCALIZAÇÃO DO ARQUIVO ---
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
arquivo_excel = None
for f in os.listdir(diretorio_atual):
    if f.lower().startswith("base_processos") and f.endswith((".xlsx", ".xls")):
        arquivo_excel = os.path.join(diretorio_atual, f)
        break

df = pd.read_excel(arquivo_excel)
if 'STATUS_ROBO' not in df.columns:
    df['STATUS_ROBO'] = ""

# --- CONFIGURAÇÃO DO NAVEGADOR ---
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

try:
    for index, linha in df.iterrows():
        # PULA PROCESSOS QUE JÁ TÊM STATUS (Para continuar após erro)
        if pd.notna(linha['STATUS_ROBO']) and linha['STATUS_ROBO'] != "":
            continue

        processo_full = str(linha['PROCESSO'])
        processo_limpo = processo_full.replace(".", "").replace("-", "")
        parte_principal = processo_limpo[0:13]
        foro_comarca = processo_limpo[-4:]

        print(f"[{index+1}/{len(df)}] Verificando: {processo_full}")

        try:
            navegador.get("https://www2.tjal.jus.br/cpopg/open.do")
            time.sleep(2)

            script = "document.getElementById('numeroDigitoAnoUnificado').value = arguments[0]; document.getElementById('foroNumeroUnificado').value = arguments[1];"
            navegador.execute_script(script, parte_principal, foro_comarca)
            
            campo_foro = navegador.find_element(By.ID, "foroNumeroUnificado")
            campo_foro.send_keys(Keys.ENTER)
            time.sleep(4)

            # --- LÓGICA DE CAPTURA MULTI-STATUS ---
            corpo_site = navegador.find_element(By.TAG_NAME, "body").text.lower()
            
            if "baixado" in corpo_site:
                resultado = "BAIXADO"
            elif "em grau de recurso" in corpo_site:
                resultado = "EM GRAU DE RECURSO"
            elif "julgado" in corpo_site:
                resultado = "JULGADO"
            elif "não existem informações disponíveis" in corpo_site:
                resultado = "NÃO ENCONTRADO"
            else:
                resultado = "EM ANDAMENTO"

            df.at[index, 'STATUS_ROBO'] = resultado
            print(f" -> Resultado: {resultado}")

        except Exception as e:
            print(f" -> Erro no processo {processo_full}: {e}")
            continue # Pula para o próximo se um processo falhar individualmente

        # Salva a cada 2 processos para garantir
        if index % 2 == 0:
            df.to_excel(arquivo_excel, index=False)

    df.to_excel(arquivo_excel, index=False)
    print("\n✅ Finalizado com sucesso!")

except Exception as e:
    print(f"\n❌ Erro crítico: {e}")
    df.to_excel(arquivo_excel, index=False)

finally:
    navegador.quit()
