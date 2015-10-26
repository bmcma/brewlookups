__author__ = 'Brian McMahon'

# connect to BreweryDB to make get and post requests
from secrets import brewerydb_api
import requests

BASE_URL = "http://api.brewerydb.com/v2/"
API_KEY = brewerydb_api
BASE_PARAM = {'key': API_KEY}

""" get request on BreweryDB - example
    test = {'key': api, 'q': 'Mill Street'}
    r = requests.get(uri + "search?", params=test)

    print(r.json())"""


class BreweryDB(object):
    # returns a brewery based on the name
    def get_brewery_by_name(self, name):
        # sets up parameters for request
        # param = {'key': API_KEY, 'q': name}
        BASE_PARAM['q'] = name
        return requests.get(BASE_URL + "search?", params=BASE_PARAM).json()

    # returns a beer based on the name
    def get_beer_by_name(self, name):
        param = {'key': API_KEY, 'name': name}
        return requests.get(BASE_URL + "beers", params=param).json()
        """
        !!!!!!!!!!!!!!need tp find a way to format the json response to extract the data I need. SEE BOTTOM TEST!!!!!!!!!!!!
        r = requests.get(BASE_URL + "beers?", params=param).json()
        for key, value in r.iteritems():
            #if key == name:
                print str(key) + " = " + str(value)

        !!!!!!!!!!!!!!WANT TO QUERY THE JSON RESPONSE AND RETURN THE VALUES I NEED TO DISPLAY TO THE USER!!!!!!!!!!!!!!
                """

    # returns all beer styles
    def get_beer_styles(self):
        #param = {'key': API_KEY}
        return requests.get(BASE_URL + "styles", params=BASE_PARAM).json()

    # returns all ingredients
    def get_ingredients(self):
        return requests.get(BASE_URL + "ingredients", params=BASE_PARAM).json()

    # return ingredients based on ingredientId
    def get_ingredient_by_id(self, id):
        r = requests.get(BASE_URL + "ingredient/" + str(id), params=BASE_PARAM)

        #return requests.get(BASE_URL + "ingredient/" + str(id), params=BASE_PARAM).json()
        # todo revise - this is how you get the individual aspects from json response
        return r.json()['data']['category']


    # TODO set up required methods for each query

    """
    search_brewery(search_term, type):
        values = {'key': api, 'q': search_term, 'type': type}
        r = requests.get(uri + "search?", params=values)
        return r.json
    """
run_test = BreweryDB()
import json
#print(run_test.get_brewery_by_name("mill street"))
#print json.dumps(run_test.get_beer_by_name("Naughty 90"), sort_keys=True, indent=4)
#run_test.get_beer_by_name("Naughty 90")
#print(run_test.get_beer_styles())
#print json.dumps(run_test.get_ingredients(), sort_keys=True, indent=4)
#print json.dumps(run_test.get_ingredient_by_id(1), sort_keys=True, indent=4)
print(run_test.get_ingredient_by_id(1))
