# virtual-school-controller

### About ###
A simple python statusbar app for Macos to open Webex/Zoom links at specified times. 
Built using rumps and py2app.

### Download ###
Download the latest _VirtualSchoolController.zip_ [here](https://github.com/MatthewOates36/virtual-school-controller/releases/download/v0.1-alpha/VirtualSchoolController.zip) or from the releases section on the right sidebar.

### Getting Started ###
* Unzip the file and move _Virtual School Controller.app_ to desired location
* Start app by double clicking on it - the app can also be added as a start item to your user so the app will run on startup
* Make a .json file anywhere on your machine - text edit is a good app for this
* Configure .json file using the _virtual-school.json_ file in this project as an example
* Point the program to the absolute path of your file with the _Set config file path_ button in the statusbar menu
* You should see all configured classes in the _Class options_ section of the statusbar menu if the app has been configured properly

### Features ###
* Config classes with json file, which is automatically read by the app upon user edit
* Next class display in statusbar menu
* Pause button to temporarily stop notifications and joining classes
* Class list in statusbar menu with ability to quickly join class and add a one time class meeting without config file editing 
* Low overhead statusbar app designed to run using minimal system resources
