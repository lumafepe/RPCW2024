from SPARQLWrapper import SPARQLWrapper, JSON,N3
import rdflib

def sparql_get_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/MAPA")
    sparql.setMethod('GET')
    sparql.setQuery(query)
    sparql.setReturnFormat(N3)
    return sparql.query().convert()

def sparql_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/MAPA/statements")
    sparql.setMethod('POST')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()



def parse_lig(data):
    return {
        'ori':data['ori']['value'].split('#')[-1],
        'des':data['des']['value'].split('#')[-1]
    }

query = """
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

CONSTRUCT {
  _:ligacao a :Ligação;
            :origem ?ori;
            :destino ?des.
}
WHERE {
  ?ori a :Cidade.
  ?lig a :Ligação.
  ?lig :origem ?ori.
  ?lig (:destino/^:origem)* ?ligações.
  ?ligações :destino ?des.
}
"""
result = sparql_get_query(query)
graph = rdflib.Graph()
graph.parse(data=result, format='n3')

n3_data = graph.serialize(format='n3').encode('utf-8')

insert_query = f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

INSERT DATA {{
  {n3_data}
}}
"""

sparql_query(insert_query)