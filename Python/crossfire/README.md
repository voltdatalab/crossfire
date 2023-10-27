
<img src="https://raw.githubusercontent.com/voltdatalab/crossfire/master/crossfire_hexagono.png" width="130px" alt="hexagon crossfire"/>


# crossfire

`crossfire` is a package created to give easier access to the datasets of the project [Fogo Cruzado](https://fogocruzado.org.br/), which is a digital collaboration platform to register gun shootings in the metropolitan areas of Rio de Janeiro and Recife.

The package facilitates data extraction from the [project open-data API](https://api.fogocruzado.org.br/), developed by [Volt Data Lab](https://www.voltdata.info/en-lg).

## Installing and loading the package

Currently, the `crossfire` package can be installed directly from pip:

```
pip install crossfire
```

## Functions

`crossfire` has 3 functions: `fogocruzado_signin`, `get_fogocruzado` and `get_cities`.

* `fogocruzado_signin` is used to give access to Fogo Cruzado's API. To access Fogo Cruzado's API, [users should be registered](https://api.fogocruzado.org.br/register) and insert their e-mail and password for authentication. Thus, the function registers these information on the current R session, so that it can be used to obtain the Bearer token to extract data using the API. 


```
>>> from crossfire import fogocruzado_signin
>>> fogocruzado_signin('user@host.com', 'password')
```

* `get_fogocruzado` extracts slices or the whole dataset of shootings registered by Fogo Cruzado. The function returns a data frame, in which each line corresponds to a shooting registered and its information. It can also filter the data according to some parameters,  city/state - `city` and `state` -, initial and final date - `initial_date` and `final_date` -, and the presence of security forces - `security_agent`. One should note that each request using the `crossfire` package needs to be under a 210 days (roughly 7 months) time interval, from any portion of the full dataset.

```
>>> from crossfire import get_fogocruzado
>>> fogocruzado = get_fogocruzado(state=['RJ'])
```

## Other examples

```
from datetime import date
from crossfire import fogocruzado_signin, get_fogocruzado

# Extract data for all registered shootings
fogocruzado = get_fogocruzado(()

# Extract data for shootings in the cities of Rio de Janeiro and Recife in 2018
fogocruzado_rj_recife = get_fogocruzado(
    city = ["Rio de Janeiro, "Recife"],
    initial_date = date(2018, 07, 01),
    final_date = date(2018, 12, 31))

# Extract data from occurents reported by the police and in which security agents were present
fogocruzado_security = get_fogocruzado(security_agent = [1])
```

* `get_cities()` returns a `data.frame` with information about all cities from the Rio de Janeiro and Recife metropolitan areas covered by the Fogo Cruzado initiative.

## More information

For more information on how the package works and for a complete list of functions, see the tutorials (in [English](https://github.com/voltdatalab/crossfire/blob/master/Introduction_crossfire.md) and [Portuguese](https://github.com/voltdatalab/crossfire/blob/master/Introducao_crossfire.md)).

## Python module authors

[Felipe Sodré Mendes Barros](https://github.com/FelipeSBarros)
> Funding: This implementation was funded by CYTED project number 520RT0010. redGeoLIBERO

## API Authors

[Lucas Gelape](https://github.com/lgelape), for [Volt Data Lab](https://www.voltdata.info/en-lg).

## Contributors

[Sérgio Spagnuolo](https://github.com/voltdatalab) and [Denisson Silva](https://github.com/silvadenisson).
