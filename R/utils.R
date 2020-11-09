# Get Fogo Cruzado's API from user and password informed in fogocruzado_signin()

fogocruzado_key <- function (){

  key <- Sys.getenv("FOGO_CRUZADO_API_TOKEN")

  if (key == "") {

    stop("There's no key available. Please check your sign-in information.\nIf you haven't included an authorized e-mail and password in this R session yet, please do so using the fogocruzado_signin() function")

    } else

  return(key)

}

# Get token from Fogo Cruzado's API

get_token_fogocruzado <- function(){

  post_fogocruzado <- httr::POST("https://api.fogocruzado.org.br/api/v1/auth/login",
                                 body = list(email = Sys.setenv("email_fogocruzado"),
                                             password = Sys.setenv("password_fogocruzado")))

  post_fogocruzado <- httr::content(post_fogocruzado, as = "text", encoding = "utf8")

  access_fogocruzado <- jsonlite::fromJSON(post_fogocruzado)[[1]]

  accesstoken_fogocruzado <- paste("Bearer", access_fogocruzado)

  if(access_fogocruzado != "Unauthorized"){

    Sys.setenv("FOGO_CRUZADO_API_TOKEN" = accesstoken_fogocruzado)

  } else

    stop("These credentials do not correspond to Fogo Cruzado's records. \nPlease check your e-mail and password or access https://api.fogocruzado.org.br/register to register.")

}

# Extract data from occurrences in Fogo Cruzado's API

extract_data_api <- function(){

  message("\nExtracting data from Fogo Cruzado's API.\n \n...\n")

  fogocruzado_request <- httr::GET("https://api.fogocruzado.org.br/api/v1/occurrences",
                                   httr::add_headers(Authorization = fogocruzado_key()))

  fogocruzado_request_data <- httr::content(fogocruzado_request, as = "text", encoding = "utf8")

  banco <- jsonlite::fromJSON(fogocruzado_request_data)

  return(banco)

}

# Extract data from cities in Fogo Cruzado's API

extract_cities_api <- function(){

  message("\nExtracting data from Fogo Cruzado's API.\n \n...\n")

  fogocruzado_cities <- httr::GET("https://api.fogocruzado.org.br/api/v1/cities",
                                httr::add_headers(Authorization = fogocruzado_key()))

  fogocruzado_request_data <- httr::content(fogocruzado_cities, as = "text", encoding = "utf8")

  banco <- jsonlite::fromJSON(fogocruzado_request_data)

  return(banco)

  }

