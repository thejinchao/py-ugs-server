# py-ugs-server
An [Unreal Game Sync(UGS)](https://docs.unrealengine.com/5.1/en-US/unreal-game-sync-ugs-for-unreal-engine) metadata server written in python.
The official MetadataServer provided by EPIC must be deployed on the windows server with IIS and .NET installed. For many developers, using Windows in a production environment is much more expensive than Linux. The intention of this project is to provide a set of ugs server environment that can be deployed easily and quickly.

## Setup
It is recommended to deploy through docker. Before deployment, you need to install [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) environment on the host machine. Then copy `devops` folder to your host machine, run the following command to start the server:
```shell
docker-compose up -d
```
This docker-compose environment uses two docker images, including `thejinchao/ugs-python:latest` and `mysql:8.0`.

## Modify listen port
The default listen port is 5001. If you need to modify it, you can edit the `docker-compose.yml` file and modify the environment value of `UGS_LISTEN_PORT`.

## Test
Open any browser, enter the address of the server, for example `http://ugs.thecodeway.com:5001`, if it works properly, it should be displayed as follows:
```
UnrealGameSync Metadata Server(Python Version)
```

## Configure project
If you use the server in the project, need to modify the `Build/UnrealGameSync.ini` file in the project directory:
```
[Default]
ApiUrl=http://ugs.thecodeway.com:5001
```
