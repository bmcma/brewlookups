__author__ = 'Brian McMahon'

from brewerydb import *
from secrets import brewerydb_api

BASE_URI = "http://api.brewerydb.com/v2"
API_KEY = brewerydb_api


# Contains the beer related classes

"""
=======================================================
Section contains base classes for beer related objects
=======================================================
"""


class Brewery(object):
    """Brewery class containing all the attributes of a brewery and methods for retrieving attributes"""
    name = ''
    brewery_id = ''
    established = ''
    description = ''
    website = ''
    #location = ''

    def __init__(self, name, brewery_id, established, description, website):
        self.name = name
        self.brewery_id = brewery_id
        self.established = established
        self.description = description
        self.website = website
        # self.location = location

    def get_name(self):
        """:return: returns the name of the brewery"""
        return self.name

    def get_brewery_id(self):
        """:return: returns the id of the brewery"""
        return self.brewery_id

    def get_date_established(self):
        """:return: returns the date the brewery was established """
        return self.established

    def get_description(self):
        """:return: returns the description of the brewery"""
        return self.description

    def get_website(self):
        """:return: returns the website for the brewery"""
        return self.website


class Beer(object):
    """Beer class containing all the attributes of a beer and methods for retrieving attributes"""
    name = ''
    beer_id = ''
    abv = ''
    ibu = ''
    style = ''

    def __init__(self, name, beer_id, ibu, abv, style):
        self.name = name
        self.beer_id = beer_id
        self.ibu = ibu
        self.abv = abv
        self.style = style

    def get_name(self):
        """:return: returns the name of the beer"""
        return self.name

    def get_beer_id(self):
        """:return: returns the id of the beer"""
        return self.beer_id

    def get_abv(self):
        """:return: returns the abv of the beer"""
        return self.abv

    def get_ibu(self):
        """:return: returns the ibu of the beer"""
        return self.ibu

    def get_style(self):
        """:return: returns the style of the beer"""
        return self.style


class BeerStyle(object):
    style_id = ''
    name = ''
    description = ''
    ibu_max = ''
    ibu_min = ''
    abv_min = ''
    abv_max = ''

    def __init__(self, style_id, name, description, ibu_max, ibu_min, abv_min, abv_max):
        self.style_id = style_id
        self.name = name
        self.description = description
        self.ibu_max = ibu_max
        self.ibu_min = ibu_min
        self.abv_min = abv_min
        self.abv_max = abv_max

    def get_name(self):
        return self.name

    def get_style_id(self):
        return self.style_id

    def get_description(self):
        return self.description

    def get_ibu_min(self):
        return self.ibu_min

    def get_ibu_max(self):
        return self.ibu_max

    def get_abv_min(self):
        return self.abv_min

    def get_abv_max(self):
        return self.abv_max

    def show_style(self):
        new_line = "\n"
        return self.get_name() + new_line + self.get_description() + new_line + "Min IBU: " + self.get_ibu_min()\
            + new_line + "Max IBU: " + self.get_ibu_max() + new_line + "Min ABV: " +self.get_abv_min() \
            + new_line + "Max ABV " + self.get_abv_max()

    def get_style_by_name(self):
        # can you query for all styles and then search by name??????
        pass


class Ingredients(object):
    id = ''
    name = ''
    type = '' # the category, ie hops

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
"""
=================================================================
Section contains classes for searching and updating the database
=================================================================
"""


class Search(object):
    """
    pass in search terms from search below,
    populate brewery, beer_style etc from results
    pass results to relevant class functions"""

    # configures the BreweryDB wrapper for use as per https://github.com/yarian/brewerydb
    BreweryDb.configure(API_KEY, BASE_URI)

    def search_by_name(self, search_for, query):
        """Queries BreweryDB for breweries/beers based on a search term

        :param search_for: the type of search to perform, ie brewery or beer
        :param query: the query to be searched
        :return: the result of the search

        """

        params = {'type': search_for, 'q': query}
        #TODO REVISIT if else ie if searching for brewery call create_brewery and fill in details + return results
        """search_result = BreweryDb.search(params)
        if search_for == 'beer':
            return self.create_beer(search_result).get_style()
        elif search_for == 'brewery':
            self.create_brewery(query)
        else:
            return "No results found"
            """
        return BreweryDb.search(params)['data']

    def search_brewery_location(self, brewery_id, location):
        #returns location for brewery - good for one brewery but bad if they have multiple locations
        #todo format results to include location details - add to list to be retieved?
        return BreweryDb.brewery(brewery_id + '/' + location)

    def search_all_breweries_by_location(self, location):
        """
        Search for breweries in a certain location and return a list of all breweries

        :param location: the city to be searched
        :return: the list of breweries found at given location

        """

        params = {'locality': location}
        num = 0
        search_results_dict = BreweryDb.locations(params)['data']
        brewery_list = []
        # create brewery object for each result in location and save in a list
        # todo remove try/except and add get method - create brewery method needs to be changed
        for value in search_results_dict:
            try:
                name = value['brewery']['name']
                brewery_id = value['brewery']['id']
                established = value['brewery'].get('established', "unknown")
                description = value['brewery'].get('description', "No description is available at this time")
                website = value['brewery']['website']
            except KeyError, e:
                print e
            # todo is list really necessary???
            brewery = Brewery(name, brewery_id, established, description, website)
            brewery_list.insert(num, brewery)
            num += 1
        return brewery_list

    def print_local_breweries(self, brewery_list):
        """

        Method to print the list of breweries and their key details

        :param brewery_list: the location of the breweries
        :return: prints the output of brewery name, established date, description and website

        """

        for brewery in brewery_list:
            print brewery.get_name() + "\n" + \
                  "Established: " + brewery.get_date_established() + "\n" + \
                  brewery.get_description() + "\n" + brewery.get_website() + "\n"

    def search_brewery(self, name):
        """
        Search all breweries by brewery name - name must be an exact match for the brewery name
        :param name: the name of the brewery to be searched
        :return: returns the matching brewery
        """
        # must be exact name - better to search with search_by_name first
        params = {'name': name}
        return BreweryDb.breweries(params)


    def search_beer_styles(self):
        """

        Method to search for all beer styles and return them

        :return: returns all beer styles

        """
        # query for styleId and then query by the style itself
        # call the get beer styles run through the response to pull up the desired style
        beer_styles = BreweryDb.styles()['data']
        return beer_styles

    def search_style_by_name(self, search_term, beer_styles):
        """
        Method to search for a beer style by name based on user input search value
        :param search_term: the string to search
        :param beer_styles: the available beer_styles returned from search_beer_styles() method
        :return: descriptions of all beer_styles with a search match
        """

        for style in beer_styles:
            if search_term in style['name']:
                beer_style = self.create_beer_style(style)
                print beer_style.show_style()

    def print_all_style_descriptions(self, beer_styles):
        """
        Method to print all beer styles with name and description
        :param beer_styles: The result of calling the method search_beer_styles
        :return:
        """
        new_line = "\n"
        for style in beer_styles:
            beer_style = self.create_beer_style(style)
            print beer_style.get_name() + new_line + beer_style.get_description() + new_line

    def print_full_style_descriptions(self, beer_styles):
        """
        Method to print the full descriptions of beer of all beer styles
        :param beer_styles: results of searching all beer_styles from search_beer_style() method
        :return: the full description of all beer_styles
        """
        for style in beer_styles:
            beer_style = self.create_beer_style(style)
            print beer_style.show_style()

    # todo move to another section - only search queries to be located in Search class
    # todo add .get method to avoid key errors
    def create_beer(self, search_results):
        """
        Creates an instance of a Beer and returns it

        A new beer is created based on the results of the search_by_name() method which extracts data about the beer
        :param search_results: the result of the search_by_name method - searches beer by name
        :return: returns the new beer

        """
        # set the attributes to be passed into the beer based on the first returned result
        style = search_results[0]['style']['name']
        name = search_results[0]['nameDisplay']
        beer_id = search_results[0]['id']
        ibu = search_results[0]['ibu']
        abv = search_results[0]['abv']
        # create the instance of the beer
        beer = Beer(name, beer_id, ibu, abv, style)
        return beer

    def create_brewery(self, search_results):

        """
        Creates an instance of a Brewery and returns it

        A new brewery is created based on the results of the search_by_name() method which extracts data about the brewery
        :param search_results: the result of the search_by_name method - searches brewery by name
        :return: returns the new brewery

        """
        #todo need to do find a way to list the location
        # takes the first result from the list and populates the variables
        name = search_results[0]['name']
        brewery_id = search_results[0]['id']
        established = search_results[0]['established']
        description = search_results[0]['description']
        website = search_results[0]['website']
        # location = ''
        brewery = Brewery(name, brewery_id, established, description, website)
        return brewery

    # todo review the or "" below.
    def create_beer_style(self, beer_style):
        """
        Creates an instance of a Beer style and returns it
        :param beer_style:
        :return:
        """
        name = beer_style.get('name', "Not available")
        style_id = beer_style.get('id', "Not available")
        description = beer_style.get('description', "Not available")
        ibu_min = beer_style.get('ibuMin', "Not available")
        ibu_max = beer_style.get('ibuMax', "Not available")
        abv_min = beer_style.get('abvMin', "Not available")
        abv_max = beer_style.get('abvMax', "Not available")
        # create an instance of BeerStyle
        style = BeerStyle(style_id, name, description, ibu_max, ibu_min, abv_min, abv_max)
        return style


class UpdateDB(object):
    # class to update the BreweryDB with new Beer or Brewery
    # calls on post methods
    pass


class UserInputs(object):
    # class to take user inputs for search terms, database updates etc
    search_term = ''
    # for assign3 take as rawinput in console
    # for web app take as text input in Django form

    def get_user_input(self):
        search_term = raw_input("Enter search term")
        return search_term

s = Search()

"""test search name for brewery/beer"""
#print s.create_beer(s.search_by_name('beer', 'Naughty 90')).get_style()
#print s.create_brewery('mill street').get_website()
#print (s.search_by_name('beer', 'Naughty 90'))

"""test search brewery locations by breweryid"""
#print s.search_brewery_location('KzHweV', 'locations')

"""test search brewery name"""
#print s.search_brewery('mill street brewery')['data'][0]['id']

"""test location search"""
#print (s.search_location('ottawa'))['data'][0]['name']
#s.search_all_breweries_by_location('ottawa')
#s.print_local_breweries(s.search_all_breweries_by_location('ottawa'))

"""test style search"""
#print s.search_beers_by_style()['data'][0]['category']['name']
#s.search_beer_styles()
#s.print_all_styles(s.search_beer_styles())
#s.print_full_style_descriptions(s.search_beer_styles())
s.search_style_by_name('India', s.search_beer_styles())


