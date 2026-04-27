# Automação de Consulta Processual - TJAL ⚖️

Este projeto automatiza a consulta de processos no portal do Tribunal de Justiça de Alagoas (TJAL). O robô foi desenvolvido para otimizar o fluxo de trabalho jurídico, eliminando a necessidade de buscas manuais repetitivas.

## 🚀 Funcionalidades
- **Leitura de Dados:** Integração com Excel via Pandas para processar grandes listas de processos.
- **Tratamento de Strings:** Limpeza automática de números de processos (remoção de pontos e traços).
- **Automação Web:** Navegação inteligente utilizando Selenium para realizar consultas em tempo real.
- **Resiliência:** O robô identifica e pula processos que já possuem status preenchido, permitindo retomar a tarefa de onde parou.

## 🛠️ Tecnologias
- **Python 3.x**
- **Selenium**: Automação de navegador.
- **Pandas**: Manipulação e análise de dados.
- **WebDriver Manager**: Gerenciamento automático do driver do Chrome.

## 📋 Como usar
1. Instale as dependências: `pip install -r requirements.txt`
2. Certifique-se de ter o Google Chrome instalado.
3. Insira sua planilha com o nome iniciando em `base_processos` na pasta do script.
4. Execute o robô: `python ROBO_AUTOMACAO_ALAGOAS.py`
