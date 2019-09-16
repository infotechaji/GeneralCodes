import geograpy
url = 'http://www.bbc.com/news/world-europe-26919928'
places = geograpy.get_place_context(url=url)

print places.countries
# places.countries contains a list of country names
# places.regions contains a list of region names
# places.cities contains a list of city names
# places.other lists everything that wasn't clearly a country, region or city

print 'places.countries :',places.countries  
print 'places.regions :',places.regions 
print 'places.cities :',places.cities 
print 'places.other :',places.other 

# places.country_regions regions broken down by country
# places.country_cities cities broken down by country
# places.address_strings city, region, country strings useful for geocoding
# Last But Not Least
# While a text might mention many places, it's probably focused on one or two, so Geograpy also breaks down countries, regions and cities by number of mentions.

# places.country_mentions
# places.region_mentions
# places.city_mentions