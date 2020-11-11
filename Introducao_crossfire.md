# Introdução ao crossfire

O `crossfire` é um pacote criado para facilitar a utilização do banco de dados do projeto [Fogo Cruzado](https://fogocruzado.org.br/), "[uma plataforma digital colaborativa que tem o objetivo de registrar a incidência de tiroteios e a prevalência de violência armada na região metropolitana do Rio de Janeiro e de Recife](https://fogocruzado.org.br/perguntas-frequentes/#1553708190395-3a432702-4810)".

O pacote facilita a extração de dados da [API de dados abertos desse repositório](https://api.fogocruzado.org.br/), desenvolvida pelo [Volt Data Lab](https://www.voltdata.info/).

## Instalando e carregando o pacote

No momento, o pacote `crossfire` pode ser instalado diretamente da sua página no github:

```
if (!require("devtools")) install.packages("devtools")
devtools::install_github("voltdatalab/crossfire")
```

Assim como os demais pacotes em R, uma vez instalado, ele deve ser carregado com a função `library()`.

```
library(crossfire)
```

## Funções

O pacote `crossfire` possui 3 funções: `fogocruzado_signin`, `get_fogocruzado` e `get_cities`. A seguir, explicamos o funcionamento de cada uma delas.

### fogocruzado_signin

Para acessar a API do Fogo Cruzado, os [usuários devem ser registrados](https://api.fogocruzado.org.br/register) e usar o seu e-mail e senha. A função `fogocruzado_signin` realiza a inserção do usuário e senha, para que seja possível obter o Bearer token necessário para extração dos dados da API. 

A função registra o e-mail e senha no ambiente do R para a sessão atual, sendo necessário que o usuário repita essa operação a cada nova sessão em que pretenda utilizar o pacote `crossfire`. Lembramos que a senha para utilização da API é pessoal e intransferível. Portanto, os usuários devem ter cuidado ao registrá-la em scripts, para evitar seu compartilhamento.

```
# Registra usuario e senha
fogocruzado_signin(email = "exemplo@conta_exemplo.com", password = "senha")
```

### get_fogocruzado

A principal função do `crossfire` é a `get_fogocruzado`, que permite extrair recortes dos registros de tiroteios compilados pelo Fogo Cruzado. Ela retorna um banco de dados (`data.frame`) que traz em cada linha um registro e 67 colunas de informações sobre esta ocorrência. A função possui os seguintes argumentos: `city`, `initial_date`, `final_date`, `state` e `security_agent`.

* O argumento `city` (cidade) permite filtrar os registros por algumas cidades. O padrão desse argumento retorna as ocorrências em todas as cidades. A lista completa de cidades (com a grafia de seus nomes) pode ser obtida usando a função `get_cities`.

```
# Extrai os dados para todos os registros do repositorio de dados
fogocruzado_all <- get_fogocruzado()

# Extrai os dados para todos os registros nas cidades do Rio de Janeiro e Recife
fogocruzado_rj_recife <- get_fogocruzado(city = c("Rio de Janeiro", "Recife"))
```

* Os argumentos `initial_date` (data inicial) e `final_date` (data final) permitem filtrar as observações segundo a data inicial e a data final da ocorrência, sendo que o padrão da função é o dia da consulta como data final, e seis meses antes como data inicial. Na nova versão da API, limitamos as consultas do pacote a um período máximo de 210 dias (cerca de 7 meses), que podem abranger qualquer período disponibilizado. [O Fogo Cruzado coleta dados sobre região metropolitana do Rio de Janeiro desde 05 de julho de 2016 e do Recife desde 01 de abril de 2018](https://fogocruzado.org.br/perguntas-frequentes/#1553708190396-78173b2a-059c). As datas devem ser incluídas como `character` no formato `"YYYY-MM-DD"` (Ano-Mês-Dia).

```
# Extrai todos os registros do ano de 2018
fogocruzado_2018 <- get_fogocruzado(initial_date = "2018-07-01", final_date = "2018-12-31")
```

* O argumento `state` possibilita selecionar os registros segundo o estado em que ocorreram. O padrão retorna todas as ocorrências.

```
# Obtem dados de ocorrencias em cidades de Pernambuco
fogocruzado_pe <- get_fogocruzado(state = "PE")
```

* Por fim, o argumento `security_agent` possibilita a seleção das ocorrências segundo a presença - `security_agent = 1` - ou não - `security_agent = 0` - das forças de segurança. 

```
# Extrai os dados de todas as ocorrencias com presenca de agentes de seguranca
fogocruzado_security <- get_fogocruzado(security_agent = 1)
```

### get_cities

A função `get_cities()` retorna um `data.frame` com informações sobre todas as cidades das regiões metropolitanas e do Rio de Janeiro e do Recife cobertas pela iniciativa.

```
cidades <- get_cities()
```

