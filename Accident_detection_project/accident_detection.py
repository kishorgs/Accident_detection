from tkinter.ttk import Entry
from tkinter import *	
import cv2
import torch

from PIL import Image, ImageFile
from torch import nn
from torch import optim as optim
from torch.optim import lr_scheduler

from torchvision import datasets, models, transforms
from tkinter import Tk, Label, Button, mainloop, StringVar, Toplevel, messagebox
import serial
import time
from pathlib import Path

sent = False

def detect():
    com_val= com_port.get()
    print("Com value: ",com_val)
    ser = serial.Serial("COM"+com_val, 9600)
    global ret,sent,index
    global ret
    basepath = Path("vid")
    files_in_basepath = basepath.iterdir()
    for item in files_in_basepath:
        print(item)
        vid = cv2.VideoCapture("{}".format(item))
        while True:
            if ret == True:
                ret, frame = vid.read()
                try:
                    img = Image.fromarray(frame)
                except ValueError:
                    print(ValueError)
                    break
                except AttributeError:
                    print(AttributeError)
                    break
                img = test_transforms(img)
                img = img.unsqueeze(dim=0)
                img = img.cpu()
                model.eval()
                with torch.no_grad():
                    output = model(img)

                    _, predicted = torch.max(output, 1)

                    index = int(predicted.item())
                    if index == 0:

                        if not sent:
                            print("accident detected")
                            ser.write(b'S')
                            time.sleep(1)
                            sent = True
                    else:
                        sent = False
                    labels = 'status: ' + classes[index]

                cv2.putText(frame, labels, (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
                cv2.imshow('Crash Notifier', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        vid.release()
        cv2.destroyAllWindows()


ImageFile.LOAD_TRUNCATED_IMAGES = True

test_transforms = transforms.Compose([transforms.Resize(255),
                                      #  transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      ])

model = models.densenet161()

model.classifier = nn.Sequential(nn.Linear(2208, 1000),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),
                                 nn.Linear(1000, 2),
                                 nn.LogSoftmax(dim=1))

criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

model = model.cpu()

model.load_state_dict(torch.load('tensorboardexp.pt', map_location=torch.device('cpu')))
classes = ["accident", "noaccident"]
index=0
ret = True
print("Model loaded")


def login():
	
	global login_window

	login_window = Toplevel(root)

	login_window.title("Login page")

	login_window.iconbitmap(icon_path)

	login_window.config(bg=bg_color)

	login_window.geometry(f'{app_width}x{app_height}+{int(X)+20}+{int(Y)+20}')

	global username
	global password
	global username_entry
	global password_entry
	global com_port

	username = StringVar()
	password = StringVar()
	com_port = StringVar()

	Label(login_window,text="Accident",font=('calibre', 12, 'bold'),bg=bg_color).place(x=250,y=25,anchor="center")

	username_label = Label(login_window, text='Username', font=('calibre', 10, 'bold'),bg=bg_color).place(x=100, y=60, anchor="center")
	username_entry = Entry(login_window, textvariable=username, font=('calibre', 10, 'normal'))
	username_entry.place(x=250, y=60, anchor="center")

	password_label = Label(login_window, text='Password', font=('calibre', 10, 'bold'),bg=bg_color).place(x=100, y=110, anchor="center")
	password_entry = Entry(login_window, textvariable=password, font=('calibre', 10, 'normal'))
	password_entry.place(x=250, y=110, anchor="center")

	Button(login_window,text="Submit",command=submit,bg="#800000",fg="white",font=('calibre', 10, 'bold'),activebackground="#800000",activeforeground="white",borderwidth=0,cursor="hand2").place(x=250,y=170,anchor="center",width=120,height=40)



def run_window():
    
    newWindow = Toplevel(login_window)

    newWindow.title("Crash Notifier")

    newWindow.iconbitmap(icon_path)

    newWindow.config(bg=bg_color)


    newWindow.geometry(f'{app_width}x{app_height}+{int(X)+40}+{int(Y)+40}')

    com_label = Label(newWindow, text='Enter Com', font=('calibre', 10, 'bold'),bg=bg_color).place(x=100, y=50, anchor="center")
    com_entry = Entry(newWindow, textvariable=com_port, font=('calibre', 10, 'normal'))
    com_entry.place(x=250, y=50, anchor="center")

    run_btn = Button(newWindow, text="Run", command=detect,bg="#800000",fg="white",font=('calibre', 10, 'bold'),activebackground="#800000",activeforeground="white",borderwidth=0,cursor="hand2")
    run_btn.place(x=250, y=100, anchor="center",width=120,height=40)

def submit():
    username_e = username.get()
    email_e = password.get()

    if username_e=="hi" and email_e=="hi":
        print("welcome")
        username_entry.delete(0,'end')
        password_entry.delete(0, 'end')
        run_window()
    else:
        messagebox.showerror("Error", "Invalid credentials")



root = Tk()

global icon_path
icon_path = "img/car.ico"

root.title("Crash Notifier")

root.iconbitmap(icon_path)

bg_color= "#F4B400"

root.config(bg=bg_color)

global screenwidth
global screenheight
global app_width
global app_height

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

app_width = 500
app_height = 300

X = (screenwidth / 2) - (app_width / 2)
Y = (screenheight / 2) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(X)}+{int(Y)}')


label_1 = Label(root, text='Start accident detection project', font=('calibre', 10, 'bold'),bg=bg_color).place(x=250, y=50, anchor="center")

start_btn = Button(root, text="Start >>", command=login,padx=20,pady=20,bg="#800000",fg="white",font=('calibre', 10, 'bold'),activebackground="#800000",activeforeground="white",borderwidth=0,cursor="hand2")

start_btn.place(x=250, y=100, anchor="center",width=120,height=40)


mainloop()
