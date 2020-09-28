from pytube import *
from pytube import YouTube
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox, ttk
from threading import *
from PIL import ImageTk, Image

file_size = 0

def progress(stream=None, chunk=None, file_handle=None, reamining=None):
    file_downloaded = (file_size - file_handle)
    per = (file_downloaded / file_size) * 100
    download_progress['value'] = per
    DB.config(text="{:00.0f} % Downloaded".format(per), foreground="white")
    if per == 100:
        download_progress['value'] = 0

def Browse():
    path = askdirectory(initialdir="YOUR DIRECTORY PATH")
    if path is None:
        return
    d_Path.set(path)

def start_download():
    global file_size
    global is_cancelled
    try:
        is_cancelled = False
        link = Link.get()
        folder = d_Path.get()
        ob = YouTube(link, on_progress_callback=progress)
        stream = ob.streams.get_highest_resolution()
        file_size = stream.filesize
        DB.config(text="Please wait......")
        DB.config(state=DISABLED)
        stream.download(folder)
        DB.config(text="Download")
        DB.config(state=NORMAL)
        messagebox.showinfo("COMPLETED", "Download And Save In\n" + folder)

    except Exception as e:
        print(e)
        messagebox.showinfo("ERROR", "Please try again")

def startdownloadThead():
    thread = Thread(target=start_download)
    thread.start()

root = Tk()

root.geometry('500x500')
root.title("YouTube Downloader")
root.iconbitmap('download.ico')
root.config(background="#000000")

Link = StringVar()
d_Path = StringVar()

file = Image.open('Youtube.png')
file = file.resize((500, 300), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(file)
headingIcon = Label(root, image=my_img)
headingIcon.grid(row=1, column=0, columnspan=3)

url = Label(root, text="YouTube URL : ")
url.grid(row=2, column=0)

root.urlText = Entry(root, width=58, textvariable=Link)
root.urlText.grid(row=2, column=1, pady=4, padx=4, columnspan=2)

destination_label = Label(root, text="Destination : ")
destination_label.grid(row=3, column=0)

root.destinationText = Entry(root, width=40, textvariable=d_Path)
root.destinationText.grid(row=3, column=1, pady=5, padx=5)

bB = Button(root, text="Browse", foreground="white", command=Browse, width=10, bg="#00002C", font=("vardana", 10), relief="ridge")
bB.grid(row=3, column=2, pady=2, padx=2)

DB = Button(root, text="Download", foreground="white", command=startdownloadThead, width=20, bg="#00002C", font=("vardana", 10), relief="ridge")
DB.grid(row=5, column=1, pady=10)

download_progress = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
download_progress.grid(row=7, column=1, pady=3, padx=3)

root.mainloop()
