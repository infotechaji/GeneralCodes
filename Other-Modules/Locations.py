# from geograpy import places


# pc = places.PlaceContext(['Cleveland', 'Ohio', 'United States'])

# pc.set_countries()
# print pc.countries #['United States']

# pc.set_regions()
# print pc.regions #['Ohio']

# pc.set_cities()
# print pc.cities #['Cleveland']

# print pc.address_strings #['Cleveland, Ohio, United States']


import pycountry
#text = "United States (New York), United Kingdom (London)"
text = "Ukraine"
#text = "Confluence Networks British Virgin Islands"
#text = "Team Internet AG Germany"
for country in pycountry.countries:
    if country.name in text:
        print(country.name)