from rdflib import Graph,URIRef,Literal,Namespace
from rdflib.namespace import RDF,OWL
import json

g=Graph()
g.parse("mapa.ttl")

def get_uri(uri):
    return uri.split("/")[-1]

def create_uri(uri):
    return uri.replace(" ","_").replace("\"","")



with open("mapa-virtual.json") as f:
    data = json.load(f)
    mapa = Namespace("http://rpcw.di.uminho.pt/2024/mapa/")
    distritos = set()
    for cidade in data["cidades"]:
        id          = create_uri(cidade['id'])
        nome        = cidade['nome']
        população   = int(cidade['população'])
        descrição   = cidade['descrição']
        distrito    = create_uri(cidade['distrito'])
        if distrito not in distritos:
            distritos.add(distrito)
            g.add((URIRef(f"{mapa}{distrito}"),RDF.type,OWL.NamedIndividual))
            g.add((URIRef(f"{mapa}{distrito}"),RDF.type,mapa.Distrito))
            g.add((URIRef(f"{mapa}{distrito}"),mapa.nome,Literal(distrito)))
        #Classes
        g.add((URIRef(f"{mapa}{id}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{mapa}{id}"),RDF.type,mapa.Cidade))
        #dataProperties
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}id"),Literal(id)))
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}nome"),Literal(nome)))
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}população"),Literal(população)))
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}descrição"),Literal(descrição)))
        #objectProperties
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}temDistrito"),URIRef(f"{mapa}{distrito}")))
    for ligacao in data["ligações"]:
        id          = ligacao["id"]
        origem      = ligacao["origem"]
        destino     = ligacao["destino"]
        distância   = float(ligacao["distância"])
        #Classes
        g.add((URIRef(f"{mapa}{id}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{mapa}{id}"),RDF.type,mapa.Ligação))
        #dataProperties
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}id"),Literal(id)))
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}distância"),Literal(distância)))
        #objectProperties
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}origem"),URIRef(f"{mapa}{origem}")))
        g.add((URIRef(f"{mapa}{id}"),URIRef(f"{mapa}destino"),URIRef(f"{mapa}{destino}")))
    
        
with open("mapa_pg54009.ttl","w") as f:
    f.write(g.serialize())