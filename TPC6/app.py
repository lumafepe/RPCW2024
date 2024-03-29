from flask import Flask,render_template,url_for
import requests
import datetime


app = Flask(__name__)
# data do sistema no formato ISO
curr_ISO_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


#From Previous TPC

# Define the DBpedia SPARQL endpoint
SPARQL_ENDPOINT = "http://epl.di.uminho.pt:7200/repositories/cinema2024"

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
    "dbp"     : "PREFIX dbp: <http://dbpedia.org/property/>",
    "cin"      : "PREFIX cin: <http://rpcw.di.uminho.pt/2024/cinema/>"
}

class Relation():
    def __init__(self,prefix=None,name=None,optional=False,lang=None,sequence=None,isUri=False) -> None:
        self.name = name
        self.prefix = prefix
        self.optional = optional
        self.language = lang
        self.sequence = sequence
        self.isUri = isUri
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
        if self.isUri:
            s = f"{self.prefix}:{self.name}"
        elif self.sequence==None:
            s=f"?main {self.prefix}:{self.name} ?{self.name}."
        else:
            s="?main "+"/".join(map(lambda x: f"{x.prefix}:{x.name}",self.sequence)) + f" ?{self.get_name()}."
        if self.language!=None:
            s+=f"FILTER(LANG(?{self.name}) = \"{self.language}\")."
        if self.optional:
            s=f"OPTIONAL {{ {s} }}."
        return s

        
             
        

def get_query_missing_offset(relations:list[Relation],type:Relation,isUri=False):
    prefixes = []
    for x in relations:
        prefixes.extend(x.get_prefixes())
    relationName = list(map(lambda x:x.get_name(),relations))
    type_prefixes,typeName = type.get_prefixes(),type.get_name()
    all_prefixes = set(prefixes+type_prefixes)
    query  = "\n".join(map(lambda x:PREFIXLIST[x],all_prefixes))
    query += "\n"
    if not isUri: query += "SELECT ?main "+" ".join(['?'+i for i in relationName])+'\n'
    else: query += "SELECT "+" ".join(['?'+i for i in relationName])+'\n'
    query += "WHERE {\n"
    if not isUri: 
        query += f"?main a {type_prefixes[0]}:{typeName}.\n"
        query += "\n".join(map(lambda x:x.getQueryLine(),relations))
    else:
        query += "\n".join(map(lambda x:x.getQueryLine().replace("?main",type.getQueryLine()),relations))
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

#classes
filmRel  = Relation("cin", "Film")
personRel = Relation("cin", "Person")
directorRel = Relation("cin", "Director")
screenWriterRel = Relation("cin", "ScreenWriter")
actorRel = Relation("cin", "Actor")
producerRel = Relation("cin", "Producer")
genreRel = Relation("cin", "Genre")

#dataProperties
birthDateRel = Relation("cin", "birthDate",optional=True)
descriptionRel = Relation("cin", "description",optional=True)
durationRel = Relation("cin", "duration",optional=True)
nameRel = Relation("cin", "name",optional=True)
titleRel = Relation("cin", "title",optional=True)

#objectProperties

actedRel = Relation("cin", "acted",optional=True)
hasActorRel = Relation("cin", "hasActor",optional=True)

directedRel = Relation("cin", "directed",optional=True)
hasDirectorRel = Relation("cin", "hasDirector",optional=True)

producedRel = Relation("cin", "produced",optional=True)
hasProducerRel = Relation("cin", "hasProducer",optional=True)

screenWroteRel = Relation("cin", "screenWrote",optional=True)
hasScreenWriterRel = Relation("cin", "hasScreenWriter",optional=True)

hasGenreRel = Relation("cin", "hasGenre",optional=True)

def getUri(uri):
    return uri.split('/')[-1].replace('_','-')

def mapDicData(data,obj,func):
    for i in range(len(data)): data[i][obj] = func(data[i][obj])


@app.route("/")
def index():
    return render_template("index.html",data={
        "date":curr_ISO_date
    })

@app.get("/filmes/",endpoint='filmes')
def filmes():
    data = get_all_data(get_query_missing_offset([titleRel],filmRel))
    mapDicData(data,'main',getUri)
    return render_template("filmes.html",data={
        "filmes": data,
        "date":curr_ISO_date
    })

@app.get("/filme/{string:movieName}/",endpoint='filme')
def filme(movieName:str):
    filmeR = Relation("cin",movieName.replace('-','_'),isUri=True)
    data = get_all_data(get_query_missing_offset([titleRel,descriptionRel,durationRel],filmeR,isUri=True))
    print(get_query_missing_offset([titleRel,descriptionRel,durationRel],filmeR,isUri=True))
    data=data[0]
    data["hasActor"] = get_all_data(get_query_missing_offset([hasActorRel],filmeR))
    mapDicData(data["hasActor"],'hasActor',lambda x: x["hasActor"])
    data["hasDirector"] = get_all_data(get_query_missing_offset([hasDirectorRel],filmeR))
    mapDicData(data["hasDirector"],'hasDirector',lambda x: x["hasDirector"])
    data["hasProducer"] = get_all_data(get_query_missing_offset([hasProducerRel],filmeR))
    mapDicData(data["hasProducer"],'hasProducer',lambda x: x["hasProducer"])
    data["hasScreenWriter"] = get_all_data(get_query_missing_offset([hasScreenWriterRel],filmeR))
    mapDicData(data["hasScreenWriter"],'hasScreenWriter',lambda x: x["hasScreenWriter"])
    data["hasGenre"] = get_all_data(get_query_missing_offset([hasGenreRel],filmeR))
    mapDicData(data["hasGenre"],'hasGenre',lambda x: x["hasGenre"])
    
    return render_template("filme.html",data={
        "filme": data,
        "date":curr_ISO_date,
        "filme_Uri":movieName
    })

@app.get("/pessoas/",endpoint='pessoas')
def pessoas():
    data = get_all_data(get_query_missing_offset([birthDateRel,descriptionRel,nameRel],personRel))
    mapDicData(data,'main',getUri)
    return render_template("pessoas.html",data={
        "pessoas": data,
        "date":curr_ISO_date
    })
    
    
def getType(type):
    data = get_all_data(get_query_missing_offset([birthDateRel,descriptionRel,nameRel],Relation("cin", type)))
    mapDicData(data,'main',getUri)
    return render_template("pessoasEspecializadas.html",data={
        "pessoas": data,
        "date":curr_ISO_date,
        "tipo":type
    })
    
@app.get("/pessoas/Actor/",endpoint='atores')
def atores():
    return getType("Actor")

@app.get("/pessoas/Diretor/",endpoint='diretores')
def diretores():
    return getType("Director")

@app.get("/pessoas/Produtor/",endpoint='produtores')
def produtores():
    return getType("Producer")

@app.get("/pessoas/Argumentista/",endpoint='argumentistas')
def argumentistas():
    return getType("ScreenWriter")
    

@app.get("/pessoa/{string:pessoaName}/",endpoint='pessoa')
def pessoa(pessoaName:str):
    pessoaR = Relation("cin",pessoaName.replace('-','_'),isUri=True)
    data = get_all_data(get_query_missing_offset([titleRel,descriptionRel,durationRel],pessoaR,isUri=True))
    print(get_query_missing_offset([titleRel,descriptionRel,durationRel],pessoaR,isUri=True))
    data=data[0]
    data["acted"] = get_all_data(get_query_missing_offset([actedRel],pessoaR))
    mapDicData(data["acted"],'acted',lambda x: x["acted"])
    data["directed"] = get_all_data(get_query_missing_offset([directedRel],pessoaR))
    mapDicData(data["directed"],'directed',lambda x: x["directed"])
    data["produced"] = get_all_data(get_query_missing_offset([producedRel],pessoaR))
    mapDicData(data["produced"],'produced',lambda x: x["produced"])
    data["screenWrote"] = get_all_data(get_query_missing_offset([screenWroteRel],pessoaR))
    mapDicData(data["screenWrote"],'screenWrote',lambda x: x["screenWrote"])
    
    return render_template("pessoa.html",data={
        "pessoa": data,
        "date":curr_ISO_date,
        "pessoa_Uri":pessoaName
    })
    
    
if __name__ == "__main__":
    app.run(debug=True)