#' Retrieve a Fogo Cruzado's API token
#'
#' @description Sets Fogo Cruzado's user and password for the current
#' R session, in order to require a token to use its API. See the details
#' section for more information.
#'
#' @usage fogocruzado_signin(email, password)
#'
#' @param email e-mail which was registered to access Fogo Cruzado's API.
#' @param password password which was registered to access Fogo Cruzado's API.
#'
#' @return Sets "email_fogocruzado", "password_fogocruzado" and
#' "FOGO_CRUZADO_API_TOKEN" as environment variables.
#'
#' @details Fogo Cruzado's API (\url{https://api.fogocruzado.org.br/}) allows easier
#' access to Fogo Cruzado's data from shootings and fire gun shots recorded
#' in Brazil. The API requires a token to be used. This token expires within
#' an hour, after  which it needs to be refreshed. Only registered users can
#' require a token in the API. To register, users should access:
#' \url{https://api.fogocruzado.org.br/register}.
#'
#' Once users are registered and have authorized access, they need to request
#' a token to extract data using the API. This can be done using
#' \code{fogocruzado_signin} function. Fogo Cruzado uses a JWT
#' authentication standard to grant users access to the API.
#'
#' \code{fogocruzado_signin} function sets the API user (e-mail) and password
#' only for the current R session. However, since the user and password are
#' personal and private, we recommend a careful use of this function in
#' R script files, so that users do not share these information.
#'
#' @export
#'
#' @author The function design was inspired by the \code{register_google()}
#' function, from the \code{ggmap} package.
#'
#' @examples
#'
#' # this sets your email and password for the current session and retrieves a
#' # Bearer token that lasts for 1 hour. If the current token is expired, this
#' # function uses the information previously set to retrieve a new one.
#'
#' \dontrun{
#' fogocruzado_signin(email = "example@@email.com", password = "yourpassword")
#' }
#'

fogocruzado_signin <- function(email,
                            password){

  Sys.setenv("FOGO_CRUZADO_EMAIL" = email,
             "FOGO_CRUZADO_PASSWORD" = password)

  get_token_fogocruzado()

}





