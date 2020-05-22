import enum
import logging

from anisub.processors import SubtitlesProcessor
from anisub.providers import AnimeInformationProvider


class NameOrder(enum.Enum):
    eastern = 0
    western = 1

    def __str__(self):
        return self.name


class NameOrderProcessor(SubtitlesProcessor):

    def __init__(self, anime_information_provider: AnimeInformationProvider,
                 preferred_name_order: NameOrder = NameOrder.eastern):
        self.anime_information_provider = anime_information_provider
        self.preferred_name_order = preferred_name_order
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, text: str, anime_name: str):
        names = self.anime_information_provider.anime_to_characters_names(anime_name)

        for name in names:
            from_name = name.western_order if self.preferred_name_order == NameOrder.eastern else name.eastern_order
            to_name = name.eastern_order if self.preferred_name_order == NameOrder.eastern else name.western_order
            updated_text = text.replace(from_name, to_name)
            if text != updated_text:
                self.logger.debug('Changed: {} to {}', from_name, to_name)
            text = updated_text
        return text
