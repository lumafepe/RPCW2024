
## analizar o dataset

- Podemos dividir o dataset em Plantas e Ruas

- Ruas tem as características: Código de rua, Rua, Local, Freguesia
- Plantas tem as caracterísitcas: Id, Número de Registo, Espécie, Nome Científico, Origem, Data de Plantação, Estado, Caldeira, Tutor, Implantação, Gestor, Data de actualização, Número de intervenções


## Processar dados

O script python a escreve um cabeçalho constante, que corresponde às definições das classes, data properties e object properties. Depois, o ficheiro JSON é lido entrada por entrada. Para cada planta, é escrita uma nova instância da classe Planta, e também uma instância de Rua caso a rua não exista ainda.

