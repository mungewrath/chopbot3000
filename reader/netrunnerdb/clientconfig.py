import yaml
import os
import logging
logger = logging.getLogger(__name__)


class ClientConfig:
    def __init__(self, config_path="./config/clientconfig.yml"):
        if not os.path.isfile(config_path):
            logger.critical('Unable to load the configuration file')
            raise FileNotFoundError

        with open(config_path, 'r') as yml_file:
            cfg = yaml.safe_load(yml_file)

        self.__server = "{}{}".format(cfg['server']['protocol'],
                              cfg['server']['domain'])
        self.__api_root = "{}{}".format(self.__server, cfg['server']['api_root'])
        self.__get_card = "{}{}".format(self.__api_root, cfg['rest']['get_card'])
        self.__get_cards = "{}{}".format(self.__api_root, cfg['rest']['get_cards'])
        self.__get_card_png = "{}".format(cfg['non_rest']['get_card_png'])
        self.__cache_max_age = cfg['cache']['max_age_in_seconds']

    @property
    def get_card(self):
        return self.__get_card

    @property
    def get_cards(self):
        return self.__get_cards

    @property
    def get_card_png(self):
        return self.__get_card_png

    @property
    def cache_max_age_in_seconds(self):
        return self.__cache_max_age
