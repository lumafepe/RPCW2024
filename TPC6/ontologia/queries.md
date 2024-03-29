- Quantos filmes existem no repositorio
```
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select (COUNT(?filme) as ?filmCount) where {
    ?filme a :Film .
}
```
- Qual a distribuição de filmes por ano de lançamento
- Qual a distribuição de filmes por género
```
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?genre (COUNT(?f) as ?number_films) where {
    ?genre a :Genre .
    ?f a :Film.
    ?f :hasGenre ?genre.
} GROUP BY ?genre
```
- Em que filmes participou o ator "Burt Reynolds"
```
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?f where {
    ?f a :Film.
    ?a a :Actor.
    ?a :name "Burt Reynolds".
    ?f :hasActor ?a.
}
```
- Produz uma lista de realizadores o seu nome e o número de filmes que realizou
```
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?nome (COUNT(?f) as ?number_films) where {
    ?director a :Director .
    ?director :name ?nome .
    ?f a :Film.
    ?f :hasDirector ?director.
} GROUP BY ?nome
```
- Quais os titulos dos livros que aparecem associados a filmes
