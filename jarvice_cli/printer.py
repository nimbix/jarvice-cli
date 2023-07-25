import os
import sys
from typing import Dict, List, Union, Tuple
from pydantic import StrictStr
import rich
import rich.table
import rich.style
import rich.color
import json
import jarviceapi_client as api
import datetime

import typer

#TODO Richify a lot
class GenPrinter:

    _fields : List[Tuple[str,str]]

    def __init__(self):
        self._fields = []
              
    def newField(self, fieldName : str, fieldValue : str):
        self._fields.append((fieldName, fieldValue))

    def flushField(self, title : str = ""):
        if title != "":
            print(title)
        for field in self._fields:
            print(f"{field[0]}: {field[1]}")
        self._fields.clear()

    def printMachines(self, machineList : Dict[str,api.MachineDef]):
        
        for name,mc in machineList.items():
            self.newField("Description", str(mc.mc_description))
            self.newField("Arch", str(mc.mc_arch))
            if mc.mc_slave_cores:
                self.newField("Cores", str(mc.mc_slave_cores))
                self.newField("RAM", str(mc.mc_slave_ram))
                self.newField("GPUs", str(mc.mc_slave_gpus))
                self.newField("Properties", str(mc.mc_slave_properties))
            else:
                self.newField("Cores", str(mc.mc_cores))
                self.newField("RAM", str(mc.mc_ram))
                self.newField("GPUs", str(mc.mc_gpus))
                self.newField("Properties", str(mc.mc_properties))
            self.newField("Devices", str(mc.mc_devices))
            self.newField("Scratch", str(mc.mc_scratch))
            self.newField("Swap", str(mc.mc_swap))
            self.newField("Min Scale", str(mc.mc_scale_min))
            self.newField("Max Scale", str(mc.mc_scale_max))
            self.newField("Price", str(mc.mc_price))

            self.flushField(name)

    def formatSize(self, string : Union[StrictStr,None], length : int):
        if string is None:
            return " "*length
        else:
            if len(string) > length:
                return string[0:length-3]+"..."
            else:
                return string + " "*(length-len(string))

    def printJobEntry(self, jobEntryList : Dict[str, api.JobEntry], verbose=False):
        if verbose:
            new_dict = {}
            for id,jobEntry in jobEntryList.items():
                new_dict[id] = json.loads(jobEntry.to_json())
            print(json.dumps(new_dict, indent= 2))
        else:
            for id,jobEntry in jobEntryList.items():
                deltaTime, nbNodes, machineType = self.extractFromJobEntry(jobEntry)
                print("ID  ",
                      "Name"+ 16*" ",
                      "App"+ 17*" ",
                      "User"+ 11*" ",
                      "St",
                      "Time"+ 6*" ",
                      "#N  ",
                      "Machine type", sep=" ")
                print(f"{self.formatSize(id,4)}",
                      f"{self.formatSize(jobEntry.job_name, 20)}",
                      f"{self.formatSize(f'{jobEntry.job_application}/{jobEntry.job_command}',20)}",
                      f"{self.formatSize(jobEntry.job_owner_username,15)}",
                      f"{self.shortStatus(jobEntry.job_status)}",
                      f"{self.formatSize(deltaTime,10)}",
                      f"{self.formatSize(str(nbNodes), 4)}",
                      f"{self.formatSize(machineType,18)}",
                      sep=" ")
 
    def shortStatus(self, string : Union[StrictStr,None]):
        # Setting color from status
        if string == "COMPLETED":
            return "CD"
        elif string =="EXEMPT":
            return "CG"
        elif string == "COMPLETED WITH ERROR":
            return " F"
        elif string == "SUBMITTED" or string =="SEQUENTIALLY QUEUED":
            return "PD"
        elif string == "PROCESSING STARTING":
            return " R"
        elif string == "TERMINATED" or string == "CANCELED":
            return "ST"
        else:
            return "UN"   

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
    
    def printRuntimeInfo(self, rtInfo : api.RuntimeInfo):
        print(f"address: {rtInfo.address}",
              f"password: {rtInfo.password}",
              f"url: {rtInfo.url}",
              f"about: {rtInfo.about}",sep="\n")
        if bool(rtInfo.actions):
            print("actions:")
            for k,v in rtInfo.actions:
                print(f"{k}: {v}")

    def printSchedStatusEntry(self,id : int, entry : api.SchedJobStatusEntry):
        print(f"ID: {id}",
              f"Job Name: {entry.job_name}",
              f"Project: {entry.job_project}",
              f"Application: {entry.job_application}/{entry.job_command}",
              f"Status: {entry.job_status} ({self.shortStatus(entry.job_status)})",
              f"SStatus: {entry.job_substatus}",
              sep="\n")
        if entry.job_submit_time:
              print(f"Submit Time: {datetime.datetime.fromtimestamp(entry.job_submit_time)}")
        if entry.job_start_time:
              print(f"Start Time: {datetime.datetime.fromtimestamp(entry.job_start_time)}")
        if entry.job_end_time:
              print(f"End Time: {datetime.datetime.fromtimestamp(entry.job_end_time)}")
        if entry.job_walltime:
              print(f"Walltime: {entry.job_walltime}")
    
    def printApps(self, apps : Dict[str, api.App], verbose = False):
        if verbose:
            print(apps)
        else:
            for k,v in apps.items():
                if v.data is None:
                    print(k)
                else:
                    if v.data.commands is None:
                        commands =""
                    else:
                        commands = ",".join(v.data.commands.keys())
                        commands = ": [" + commands + "]"
                    print(f"{k} : {v.data.name} {v.data.author} {commands}")

    def printApp(self, app : api.App, verbose = False):
        if verbose:
            print(app)
        else:
            if app.data is None:
                print(app.id)
                return
            
            print(f"{app.data.name} {app.data.author}")

            if app.data.commands is not None:
                for cmd, data in app.data.commands.items():
                    print(f"{cmd} : {data.description}")


class RichPrinter(GenPrinter):

    #_fields : List[Tuple[str,str]]

    def __init__(self):
        super().__init__()

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
            table.add_column("St")
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
                              self.shortStatus(jobEntry.job_status),
                              deltaTime,
                              f"{nbNodes}",
                              machineType,
                              style=rowStyle)

            console = rich.console.Console()
            console.print(table)
   
    def printApps(self, apps : Dict[str, api.App], verbose = False):
        if verbose:
            for k,v in apps.items():
                rich.inspect(v)
        else:
            table = rich.table.Table(style="on black")
            table.add_column("ID")
            table.add_column("App")
            table.add_column("Author")
            table.add_column("Commands")
            for k,v in apps.items():
                if v.data is None:
                    name = ""
                    author = ""
                    commands = ""
                else:
                    name = v.data.name
                    author = v.data.author
                    if v.data.commands is None:
                        commands =""
                    else:
                        commands = ",".join(v.data.commands.keys())
                    
                table.add_row(k, name, author, commands)

            console = rich.console.Console()
            console.print(table)

    def printApp(self, app : api.App, verbose = False):
        if verbose:
            rich.inspect(app)
        else:
            if app.data is None:
                print(app.id)
                return
            
            table = rich.table.Table(title=f"{app.data.name} {app.data.author}", style="on black")

            if app.data.commands is not None:
                table.add_column("Command")
                table.add_column("Description")
                for cmd, data in app.data.commands.items():
                    table.add_row(cmd, data.description)
            console = rich.console.Console()
            console.print(table)