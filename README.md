# INSTRUÇÕES

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