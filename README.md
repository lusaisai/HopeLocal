# Hope
Hope is a proxy application.
* [HopeLocal](https://github.com/lusaisai/HopeLocal) runs services in local servers.
* [HopeServer](https://github.com/lusaisai/HopeServer) runs services on google app engine.

Here is an overview of the architecture
![architecture](https://raw.githubusercontent.com/lusaisai/HopeLocal/master/docs/architecture.png)

## Setup
### HopeLocal

#### Prerequisites
* [Python2.7](https://www.python.org/downloads/)

#### Steps
1. Download the repository.
2. Install python dependencies, run **pip install -r requirements.txt** on command line. (Tip: On Windows, you can use shift+rightclick to open cmd from the explorer)
3. Run **start_services.pyw** to start the services.

Front server listens on **127.0.0.1:5000** by default.

### HopeServer
#### Prerequisites
* [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads)

#### Steps
1. Download the repository.
2. Create projects(applications) from [google console](https://console.developers.google.com/project).
3. Modify **upload.cmd** accordingly and run it.

## Settings
Modify **settings.py** or create a **user_settings.py** to override default settings.

## Certificate Authority
About https, Hope will create a file **certs/hopeca.crt**, install(import) it to your system(browser) so it can be trusted.
