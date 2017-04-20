"""
Author Benjamin Welsh
Library for fetching remote images, including local caching
"""
import urllib.request
import pygame, json
import io
import os
import hashlib
import settings

def fetch_image(image_url, cache=True, cached_name=None):
    """
    Fetches an image from the web.
    Checks and loads a cached image if found
    :param image_url:
    :param cache: whether to load from cache
    :param cached_name: overrides the name of the cached file
    :return:
    """
    if not cached_name:
        cache_hash = hashlib.md5(image_url.encode("utf-8")).hexdigest()
        cache_path="cache/"+cache_hash+".jpg"
    else:
        cache_path="cache/"+cached_name+".jpg"
    # Check for cached image, and load it if found
    if cache and os.path.exists(cache_path):
            print("Loaded cached version of",image_url)
            return pygame.image.load(cache_path)
    elif not settings.CACHED_ONLY:
        image_str = urllib.request.urlopen(image_url).read()
        # create a file object (stream)
        image_file = io.BytesIO(image_str)
        image = pygame.image.load(image_file)
        if cache:
            print("Caching",cache_path)
            pygame.image.save(image,cache_path)
        return image
    else:
        return None
def check_if_cached(name):
    cache_path = "cache/" + name + ".jpg"
    return os.path.exists(cache_path)

def get_web_json(url):
    filename, headers = urllib.request.urlretrieve(url)
    f = open(filename)
    j = json.load(f)
    f.close()
    return j

def fetchLocationImage(country):
    country=country.replace(" ","+")
    if check_if_cached("map_"+country):
        return fetch_image("", cached_name="map_" + country)  # pygame.image.load('images/biology_icon.jpg')
    else:
        geodataUrl="https://maps.googleapis.com/maps/api/geocode/json?&address={}".format(country)
        try:
            countryCoords=get_web_json(geodataUrl)["results"][0]["geometry"]["location"]
        except IndexError as e:
            print(get_web_json(geodataUrl))
            raise
        markerCode="{lat},{lng}".format(**countryCoords)
        #print(markerCode)
        url="https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBOkDGhG5_cTW9iO-KNTliukNSN6uoD_FI&visible=\"{}\"&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&size=320x320&markers=".format(country)+markerCode
        #url="https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBOkDGhG5_cTW9iO-KNTliukNSN6uoD_FI&visible=53.56097399999999,134.7728099|17.9996,73.4994136&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Celement:labels.text%7Cvisibility:off&style=feature:poi.business%7Cvisibility:off&style=feature:road%7Cvisibility:off&style=feature:road%7Celement:labels.icon%7Cvisibility:off&style=feature:transit%7Cvisibility:off&size=180x180"
        return fetch_image(url,cached_name="map_"+country)  #pygame.image.load('images/biology_icon.jpg')

def fetchFlag(cc):
    try:
        return fetch_image("http://flags.fmcdn.net/data/flags/normal/{}.png".format(cc),cached_name="flag_"+cc)
    except urllib.error.HTTPError as e:
        print(e)
        return None #pygame.image.load("images/MISSING_TEXTURE.png")
