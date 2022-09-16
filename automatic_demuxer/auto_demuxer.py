from __future__ import annotations

import pathlib
import shutil
from os import PathLike
from typing import Callable, Optional

from automatic_demuxer.demuxer import Demuxer
from automatic_demuxer.video_extension import get_video_extension

from pymediainfo import MediaInfo


class AutoDemuxer:

    def __init__(self):
        """set default variables to be utilized"""
        self.parse_file = None
        self.duration = None
        self.file = None
        self.ffmpeg = None
        self.track_number = None
        self.extension = None
        self.callback = None

    @staticmethod
    def _check_file(file: str | PathLike):
        """
        check file input

        :param file: Path to input file.
        :return: Full path to input file.
        """
        file_exists = pathlib.Path(file).is_file()

        if file_exists:
            return pathlib.Path(file)
        if not file_exists:
            raise FileNotFoundError(f"Could not locate '{file}'")

    @staticmethod
    def _check_ffmpeg(ffmpeg: str | PathLike):
        """
        If ffmpeg is not None then check if ffmpeg is a file.
        If ffmpeg is None check for ffmpeg on the path.
        Once ffmpeg is found it'll be returned with the full path, if ffmpeg is not found raise an Exception.

        :param ffmpeg: path to ffmpeg executable
        :return: Full path to ffmpeg
        """
        # if user defines path to ffmpeg
        if ffmpeg:
            if pathlib.Path(ffmpeg).is_file():
                return pathlib.Path(ffmpeg)
            if not pathlib.Path(ffmpeg).is_file():
                raise Exception("Could not locate ffmpeg")

        # if user leaves ffmpeg set to None
        elif not ffmpeg:
            ffmpeg_on_path = shutil.which("ffmpeg")

            if ffmpeg_on_path:
                return pathlib.Path(ffmpeg_on_path)
            elif not ffmpeg_on_path:
                raise Exception("Could not locate ffmpeg")

    def video_demux(self,
                    file_input: str | PathLike,
                    ffmpeg_path: str | PathLike | None = None,
                    track_number: int | str = 0,
                    video_output_extension: str | None = None,
                    callback: Optional[Callable[[dict], None]] | None = None,
                    fallback_ext: str = "mkv"):
        """
        Take all the input parameters and utilize them to extract the video from the input file.
        The only required parameter is file_input.

        :param file_input: String or Pathlike path to input file.
        :param ffmpeg_path: String or Pathlike path to ffmpeg.
        :param track_number: Track number based off of ffmpeg stream selection or mediainfo's 'Stream identifier'.
        :param video_output_extension: The output extension in the form of a string. e.g. "mkv" or ".mkv"
        :param callback: Log callback progress to a variable instead of printing to consoleStream identifier
        :param fallback_ext: Extension on the form of a string. e.g. "mkv" or "mp4". Default is "mkv", if changed the
            program will fall back to what ever extension is selected
        :return: None
        """

        # open the input file with mediainfo
        self.parse_file = MediaInfo.parse(pathlib.Path(file_input))
        self.duration = self.parse_file.video_tracks[int(track_number)].duration

        self.file = self._check_file(file_input)
        self.ffmpeg = self._check_ffmpeg(ffmpeg_path)
        self.track_number = track_number
        self.extension = get_video_extension(file_input, self.parse_file, track_number, fallback_ext,
                                             video_output_extension)
        self.callback = callback

        # create completed output directory
        output_dir = pathlib.Path(self.file).parent
        output_file_name = pathlib.Path(str(pathlib.Path(pathlib.Path(self.file).name).with_suffix("")) +
                                        str(self.extension))
        output = pathlib.Path(output_dir / output_file_name)

        # build out command
        command = [self.ffmpeg, "-y", "-i", self.file, "-map", f"0:v:{str(self.track_number)}", "-c:v:0", "copy",
                   output, "-hide_banner"]

        # run the demuxer class to demux the file
        Demuxer(command, self.duration, callback=self.callback)


if __name__ == '__main__':
    # example of video_demux with a call back "testing"
    def testing(x):
        print(x)

    demux = AutoDemuxer()
    demux.video_demux(file_input=r"fileinput.mkv", callback=testing)
