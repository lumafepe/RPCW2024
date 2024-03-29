from rdflib import Graph,URIRef,Literal,Namespace
from rdflib.namespace import RDF,OWL
import pprint
import json


g=Graph()
g.parse("Cinema.ttl")

def get_uri(uri):
    return uri.split("/")[-1]

def create_uri(uri):
    return uri.replace(" ","_").replace("\"","")

with open("out.json") as f:
    categories = set()
    data = json.load(f)
    cinema = Namespace("http://rpcw.di.uminho.pt/2024/cinema/")
    
    #handle persons
    for pessoa in data["pessoas"].values():
        uriName = get_uri(pessoa["uri"])
        g.add((URIRef(f"{cinema}{uriName}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{cinema}{uriName}"),RDF.type,cinema.Person))
        if "descricao" in pessoa:
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}description"),Literal(pessoa["descricao"])))
        if "nome" in pessoa:
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}name"),Literal(pessoa["nome"])))
        if "data_nascimento" in pessoa:
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}birthDate"),Literal(pessoa["data_nascimento"])))
    
    #handle movies
    for filme in data["filmes"].values():
        
        uriName = get_uri(filme["uri"])
        g.add((URIRef(f"{cinema}{uriName}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{cinema}{uriName}"),RDF.type,cinema.Film))
        
        for genre in filme["categoria"]:
            uri = create_uri(genre)
            if genre not in categories:
                categories.add(genre)
                g.add((URIRef(f"{cinema}{uri}"),RDF.type,OWL.NamedIndividual))
                g.add((URIRef(f"{cinema}{uri}"),RDF.type,cinema.Genre))
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}hasGenre"),URIRef(f"{cinema}{uri}")))
        
        for actor in map(lambda x:get_uri(data["pessoas"][x]["uri"]),filme["atores"]):
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}hasActor"),URIRef(f"{cinema}{actor}")))
            g.add((URIRef(f"{cinema}{actor}"),RDF.type,cinema.Actor))

        for director in map(lambda x:get_uri(data["pessoas"][x]["uri"]),filme["diretor"]):
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}hasDirector"),URIRef(f"{cinema}{actor}")))
            g.add((URIRef(f"{cinema}{actor}"),RDF.type,cinema.Director))
            
        for producer in map(lambda x:get_uri(data["pessoas"][x]["uri"]),filme["produtor"]):
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}hasProducer"),URIRef(f"{cinema}{producer}")))
            g.add((URIRef(f"{cinema}{actor}"),RDF.type,cinema.Producer))
        
        for screenWriter in map(lambda x:get_uri(data["pessoas"][x]["uri"]),filme["argumentista"]):
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}hasScreenWriter"),URIRef(f"{cinema}{screenWriter}")))
            g.add((URIRef(f"{cinema}{actor}"),RDF.type,cinema.ScreenWriter))
        
        if "descricao" in filme:
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}description"),Literal(filme["descricao"])))
        
        if "nome" in filme:
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}title"),Literal(filme["nome"])))
        
        if "duracao" in filme:
            h,m,s = filme["duracao"].split(":") 
            h,m,s = int(h),int(m),int(s)
            g.add((URIRef(f"{cinema}{uriName}"),URIRef(f"{cinema}duration"),Literal((h*60+m)*60+s)))

with open("cinema_pg54009.ttl","w") as f:
    f.write(g.serialize())
    
