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

On Windows, it's better to add **C:\Python27\;C:\Python27\Scripts;** to your PATH environment variable.

#### Steps
1. Download the repository.
2. Install python dependencies, run **pip install -r requirements.txt** on command line.
3. Run **start_services.cmd** or **start_services.pyw** to start the services. See GUI below for alternative ways of starting the services.

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

## GUI
### Windows
#### Steps
1. Install windows api dependency, run **pip install pypiwin32** on command line.
2. Double click **win32gui_start.pyw** to start the services. A tray icon will be created where you can restart/exit.

### Windows and Linux
#### Steps
1. Install PyQT 4
   * Windows: https://www.riverbankcomputing.com/software/pyqt/download
   * Linux(Ubuntu): sudo apt-get install python-qt4
2. Run **qt_start.pyw** to start the services.


## Tips
1. For Youtube, you'll have a better user experience if you select the video quality directly rather than letting youtube change it automatically.
