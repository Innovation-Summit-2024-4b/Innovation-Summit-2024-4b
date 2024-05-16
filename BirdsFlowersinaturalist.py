import os
import requests
from pyinaturalist import get_taxa, get_observations


# Function to create a directory to save images
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to download and save images
def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)


# Function to scrape images of a given taxon (species)
def scrape_images(taxon_name):
    # Search for the taxon by name
    taxa = get_taxa(q=taxon_name)
    if not taxa['results']:
        print(f"No taxa found for '{taxon_name}'")
        return

    # Get the taxon ID
    taxon_id = taxa['results'][0]['id']

    # Get observations for the taxon
    observations = get_observations(taxon_id=taxon_id)

    # Directory to save images
    directory = f'inat_images_{taxon_name.replace(" ", "_")}'
    create_directory(directory)

    # Loop through each observation and download the images
    for obs in observations['results']:
        for photo in obs['photos']:
            image_url = photo['url'].replace('square', 'large')
            file_extension = image_url.split('.')[-1]
            filename = f"{obs['id']}_{photo['id']}.{file_extension}"
            save_path = os.path.join(directory, filename)

            # Download and save the image
            download_image(image_url, save_path)
            print(f"Downloaded {filename}")


# Run the scraper
taxon_name = 'Calypte anna'
scrape_images(taxon_name)
