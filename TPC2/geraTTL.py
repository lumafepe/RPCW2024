import json

with open("db.json") as f:
    bd = json.load(f)


ttl="""@prefix : <http://rpcw.di.uminho.pt/2024/music#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/music> .

<http://rpcw.di.uminho.pt/2024/music> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/music#emCurso
:emCurso rdf:type owl:ObjectProperty ;
         rdfs:domain :Alunos ;
         rdfs:range :Cursos .


###  http://rpcw.di.uminho.pt/2024/music#ensinaInstrumento
:ensinaInstrumento rdf:type owl:ObjectProperty ;
                   rdfs:domain :Cursos ;
                   rdfs:range :Instrumentos .


###  http://rpcw.di.uminho.pt/2024/music#temInstrumento
:temInstrumento rdf:type owl:ObjectProperty ;
                rdfs:domain :Alunos ;
                rdfs:range :Instrumentos .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/music#anoCurso_aluno
:anoCurso_aluno rdf:type owl:DatatypeProperty ;
                rdfs:domain :Alunos ;
                rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/music#dataNascimento_aluno
:dataNascimento_aluno rdf:type owl:DatatypeProperty ;
                      rdfs:domain :Alunos ;
                      rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/music#designacao_curso
:designacao_curso rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Cursos ;
                  rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/music#duracao_curso
:duracao_curso rdf:type owl:DatatypeProperty ;
               rdfs:domain :Cursos ;
               rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/music#id_aluno
:id_aluno rdf:type owl:DatatypeProperty ;
          rdfs:domain :Alunos ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/music#id_curso
:id_curso rdf:type owl:DatatypeProperty ;
          rdfs:domain :Cursos ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/music#id_instrumento
:id_instrumento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Instrumentos ;
                rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/music#nome_aluno
:nome_aluno rdf:type owl:DatatypeProperty ;
            rdfs:domain :Alunos ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/music#text_instrumento
:text_instrumento rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Instrumentos ;
                  rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/music#Alunos
:Alunos rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/music#Cursos
:Cursos rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/music#Instrumentos
:Instrumentos rdf:type owl:Class .


#################################################################
#    General axioms
#################################################################

[ rdf:type owl:AllDisjointClasses ;
  owl:members ( :Alunos
                :Cursos
                :Instrumentos
              )
] .
"""

d = {}

for obj in bd["instrumentos"]:
    d[obj["#text"]] = obj["id"]
    ttl+=f"""###  http://rpcw.di.uminho.pt/2024/music#{obj["id"]}
<http://rpcw.di.uminho.pt/2024/music#{obj["id"]}> rdf:type owl:NamedIndividual ,
    :Instrumentos ;
  :text_instrumento "{obj["#text"]}"^^xsd:string ;
  :id_instrumento "{obj["id"]}"^^xsd:string .
  
"""

for obj in bd["cursos"]:
    ttl+=f"""###  http://rpcw.di.uminho.pt/2024/music#{obj["id"]}
<http://rpcw.di.uminho.pt/2024/music#{obj["id"]}> rdf:type owl:NamedIndividual ,
    :Cursos ;
  :designacao_curso "{obj["designacao"]}"^^xsd:string ;
  :duracao_curso "{obj["duracao"]}"^^xsd:long ;
  :id_curso "{obj["id"]}"^^xsd:long ;
  :ensinaInstrumento <http://rpcw.di.uminho.pt/2024/music#{obj["instrumento"]["id"]}> .
  
"""

for obj in bd["alunos"]:
  ttl+=f"""###  http://rpcw.di.uminho.pt/2024/music#{obj["id"]}
<http://rpcw.di.uminho.pt/2024/music#{obj["id"]}> rdf:type owl:NamedIndividual ,
    :Alunos ;
  :nome_aluno "{obj["nome"]}"^^xsd:string ;
  :dataNascimento_aluno "{obj["dataNasc"]}"^^xsd:string ;
  :id_aluno "{obj["id"]}"^^xsd:string ;
  :emCurso <http://rpcw.di.uminho.pt/2024/music#{obj["curso"]}> ;
  :anoCurso_aluno "{obj["anoCurso"]}"^^xsd:long ;
  :temInstrumento <http://rpcw.di.uminho.pt/2024/music#{d[obj["instrumento"]]}> .
  
"""


with open("music.ttl","w") as f:
    f.write(ttl)