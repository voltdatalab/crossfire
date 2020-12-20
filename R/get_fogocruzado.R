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
#' @param initial_date initial date to filter occurrences starting from a certain day.
#'   \code{character} in the "YYYY-MM-DD" format. Default is set to six months from
#'   the current date. The difference betweet the final and the initial dates
#'   cannot be longer than 210 days (roughly 7 months).
#' @param final_date final date to filter occurrences up until in a certain day.
#'   \code{character} in the "YYYY-MM-DD" format. Default is set for the current day
#'   \code{Sys.Date()}. The difference betweet the final and the initial dates
#'   cannot be longer than 210 days (roughly 7 months).
#' @param security_agent Number (\code{integer}) indicating if the user wishes
#'   to filter observations according to the presence of security agents in
#'   the occurrence. Can assume the values of 1 for "yes" and 0 for "no".
#'   Default returns all occurrences.
#'
#' @return A \code{data.frame} with 67 columns. They are described \href{https://github.com/voltdatalab/crossfire/blob/master/tables/list_columns.md}{in English}
#' and \href{https://github.com/voltdatalab/crossfire/blob/master/tables/lista_colunas.md}{in Portuguese}.
#'
#' @importFrom magrittr %>%
#' @importFrom rlang .data
#'
#' @export
#'
#' @seealso \code{\link{get_cities}} \code{\link{fogocruzado_signin}}
#'
#' @examples
#' # returns a data.frame with all occurrences in the data repository over the last 210 days
#'
#' \dontrun{
#' df <- get_fogocruzado()
#' }
#'
#' # returns a data.frame with all occurrences in the city of Belford Roxo
#' # starting in January 1st, 2017 and finishing in June 30th, 2018.
#'
#' \dontrun{
#' df <- get_fogocruzado(city = "Belford Roxo", initial_date = "2017-01-01", final_date = "2018-06-31")
#' }

get_fogocruzado <- function(city = NULL,
                            initial_date = Sys.Date()-months(6),
                            final_date = Sys.Date(),
                            state = c("PE", "RJ"),
                            security_agent = c(0:1)){

  lifecycle::deprecate_warn("0.2.0", "crossfire::get_fogocruzado(source = )")
  lifecycle::deprecate_warn("0.2.0", "crossfire::get_fogocruzado(initial_date = 'must be within 210 days from final_date')")

  if(as.Date(final_date) - as.Date(initial_date) >= months(7)){

    stop("The interval between the initial and final date cannot be longer than 210 days (7 months). Please check your inputs.")

  } else

  banco <- extract_data_api(paste0("https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]=",
                                    initial_date, "&data_ocorrencia[lt]=", final_date))

  if(!is.data.frame(banco)) {

    get_token_fogocruzado()

    message("Renovating token...")

    banco <- extract_data_api(paste0("https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]=",
                                     initial_date, "&data_ocorrencia[lt]=", final_date))

  } else

  banco$cod_ibge_cidade <- as.character(banco$cod_ibge_cidade)
  banco$cod_ibge_estado <- as.character(banco$cod_ibge_estado)
  banco$densidade_demo_cidade <- as.numeric(banco$densidade_demo_cidade)

  if(!is.null(city)){

    banco <- banco %>%
      dplyr::filter(.data$nome_cidade %in% city,
                    .data$uf_estado %in% state,
                    .data$presen_agen_segur_ocorrencia %in% security_agent)

  } else

    banco <- banco %>%
      dplyr::filter(.data$uf_estado %in% state,
                    .data$presen_agen_segur_ocorrencia %in% security_agent)

  return(banco)
}



