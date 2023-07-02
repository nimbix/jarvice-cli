import configparser
from pathlib import Path
import sys
import typer
import os
from typing import Optional, Annotated, Dict

#from jarviceapi import *
import jarviceapi_client
from jarvice_cli.jarviceapi import jarviceapi
from jarvice_cli.printer import *

jarvice_cli = typer.Typer(help="The JARVICE CLI for interacting with Jarvice XE")

api_values : Dict[str, str]= {}

def validateJobidJobname(jobid: Optional[int], jobname: Optional[str]):
    if jobid is None and jobname is None:
        raise typer.BadParameter("Define jobid or jobname")
    if jobid is not None and jobname is not None:
        raise typer.BadParameter("jobid and jobname both specified. Specify only one")

def getEnvValue(argName: str, argValue: Optional[str], envVarName: str):
    """
    If parameter is None, it is not in command.
    First it searches in env variables, second, it searches in ~/.jarvice.cfg
    """
    if argValue is None:
        if envVarName in os.environ:
            api_values[argName] = os.environ[envVarName]
        elif os.path.exists(os.path.expanduser("~/.jarvice.cfg")):
            CParser = configparser.ConfigParser()
            CParser.read(
                [
                    os.path.expanduser("~/.jarvice.cfg"),
                ]
            )
            try:
                api_values[argName] = CParser.get("auth", argName)
            except:
                pass
        else:
            
            raise typer.BadParameter(f"{argName} undefined\n"
                "username, apikey and url must be passed as arguments, "
                "or in env variables (JARVICE_USER, JARVICE_API_KEY, JARVICE_API_URL) "
                "or set in ~/.jarvice.cfg")
    else:
        api_values[argName] = argValue


@jarvice_cli.callback()
def getCredentials(
    ctx: typer.Context,
    url: Annotated[
        Optional[str], typer.Option("--url", help="URL of Jarvice XE")
    ] = None,
    username: Annotated[
        Optional[str], typer.Option("--username", "-u", help="Login name in Jarvice XE")
    ] = None,
    apikey: Annotated[
        Optional[str], typer.Option("--apikey", "-k", help="API key in Jarvice XE")
    ] = None,
):

    if not any([x in sys.argv for x in ctx.help_option_names]):
        getEnvValue("username", username, "JARVICE_USER")
        getEnvValue("apikey", apikey, "JARVICE_API_KEY")
        getEnvValue("url", url, "JARVICE_API_URL")
        global jarvice_api
        jarvice_api = jarviceapi(api_values["username"], api_values["apikey"], api_values["url"])

## Interacting with jobs ##

@jarvice_cli.command()
def submit(
    job_json: Annotated[
        Path,
        typer.Argument(
            help="json file with job submission",
            exists=True,
            readable=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
        ),
    ],
):
    """
    Submit a job
    """
    try:
        retDict = jarvice_api.submitJsonFile(job_json)
        print("Submitted:",
              f"- ID  : {retDict['number']}",
              f"- Name: {retDict['name']}", sep='\n')
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def tail(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
    lines: Annotated[
        Optional[int], typer.Option("-l", "--lines",  help="Number of lines to display")
    ] = 0
):
    """
    See the output/error of a currently running job
    """
    validateJobidJobname(jobid, jobname)
    
    try:
        if lines is None:
            lines = 0
        if jobid is not None:
            print(jarvice_api.tail(jobid, lines))
        elif jobname is not None:
            print(jarvice_api.tail(jobname, lines))
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def output(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
    lines: Annotated[
        Optional[int], typer.Option("-l", "--lines",  help="Number of lines to display")
    ] = 0
):
    """
    See the output of a job that has ended
    """
    validateJobidJobname(jobid, jobname)    
    try:
        if lines is None:
            lines = 0
        if jobid is not None:
            print(jarvice_api.output(jobid, lines))
        elif jobname is not None:
            print(jarvice_api.output(jobname, lines))
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def connect(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
):
    """
    Get connection details (address, password)
    """
    validateJobidJobname(jobid, jobname)
    try:
        if jobid is not None:
            address,password = jarvice_api.connect(jobid)
        elif jobname is not None:
            address,password = jarvice_api.connect(jobname)
        else:
            return
        print(f"Address : {address}")
        print(f"Password : {password}")
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def shutdown(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
):
    """
    Cleanly shutdown a job (with shutdown signal)
    """
    validateJobidJobname(jobid, jobname)
    try:
        if jobid is not None:
            jarvice_api.shutdown(jobid)
        elif jobname is not None:
            jarvice_api.shutdown(jobname)
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def terminate(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
):
    """
    Force termination of a job (like kill -9)
    """
    validateJobidJobname(jobid, jobname)
    try:
        if jobid is not None:
            jarvice_api.terminate(jobid)
        elif jobname is not None:
            jarvice_api.terminate(jobname)
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def info(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
    raw : Annotated[Optional[bool], typer.Option("--no-rich",help="Without color")] = False
):
    """
    Get the stats on your job
    """
    validateJobidJobname(jobid, jobname)
    try:
        if jobid is not None:
            entry = jarvice_api.info(jobid)
        elif jobname is not None:
            entry = jarvice_api.info(jobname)
        else:
            return
        if raw:
            printer = NoRichPrinter()
        else:
            printer = RichPrinter()

        printer.printRuntimeInfo(entry)
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def status(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
    raw : Annotated[Optional[bool], typer.Option("--no-rich",help="Without color")] = False
):
    """
    Get status of a job
    """
    validateJobidJobname(jobid, jobname)
    try:
        if jobid is not None:
            entry = jarvice_api.status(jobid)
        elif jobname is not None:
            entry = jarvice_api.status(jobname)
        else:
            return
        if raw:
            printer = NoRichPrinter()
        else:
            printer = RichPrinter()
        
        for k,v in entry.items():
            printer.printSchedStatusEntry(int(k),v)

    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command(deprecated=True)
def action(
    action: Annotated[str, typer.Argument(help="action name, given by info")],
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
):
    """
    Perform a configured action on your job
    """
    validateJobidJobname(jobid, jobname)
    try:
        if jobid is not None:
            jarvice_api.action(action, jobid)
        elif jobname is not None:
            jarvice_api.action(action, jobname)
        print(f"Action requested : {action}")
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def jobs(
    verbose: Annotated[Optional[bool], typer.Option("-v", "--verbose",help="Full JSON payload")] = False,
    raw : Annotated[Optional[bool], typer.Option("--no-rich",help="Without color")] = False
    ):
    """
    Get a list of currently running jobs\n
    Job Status :\n
    CD 	The job has completed successfully.\n
    CG 	The job is finishing but some processes are still active.\n
    F 	The job terminated with a non-zero exit code and failed to execute.\n
    PD 	The job is waiting for resource allocation. It will eventually run.\n
    R 	The job currently is allocated to a node and is running.\n
    ST 	A running job has been canceled or terminated.\n
    UN 	Unknown status.
    """
    try:
        if verbose is None:
            verbose = False
        if raw:
            printer = NoRichPrinter()
        else:
            printer = RichPrinter()

        joblist = jarvice_api.jobs()
        printer.printJobEntry(joblist, verbose)
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def shutdown_all():
    """
    Cleanly shutdown all currently running jobs
    """
    try:
        jarvice_api.shutdown_all()
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def terminate_all():
    """
    Force termination of all jobs (like kill -9)
    """
    try:
        jarvice_api.terminate_all()
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")

@jarvice_cli.command()
def wait_for(
    jobid: Annotated[Optional[int], typer.Option("-j", "--jobid",help="ID of the job [required or --jobname required]")] = None,
    jobname: Annotated[Optional[str], typer.Option("-n", "--jobname",help="Name of the job [required or --jobid required]")] = None,
):
    """
    Wait for a job to end
    """
    validateJobidJobname(jobid, jobname)
    try:        
        if jobid is not None:
            jarvice_api.wait_for(jobid)
        elif jobname is not None:
            jarvice_api.wait_for(jobname)
    except jarviceapi_client.OpenApiException as e:
        print(f"Error : {e}")


## Data Management ##

@jarvice_cli.command()
def download(
    source: Annotated[str, typer.Argument(help="File/directory to download")],
    destination: Annotated[str, typer.Argument(help="File/directory destination")],
    storage : Annotated[str, typer.Argument(help="vault name")],
):
    """
    Download file or directory 
    """
    try:        
        jarvice_api.download(source, destination, storage)
    except Exception as e:
        print(e)

@jarvice_cli.command()
def upload(
    source: Annotated[str, typer.Argument(help="File/directory to upload")],
    destination: Annotated[str, typer.Argument(help="File/directory destination")],
    storage : Annotated[str, typer.Argument(help="vault name")],
):
    """
    Upload file or directory 
    """
    try:        
        jarvice_api.upload(source, destination, storage)
    except Exception as e:
        print(e)

@jarvice_cli.command()
def ls(
    storage : Annotated[str, typer.Argument(help="vault name")],
    remote_dir: Annotated[
        Optional[str], typer.Option("-d", help="Remote directory")
    ] = None,
):
    """
    List files
    """
    try:        
        jarvice_api.ls(storage, remote_dir)
    except Exception as e:
        print(e)

## Querying JARVICE Options ##

@jarvice_cli.command()
def apps():
    """
    List apps and gives a schema describing outputs
    """
    try:        
        jarvice_api.apps()
    except Exception as e:
        print(e)

@jarvice_cli.command()
def machines():
    """
    List all instances
    """
    try:        
        jarvice_api.machines()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    jarvice_cli()
