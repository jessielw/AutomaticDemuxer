import pathlib
from os import PathLike
from typing import Union

from automatic_demuxer.format_extensions import mkv_video_formats_conversion


def get_video_extension(
    file_input: Union[str, PathLike],
    media_info_instance: object,
    track_number: Union[str, int],
    fallback_ext: str,
    extension: Union[str, None],
):
    """
    Check for video tracks and automatically generate the elementary video with a proper extension to demux

    :param file_input: String or Pathlike to video input
    :param media_info_instance: Object of a mediainfo class instance
    :param track_number: Integer to be sent to mediainfo to select the video track. Default is 0.
    :param fallback_ext: String in the form of an extension, default is "mkv" but can be overridden.
    :param extension: If set to None we will automatically determine the output extension based off of the codec
    ID. If an extension is supplied automatic detection will be skipped.
    :return: A string in the format of ".avc"
    """

    # if there is no video tracks
    if not media_info_instance.video_tracks:
        raise Exception(
            f"{str(pathlib.Path(file_input).name)} does not contain any video tracks"
        )

    # if there is a video track
    elif media_info_instance.video_tracks:
        # if extension was provided clean the input up and return it
        if extension:
            return str(f".{extension.lower().replace('.', '')}")

        # if extension was not provided attempt to automatically detect output extension based off of the format
        # extension list
        elif not extension:

            # if file is mkv or webm attempt to automatically detect video output extension based off codec id
            if (
                pathlib.Path(file_input).suffix == "mkv"
                or pathlib.Path(file_input).suffix == "webm"
            ):
                # if extension is found return it
                try:
                    generate_extension = mkv_video_formats_conversion[
                        str(
                            media_info_instance.video_tracks[int(track_number)].codec_id
                        ).upper()
                    ]
                    return str(f".{generate_extension}")

                # if codec ID does not match any in the dictionary return fallback_ext
                except KeyError:
                    return str(f".{fallback_ext}")

            # if file is anything other than mkv/webm default to the fallback_ext
            else:
                return str(f".{fallback_ext}")
