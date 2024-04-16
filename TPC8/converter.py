from rdflib import Graph,URIRef,Literal,Namespace
from rdflib.namespace import RDF,OWL
import pprint
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

g=Graph()
g.parse("familia-base.ttl")


familia = Namespace("http://rpcw.di.uminho.pt/2024/familia/")

tree = ET.parse('biblia.xml')
root = tree.getroot()



def pessoaF():
    return {"nome":"","sexo":"","filhos":set()}

def familiaF():
    return {"pais":set(),"filhos":set()}

pessoas=defaultdict(pessoaF)
familias=defaultdict(familiaF)

for child in root:
    if child.tag == 'person':
        if pessoas[child.find('id').text]["nome"] == '':
            pessoas[child.find('id').text]["nome"] =  child.find('namegiven').text
        
        if pessoas[child.find('id').text]["sexo"] == '':
            pessoas[child.find('id').text]["sexo"] =  child.find('sex').text
            
        for familyasspouse in child.findall('familyasspouse'):
            familias[familyasspouse.get('ref')]['pais'].add(child.find('id').text)
            
        for familyaschild in child.findall('familyaschild'):
            familias[familyasspouse.get('ref')]['filhos'].add(child.find('id').text)
        
        for parent in child.findall('parent'):
            if parent.get('ref') not in pessoas:
                pessoas[parent.get('ref')]["nome"] = parent.text
            pessoas[parent.get('ref')]["filhos"].add(child.find('id').text)
            
        for children in child.findall('child'):
            if children.get('ref') not in pessoas:
                pessoas[children.get('ref')]["nome"] = children.text
            pessoas[child.find('id').text]["filhos"].add(children.get('ref'))
            
for k in familias:
    familias[k]['filhos'] = familias[k]['filhos'] - familias[k]['pais'] 
        
for k,p in pessoas.items():
    g.add((URIRef(f"{familia}{k}"),RDF.type,OWL.NamedIndividual))
    g.add((URIRef(f"{familia}{k}"),RDF.type,familia.Pessoa))
    g.add((URIRef(f"{familia}{k}"),familia.nome,Literal(p['nome'])))
    for c in p['filhos']:
        g.add((URIRef(f"{familia}{c}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{familia}{c}"),RDF.type,familia.Pessoa))
        g.add((URIRef(f"{familia}{c}"),familia.nome,Literal(pessoas[c]['nome'])))
        if p['sexo']=='M':
            g.add((URIRef(f"{familia}{c}"),familia.temPai,URIRef(f"{familia}{k}")))
        else:
            g.add((URIRef(f"{familia}{c}"),familia.temMae,URIRef(f"{familia}{k}")))


    
with open("biblia.ttl","w") as f:
    f.write(g.serialize())
    