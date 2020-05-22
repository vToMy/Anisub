import logging
from pathlib import Path
from typing import List

from gooey import Gooey, GooeyParser

from anisub.detectors import AnimeDetector
from anisub.detectors.file_name_detector import FileNameDetector
from anisub.models.video_files.mkv_video_file import MkvVideoFile, MKVTOOLNIX_DOWNLOAD_URL
from anisub.processors import SubtitlesProcessor
from anisub.processors.name_order_processor import NameOrderProcessor, NameOrder
from anisub.providers import AnimeInformationProvider
from anisub.providers.my_anime_list import MyAnimeList


class Main:
    ENGLISH_LANGUAGE = ('english', 'eng', 'en')

    def __init__(self,
                 anime_information_provider: AnimeInformationProvider = MyAnimeList(),
                 detector: AnimeDetector = FileNameDetector(),
                 processors: List[SubtitlesProcessor] = None,
                 language=ENGLISH_LANGUAGE):
        self.anime_information_provider = anime_information_provider
        self.detector = detector
        self.processors = processors
        if self.processors is None:
            self.processors = []
        self.language = tuple(language)
        self.logger = logging.getLogger(self.__class__.__name__)

    def main(self, input_path: Path, output_path: Path = None, name_order: NameOrder = None, anime_name: str = None,
             mkvtoolnix_path: Path = None):
        self.logger.info('Reading: %s.', input_path.name)
        file = MkvVideoFile(input_path, mkvtoolnix_path)
        subtitles_text = file.get_subtitles_text(self.language)
        if not anime_name:
            anime_name = self.detector.get_anime_name(input_path)

        updated_subtitles_text = subtitles_text
        if name_order is not None:
            self.processors.append(NameOrderProcessor(self.anime_information_provider))
        for processor in self.processors:
            updated_subtitles_text = processor.process(updated_subtitles_text, anime_name)

        if updated_subtitles_text == subtitles_text:
            self.logger.debug('No changes needed for subtitles for %s.', input_path.name)
            return

        file.add_subtitles(updated_subtitles_text, self.language)


@Gooey(program_name='Anime subtitles fixer')
def parse_args():
    parser = GooeyParser(description='Process anime subtitles.')
    io_group = parser.add_argument_group('Input/Output', 'Choose input and output paths.')
    io_group.add_argument('input', metavar='Input path', help='Input file path', widget='FileChooser')
    io_group.add_argument('--output', metavar='Output path',
                          help='Output file path (leave empty for autogenerated file name)',
                          required=False, widget='FileChooser')

    processing_group = parser.add_argument_group('Processing Options')
    processing_group.add_argument('--anime-name', metavar='Anime name', help='Leave empty to autodetect',
                                  required=False)
    processing_group.add_argument('--name-order', metavar='Name Order', help='Choose eastern/western name order',
                                  dest='name_order', choices=[NameOrder.western, NameOrder.eastern], required=False)

    configuration = parser.add_argument_group('Configuration')
    configuration.add_argument('--mkvtoolnix-path', metavar='MkvToolNix directory path',
                               help='Choose the directory of MKVToolNix.\n'
                                    'Can be downloaded from here: {}.\n'
                                    'Leave empty to use default install location (windows only).'
                               .format(MKVTOOLNIX_DOWNLOAD_URL), widget='DirChooser', required=False)

    return parser.parse_args()


def main(**kwargs):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(name)-4s %(levelname)-5s %(message)s')
    logging.getLogger('urllib3').setLevel(level=logging.INFO)

    Main().main(**kwargs)


if __name__ == '__main__':
    main(**vars(parse_args()))
