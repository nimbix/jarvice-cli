from collections import OrderedDict
import json
from typing import Optional, Tuple, Union
import jarviceapi_client
import jarviceapi_client.exceptions as apiException
from pathlib import Path
from traceback import print_exc

import rich

from jarvice_cli.__main__ import jobs

class jarviceapi:
    _username : str
    _apikey : str
    _configuration : jarviceapi_client.Configuration

    def __init__(self, username : str, apikey : str, url : str):
        self._username = username
        self._apikey = apikey
        self._configuration = jarviceapi_client.Configuration(
            host = url
        )

    def submitJson(self, jobSubmission : jarviceapi_client.Submission):
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.JobControlApi(api_client)
            # Inject user
            if jobSubmission.user is None:
                jobSubmission.user = jarviceapi_client.SubmitUser()
            jobSubmission.user.username = self._username
            jobSubmission.user.apikey = self._apikey

            return api_instance.submit_post(jobSubmission)


    def submitJsonFile(self, job_jsonfile : Path):
        """
        Submits a job to Jarvice XE
        
        Args:
            job_jsonfile (Path) : json file containing job launch definition

        Raises:
            apiException.OpenApiException
        """
        with open(job_jsonfile) as job_jsonfile_hd:
            json_object = json.load(job_jsonfile_hd)
            jobSubmission = jarviceapi_client.Submission.from_dict(json_object)
            return self.submitJson(jobSubmission)

    def tail(self, job : Union[int, str], lines = 0):
        """
        See the output/error of a currently running job
        
        Raises:
            Exception: Raises an exception.
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.StatusAndInformationApi(api_client)
            if type(job) is str:
                return api_instance.tail_get(self._apikey, self._username, name=job, lines=lines)
            elif type(job) is int:
                return api_instance.tail_get(self._apikey, self._username, number=job, lines=lines)
            
    
    def output(self, job : Union[int, str], lines):
        """
        See the output of a currently running job
        
        Raises:
            Exception: Raises an exception.
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.StatusAndInformationApi(api_client)
            if type(job) is str:
                return api_instance.output_get(self._apikey, self._username, name=job, lines=lines)
            elif type(job) is int:
                return api_instance.output_get(self._apikey, self._username, number=job, lines=lines)
    
    def connect(self, job : Union[int, str]):
        """
        Get connection details (address, password)
        Raises:
            Exception: Raises an exception.
        """
        address : str = "NONE"
        password : str = "NONE"
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.StatusAndInformationApi(api_client)
            
            runtimeConnect : jarviceapi_client.RuntimeConnect
            if type(job) is str:
                runtimeConnect = api_instance.connect_get(self._apikey, self._username, name=job)
            elif type(job) is int:
                runtimeConnect = api_instance.connect_get(self._apikey, self._username, number=job)
            else:
                raise apiException.ApiException(status=501, http_resp="Invalid parameters")
            if runtimeConnect:
                if runtimeConnect.address:
                    address = runtimeConnect.address
                if runtimeConnect.password:
                    password = runtimeConnect.password
            return address,password

    
    def shutdown(self, job : Union[int, str]):
        """
        Cleanly shutdown a job (with shutdown signal)

        Raises:
            Exception: Raises an exception.
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.JobControlApi(api_client)
            
            if type(job) is str:
                api_instance.shutdown_get(self._apikey, self._username, name=job)
            elif type(job) is int:
                api_instance.shutdown_get(self._apikey, self._username, number=job)
            else:
                raise apiException.ApiException(status=501, http_resp="Invalid parameters")
    
    def terminate(self, job : Union[int, str]):
        """
        Force termination of a job (like kill -9)

        Raises:
            Exception: Raises an exception.
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.JobControlApi(api_client)
            
            if type(job) is str:
                api_instance.terminate_get(self._apikey, self._username, name=job)
            elif type(job) is int:
                api_instance.terminate_get(self._apikey, self._username, number=job)
            else:
                raise apiException.ApiException(status=501, http_resp="Invalid parameters")

    def info(self, job : Union[int, str]):
        """
        Get the stats on your job

        Raises:
            Exception: Raises an exception.
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.StatusAndInformationApi(api_client)
            
            if type(job) is str:
                return api_instance.info_get(self._apikey, self._username, name=job)
            elif type(job) is int:
                return api_instance.info_get(self._apikey, self._username, number=job)
            else:
                raise apiException.ApiException(status=501, http_resp="Invalid parameters")

    def status(self, job : Union[int, str]):
        """
        Get status of a job

        Raises:
            Exception: Raises an exception.
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.StatusAndInformationApi(api_client)
            
            if type(job) is str:
                return api_instance.status_get(self._apikey, self._username, name=job)
            elif type(job) is int:
                return api_instance.status_get(self._apikey, self._username, number=job)
            else:
                raise apiException.ApiException(status=501, http_resp="Invalid parameters")

    def action(self, action : str, job : Union[int, str]):
        """
        Perform a configured action on your job

        Raises:
            apiException.OpenApiException
        """
        with jarviceapi_client.ApiClient(self._configuration) as api_client:
            api_instance = jarviceapi_client.JobControlApi(api_client)
            if type(job) is str:
                return api_instance.action_get(self._apikey, self._username, action, name=job)
            elif type(job) is int:
                return api_instance.action_get(self._apikey, self._username, action, number=job)


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
            apiException.OpenApiException
        """
        jobs = self.jobs()
        for k,_ in jobs.items():
            self.shutdown(int(k))
    
    
    def terminate_all(self):
        """
        Force termination of all jobs (like kill -9)

        Raises:
            Exception: Raises an exception.
        """
        jobs = self.jobs()
        for k,_ in jobs.items():
            self.terminate(int(k))

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

