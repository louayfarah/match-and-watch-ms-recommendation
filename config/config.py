from dotenv import load_dotenv
from pyaml_env import parse_config
from patterns import Singleton


load_dotenv()


class Config(metaclass=Singleton):
    def __init__(self) -> None:
        """
        Constructor of the class
        """
        try:
            self.conf = parse_config("config.yml", tag=None, default_value=None)
        except FileNotFoundError:
            print("Warning: Configuration file was not found, hence not parsed!")

    def get_database_connection_string(self):
        return self.conf["db"]["postgres"]["url"]

    def get_tmdb_token(self):
        return self.conf["tmdb"]["token"]

    def get_movieglu_client(self):
        return self.conf["movieglu"]["client"]

    def get_movieglu_api_key(self):
        return self.conf["movieglu"]["api_key"]

    def get_movieglu_authorization(self):
        return self.conf["movieglu"]["authorization"]

    def get_movieglu_territory(self):
        return self.conf["movieglu"]["territory"]

    def get_movieglu_api_version(self):
        return self.conf["movieglu"]["api_version"]

    def get_movieglu_geolocation(self):
        return self.conf["movieglu"]["geolocation"]
    
    def get_user_microservice_url(self):
        return self.conf["user_microservice"]["url"]
    
    def get_database_connection_string(self):
        return self.conf["db"]["postgres"]["url"]
