# Introduction to crossfire

`crossfire` is a package created to give easier access to the datasets of the project [Fogo Cruzado](https://fogocruzado.org.br/), which is a digital collaboration platform to register gun shootings in the metropolitan areas of Rio de Janeiro and Recife.

The package facilitates data extraction from the [project open-data API](https://api.fogocruzado.org.br/), developed by [Volt Data Lab](https://www.voltdata.info/en-lg).

## Installing and loading the package

Currently, the `crossfire` package can be installed directly from its GitHub repository:

```
if (!require("devtools")) install.packages("devtools")
devtools::install_github("voltdatalab/crossfire")
```

Once installed, it can be loaded using the `library` function.

```
library(crossfire)
```

## Functions

`crossfire` has 3 functions: `fogocruzado_signin`, `get_fogocruzado` and `get_cities`. Below, we explain how they can be used.

### fogocruzado_signin

To access Fogo Cruzado's API, [users should be registered](https://api.fogocruzado.org.br/register) and insert their e-mail and password for authentication. `fogocruzado_signin` function registers these information on the current R session, so that it can be used to obtain the Bearer token to extract data using the API. 

As noted, the function sets the e-mail and password in the current R environment. Thus, users should repeat this operation on every new R session in which they intend to use the `crossfire` package. We note that user and password are personal. Therefore, users should be careful when writing and saving them in R scripts, in order to avoid sharing these information.

```
# Registers user and password
fogocruzado_signin(email = "example@account_exeample.com", password = "pass")
```

### get_fogocruzado

`crossfire` main function is `get_fogocruzado`. It allows the extraction from slices to the whole dataset of shootings registered by Fogo Cruzado. The function returns a data frame, in which each line corresponds to a shooting registered and its information. The function has the following arguments: `city`, `initial_date`, `final_date`, `state`, `security_agent` and `source`.

* `city` allows to filter the observations by some cities. Their default returns all observations. The complete list of cities can be found using the `get_cities` function.

```
# Extract data for all registered shootings
fogocruzado_all <- get_fogocruzado()

# Extract data for shootings in the cities of Rio de Janeiro and Recife
fogocruzado_rj_recife <- get_fogocruzado(city = c("Rio de Janeiro", "Recife"))
```

* `initial_date` and `final_date` let users select observations according to a certain period of time. Their default does not set any initial or final date ([however, Fogo Cruzado has been collecting data about Rio de Janeiro's metropolitan area since July 5th, 2016 and Recife's metropolitan area since April 1st, 2018](https://fogocruzado.org.br/perguntas-frequentes/#1553708190396-78173b2a-059c)). Initial and final dates should be included as `character` in the `"YYYY-MM-DD"` format.

```
# Extract all data from 2018
fogocruzado_2018 <- get_fogocruzado(initial_date = "2018-01-01", final_date = "2018-12-31")
```

* `state` let users filter occurences according to the country's state where they happened. Default returns all observations.

```
# Get all data from shootings registered in Pernambuco
fogocruzado_pe <- get_fogocruzado(state = "PE")
```

* `security_agent` allows users to select shootings according to the presence of security agents in the occurrence, assuming the value of `security_agent = 1` when they are present, and `security_agent = 0` - when they're not. 

```
# Extract data from occurents where security agents were present
fogocruzado_security <- get_fogocruzado(security_agent = 1)
```

* `source` let users filter occurences according to the source who reported the shooting: 0 for credible users ([known sources, such as associations or local leaders](https://fogocruzado.org.br/perguntas-frequentes/#1553710609713-711f6233-9412)")), 1 for the press imprensa, and 2 for police authorities.

```
# Get data from shootings reported by the press
fogocruzado_security <- get_fogocruzado(source = 1)
```

### get_cities

`get_cities()` returns a `data.frame` with information about all cities from the Rio de Janeiro and Recife metropolitan areas covered by the Fogo Cruzado initiative.

```
cities <- get_cities()
```
