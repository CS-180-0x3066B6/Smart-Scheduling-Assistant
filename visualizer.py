from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import json
from operator import itemgetter

root = Tk()
root.title("Main")
root.geometry("700x700")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
second_frame = Frame(my_canvas)
my_canvas.create_window((0,0),window=second_frame, anchor="nw")

def days(month):
    if(month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10" or month == "12" ):
        day = "31"
    elif(month == "04" or month == "06" or month == "09" or month == "11" ):
        day = "30"
    else:
        day = "28"
    return day
 
def buttonFunction1(pic1):
    butt1 = Toplevel(root)
    butt1.title("View Subimage")
    butt1.geometry("500x500")
    img = ImageTk.PhotoImage(Image.open(pic1))
    picture = Label(butt1, image=img)
    picture.pack()
    butt1.mainloop()
    
def buttonFunction2(pic2):
    butt2 = Toplevel(root)
    butt2.title("View Image")
    butt2.geometry("500x500")
    img = ImageTk.PhotoImage(Image.open(pic2))
    picture = Label(butt2, image=img)
    picture.pack()
    butt2.mainloop()

datelist =[]
with open("data.json") as f:
    for jsonObj in f:
        datedict = json.loads(jsonObj)
        if(len(datedict["Date"]) == 10):
            date2 = datedict["Date"][-4:] + "-" + datedict["Date"][:3] + datedict["Date"][3:5]   
        elif(len(datedict["Date"]) == 7):
            date2 =  datedict["Date"][-4:] + "-" + datedict["Date"][:3] + days(datedict["Date"][0:2]) 
        else:
            date2 =  datedict["Date"] + "12-31-" 
        datedict.update({"Datesort": date2})
        datelist.append(datedict)

newdatelist = sorted(datelist, key=itemgetter("Datesort"))

for i in range(len(newdatelist)):
    date = Label(second_frame, height = 1, width = 12, text = newdatelist[i]["Date"]) 
    date.grid(row = i, column = 0)
    b1 = Button(second_frame, height = 1, width = 12, text = "View Subimage", command = lambda i=i: buttonFunction1(newdatelist[i]["Subimage_Path"]))
    b1.grid(row = i, column = 1)
    b2 = Button(second_frame, height = 1, width = 12, text = "View Image", command = lambda i=i: buttonFunction2(newdatelist[i]["Image_Path"]))
    b2.grid(row = i, column =2)
root.mainloop()
