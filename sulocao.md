# A Solução: Consultas Parametrizadas

A solução definitiva e padrão na indústria para mitigar este problema é a Parametrização.

Em vez de juntar o texto introduzido pelo utilizador diretamente na string do comando, enviamos uma estrutura fixa para o banco de dados utilizando marcadores de posição (conhecidos como placeholders, representados por %s no MySQL) e passamos os dados reais de forma totalmente separada através de uma tupla no Python.

Com esta abordagem, a query torna-se estática e o banco de dados já sabe exatamente o que ela faz antes de receber os dados. O driver envia o comando SELECT \* FROM users WHERE username = %s AND password = %s e, em seguida, executa o comando passando as variáveis de username e password à parte.

Esta técnica é 100% segura porque, ao receber o comando com os marcadores %s, o MySQL compila a estrutura da query antes sequer de olhar para as entradas do utilizador. Quando os dados finalmente chegam, o banco de dados trata-os estritamente como strings literais (valores puros e isolados). Se o atacante tentar introduzir o texto ' OR '1'='1, o banco de dados limitará a sua pesquisa a procurar, de forma literal, por um utilizador cujo nome seja exatamente o texto composto por aspas e operadores. O comando malicioso perde, assim, toda a capacidade de ser executado como código.

# Resumo de Boas Práticas

Nunca coloque aspas nos placeholders: Escreva sempre a estrutura como WHERE coluna = %s e nunca envolva o marcador em aspas simples como WHERE coluna = '%s'. Se colocar aspas, o MySQL tratará o símbolo como texto literal (a letra % e a letra s) em vez de o reconhecer como um ponto de parametrização.

Tratamento especial para o operador LIKE: Nunca tente escrever a instrução LIKE '%%s%' diretamente na query. O correto é manter apenas LIKE %s no comando SQL e concatenar as percentagens de pesquisa do lado do Python, definindo o parâmetro como uma string formatada contendo a palavra pretendida entre os símbolos de percentagem.

Atenção às tuplas de um só elemento: No ecossistema Python, para passar apenas uma única variável dentro de uma tupla no método de execução do banco de dados, é obrigatório colocar uma vírgula logo após o elemento. Caso escreva apenas a variável entre parênteses, o Python interpretará a sintaxe apenas como parênteses matemáticos comuns e a execução do código irá falhar.
