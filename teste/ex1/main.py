from typing import Union

from fastapi import FastAPI
from generate import get_all_data, get_query_missing_offset,Relation
import requests
app = FastAPI()

SPARQL_ENDPOINT = "http://localhost:7200/repositories/teste2"

# Define the headers
HEADERS = {
    "Accept": "application/sparql-results+json"
}
getParams = lambda query: {"query": query,"format": "json"}
request_data = lambda query : requests.get(SPARQL_ENDPOINT, params=getParams(query), headers=HEADERS)

def getValues(lm):
    return [{k : v['value'] for k,v in i.items()} for i in lm]






@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/alunos")
def getAlunos(curso: str = None, groupBy: str = None):
    if groupBy=="curso":
        query=f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select DISTINCT ?curso (count(?aluno) as ?n_alunos)
where {{
    ?aluno a :Aluno ;
    :curso ?curso .
}} GROUP BY ?curso ORDER BY ?curso
"""
    elif groupBy == "projeto":
        query=f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select ?notaProjeto (count(?alunos) as ?N_alunos)
where {{
?alunos a :Aluno .
?aluno :projeto ?notaProjeto .
}} group by ?notaProjeto
"""
    elif groupBy == "recurso":
        query="""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select ?idAluno ?nome ?curso ?notaExame
where {
	?aluno a :Aluno .
	?exame a :Recurso .
	?aluno :exame ?exame.
    ?exame :nota ?notaExame .
	?aluno :nome ?nome .
	?aluno :id ?idAluno .
	?aluno :curso ?curso .
} ORDER BY ?nome
"""
    else:
        query=f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select ?nome ?idAluno ?curso
where {{
?alunos a :Aluno ;
    :nome ?nome ;
    :id ?idAluno ;
    {':curso "'+curso+'" ;' if curso else ""}
    :curso ?curso .
}} ORDER BY ?nome
"""
        

    responses = request_data(query)
    results = responses.json()
    r=getValues(results["results"]["bindings"])
    
    return r

@app.get("/api/alunos/tpc")
def getAlunosTPC():
    query=f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select ?nome ?idAluno ?curso (count(?tpcs) as ?n_tpcs)
where {{
?alunos a :Aluno ;
    :nome ?nome ;
    :id ?idAluno ;
    :tpc ?tpcs ;
    :curso ?curso .
}} GROUP BY ?nome ?idAluno ?curso ORDER BY ?nome
"""

    responses = request_data(query)
    results = responses.json()
    r=getValues(results["results"]["bindings"])
    
    return r

@app.get("/api/alunos/avaliados")
def getAlunosAvalidados():
    query=f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select ?nome ?idAluno ?curso ?projeto (SUM(?tpcs) AS ?tpcstotal) (MAX(?exames) AS ?exame)
where {{
?alunos a :Aluno ;
    :nome ?nome ;
    :id ?idAluno ;
    :curso ?curso ;
    :tpc/:nota ?tpcs ;
    :projeto ?projeto ;
    :exame/:nota ?exames .
}} GROUP BY ?aluno ?idAluno ?nome ?curso ?projeto
ORDER BY ?nome 
"""
    def x(y):
        print(y)
        nf = float(y['tpcstotal']) + 0.4 * int(y['projeto']) + 0.4 * int(y['exame']) 
        if int(y['projeto']) < 10 or int(y['exame']) < 10 or nf<10:
            y['notaFinal'] = 'R'
        else:
            y['notaFinal'] = nf

        del y['tpcstotal']
        del y['projeto']
        del y['exame']
        return y

    responses = request_data(query)
    results = responses.json()
    r=getValues(results["results"]["bindings"])
    

    return list(map(x,r))




@app.get("/api/alunos/{id}")
def getAluno(id:str,q: Union[str, None] = None):    
    query=f"""
PREFIX : <http://rpcw.di.uminho.pt/2024/teste/>
select ?nome ?idAluno ?curso
where {{
:{id}    :nome ?nome ;
    :id ?idAluno ;
    :curso ?curso ;
    :projeto ?projeto ;
    :tpc ?tpc ;
    :exame ?exame .
}}
"""
    responses = request_data(query)
    results = responses.json()
    r=getValues(results["results"]["bindings"])
    
    return r[0]

