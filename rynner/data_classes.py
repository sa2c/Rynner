from dataclasses import dataclass
from typing import Union
from pathlib import PurePosixPath

@dataclass
class Run:
	"""This is a dataclass describing a job submission and its status.

	This is the body of the docstring description.


	Attributes
	----------
	submission_id: str
		A unique submission identifier generated via the `uuid` module.
	job_name : str
		The name of the submitted job that can be seen in the job queue and in
		the submission script itself.
	remote_dir: PurePosixPath
		The directory on a remote machine that contains all files related to
		the submission.
	uploads: Union[list[str], list]
		A list of local paths to files that get transferred to a remote machine.
	downloads: Union[list[str], list]
		A list of remote paths to files that get transferred to the local
		machine.
	script: str
		This string contains the code that is executed on a remote machine.
		This code is automatically integrated into a submission script.
	job_status: Union[str, int]
		The status of the submission, can accept values from the following list:
		'PENDING', 'RUNNING', 'CANCELLED', 'COMPLETED' or an integer.
	namespace: str
		An additional path parameter that is used for more accurate data
		management.
	upload_status: float
		An attribute ranging from 0 to 1, shows how many files have been
		uploaded.
	download_status: float
		An attribute ranging from 0 to 1, shows how many files have been
		downloaded.
	upload_time: float
		The time when a file gets uploaded as Unix time.
	job_id: Union[str, None]
		The SLURM id of a submitted job, initialized as None.

	"""

	submission_id: str
	job_name: str
	remote_dir: PurePosixPath
	uploads: Union[list[str], list]
	downloads: Union[list[str], list]
	script: str
	job_status: Union[str, int]
	namespace: str
	upload_status: float
	download_status: float
	upload_time: float
	job_id: Union[str, None]
