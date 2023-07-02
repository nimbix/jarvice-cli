import os
import sys
from typing import Dict, Union
from pydantic import StrictStr
import rich
import rich.table
import rich.style
import rich.color
import json
import jarviceapi_client as api
import datetime

import typer

class GenPrinter:
    def __init__(self):
        pass

    def printJobEntry(self, jobEntryList : Dict[str, api.JobEntry], verbose=False):
        pass
    
    def formatSize(self, string : Union[StrictStr,None], length : int):
        if string is None:
            return " "*length
        else:
            if len(string) > length:
                return string[0:length-3]+"..."
            else:
                return string + " "*(len(string)-length)

    def extractFromJobEntry(self, jobEntry : api.JobEntry):
        # Compute time depending on status
        deltaTime = ""
        if jobEntry.job_status == "SUBMITTED" or jobEntry.job_status =="SEQUENTIALLY QUEUED":
            if jobEntry.job_stats is not None and jobEntry.job_stats.queue_time is not None:
                deltaTime = str(datetime.timedelta(seconds=jobEntry.job_stats.queue_time))
        else:
            if jobEntry.job_stats is not None and jobEntry.job_stats.compute_time is not None:
                deltaTime = str(datetime.timedelta(seconds=jobEntry.job_stats.compute_time))

        if jobEntry.job_api_submission is None or jobEntry.job_api_submission.machine is None :
            nbNodes = "#"
            machineType = "#"
        else:
            nbNodes = jobEntry.job_api_submission.machine.nodes if jobEntry.job_api_submission.machine.nodes is not None else "#"
            machineType = jobEntry.job_api_submission.machine.type if jobEntry.job_api_submission.machine.type is not None else "#"
        return deltaTime, nbNodes, machineType


class RichPrinter(GenPrinter):
    def __init__(self):
        pass

    ##TODO : (TOFIX) jobEntry.job_stats.compute_time is always 0
    def printJobEntry(self, jobEntryList : Dict[str,api.JobEntry], verbose = False):
        if verbose:
            for _,jobEntry in jobEntryList.items():
                rich.inspect(jobEntry)
        else:
            """
            Default format : 
                JobNumber JobName App/app_command User Status Time Nodes InstanceType
            """
            table = rich.table.Table(style="on black")
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("App")
            table.add_column("User")
            table.add_column("Status")
            table.add_column("Time")
            table.add_column("Nodes")
            table.add_column("Machine type")

            for number,jobEntry in jobEntryList.items():
                # Setting color from status
                if jobEntry.job_status == "COMPLETED":
                    rowStyle = rich.style.Style(color="gray")
                elif jobEntry.job_status == "COMPLETED WITH ERROR" or jobEntry.job_status =="TERMINATED" or jobEntry.job_status == "CANCELED":
                    rowStyle = rich.style.Style(color="dark_red")
                elif jobEntry.job_status == "SUBMITTED" or jobEntry.job_status =="SEQUENTIALLY QUEUED" or jobEntry.job_status =="EXEMPT":
                    rowStyle = rich.style.Style(color="yellow")
                elif jobEntry.job_status == "PROCESSING STARTING":
                    rowStyle = rich.style.Style(color="green")
                else:
                    rowStyle = rich.style.Style()
                
                # Compute time depending on status
                deltaTime, nbNodes, machineType = self.extractFromJobEntry(jobEntry)

                table.add_row(number, 
                              jobEntry.job_name,
                              f"{jobEntry.job_application}/{jobEntry.job_command}",
                              jobEntry.job_owner_username,
                              jobEntry.job_status,
                              deltaTime,
                              f"{nbNodes}",
                              machineType,
                              style=rowStyle)

            console = rich.console.Console()
            console.print(table)

class RawPrinter(GenPrinter):
    def __init__(self):
        pass



    def printJobEntry(self, jobEntryList : Dict[str, api.JobEntry], verbose=False):
        if verbose:
            new_dict = {}
            for id,jobEntry in jobEntryList.items():
                new_dict[id] = json.loads(jobEntry.to_json())
            print(json.dumps(new_dict, indent= 2))
        else:
            for id,jobEntry in jobEntryList.items():
                deltaTime, nbNodes, machineType = self.extractFromJobEntry(jobEntry)
                print("ID,Name,App,User,Status,Time,Nodes,Machine type")
                print(f"id,",
                      f"{jobEntry.job_name}",
                      f"{jobEntry.job_application}/{jobEntry.job_command}",
                      f"{jobEntry.job_owner_username}",
                      f"{jobEntry.job_status}",
                      f"{deltaTime}",
                      f"{nbNodes}",
                      f"{machineType}",
                      sep=",")
