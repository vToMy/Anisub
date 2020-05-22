import re
from pathlib import Path
from typing import Pattern

from anisub.detectors import AnimeDetector


class FileNameDetector(AnimeDetector):

    DEFAULT_PATTERN = re.compile(r'\[.*?](.+?)\d{2,}')

    def __init__(self, pattern: Pattern = DEFAULT_PATTERN):
        self.pattern = pattern

    def get_anime_name(self, file_path: Path):
        match = self.pattern.match(file_path.name)
        if match:
            anime_name = match.group(1)
            anime_name = anime_name.replace('_', '').replace('-', '').strip()
            return anime_name
        raise Exception('Could not determine anime name from file name: {}'.format(file_path.name))
