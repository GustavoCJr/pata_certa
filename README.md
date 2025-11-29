# INSTRUÇÕES

**INSTALAR AS DEPENDÊNCIAS**:
    utilize o comando `pip install -r requirements.txt`.

**COMANDO DE EXECUÇÃO**:
    `python app.py` para executar a aplicação.

**MODELO DE DADOS**:
    Clique para ver [modelo de dados](models.py). (Classes e Tabelas).

## ROTAS CONSTRUÍDAS

`/` (metodos: GET)

Rota padrão exibe a página home, *index.html*.

`/exibir_pet/<pet_id>` (metodos: GET)

*GET* -> recebe junto a URL uma variavel "pet_id" (do tipo inteiro), faz a busca do pet com esse ID requisitado e exibe os dados dele junto a *pet.html*.

`/registrar_pet` (metodos: POST e GET)

*GET* -> Envia para a página formulário de registrar um pet, *registrar_pet_form.html*.

*POST* -> Espera os valores de **Animal** (ver [modelo de dados](models.py)), registra na tabela *animais* do banco de dados os valores, e redireciona para a página de exibição do animal (rota: `/exibir_pet/<ID_Gerado>`).

`/login` (metodos: GET e POST)

*GET* -> Envia para a página de formulário de login da ONG, `login_form.html`.

*POST* -> Recebe as credenciais (*e-mail* e *senha*), verifica a autenticidade da ONG no banco de dados e, se for bem-sucedido, inicia a sessão de login (`login_user`). Caso contrário, exibe uma mensagem de erro na tela.

`/logout` (metodos: GET)

*GET* -> Encerra a sessão de login atual (`logout_user`), remove o usuário da sessão do navegador e redireciona para a página inicial (`/`).

`/cadastro/ong` (metodos: GET e POST)

*GET* -> Envia para a página de formulário de cadastro de ONG, `cadastro_ong_form.html`.

*POST* -> Recebe os dados da ONG, valida duplicidade (CNPJ/Email), hasheia a senha, registra a nova ONG e redireciona para o login.

`/sobre` (metodos: GET)

*GET* -> Exibe informações sobre o propósito, missão e a tecnologia do projeto PataCerta, renderizando a página `sobre.html`.