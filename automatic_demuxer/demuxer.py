import re
import subprocess
import threading
from os import PathLike
from sys import platform
from typing import Callable, Union


class Demuxer:
    """Uses subprocess module to run ffmpeg to demux with passed parameters"""

    def __init__(
        self,
        command: Union[str, list],
        output_filename: Union[str, PathLike],
        duration: Union[float, None],
        callback: Callable[[dict], None] = None,
    ):
        """
        Defines the variables for the class and executes the job in a thread, once completed joins the thread to
        clean up.

        :param command: Command in the format of a list for each white space ["echo", "hello!"]
        :param output_filename: String/Path of the full output filename
        :param duration: Float of the total track duration, None if it could not be found
        :param callback: This will allow you to collect the progress in a variable instead of printing to console
        """
        self.command = command
        self.output_filename = output_filename
        self.duration = duration
        self.callback = callback

        # variables to update as the program is running
        self.job = None
        self.status = None

        # start the job in a thread
        self.t1 = threading.Thread(target=self._run_job, daemon=True)
        self.t1.start()
        self.t1.join()

    def _run_job(self):
        """run the job via subprocess Popen and call parse_output()"""

        # if os is Windows
        if platform.startswith("win32"):
            self.job = subprocess.Popen(
                self.command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
                | subprocess.CREATE_NEW_PROCESS_GROUP,
            )

        # if os is anything other than Windows
        else:
            self.job = subprocess.Popen(
                self.command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
            )

        # run output parser
        self._parse_output()

    def _parse_output(self):
        """loop through the output from stdout/stderr to display progress"""
        for line in self.job.stdout:
            # use regex to clean up extra spaces/newlines
            formatted_line = re.sub(r"\s{2,}|\n+", "", line)

            # if there is no call back set simply print the formatted output
            if not self.callback:
                print(formatted_line)

            # if there is a call back set return a dictionary of the output, percent and job process ID
            elif self.callback:
                # call convert_to_percent() function to display the percent to the user
                convert_to_percent = self._convert_to_percent(formatted_line)
                self.callback(
                    {
                        "output": str(formatted_line),
                        "percent": convert_to_percent,
                        "job_pid": self.job.pid,
                    }
                )

        # run return code method after loop has exited
        self._return_code()

    def _convert_to_percent(self, formatted_line):
        """if there is a duration detected in the input track convert it to ms to obtain an accurate percentage"""
        if self.duration:
            # use regex to obtain the 'time=x' from FFmpeg's output
            get_ffmpeg_time = re.search(r"time=(.*?)\s*b", formatted_line)

            # if time is found in the output convert and return the progress percentage
            if get_ffmpeg_time:
                progress = (
                    sum(
                        x * float(t)
                        for x, t in zip(
                            [1, 60, 3600], reversed(get_ffmpeg_time.group(1).split(":"))
                        )
                    )
                    * 1000
                )
                percent = str("{:.1%}".format(float(progress) / float(self.duration)))
                return percent

            # if time is not found return None
            elif not get_ffmpeg_time:
                return None

        # if no duration is found return None
        elif not self.duration:
            return None

    def _return_code(self):
        """
        Wait for subprocess job to end and return the job code, output file name, and status.
        If the self.job.poll() returned 0 it's a good indicator that the job was completed.
        We will check for full path and job code equaling 0 and return the status of "Ok".
        """
        self.job.wait()

        if self.job.poll() == 0:
            job_status = "Ok"
        else:
            job_status = "Error"

        # update status with return code and output file name
        self.status = {
            "return_code": self.job.poll(),
            "output_filename": self.output_filename,
            "status": job_status,
        }
