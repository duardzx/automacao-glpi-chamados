# 🤖 GLPI Automation Bot

Uma solução de automação robótica de processos (RPA) desenvolvida em **Python** e **Selenium** para abertura, encerramento dinâmico e aprovação em lote de chamados no sistema **GLPI**.

O script substitui tarefas repetitivas de suporte por um fluxo orientado a dados (CSV-driven), eliminando cliques manuais e garantindo alta resiliência contra oscilações de rede (*lag*) e requisições assíncronas do front-end do GLPI.

---

## 🚀 Destaques e Funcionalidades

- **Mapeamento Dinâmico por CSV:** Alimente o arquivo `.csv` com múltiplos chamados, instituições, emails, filas e quantidades. O robô processa tudo em sequência.
- **Tratamento Dinâmico de Select2 (AJAX):** Lida nativamente com os componentes dropdown assíncronos do GLPI através da simulação do comportamento do usuário e teclas de navegação.
- **Mecanismo Anti-Lag (Validação & Retry):** Sistema inteligente que valida se o campo Select2 foi preenchido corretamente. Se o servidor engasgar e deixar o campo em branco (`-----`), o script executa *retry* automático antes de prosseguir.
- **Manipulação de iFrames e Rich Text Editor (TinyMCE):** Injeta a solução do chamado diretamente no editor WYSIWYG via DOM JavaScript.
- **Validação de Execução:** Checa no DOM a gravação da solução antes de acionar os eventos de inclusão e aprovação verde definitiva.

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.12](https://www.python.org/)**
- **[Selenium WebDriver](https://www.selenium.dev/)** — Automação web e navegação no DOM.
- **[Pandas](https://pandas.pydata.org/)** — Leitura e manipulação estruturada do CSV.
- **[WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)** — Gerenciamento automático do ChromeDriver.

---

## 📋 Pré-requisitos

1. **Python 3.10+** instalado.
2. Navegador **Google Chrome** instalado.

---

## 🔧 Configuração do Ambiente

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/seu-usuario/glpi-automation-bot.git
   cd glpi-automation-bot

Crie e ative um ambiente virtual (venv):

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

Instale as dependências:

pip install pandas selenium webdriver-manager

Crie um arquivo chamado chamados.csv na raiz do projeto (utilizando separador ; e codificação utf-8-sig).

💡 Nota: Utilize o arquivo chamados.csv disponível no repositório como modelo.

Antes de rodar, abra o arquivo script.py (ou script2.py) e garanta que a variável da URL esteja apontando para o seu servidor GLPI:


# URL do formulário do GLPI
url_formulario = "https://seu-glpi.suaempresa.com.br"

🎯 Como Executar

Execute o script Python:
python script.py
O Google Chrome será aberto automaticamente na página de login do GLPI.

Faça o login manualmente e navegue até a tela do formulário limpo.

Volte ao terminal e pressione ENTER para iniciar o robô.

🛡️ Segurança e Privacidade
Este repositório não contém credenciais hardcoded, URLs internas corporativas ou dados sensíveis de produção. Certifique-se de manter o arquivo .gitignore ativo para não subir acidentalmente o seu chamados.csv real contendo dados de clientes/usuários.

Plaintext
# .gitignore
chamados.csv
.venv/
.venv-1/
__pycache__/
*.pyc
