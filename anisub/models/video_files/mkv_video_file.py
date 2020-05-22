import logging
import os
import platform
import subprocess
from pathlib import Path

from pymkv import MKVFile, MKVTrack

from anisub.models.video_files import VideoFile


MKVTOOLNIX_DOWNLOAD_URL = 'https://mkvtoolnix.download/downloads.html'
MKVTOOLNIX_WINDOWS_DEFAULT_INSTALL_PATH = r'C:\Program Files\MKVToolNix'


class MkvVideoFile(VideoFile):
    def __init__(self, path: Path, mkvtoolnix_path: Path = None):
        self.path = path
        self.folder = path.parent
        self.mkv_file = MKVFile(path.__str__())
        self.logger = logging.getLogger(__name__)

        if platform.system() == 'Windows':
            if not mkvtoolnix_path:
                mkvtoolnix_path = MKVTOOLNIX_WINDOWS_DEFAULT_INSTALL_PATH
            os.environ['PATH'] += os.pathsep + mkvtoolnix_path
        self.mkvtoolnix_path = mkvtoolnix_path

    def get_subtitles_track(self, language):
        self.logger.debug('Looking for subtitles track for language: %s.', language)
        if not isinstance(language, tuple):
            language = language,
        track: MKVTrack
        for track in self.mkv_file.tracks:
            if track.track_type == 'subtitles' and track.language in language:
                self.logger.info('Found subtitles track for language: %s.', track.language)
                return track
        raise Exception('Could not find subtitles track for: {}.'.format(language))

    def get_subtitles_text(self, language):
        track = self.get_subtitles_track(language)
        self.logger.debug('Extracting subtitles.')
        # TODO until pymkv supports subtitles extraction:
        subtitles_file_path = self.folder.joinpath('subtitles.txt')
        subprocess.check_output(
            'mkvextract tracks "{}" {}:{}'.format(self.path.name, track.track_id, subtitles_file_path.name),
            cwd=self.folder.__str__())
        with subtitles_file_path.open('r', encoding='utf-8') as subtitles_file:
            subtitles_text = subtitles_file.read()
        os.remove(subtitles_file_path.__str__())
        self.logger.debug('Successfully extracted subtitles.')
        return subtitles_text

    def add_subtitles(self, subtitles_text: str, language):
        self.logger.debug('Adding subtitles.')
        track = self.get_subtitles_track(language)
        fixed_subtitles_path = self.folder.joinpath('subtitles-fixed.txt')
        with fixed_subtitles_path.open('w', encoding='utf-8') as fixed_subtitles_file:
            fixed_subtitles_file.write(subtitles_text)
        fixed_track = MKVTrack(fixed_subtitles_path.__str__())
        fixed_track.track_name = track.track_name + '-fixed'
        fixed_track.language = track.language
        self.mkv_file.add_track(fixed_track)
        output_name = Path(self.path.stem + '-fixed').with_suffix(self.path.suffix)
        output_path = self.path.with_name(output_name)
        self.mkv_file.mux(output_path.__str__())
        os.remove(fixed_subtitles_file.__str__())
        self.logger.debug('Successfully added subtitles.')
