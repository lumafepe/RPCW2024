from flask import Flask,render_template,url_for
from datetime import datetime
import requests

app = Flask(__name__)
# data do sistema no formato ISO
curr_ISO_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


#GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/Tabelaperiodica"


def get_from_db(query):
    return requests.get(graphdb_endpoint,
                            params={"query":query},
                            headers={"Accept":"application/sparql-results+json"}
    )



@app.route("/")
def index():
    return render_template("index.html",data={
        "date":curr_ISO_date
    })
    
@app.route("/elemento/<int:atomicNumber>")
def element(atomicNumber):
    sparql_query=f"""
PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select * where {{
	?s a tp:Element ;
    tp:atomicNumber {atomicNumber} ;
   	tp:block ?block ;
    tp:classification ?classification ;
    tp:group ?group ;
    tp:period ?period ;
    tp:standardState ?standardState ;
    tp:atomicWeight ?atomicWeight ;
    tp:casRegistryID ?casRegistryID ;
    tp:color ?color ;
    tp:name ?name ;
    tp:symbol ?symbol .
}}
"""
    response = get_from_db(sparql_query)
    if response.status_code == 200:
        data = response.json()['results']['bindings']
        return render_template("element.html",data={
            "element": data[0],
            "date":curr_ISO_date,
            "element_id": atomicNumber
        })
    else:
        return render_template("empty.html",data={"date":curr_ISO_date})
    

@app.route("/elementos")
def elements():
    sparql_query="""
PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select * where {
	?s a tp:Element ;
   	tp:symbol  ?symbol ;
    tp:name  ?name ;
    tp:atomicNumber ?atomicNumber ;
    tp:group ?group 
} order by ?atomicNumber
"""
    response = get_from_db(sparql_query)
    if response.status_code == 200:
        data = response.json()['results']['bindings']
        print(data[0])
        return render_template("elements.html",data={
            "elements": data,
            "date":curr_ISO_date
        })
    else:
        return render_template("empty.html",data={"date":curr_ISO_date})
    
@app.route("/grupo/<string:id>",endpoint='grupo')
def groups(id):
    sparql_query=f"""
PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select * where {{
	tp:group_{id} a tp:Group .
    optional {{ tp:group_{id} tp:number ?number }}.
    optional {{ tp:group_{id} tp:name ?name }}.
    optional {{ tp:group_{id} (tp:element/tp:atomicNumber) ?element }}.
}} 
"""
    response = get_from_db(sparql_query)
    if response.status_code == 200:
        data = response.json()['results']['bindings']
        clean_data = data[0]
        clean_data['element'] = [clean_data['element']]
        for i in data[1:]:
            clean_data['element'].append(i['element'])
        return render_template("group.html",data={
            "group": clean_data,
            "date":curr_ISO_date,
            "group_id": id
        })
    else:
        return render_template("empty.html",data={"date":curr_ISO_date})
    
@app.route("/grupos",endpoint='grupos')
def groups():
    sparql_query="""
PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select * where {
	?s a tp:Group .
    optional { ?s tp:number ?number }.
    optional { ?s tp:name ?name }.
} 
"""
    response = get_from_db(sparql_query)
    print(response)
    if response.status_code == 200:
        data = response.json()['results']['bindings']
        print(data[0])
        return render_template("groups.html",data={
            "groups": data,
            "date":curr_ISO_date
        })
    else:
        return render_template("empty.html",data={"date":curr_ISO_date})
    
    
if __name__ == "__main__":
    app.run(debug=True)