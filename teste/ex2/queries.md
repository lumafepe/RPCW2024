# 1
```
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

SELECT ?id ?nome ?pop ?desc ?dist
WHERE {
  ?cidade a :Cidade;
	:id ?id;
	:nome ?nome;
	:população ?pop;
	:descrição ?desc;
	:temDistrito/:nome ?dist ;
    :nome ?nome .
}
ORDER BY ?nome
```
# 2
```
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

SELECT ?nome (COUNT(?cidade) AS ?numeroDeCidades)
WHERE {
  ?cidade a :Cidade.
  ?distrito a :Distrito.
  ?cidade :temDistrito ?distrito.
  ?distrito :nome ?nome.
}
GROUP BY ?nome
ORDER BY ?nome
```
# 3
```
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

SELECT ?desNome ?oriNome
WHERE {
  ?lig a :Ligação.
  ?lig :destino ?des.
  ?lig :origem ?ori.
  ?des :nome ?desNome.
  ?ori :nome ?oriNome.
  FILTER(?desNome = "Braga" || ?oriNome = "Braga")
}
```
# 4
```
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

SELECT DISTINCT ?desNome
WHERE {
  ?lig a :Ligação.
  ?lig :origem ?ori.
  ?ori :nome "Braga".
  ?lig (:destino/^:origem)* ?ligações.
  ?ligações :destino/:nome ?desNome.
}
ORDER BY ?desNome
```
# 5
```
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

CONSTRUCT {
  :ligacao a :Ligação;
            :origem ?ori;
            :destino ?des.
}
WHERE {
  ?lig a :Ligação.
  ?lig :origem ?ori.
  ?ori :nome "Braga".
  ?lig (:destino/^:origem)* ?ligações.
  ?ligações :destino ?des.
}
```
# 6
```
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

CONSTRUCT {
  :ligacao a :Ligação;
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
```