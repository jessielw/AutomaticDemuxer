# Automatic Demuxer

Package to demux media-files into single file formats to be used elsewhere.

*Video tracks are only supported as of v1.2*

Developed by Jessie Wilson (2022)

## Install

`pip install AutomaticDemuxer`

**If using Linux you must also install MediaInfo**

`sudo apt install mediainfo`

## Uninstall

`pip uninstall AutomaticDemuxer`

## Examples of How To Use

**Video: Example with callback**

```python
from automatic_demuxer import AutoDemuxer


def callback_func(x):
    """
    AutoDemuxer will return a dictionary with keys 'output' and 'percent'
    "output" will always display the ffmpeg command line output
    "percent" will return None if there is no track duration OR when the job hasn't fully started/is finished
    """
    print(x["output"])
    print(x["percent"])

    # check if x["percent"] is not none before using output
    if x["percent"]:
        print(f"do something with {str(x['percent'])}")


demux = AutoDemuxer()
demux.video_demux(file_input=r"fileinput.mkv", callback=callback_func)
```

\
**Video: Example without callback**

When not using callback the FFMPEG output is automatically printed to console in the format of a string.
This does not include percentage.

```python
from automatic_demuxer import AutoDemuxer

demux = AutoDemuxer()
demux.video_demux(file_input=r"fileinput.mkv")
```

## Video Parameters

`file_input` String or Pathlike path to input file.

`ffmpeg_path` String or Pathlike path to ffmpeg.\
*Optional: Will raise an error if not found on path or defined*

`track_number` Track number based off of ffmpeg stream selection or mediainfo's 'Stream identifier'.\
*Optional: Defaults to 0*

`suffix` String to define the output ending suffix.\
*Optional: Defaults to "\_out\_"*

`insert_delay` Bool to insert delay string into filename output if delay is detected.\
*Optional: Defaults to True*

`video_output_extension` The output extension in the form of a string. e.g. "mkv" or ".mkv"\
*Optional: Defaults to "mkv"*

`callback` Log callback progress to a variable instead of printing to console\
*Optional: Defaults to None*

`fallback_ext` Extension in the form of a string. e.g. "mkv" or "mp4". Default is "mkv", if changed the program will
fall back to what ever extension is selected\
*Optional: Defaults to "mkv"*
