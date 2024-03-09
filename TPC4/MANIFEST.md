## Requisitos
É necessário ter o GraphDB com um repositório chamado ``` Tabelaperiodica ``` com os dados da tabela periódica.
É também necessário a livraria ``` flask ``` de Python.

## Executar a aplicação
Para fazer o website ficar disponível é necessário executar ``` python3 app.py ```. O website fica disponível em ```localhost:5000```.

## Paginas
- /index -> index de páginas principais.
- /elementos -> tabela de todos os elementos ordenados por número atómico e com referência para a página individual de cada elementos e para a do grupo do elemento.
- /elemento/\<Número Atómico\> -> Informação do elemento com o Número Atómico correspondente.
- /grupos tabela de todos os grupos e com referência para a página individual de cada grupo.
- /grupo/\<id do grupo\> Informação do grupo com o id correspondente. 


