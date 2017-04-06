"""
Author Benjamin Welsh
Library for fetching remote images, including local caching
"""
import urllib.request
import pygame, json
import io
import os
import hashlib

def fetch_image(image_url, cache=True):
    cache_hash = hashlib.md5(image_url.encode("utf-8")).hexdigest()
    cache_path="cache/"+cache_hash+".jpg"
    # Check for cached image, and load it if found
    if cache and os.path.exists(cache_path):
            print("Loaded cached version of",image_url)
            return pygame.image.load(cache_path)
    image_str = urllib.request.urlopen(image_url).read()
    # create a file object (stream)
    image_file = io.BytesIO(image_str)
    image = pygame.image.load(image_file)
    if cache:
        pygame.image.save(image,cache_path)
    return image

def get_web_json(url):
    filename, headers = urllib.request.urlretrieve(url)
    f = open(filename)
    j = json.load(f)
    f.close()
    return j

def fetchLocationImage(country):
    country=country.replace(" ","+")
    geodataUrl="https://maps.googleapis.com/maps/api/geocode/json?&address={}".format(country)
    countryCoords=get_web_json(geodataUrl)["results"][0]["geometry"]["location"]
    markerCode="{lat},{lng}".format(**countryCoords)
    print(markerCode)
    url="https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBOkDGhG5_cTW9iO-KNTliukNSN6uoD_FI&visible=\"{}\"&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&size=320x320&markers=".format(country)+markerCode
    #url="https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBOkDGhG5_cTW9iO-KNTliukNSN6uoD_FI&visible=53.56097399999999,134.7728099|17.9996,73.4994136&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Celement:labels.text%7Cvisibility:off&style=feature:poi.business%7Cvisibility:off&style=feature:road%7Cvisibility:off&style=feature:road%7Celement:labels.icon%7Cvisibility:off&style=feature:transit%7Cvisibility:off&size=180x180"
    return fetch_image(url)  #pygame.image.load('images/biology_icon.jpg')

def fetchFlag(cc):
    try:
        return fetch_image("http://flags.fmcdn.net/data/flags/normal/{}.png".format(cc))
    except urllib.error.HTTPError as e:
        print(e)
        return None #pygame.image.load("images/MISSING_TEXTURE.png")