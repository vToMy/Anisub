import logging

from jikanpy import Jikan

from anisub.models.name import Name
from anisub.providers import AnimeInformationProvider


class MyAnimeList(AnimeInformationProvider):

    def __init__(self):
        self.jikan = Jikan()
        self.logger = logging.getLogger(self.__class__.__name__)

    def anime_to_characters_names(self, anime_name: str):
        animes = self.jikan.search('anime', anime_name)['results']
        if not animes:
            raise Exception('Could not find anime: {}'.format(anime_name))
        anime = animes[0]
        anime_title = anime['title']
        self.logger.debug('Found anime: %s.', anime_title)

        characters = self.jikan.anime(anime['mal_id'], extension='characters_staff')['characters']
        self.logger.debug('Found %s characters for the anime: %s.', len(characters), anime_title)
        names = []
        for character in characters:
            full_name = character['name']
            name_parts = full_name.split(',')
            if len(name_parts) == 2:
                last_name = name_parts[0]
                first_name = name_parts[1]
                names.append(Name(last_name=last_name, first_name=first_name))
        return names
