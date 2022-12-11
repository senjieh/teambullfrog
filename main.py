import routeFinder
import tkinter as tk
from tkinter import BOTH, END, LEFT
import json

import DBManager
import routeFinder



# Function called when button is clicked
def my_upd():

    t3.delete('1.0', END)
    # origin and destination strings which can be then passed to back end code
    origin = t1.get('1.0', END)
    destination = t2.get('1.0', END)

    # Array of array of json objects. Routes[flights[{}]]. Each route has multiple flights. Each flight has json data.
    groupArrays = routeFinder.getRoute((origin).rstrip(), destination.rstrip())

    print(groupArrays)
    
    # Update string with data given the array above
    output = make_string(groupArrays)

    # insert to textbox and delete others
    t3.insert(tk.END,output)
    t1.delete('1.0',END)
    t2.delete('1.0',END)

# Create string given an array of json object arrays
def make_string(jsonArray):
    mystr = ""
    # counter for routes
    routeCounter = 1
    # for each route in in the array
    for route in jsonArray:
        mystr += "--------Route {}--------\r\n".format(routeCounter)
        # counter for number of flights in the route
        flightCounter = 1
        # for each flight in the route
        for item in route:
            mystr += "Flight {} ({}):\r\n".format(flightCounter,get_stop(flightCounter, len(route)))
            # update flight counter
            flightCounter += 1
            # for each key in the flight data
            for key in item:
                try:
                    mystr += "{}: {}\r\n".format(key,item[key])
                except:
                    mystr = mystr
            mystr += "\r\n"
        mystr += "\r\n"
        # update route counter
        routeCounter += 1
    # return string
    return mystr

# For labeling purposes
def get_stop(count, length):
    # if count is one then this is the first flight
    if (count == 1):
        return "From Origin to Stop {}".format(count)
    # if count < length this a midway flight
    elif (count < length):
        return "Stop {} to Stop {}".format(count-1, count)
    # else this is the last flight until the final destination
    else:
        return "From Stop {} To Destination".format(count-1)

# Create pop up box
my_w = tk.Tk()
my_w.geometry("850x600")


# Create label for Aiport A fffde3
l1 = tk.Label(my_w,text='Origin Airport')
l1.grid(row=1,column=1)
# Create textbox for Aiport A input
t1 = tk.Text(my_w,height=1,width = 15,bg='#ada9a8')
t1.grid(row=1,column=2)

# Create label for Aiport B
l2 = tk.Label(my_w,text='Destination Airport')
l2.grid(row=2,column=1)
# Create textbox for Aiport B input
t2 = tk.Text(my_w,height=1,width = 15,bg='#ada9a8')
t2.grid(row=2,column=2)

# Create output label and textbox
l3 = tk.Label(my_w,text='Most efficient routes:')
l3.grid(row=5,column=2)
t3 = tk.Text(my_w,height=30,width = 80,bg='#ada9a8')
t3.grid(row=8,column=2)

# Add button which will call our method
b1 = tk.Button(my_w,text='Run Search',command=lambda:my_upd())
b1.grid(row=2,column=3)

my_w.mainloop()