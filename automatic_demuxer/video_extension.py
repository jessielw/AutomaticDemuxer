from __future__ import annotations

import pathlib
from os import PathLike

from pymediainfo import MediaInfo

from format_extensions import video_formats


def get_video_extension(file_input: str | PathLike, extension: str | None):
    """
    Check for video tracks and automatically generate the elementary video with a proper extension to demux

    :param file_input: String or Pathlike to video input
    :param extension: If set to None we will automatically determine the output extension based off of the codec
    ID. If an extension is supplied automatic detection will be skipped.
    :return: A string in the format of ".avc"
    """

    # open the input file with mediainfo
    parse_file = MediaInfo.parse(pathlib.Path(file_input))

    # if there is no video tracks
    if not parse_file.video_tracks:
        raise Exception(
            f"{str(pathlib.Path(file_input).name)} does not contain any video tracks"
        )

    # if there is a video track
    elif parse_file.video_tracks:
        # if extension was provided clean the input up and return it
        if extension:
            return str(f".{extension.lower().replace('.', '')}")

        # if extension was not provided attempt to automatically detect output extension based off of the format
        # extension list
        elif not extension:

            # if extension is found return it
            try:
                generate_extension = video_formats[
                    str(parse_file.video_tracks[0].codec_id).upper()
                ]
                return str(f".{generate_extension}")

            # if codec ID does not match any in the dictionary raise an error
            except KeyError:
                raise KeyError(
                    f"Could not automatically detect video output extension for codec "
                    f"'{str(parse_file.video_tracks[0].codec_id).upper()}'"
                )
