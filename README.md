**Repository for developement of the Weather App.**

Main language: Python 3.6

GUI created using: tkinter v. 8.6.

Internet communication library: requests v. 2.13.0.

`Goal: To create a visual representation of a weather report obtained via Open Weather API. `

The APIs used for this project:
 
 https://openweathermap.org/api - weather data
 http://api.geonames.org/timezone - time zone from geolocation service

I created this simple application to apply in practice knowledge gained in the past months of learning Python 3 and give myself a challenge and coding exercise which does not end after writing one algorithm.

The aim of refactoring the original "all in one file" approach is to learn to isolate main parts of the application from each other to allow for developing more complicated structures in the future without tying up the components to each other unnecessarily.

During the development I have found out that due to the construction of the tkinter library it is necessary to provide the root Tk() object not only for the View which will use it for drawing of its widgets but also for the Controller which requires it to create tkinter special variables like StringVar etc.

Since there can be only one active Tk() object at any time we launch our View class first which inherits from this object and then create Controller object inside the view class.

Still the View is not aware in any way of the Model and vice versa.

Architecture which I will try to implement: Model-View-Adapter (Mediating-Controller).

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

    weather_dicts: {
                    "metric": [{w_d_cur}, {w_d_short}, {w_d_long}]
                    "imperial": [{w_d_cur}, {w_d_short}, {w_d_long}]
                   } 
      





    
