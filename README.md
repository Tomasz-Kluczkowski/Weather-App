# Weather App

#### Desktop Weather Application for Linux and Windows<br>
Author: Tomasz Kluczkowski<br>
Email: tomaszk1@hotmail.co.uk

![Screenshot](https://user-images.githubusercontent.com/26039401/33391594-79bad240-d531-11e7-9826-c2e248f95fae.jpg)

## Installation For End Users:

### Windows:
- Download & run the exe file matching your OS version.
- This will open an installer with default settings.
- Follow the prompts and install in location you prefer.

### Linux:
- Download and extract the archive matching your OS version.
- Start application in terminal using ./Weather_App_32bit or ./Weather_App_64bit depending on your configuration.

## Development:

If you are interested in adding to / modifying this application, here are the main details to get you going:

- Main language: Python 3.6
- GUI created using: tkinter v. 8.6.
- Internet communication library: requests v. 2.13.0.
- Database handling: sqlite3
- Main compiler: cx_Freeze v. 5.0.2 (for creating executable builds)
- Windows Installer compiler: Inno setup compiler v. 5.5.9 (for making an installable version for Windows OS)

There is a set of scripts allowing easy building in Build_scripts folder.

### Installation For Development:

- create and activate virtual environment for project
- cd to project's folder
- pip install -r requirements.txt


## My Goal in This Application:
`To create a visual representation of a weather report obtained via Open Weather API.`

### The APIs used for this project:
 
https://openweathermap.org/api - weather data

Please obtain your unique API key at:
https://home.openweathermap.org/users/sign_up

http://api.geonames.org/timezone - time zone from geolocation service

Please register your unique user name at:
www.geonames.org/login

### Design and further info

Architecture which I implemented: Model-View-Adapter (Mediating-Controller).

Due to that some naming conventions have to be established and kept at all times to allow us to quickly, at a glance be able to get the meaning of the call without digging deep into the code.


Naming convention for actions which will be passed between the View - Controller and Model:
    
    View:
        begin_action()
        
    Controller:
        action()
        
    Model:
        finish_action()

For example to obtain a weather report after user presses the search button:

    View:
        begin_get_report()
        
    Controller:
        get_report()
    
    Model:
        finish_get_report()

Data structure obtained from the API and stored in memory in
finish_get_report: 

    status (tuple): (error_status, [weather_dicts])

    weather_dicts: [
                    "metric": [{w_d_cur}, {w_d_short}, {w_d_long}]
                    "imperial": [{w_d_cur}, {w_d_short}, {w_d_long}]
                   ]
### Data files location
All debug and database files generated by the app will be stored in: 
- C:\Users\\<user_name>\Appdata\Local\ on windows systems.
- /home/<user_name>/.local/share/Weather_App/ on Linux systems.

### Using debug option to load previously generated data   
If you wish you can use the debug option by enabling it in the controller
attributes (switch self.debug to 1). This will load data saved in Debug
folder instead of contacting the API for it. Still you have to make at least
one call or create dicts matching required data set on your own to have the data in the first place.

### Object placement assistance

To help placing objects on the canvas one can enable drawing alignment lines
on the canvas. Switch self.draw_lines to 1 in the controller attributes.
The vertical / horizontal lines have to be turned on / off by commenting
code in gui (look for self.controller.draw_lines ==).
