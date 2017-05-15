**Repository for developement of the Weather App.**

Main language: Python 3.6

GUI created using: tkinter v. 8.6.

Internet communication library: requests v. 2.13.0.

`Goal: To create a visual representation of a weather report obtained via Open Weather API. `

I created this simple application to apply in practice knowledge gained in the past 3 months and give myself a challenge and coding exercise which does not end after writing one algorithm.

The aim of refactoring the original "all in one file" approach is to learn to isolate main parts of the application from each other to allow for developing more complicated structures in the future without tying up the components to each other unnecessarily.

During the development I have found out that due to the construction of the tkinter library it is necessary to provide the root Tk() object not only for the View which will use it for its widgets but also for the Controller which requires it to create tkinter special variables like StringVar etc.

Since there can be only on active Tk() object at any time we launch our View class first which inherits from this object and then create Controller object inside the view class.

Still the View is not aware in any way of the Model and vice versa.

Architecture which I will try to implement: Model-View-Adapter (Mediating-Controller).

Due to that some naming conventions have to be established and kept at all times to allow us to quickly, at a glance be able to get the meaning of the call without digging deep into the code.

Naming convention for actions which will be passed between the Model - Controller and View:
    
    View:
        begin_action()
        
    Controller:
        action()
        
    Model:
        finish_action

For example to obtain a weather report after user presses the search button:

    View:
        begin_get_report()
        
    Controller:
        get_report()
    
    Model:
        finish_get_report()
    
    
