
## analizar o dataset

- Podemos dividir o dataset em Alunos, Cursos e Instrumentos

- Alunos tem as características: Id, Nome, Data de Nascimento, Curso, Ano no Curso, Instrumento que tocam 
- Cursos tem as características: Id, designação,duração,
e instrumento ensinado com o seu Id e Texto
- Instrumento tem as caracterísitcas: Id e Texto


## Processar dados

O script python a escreve um cabeçalho constante, que corresponde às definições das classes, data properties e object properties. Depois, o ficheiro JSON é lido entrada por entrada. 
Inicialmente para cada instrumento é cria uma entrada da classe e é guardado também qual o Id que corresponde ao nome do instrumento. 
Depois é lido cada um dos cursos criando entradas para eles e associa o curso ao instrumento que é ensinado pela ObjectProperty "ensinaInstrumento".
Por fim a cada aluno é criado uma entrada associando pela ObjectProperty "emCurso" ao curso em que está inscrito e pela "temInstrumento" ao instrumento que toca, usando o mapa de nomes para id.

## Executar conversor
Para convert o dataset em json para a ontologia em turtle basta fazer ``` python3 geraTTL.py ``` 

