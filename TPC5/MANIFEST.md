# Executar a aplicação
Para executar o recolhedor de dados é necessário executar ``` python3 db_movies.py ```. O dados serão exportados para filmes.json

# Genericos
De forma a facilitar a criação de pedidos a dbpedia foi criado 3 tipos de genericos
- ### Relation

Esta classe foi criada de forma a representar a relação de um triplo ou um objeto de um triplo.
Um objeto de esta classe pode ser defenido como o prefixo e o nome da relação ou então como uma lista de Relations, neste segundo caso é aplicado o operador ```/``` do SPARQL entre as relações.

- ### get_query_missing_offset
Esta função recebe uma lista de relações representando cada um dos atributos a ser recebido assim como uma relação que representa o tipo do objeto a ser obtido.
Esta função irá gerar a query para obter todas as entradas automaticamente faltando adicionar ao fim da string o valor do offset.

- ### get_all_data
Esta função recebe um query sobre o formato de string em que falte um offset. Visto que o dbpedia só envia 10000 valores a cada pedido, é necessário fazer pedidos iterativamente aumentando o offset para obter-se todos os valores.
Tal como dito anteriormente a função executa a query obtendo todos os valores possiveis e dá parsing aos valores returnando uma lista de dicionários em que as chaves vão sero nome de cada uma das relações o URI do objeto em questão chamar-se há ```main```.

# Dados a recolher
Os dados que são necessários recolher dividem-se em 3 tipos.
- Filmes
- Pessoas
- Categorias

A categoria foi apenas defenido como um nome pelo que não foi dividido numa nova classe.
Para Pessoas e Filmes foi atribuido um uuid a cada entidade destes tipos como forma de os identificar.

Para Filmes foi recolhido:
- Id
- Categorias
- Atores
- Musico
- Produtor
- Diretor
- Escritor
- Argumentista
- Uri
- Duração
- Short (se é curta metragem)
- Descricao
- Nome

Para Pessoas foi recolhido:
- Id
- Roles (Quais as suas profissões nos filmes)
- Uri
- Descrição
- Data de Nascimento
- Nome


# Ordem de recolha de dados
Incialmente são recolhidos os uri,duração,short,descrição e nome de todos os filmes simultaneamente visto apenas haver uma entrada de cada um dos campos. 

Posteriormente para todos os filmes vai ser recolhido pela ordem apresentada cada um dos atributos categoria,atores,musico,produtor,diretor,escritor e argumentista.

Assim toda a informação sobre os filmes já terá cido recolhida. Em simultaneo é guardado também em que empregos uma pessoa já trabalhou para ser utilizado no campo roles da pessoa.

Por fim é recolhidos todos os dados das Pessoas de uma só vez.


