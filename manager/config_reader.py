import ConfigParser
import pkg_resources
import ast, json, logging

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

param_name = ["place_name", "wifi_name", "supported_apps"]


class ConfigReader:

    def __init__(self):
        self.config_parser = ConfigParser.ConfigParser()
        self.supported_places = []
        self.all_places = {}
        self.initialize_config_reader()

    def initialize_config_reader(self):
        # Initialize parser
        config_file = pkg_resources.resource_stream(__name__, 'resources/config.ini')
        self.config_parser.readfp(config_file)

        # Get all the supported places with application list
        self.supported_places = ast.literal_eval(self.config_parser.get("supported.items", "supported_places"))
        for place in self.supported_places:
            if not self.config_parser.has_section("supported.places." + place):
                raise PlaceNotSupportedException("Provided place " + place + " does not have detail section")
            self.all_places[place] = {}
            for parameter in param_name:
                self.all_places[place][parameter] = self.config_parser.get("supported.places." + place, parameter)

    def get_supported_apps_for_place(self, place_name):
        if place_name not in self.supported_places and not self.config_parser.has_section("supported.places." + place_name):
            raise PlaceNotSupportedException("Provided place " + place_name + " is not supported ")
        return json.loads(self.config_parser.get("supported.places." + place_name, "supported_apps"))

    def get_place_with_given_network(self, network):
        place_detected = [place for place, data in self.all_places.items() if data["wifi_name"] == network.lower()]
        if len(place_detected) == 1:
            return place_detected[0]
        else:
            return None


class PlaceNotSupportedException(Exception):
    pass