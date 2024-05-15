
# Install necessary packages if not already installed
if (!require("httr")) install.packages("httr")
if (!require("jsonlite")) install.packages("jsonlite")
get_inat_photos_url <- function(species_name) {
  api_url <- sprintf("https://api.inaturalist.org/v1/taxa?q=%s", URLencode(species_name))
  
  response <- httr::GET(api_url)
  
  if (response$status_code == 200) {
    data <- httr::content(response, "parsed")
    
    if (length(data$results) > 0) {
      species_id <- data$results[[1]]$id
      species_name_url <- gsub(" ", "-", species_name)
      url <- sprintf("https://www.inaturalist.org/taxa/%s-%s/browse_photos", species_id, species_name_url)
      return(url)
    } else {
      return("No results found for the given species name.")
    }
  } else {
    return("Failed to fetch data from iNaturalist API.")
  }
}

url <- get_inat_photos_url("Andira inermis")
print(url)
