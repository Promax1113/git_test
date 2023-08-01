import ttkbootstrap as tkb
import password_processing
import os

def change_label():
    username = username_field.get()
    password = password_field.get()
    result = password_processing.password_check(username, password)
    if result == None:
        result = "Saved Password!"

    label1["text"] = f"Result: {result}"

def first_time():
    if not os.path.isfile("pass.hash"):
        label1["text"] = "Enter the password and username you want to use."
    # TODO Display message the first time

if __name__ == "__main__":
    labeltext = ""



    
    window = tkb.Window(title="Program", themename="flatly", minsize=[960, 540])

    window.bind("<Return>", change_label)

    label1 = tkb.Label(window, text=labeltext)
    first_time()

    username_label = tkb.Label(window, text="Username:")
    username_field = tkb.Entry(window)
    password_label = tkb.Label(window, text="Password:")
    password_field = tkb.Entry(window )
    button = tkb.Button(window, text="window", command=change_label)

    label1.pack()
    username_label.pack()
    username_field.pack()
    password_label.pack()
    password_field.pack()
    
    button.pack()

    window.mainloop()