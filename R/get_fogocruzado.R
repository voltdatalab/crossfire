#' Extract data from Fogo Cruzado's API of shootings in Brazil.
#'
#' \code{get_fogocruzado()} extracts data from shootings and fire gun shots
#' from Fogo Cruzado's API (\url{https://api.fogocruzado.org.br/}).
#' The function returns a  \code{data.frame} where each observation corresponds
#' to an occurrence.
#'
#' @param city City (\code{character}). Filters observations to certain
#'   cities. Complete names of the cities included in the data can be found
#'   using the \code{\link{get_cities}} function. Default returns occurrences
#'   from all cities in the data repository.
#' @param state State abbreviation in capital letters  (\code{character}).
#'   Filters observations to contain only the selected state. Default returns
#'   occurrences from both states in the data repository. Can assume 2 values:
#'   "RJ" for occurrences in the state of Rio de Janeiro and "PE" for those
#'   of Pernambuco.
#' @param initial_date allows the user to set a initial date to filter
#'   occurrences starting from a certain day. \code{character} in the
#'   "YYYY-MM-DD" format.
#' @param final_date allows the user to set a final date to filter
#'   occurrences up until in a certain day. \code{character} in the
#'   "YYYY-MM-DD" format.
#' @param security_agent Number (\code{integer}) indicating if the user wishes
#'   to filter observations according to the presence of security agents in
#'   the occurrence. Can assume the values of 1 for "yes" and 0 for "no".
#'   Default returns all occurrences.
#'   observations according to the source who reported the occurrence.
#'   Can assume the values of 0 for users, 1 for press and 2 for police.
#'   Default returns all occurrences.
#'
#' @return A \code{data.frame} with the following variables:
#'
#'   \itemize{
#'   \item id_ocorrencia: internal id number of each occurrence.
#'   \item local_ocorrencia: place where the occurrence happened.
#'   \item latitude_ocorrencia: latitude of where the occurrence happened.
#'   \item longitude_ocorrencia: longitude of where the occurrence happened.
#'   \item data_ocorrencia: occurrence's date ("YYYY-MM-DD").
#'   \item hora_ocorrencia: occurrence's time ("HH:MM:SS").
#'   \item presen_agen_segur_ocorrencia: whether there were any security agents
#'     in the occurrence (1 for yes, 0 for no).
#'   \item qtd_morto_civil_ocorrencia: number of civilians killed in the
#'     occurrence.
#'   \item qtd_morto_agen_segur_ocorrencia: number of security agents killed
#'     in the occurrence.
#'   \item qtd_ferido_civil_ocorrencia: number of civilians injured in the
#'     occurrence.
#'   \item qtd_ferido_agen_segur_ocorrencia: number of security agents injured
#'     in the occurrence.
#'   \item fonte_ocorrencia: source who reported the occurrence (0 for users,
#'     1 for press and 2 for police).
#'   \item estado_id: internal id number of the state where the occurrence
#'     happened.
#'   \item cidade_id: internal id number of the city where the occurrence
#'     happened.
#'   \item nome_cidade: city name.
#'   \item cod_ibge_cidade: IBGE's (Brazilian Institute of Geography and
#'     Statistics) code for the city where the occurrence happened.
#'   \item gentilico_cidade: city's gentilic.
#'   \item populacao_cidade: city's population.
#'   \item area_cidade: city's area.
#'   \item densidade_demo_cidade: city's population density.
#'   \item nome_estado: name of the state.
#'   \item uf_estado: abbreviation of the state's name ("RJ" for Rio de Janeiro
#'     and "PE" for Pernambuco).
#'   \item cod_ibge_estado: IBGE's (Brazilian Institute of Geography and
#'     Statistics) code for the state where the occurrence happened.
#'   }
#'
#' @importFrom magrittr %>%
#' @importFrom rlang .data
#'
#' @export
#'
#' @seealso \code{\link{get_cities}} \code{\link{fogocruzado_signin}}
#'
#' @examples
#' # returns a data.frame with all occurrences in the data repository
#'
#' \dontrun{
#' df <- get_fogocruzado()
#' }
#'
#' # returns a data.frame with all occurrences in the city of Belford Roxo
#' # starting in January 1st, 2017 and finishing in December 31st, 2018.
#'
#' \dontrun{
#' df <- get_fogocruzado(city = "Belford Roxo", initial_date = "2017-01-01", final_date = "2018-12-31")
#' }

get_fogocruzado <- function(city = NULL,
                            initial_date = NULL,
                            final_date = NULL,
                            state = c("PE", "RJ"),
                            security_agent = c(0:1),
                            source = c(0:2)
){

  banco <- extract_data_api()

  if(!is.data.frame(banco)) {

    get_token_fogocruzado()

    banco <- extract_data_api()

  } else

  banco$data_ocorrencia <- as.Date(substr(banco$data_ocorrencia, 1, 10))
  banco$cod_ibge_cidade <- as.character(banco$cod_ibge_cidade)
  banco$cod_ibge_estado <- as.character(banco$cod_ibge_estado)
  banco$densidade_demo_cidade <- as.numeric(banco$densidade_demo_cidade)

  if(!is.null(city)){

    banco <- banco %>%
      dplyr::filter(.data$nome_cidade %in% city,
                    .data$uf_estado %in% state,
                    .data$presen_agen_segur_ocorrencia %in% security_agent,
                    .data$fonte_ocorrencia %in% source)

  }

  if(!is.null(initial_date)){

    banco <- banco %>%
      dplyr::filter(.data$data_ocorrencia >= initial_date,
                    .data$uf_estado %in% state,
                    .data$presen_agen_segur_ocorrencia %in% security_agent,
                    .data$fonte_ocorrencia %in% source)

  }

  if(!is.null(final_date)){

    banco <- banco %>%
      dplyr::filter(.data$data_ocorrencia <= final_date,
                    .data$uf_estado %in% state,
                    .data$presen_agen_segur_ocorrencia %in% security_agent,
                    .data$fonte_ocorrencia %in% source)

  } else

    banco <- banco %>%
      dplyr::filter(.data$uf_estado %in% state,
                    .data$presen_agen_segur_ocorrencia %in% security_agent,
                    .data$fonte_ocorrencia %in% source)

  return(banco)
}



