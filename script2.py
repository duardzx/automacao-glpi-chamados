import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    df = pd.read_csv('chamados.csv', sep=';', encoding='utf-8-sig')
except FileNotFoundError:
    print(" O arquivo 'chamados.csv' nao foi encontrado.")
    exit()

# Inicia o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

#  FUNÇÃO PREENCHER
def preencher_select2(name_attr, texto_busca):
    texto_busca = str(texto_busca).strip()
    
    campo = wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[contains(@name, '{name_attr}')]/following-sibling::span")))
    campo.click()
    time.sleep(0.4)
    
    busca = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-search__field")))
    busca.send_keys(texto_busca)
    
    time.sleep(1.2)
    
    busca.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.3)
    busca.send_keys(Keys.ENTER)
    time.sleep(0.5)

    tentativas = 0
    while tentativas < 3 and (campo.text.strip() == "" or "----" in campo.text.strip()):
        tentativas += 1
        print(f"Re-tentando selecao para '{texto_busca}' (Tentativa {tentativas}/3)")
        try:
            campo.click()
            time.sleep(0.4)
            busca = driver.find_element(By.CLASS_NAME, "select2-search__field")
            busca.clear()
            busca.send_keys(texto_busca)
            time.sleep(1.0)
            busca.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            busca.send_keys(Keys.ENTER)
            time.sleep(0.5)
        except:
            pass

    time.sleep(0.3)
# 3. Acessa o GLPI
url_formulario = "https://seu-glpi.suaempresa.com.br"
driver.get(url_formulario)

print("Faça o login manualmente e navegue até a tela do formulário.")
input("Quando estiver na tela do formulário limpo, aperte ENTER aqui no terminal")

ocorreu_erro = False

#Loop de Execução
for index, row in df.iterrows():
    if ocorreu_erro:
        break

    qtd = int(row['Quantidade']) if 'Quantidade' in row and pd.notna(row['Quantidade']) else 1
    
    for repeticao in range(qtd):
        print(f"[{index + 1}/{len(df)}] Processando '{row['Assunto']}' (Vez {repeticao + 1} de {qtd})")
        
        try:
            # PASSO 1: INSTITUIÇÃO DE SAÚDE
            print(f"Selecionando Instituição: {row['Instituicao']}")
            preencher_select2('answers_29', str(row['Instituicao']))

            # PASSO 2: EMAIL 
            print(f"Selecionando Email: {row['Email']}")
            preencher_select2('answers_167', str(row['Email']))

            # PASSO 3: USUÁRIO E CELULAR 
            campo_usuario = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'answers_169')]")))
            campo_usuario.clear()
            campo_usuario.send_keys(str(row['Usuario']))

            campo_celular = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'answers_168')]")))
            campo_celular.clear()
            campo_celular.send_keys(str(row['Celular']))

            # PASSO 4: URGÊNCIA
            try:
                elem_urgencia = driver.find_element(By.XPATH, "//select[contains(@name, 'answers_33')]")
                Select(elem_urgencia).select_by_visible_text("Média")
            except:
                pass

            # PASSO 5: TIPO DE DEMANDA
            print("Selecionando Requisição")
            elem_demanda = wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@name, 'answers_30')]")))
            Select(elem_demanda).select_by_visible_text("Requisição")
            driver.execute_script("$(arguments[0]).trigger('change');", elem_demanda)

            wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'answers_32')]/following-sibling::span")))
            time.sleep(0.3) 

            # PASSO 6: CATÁLOGO DE REQUISIÇÕES
            print(f"Buscando no catálogo: {row['Catalogo']}")
            preencher_select2('answers_32', str(row['Catalogo']))

            # PASSO 6: CATÁLOGO DE REQUISIÇÕES
            print(f"Buscando no catálogo: {row['Catalogo']}")
            preencher_select2('answers_32', str(row['Catalogo']))

            # PASSO 7: ASSUNTO E DESCRIÇÃO
            campo_assunto = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'answers_34')]")))
            campo_assunto.clear()
            campo_assunto.send_keys(str(row['Assunto']))
            time.sleep(0.5)
            
            campo_assunto.send_keys(Keys.TAB)
            time.sleep(0.5)
            
            driver.switch_to.active_element.send_keys(str(row['Descricao']))
            time.sleep(1.0)

            # PASSO 8: FILA
            print(f"Atribuindo para a fila: {row['Fila']}")
            preencher_select2('answers_36', str(row['Fila']))

            # PASSO 9: BOTÃO ENVIAR FORMULÁRIO
            print("Enviando formulário")
            botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Enviar' or contains(., 'Enviar')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_enviar)
            time.sleep(1.0)
            
            try:
                botao_enviar.click()
            except:
                driver.execute_script("arguments[0].click();", botao_enviar)

            print("Enfileirado com sucesso. Indo encerrar")
            time.sleep(4)

            # PASSO 10: VER MEUS CHAMADOS 
            btn_meus_chamados = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Ver meus chamados')]")))
            btn_meus_chamados.click()
            time.sleep(3) 

            # PASSO 11: ABRIR O CHAMADO RECÉM-CRIADO 
            link_chamado = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{str(row['Assunto'])}')]")))
            link_chamado.click()
            time.sleep(3) 

            # PASSO 12: ABRIR CAIXA DE SOLUÇÃO
            print(" Abrindo caixa de solução...")
            time.sleep(1.0)
            
            js_abrir_solucao = """
            var btnSolucao = document.querySelector("a.action-solution, a[data-bs-target*='Solution']");
            if (btnSolucao) {
                btnSolucao.click();
                return true;
            }
            return false;
            """
            
            sucesso_abrir = driver.execute_script(js_abrir_solucao)
            if not sucesso_abrir:
                driver.execute_script("document.querySelector('button.dropdown-toggle').click();")
                time.sleep(0.5)
                driver.execute_script("document.querySelector('a.action-solution').click();")
                
            print("Esperando o editor TinyMCE")
            time.sleep(2.5)

            # PASSO 13: PREENCHIMENTO VIA DOM DO IFRAME E VALIDAÇÃO 
            print("Localizando editor e aplicando 'Resolvido'")
            time.sleep(2.0) 
            
            js_preenche_e_valida = """
            var iframes = document.querySelectorAll("iframe[id*='solution_content']");
            var textoGravado = "";
            for (var i = 0; i < iframes.length; i++) {
                if (iframes[i].offsetWidth > 0 && iframes[i].offsetHeight > 0) {
                    try {
                        var doc = iframes[i].contentDocument || iframes[i].contentWindow.document;
                        if (doc && doc.body) {
                            doc.body.innerHTML = '<p>Resolvido</p>';
                            doc.body.dispatchEvent(new Event('input', { bubbles: true }));
                            doc.body.dispatchEvent(new Event('change', { bubbles: true }));
                            textoGravado = doc.body.innerText.trim();
                            break;
                        }
                    } catch(e) {}
                }
            }
            if (typeof tinymce !== 'undefined' && tinymce.activeEditor) {
                tinymce.activeEditor.setContent('<p>Resolvido</p>');
                tinymce.activeEditor.save();
            }
            return textoGravado;
            """
            
            texto_validado = driver.execute_script(js_preenche_e_valida)
            
            if "Resolvido" not in str(texto_validado):
                print(f"VALIDAÇÃO FALHOU: O texto lido do DOM foi '{texto_validado}'. Cancelando este chamado.")
                break
                
            print(f"VALIDAÇÃO CONCLUÍDA: Texto '{texto_validado}' verificado dentro do editor!")
            time.sleep(1.0)

            print("Clicando no botão + Adicionar visível...")
            js_clicar_adicionar = """
            var botoes = document.querySelectorAll("button[name='add']");
            var clicou = false;
            for (var i = 0; i < botoes.length; i++) {
                if (botoes[i].offsetWidth > 0 && botoes[i].offsetHeight > 0) {
                    botoes[i].scrollIntoView({block: 'center'});
                    ['mousedown', 'mouseup', 'click'].forEach(evt => {
                        botoes[i].dispatchEvent(new MouseEvent(evt, { bubbles: true, cancelable: true, view: window }));
                    });
                    clicou = true;
                    break;
                }
            }
            return clicou;
            """
            
            sucesso_add = driver.execute_script(js_clicar_adicionar)
            if sucesso_add:
                print("Botão + Adicionar clicado com sucesso!")
            else:
                print("Não encontrei o botão + Adicionar visível.")

            print("Aguardando renderização pós-solução")
            time.sleep(7.0) 

            # PASSO 15: CLICAR NO BOTÃO APROVAR
            print("Clicando no botão verde de Aprovação")
            js_aprovar_definitivo = """
            var btnAprovar = document.querySelector("button.btn-outline-success");
            if (btnAprovar) {
                btnAprovar.scrollIntoView({block: 'center'});
                ['mousedown', 'mouseup', 'click'].forEach(evt => {
                    btnAprovar.dispatchEvent(new MouseEvent(evt, { bubbles: true, cancelable: true, view: window }));
                });
                return true;
            }
            return false;
            """
            
            aprovou = driver.execute_script(js_aprovar_definitivo)
            if aprovou:
                print("Chamado APROVADO com sucesso.")
            else:
                print("Botão de aprovação não encontrado após o reload.")

            time.sleep(4.0)

            # PASSO 16: RETORNO AO FORMULÁRIO
            print("Voltando para o Catálogo de Serviços...")
            menu_catalogo = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Catálogo de serviços')] | //a[contains(., 'Catálogo de serviços')]")))
            menu_catalogo.click()
            time.sleep(2)

            card_tickets = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Tickets')]")))
            card_tickets.click()
            time.sleep(2)

            card_form = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Abrir novo Chamado Interno 1')]")))
            card_form.click()
            time.sleep(3)

        except Exception as e:
            print(f"Erro na execução: {e}")
            print("Navegador MANTIDO ABERTO para inspeção.")
            ocorreu_erro = True
            input("Pressione ENTER aqui no terminal para fechar.")
            break

print("Execução finalizada. Vai beber uma água.")