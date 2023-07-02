from collections import OrderedDict
from typing import Optional, Tuple, Union
import jarviceapi_client
import jarviceapi_client.exceptions as apiException
from pathlib import Path
from traceback import print_exc

class jarviceapi:
    _username : str
    _apikey : str
    _uconfiguration : str

    def __init__(self, username : str, apikey : str, url : str):
        self._username = username
        self._apikey = apikey
        self._configuration = jarviceapi_client.Configuration(
            host = url
        )

    def submit(self, job_jsonfile : Path):
        """
        Submits a job to Jarvice XE
        
        Args:
            job_jsonfile (Path) : json file containing job launch definition

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("submit is not implemented")

    def summary(self):
        """
        List a summary of your jobs
        
        Raises:
            Exception: Raises an exception.
        """
        retval = OrderedDict()

        raise Exception("summary is not implemented")
        return retval
    
    def tail(self, job : Union[int, str], lines):
        """
        List a summary of your jobs
        
        Raises:
            Exception: Raises an exception.
        """
        retval : str
        raise Exception("tail is not implemented")
        return retval
    
    def output(self, job : Union[int, str], lines):
        retval : str
        raise Exception("output is not implemented")
        return retval
    
    def connect(self, job : Union[int, str]):
        """
        Get connection details (address, password)
        Raises:
            Exception: Raises an exception.
        """
        address : str
        password : str
        raise Exception("connect is not implemented")
        return address, password
    
    def shutdown(self, job : Union[int, str]):
        """
        Cleanly shutdown a job (with shutdown signal)

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("shutdown is not implemented")
    
    def terminate(self, job : Union[int, str]):
        """
        Force termination of a job (like kill -9)

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("terminate is not implemented")

    def info(self, job : Union[int, str]):
        """
        Get the stats on your job

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("info is not implemented")

    def status(self, job : Union[int, str]):
        """
        Get status of a job

        Raises:
            Exception: Raises an exception.
        """
        
        raise Exception("status is not implemented")

    def action(self, action : str, job : Union[int, str]):
        """
        Perform a configured action on your job

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("action is not implemented")


    def jobs(self):
        """
        Get a list of currently running jobs

        Returns:
            jobs (Dict[str, JobEntry]) : Job dictionnary

        Raises:
            apiException.OpenApiException
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.StatusAndInformationApi(api_client)
            return api_instance.jobs_get(self._apikey, self._username)

    def shutdown_all(self):
        """
        Cleanly shutdown all currently running jobs

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("shutdown_all is not implemented")
    
    
    def terminate_all(self):
        """
        Force termination of all jobs (like kill -9)

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("terminate_all is not implemented")

    def wait_for(self, job : Union[int, str]):
        """
        Wait for a job to end
        
        Raises:
            Exception: Raises an exception.
        """
        raise Exception("wait_for is not implemented")

    def download(self, source: str, destination: str, storage : str):
        """
        Download file or directory 
        
        Raises:
            Exception: Raises an exception.
        """
        raise Exception("download is not implemented")

    def upload(self, source: str, destination: str, storage : str):
        """
        Upload file or directory
        
        Raises:
            Exception: Raises an exception.
        """
        raise Exception("download is not implemented")
    
    def ls(self, storage : str, remote_dir: Optional[str] = None):
        """
        List files

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("ls is not implemented")

    def apps(self):
        """
        List apps and gives a schema describing outputs

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("apps is not implemented")

    def machines(self):
        """
        List all instances

        Raises:
            Exception: Raises an exception.
        """
        raise Exception("machines is not implemented")

