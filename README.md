
<img src="https://raw.githubusercontent.com/voltdatalab/crossfire/master/crossfire_hexagono.png" width="130px" alt="hexagon crossfire"/>


# crossfire

`crossfire` is a package created to give easier access to the datasets of the project [Fogo Cruzado](https://fogocruzado.org.br/), which is a digital collaboration platform to register gun shootings in the metropolitan areas of Rio de Janeiro and Recife.

The package facilitates data extraction from the [project open-data API](https://api.fogocruzado.org.br/), developed by [Volt Data Lab](https://www.voltdata.info/en-lg).

**Please note that as of Nov. 2020, due to changes in Fogo Cruzado's API, user's should update `crossfire` to its' `0.2.0` version**. The `get_fogocruzado()` function from the `0.1.0` version returns errors and cannot be used.

## Installing and loading the package

Currently, the `crossfire` package can be installed directly from its GitHub repository:

```
if (!require("devtools")) install.packages("devtools")
devtools::install_github("voltdatalab/crossfire")

library(crossfire)
```

## Functions

`crossfire` has 3 functions: `fogocruzado_signin`, `get_fogocruzado` and `get_cities`.

* `fogocruzado_signin` is used to give access to Fogo Cruzado's API. To access Fogo Cruzado's API, [users should be registered](https://api.fogocruzado.org.br/register) and insert their e-mail and password for authentication. Thus, the function registers these information on the current R session, so that it can be used to obtain the Bearer token to extract data using the API. 

* `get_fogocruzado` extracts slices or the whole dataset of shootings registered by Fogo Cruzado. The function returns a data frame, in which each line corresponds to a shooting registered and its information. It can also filter the data according to some parameters,  city/state - `city` and `state` -, initial and final date - `initial_date` and `final_date` -, and the presence of security forces - `security_agent`. One should note that each request using the `crossfire` package needs to be under a 210 days (roughly 7 months) time interval, from any portion of the full dataset.

```
# Extract data for all registered shootings
fogocruzado_all <- get_fogocruzado()

# Extract data for shootings in the cities of Rio de Janeiro and Recife in 2018
fogocruzado_rj_recife <- get_fogocruzado(city = c("Rio de Janeiro", "Recife"),
                                         initial_date = "2018-07-01", final_date = "2018-12-31")

# Extract data from occurents reported by the police and in which security agents were present
fogocruzado_security <- get_fogocruzado(security_agent = 1, source = 2)
```

* `get_cities()` returns a `data.frame` with information about all cities from the Rio de Janeiro and Recife metropolitan areas covered by the Fogo Cruzado initiative.

## More information

For more information on how the package works and for a complete list of functions, see:  
* the vignettes (in [English](https://github.com/voltdatalab/crossfire/blob/master/Introduction_crossfire.md) and [Portuguese](https://github.com/voltdatalab/crossfire/blob/master/Introducao_crossfire.md)), if using R package;
* the [tutorials](https://github.com/FelipeSBarros/crossfire_tutorial) using python module;

## Authors

[Lucas Gelape](https://github.com/lgelape), for [Volt Data Lab](https://www.voltdata.info/en-lg).

## Contributors

[Sérgio Spagnuolo](https://github.com/voltdatalab) and [Denisson Silva](https://github.com/silvadenisson).
