import json

with open("plantas.json") as f:
    bd = json.load(f)


ttl="""@prefix : <http://rpcw.di.uminho.pt/2024/plantas/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/plantas/> .

<http://rpcw.di.uminho.pt/2024/plantas> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#emRua
:emRua rdf:type owl:ObjectProperty ;
       rdfs:domain :Planta ;
       rdfs:range :Rua .

      
###  http://rpcw.di.uminho.pt/2024/plantas#estado
:estado rdf:type owl:ObjectProperty ;
        rdfs:domain :Planta ;
        rdfs:range :Estado .


###  http://rpcw.di.uminho.pt/2024/plantas#temCaldeira
:temCaldeira rdf:type owl:ObjectProperty ;
             rdfs:domain :Planta ;
             rdfs:range :Maybe .


###  http://rpcw.di.uminho.pt/2024/plantas#temTutor
:temTutor rdf:type owl:ObjectProperty ;
          rdfs:domain :Planta ;
          rdfs:range :Maybe .


###  http://rpcw.di.uminho.pt/2024/plantas#tipo
:tipo rdf:type owl:ObjectProperty ;
      rdfs:domain :Planta ;
      rdfs:range :Implantação .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#Código_de_rua
:Código_de_rua rdf:type owl:DatatypeProperty ;
               rdfs:domain :Rua ;
               rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/plantas#Data_de_Plantação
:Data_de_Plantação rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Planta ;
                   rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Data_de_actualização
:Data_de_actualização rdf:type owl:DatatypeProperty ;
                      rdfs:domain :Planta ;
                      rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Espécie
:Espécie rdf:type owl:DatatypeProperty ;
         rdfs:domain :Planta ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Freguesia
:Freguesia rdf:type owl:DatatypeProperty ;
           rdfs:domain :Rua ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Gestor
:Gestor rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Id
:Id rdf:type owl:DatatypeProperty ;
    rdfs:domain :Planta ;
    rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/plantas#Local
:Local rdf:type owl:DatatypeProperty ;
       rdfs:domain :Rua ;
       rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Nome_Científico
:Nome_Científico rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Planta ;
                 rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Número_de_Registo
:Número_de_Registo rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Planta ;
                   rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/plantas#Número_de_intervenções
:Número_de_intervenções rdf:type owl:DatatypeProperty ;
                        rdfs:domain :Planta ;
                        rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/plantas#Origem
:Origem rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Rua
:Rua rdf:type owl:DatatypeProperty ;
     rdfs:domain :Rua ;
     rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#Estado
:Estado rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/plantas#Implantação
:Implantação rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/plantas#Maybe
:Maybe rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/plantas#Planta
:Planta rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/plantas#Rua
:Rua rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#Adulto
:Adulto rdf:type owl:NamedIndividual ,
                 :Estado .


###  http://rpcw.di.uminho.pt/2024/plantas#Arruamento
:Arruamento rdf:type owl:NamedIndividual ,
                     :Implantação .


###  http://rpcw.di.uminho.pt/2024/plantas#Espaço_Verde
:Espaço_Verde rdf:type owl:NamedIndividual ,
                       :Implantação .


###  http://rpcw.di.uminho.pt/2024/plantas#Jovem
:Jovem rdf:type owl:NamedIndividual ,
                :Estado .


###  http://rpcw.di.uminho.pt/2024/plantas#NULL
:NULL rdf:type owl:NamedIndividual ,
               :Estado ,
               :Implantação ,
               :Maybe .


###  http://rpcw.di.uminho.pt/2024/plantas#Não
:Não rdf:type owl:NamedIndividual ,
              :Maybe .


###  http://rpcw.di.uminho.pt/2024/plantas#Outro
:Outro rdf:type owl:NamedIndividual ,
                :Estado ,
                :Implantação .


###  http://rpcw.di.uminho.pt/2024/plantas#Sim
:Sim rdf:type owl:NamedIndividual ,
              :Maybe .


###  http://rpcw.di.uminho.pt/2024/plantas#Velho
:Velho rdf:type owl:NamedIndividual ,
                :Estado .
"""

ruas = set()

for obj in bd:
    if obj["Número de intervenções"]=="":
        obj["Número de intervenções"]=0
    obj["Rua"] = obj["Rua"].replace('"', '\\"')
    id = obj["Id"]
    if obj['Código de rua']:
        codigo = obj['Código de rua']
        if codigo not in ruas:
            ruas.add(codigo)
            ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/plantas#{codigo}
<http://rpcw.di.uminho.pt/2024/plantas#{codigo}> rdf:type owl:NamedIndividual ,
                          :Rua ;
                 :Código_de_rua "{codigo}"^^xsd:long ;
                 :Freguesia "{obj["Freguesia"]}" ;
                 :Local "{obj["Local"]}" ;
                 :Rua "{obj["Rua"]}" .
"""
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/plantas#{id}
<http://rpcw.di.uminho.pt/2024/plantas#{id}> rdf:type owl:NamedIndividual ,
                                                                                             :Planta ;
    :emRua <http://rpcw.di.uminho.pt/2024/plantas#{codigo}> ; ;
    :estado "{obj['Estado']}" ;
    :temCaldeira "{obj['Caldeira']}" ;
    :temTutor "{obj['Tutor']}" ;
    :tipo "{obj['Implantação']}" ;
    :Data_de_Plantação "{obj['Data de Plantação']}" ;
    :Data_de_actualização "{obj['Data de actualização']}" ;
    :Espécie "{obj['Espécie']}" ;
    :Gestor "{obj['Gestor']}" ;
    :Id "{id}"^^xsd:long ;
    :Nome_Científico "{obj['Nome Científico']}" ;
    :Número_de_Registo "{obj["Número de Registo"]}"^^xsd:long ;
    :Número_de_intervenções "{obj["Número de intervenções"]}"^^xsd:int ;
    :Origem "{obj['Origem']}" .
"""
    
with open("plants.ttl","w") as f:
    f.write(ttl)