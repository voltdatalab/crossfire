#' Cities contained in Fogo Cruzado's API.
#'
#' \code{get_cities()} extracts data about cities covered by Fogo Cruzado's
#' project, from its API (\url{https://api.fogocruzado.org.br/}). The function
#' returns a \code{data.frame} where each observation corresponds to a city.
#'
#' @return A \code{data.frame} with the following variables:
#'
#'   \itemize{
#'   \item CidadeId: internal id number of the city where the occurrence
#'     happened.
#'   \item EstadoId: internal id number of the state where the occurrence
#'     happened.
#'   \item Cidade: city's name.
#'   \item CodigoIBGE: IBGE's (Brazilian Institute of Geography and
#'     Statistics) code for the city where the occurrence happened.
#'   \item Gentilico: city's gentilic.
#'   \item Populacao: city's population.
#'   \item Area: city's area.
#'   \item DensidadeDemografica: city's population density.
#'   \item PIBPrecoCorrente: city's gross domestic product.
#'   }
#'
#' @importFrom magrittr %>%
#' @importFrom rlang .data
#'
#' @export
#'
#' @seealso \code{\link{get_fogocruzado}} \code{\link{fogocruzado_signin}}
#'
#' @examples
#' # returns a data.frame with all cities contained in the data repository
#'
#' \dontrun{
#' cities <- get_cities()
#' }

get_cities <- function(){

  banco <- extract_cities_api()

  if(!is.data.frame(banco)) {

    fogocruzado_signin()

    banco <- extract_cities_api()

    banco$DensidadeDemografica <- as.numeric(banco$DensidadeDemografica)

  } else

  banco$DensidadeDemografica <- as.numeric(banco$DensidadeDemografica)

  return(banco)
}
