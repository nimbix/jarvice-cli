# jarvice-cli
New CLI for interacting with Jarvice XE.

This package depends on [python-jarviceapi](https://github.com/nimbix/python-jarviceapi) as it uses Jarvice API

## Requirements.

Python 3.9+

## Installation
```pip install git+https://github.com/nimbix/jarvice-cli.git```

## Usage

Command for the CLI is :

```jarvice-cli```

For this to work, it requires 3 parameters :
| username | Username to login to your endpoint |
| apikey | Apikey that you can find in your endpoint |
| url | Your endpoint url, which must finish by /api/ |

```username``` and ```apikey``` can be found in your endpoint under Account > Profile :

![screenshot username & apikey](https://github.com/nimbix/jarvice-cli/blob/test_docker/screenshot.png)

Those 3 parameters can be passed by:
-   Arguments: ```--username``` , ```--apikey``` , ```--url```
-   Environment variables: ```JARVICE_USER``` , ```JARVICE_API_KEY``` , ```JARVICE_API_URL```
-   Config file: ```~/.jarvice.cfg```

Structure for ```.jarvice.cfg```:
```
[auth]
username=<JARVICE_USER>
apikey=<JARVICE_API_KEY>
url=<JARVICE_API_URL>
```

```jarvice-cli``` contains the following commands:

| Command  | Description |
| ------------- | ------------- |
| action   | Perform a configured action on your job (deprecated)  |
| apps  | List apps and gives a schema describing AppDef  |
| connect | Get connection details (address, password)  |
| info | Get the stats on your job |
| jobs   | Get a list of currently running jobs  |
| machines | List all instances  |
| output | See the output of a job that has ended |
| shutdown | Cleanly shutdown a job (with shutdown signal)  |
| shutdown-all | Cleanly shutdown all currently running jobs  |
| status | Get status of a job |
| submit | Submit a job  |
| tail | See the output/error of a currently running job |
| terminate | Force termination of a job (like kill -9)  |
| terminate-all | Force termination of all jobs (like kill -9)  |
| wait-for | Wait for a job to end |           

## Tests

An example of Jarvice application with the CLI is integrated with this repo, which you can directly launch in Jarvice XE as an application in PushToCompute.

Read [Jarvice XE PushToCompute doc](https://jarvice.readthedocs.io/en/latest/cicd/) for more details

## Documentation

This CLI contains an extensive help message which you can find by doing:

```jarvice-cli --help```

For each command, you can get the required parameters, in addition to ```username```, ```apikey``` and ```url``` by doing:

```jarvice-cli <command> --help```

## Author

support@nimbix.net