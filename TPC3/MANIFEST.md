
## analizar o dataset

- Podemos dividir o dataset em Cidades, Distritos e Ligações

- Distritos tem a característica: nome 
- Cidades tem as características: população,nome,id,descrição e a propriedade em distrito que a associa a um distrito. 
- Ligações tem as características: distância e id, e as propriedas origem e destino que as associa a 2 cidades

## Processar dados

O script python a escreve um cabeçalho constante, que corresponde às definições das classes, data properties e object properties. Depois, o ficheiro JSON é lido entrada por entrada. 
Inicialmente para cada cidade é criada uma entrada da classe e é criado tambem o seu Distrito se ainda não existir estes dados são guardados em 2 sets distinto para verficiar se as ligações são validas.
Por fim a cada ligação é criada uma entrada associando pelas ObjectPropertys "origem" e "destino" as cidades a qual esta se refere.

## Executar conversor
Para convert o dataset em json para a ontologia em turtle basta fazer ``` python3 geraTTL.py ``` 


## Queries
As queries podem ser visualizadas no ficheiro ```queries.md```.
