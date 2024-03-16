import requests
from collections import defaultdict
import json
import datetime
import uuid

BASE_DATE = datetime.datetime(1900, 1, 1)

# Define the DBpedia SPARQL endpoint
SPARQL_ENDPOINT = "http://dbpedia.org/sparql"

# Define the headers
HEADERS = {
    "Accept": "application/sparql-results+json"
}
getParams = lambda query: {"query": query,"format": "json"}
request_data = lambda query : requests.get(SPARQL_ENDPOINT, params=getParams(query), headers=HEADERS)

PREFIXLIST={
    "dcterms" : "PREFIX dcterms: <http://purl.org/dc/terms/>",
    "madsrdf" :	"PREFIX madsrdf: <http://loc.hi.hi.gov/hihi/>",
    "bflc"    :	"PREFIX bflc: <http://id.loc.gov/ontologies/bflc/>",
    "foaf"    :	"PREFIX foaf: <http://xmlns.com/foaf/0.1/>",
    "rdf"     : "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
    "dbo"     : "PREFIX dbo: <http://dbpedia.org/ontology/>",
    "rdfs"    : "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
    "yago"    : "PREFIX yago: <http://yago-knowledge.org/resource/>",
    "dc"      : "PREFIX dc: <http://purl.org/dc/elements/1.1/>",
    "dbp"     : "PREFIX dbp: <http://dbpedia.org/property/>"
}

class Relation():
    def __init__(self,prefix=None,name=None,optional=False,lang=None,sequence=None) -> None:
        self.name = name
        self.prefix = prefix
        self.optional = optional
        self.language = lang
        self.sequence = sequence
    def get_prefixes(self) -> list[str] :
        if self.prefix!=None:
            return [self.prefix]
        l=[]
        for i in self.sequence:
            l.extend(i.get_prefixes())
        return l
    def get_name(self):
        if self.name:
            return self.name
        return self.sequence[-1].get_name()
    def getQueryLine(self):
        if self.sequence==None:
            s=f"?main {self.prefix}:{self.name} ?{self.name}."
        else:
            s="?main "+"/".join(map(lambda x: f"{x.prefix}:{x.name}",self.sequence)) + f" ?{self.get_name()}."
        if self.language!=None:
            s+=f"FILTER(LANG(?{self.name}) = \"{self.language}\")."
        if self.optional:
            s=f"OPTIONAL {{ {s} }}."
        return s

        
             
        

def get_query_missing_offset(relations:list[Relation],type:Relation):
    prefixes = []
    for x in relations:
        prefixes.extend(x.get_prefixes())
    relationName = list(map(lambda x:x.get_name(),relations))
    type_prefixes,typeName = type.get_prefixes(),type.get_name()
    all_prefixes = set(prefixes+type_prefixes)
    query  = "\n".join(map(lambda x:PREFIXLIST[x],all_prefixes))
    query += "\n"
    query += "SELECT ?main "+" ".join(['?'+i for i in relationName])+'\n'
    query += "WHERE {\n"
    query += f"?main a {type_prefixes[0]}:{typeName}.\n"
    query += "\n".join(map(lambda x:x.getQueryLine(),relations))
    query += "\n} LIMIT 10000\nOFFSET "
    return query

def get_all_data(query):
    i = 0
    r=10000
    data=[]
    while r==10000:
        get_vals = lambda x: x["value"]
        queryReal = query + str(i*10000)
        r=0
        responses = request_data(queryReal)
        if responses.status_code >= 200 and responses.status_code < 300:
            if responses.status_code!=200: 
                print(responses.status_code)
                print(queryReal)
                r=10000
                continue
            results = responses.json()
            r=len(results["results"]["bindings"])
            for pos in range(r):
                for k in results["results"]["bindings"][pos].keys():
                    results["results"]["bindings"][pos][k]=get_vals(results["results"]["bindings"][pos][k])
            data.extend(results["results"]["bindings"])
            print("gotten:",i*10000+r)
        else:
            print(f"Error:", responses.status_code)
            print(responses.text)
            exit()
        i+=1
    return data

filmesIds=defaultdict(lambda:str(uuid.uuid4()))
filmes={}

pessoasIds=defaultdict(lambda:str(uuid.uuid4()))
pessoasRoles=defaultdict(set)
pessoas={}

filmeRel  = Relation("dbo", "Film")
pessoaRel = Relation("dbo", "Person")



descriptionRel = Relation("dbo", "abstract", optional=True,lang="en")
duracaoRel     = Relation("dbo", "runtime",  optional=True)
nomeRel        = Relation("rdfs","label",    optional=True,lang="en")

#getMovie Name,description,etc 
for data in get_all_data(get_query_missing_offset([descriptionRel,duracaoRel,nomeRel],filmeRel)):
    filmeURI = data["main"]
    filmes[filmeURI]={
        "id":filmesIds[filmeURI],
        "categoria":[],
        "atores":[],
        "musico":[],
        "produtor":[],
        "diretor":[],
        "escritor":[],
        "argumentista":[],
        "uri":filmeURI
    }
    if "runtime" in data:
        duracao = int(float(data["runtime"]))
        durationStr = (BASE_DATE + datetime.timedelta(seconds=duracao)).strftime("%H:%M:%S")
        filmes[filmeURI]["duracao"] = durationStr
        filmes[filmeURI]["short"] = duracao < 30 * 60
    if "abstract" in data:
        filmes[filmeURI]["descricao"] = data["abstract"]
    if "label" in data:
        filmes[filmeURI]["nome"] = data["label"]

def appendRels(dictName:str,rel:Relation,persons=False):
    global filmeRel,filmes,pessoasRoles,pessoasIds
    query = get_query_missing_offset([rel],filmeRel)
    for data in get_all_data(query):
        filmeURI = data["main"]
        if filmeURI in filmes:
            if not persons:
                filmes[filmeURI][dictName].append(data[rel.get_name()])
            else:
                pessoaURI = data[rel.get_name()]
                filmes[filmeURI][dictName].append(pessoasIds[pessoaURI])
                pessoasRoles[pessoaURI].add(rel.get_name())
    
appendRels("categoria",Relation(sequence=[Relation("dcterms","subject"),Relation("rdfs","label")]))        
appendRels("atores",Relation("dbo","starring"),persons=True)
appendRels("musico",Relation("dbo","musicComposer"),persons=True)
appendRels("produtor",Relation("dbo","producer"),persons=True)
appendRels("diretor",Relation("dbo","director"),persons=True)
appendRels("escritor",Relation("dbo","writer"),persons=True)
appendRels("argumentista",Relation("dbo","cinematography"),persons=True)


birthdayRel = Relation("dbo","birthDate",optional=True)

for data in get_all_data(get_query_missing_offset([descriptionRel,birthdayRel,nomeRel],pessoaRel)):
    pessoaURI = data["main"]
    if pessoaURI in pessoasIds:
        person_id = pessoasIds[pessoaURI]
        pessoas[person_id]={
            "id":person_id,
            "roles":list(pessoasRoles[pessoaURI]),
            "uri":pessoaURI
        }
        if "abstract" in data:
            pessoas[person_id]["descricao"]=data["abstract"]
        if "birthDate" in data:
            pessoas[person_id]["data_nascimento"]=data["birthDate"]
        if "label" in data:
            pessoas[person_id]["nome"]=data["label"]


pessoasWithNameOnly = set(pessoasIds.keys()-set(map(lambda x:x["uri"],pessoas.values())))
for pessoaUri in pessoasWithNameOnly:
    pessoa_id = pessoasIds[pessoaUri]
    pessoas[pessoa_id] = {
        "id":pessoa_id,
        "roles":[],
        "uri":pessoaUri
    }


fullData={
    "filmes":list(filmes.values()),
    "pessoas":list(pessoas.values())
}

with open("filmes.json","w") as f:
    json.dump(fullData,f, indent=4)