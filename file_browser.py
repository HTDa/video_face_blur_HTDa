from tkinter import * 
from tkinter import filedialog
import face_blur_DSFD.video_face_blur as vfb


VIDEO_FILES_PATH = None
OUTPUT_FOLDER = None


window_geo_w = 600
window_geo_h = 250


def browseVideoFiles():
    global VIDEO_FILES_PATH

    f = filedialog.askopenfilenames(
                                    title="Select a file",
                                    filetypes = (("Video files", "*.mp4*"),
                                                ("all files", "*.*")))
    
    # change label contents
    
    # print(f)
    
    f = list(f)
    VIDEO_FILES_PATH = f
    
    display_text = "Files opened: " + str(len(f))
    
    # for f_name in f:
    #     display_text += '\n' + f_name.split('/')[-1] 
    label_browse_files.configure(text=display_text)

    # window_geo = "600x" + str(min(800, max(window_geo_h, 200 + 30*len(f))))
    # window.geometry(window_geo)
    # label_browse_files.configure(height=len(f)+3)
    
    # print(VIDEO_FILES_PATH)


def browseOutputFolder():
    global OUTPUT_FOLDER

    f = filedialog.askdirectory()
    OUTPUT_FOLDER = f
    label_output_path.configure(text="Output Path: " + f)

def blurFiles():
    global VIDEO_FILES_PATH
    global OUTPUT_FOLDER

    video_path_list = VIDEO_FILES_PATH
    output_path = OUTPUT_FOLDER
    
    if video_path_list is not None and output_path is not None:
        print(video_path_list)
        print(output_path)

        for video_path in video_path_list:
            vfb.videoFaceBlur(video_path, output_path)



window = Tk()


window.title("File Explorer")

window.geometry(str(window_geo_w) + "x" + str(window_geo_h))

window.config(background="white")

label_browse_files = Label(window,
                            text="Browse Files",
                            width=85, height=4,
                            fg="blue")


button_browse_files = Button(window,
                        text="Browse Files",
                        command=browseVideoFiles)


label_output_path = Label(window,
                            text="Output Folder: ",
                            width=85, height=3,
                            fg="red")


button_output_path = Button(window,
                            text="Browse Output Folder",
                            command=browseOutputFolder)


button_apply_blur = Button(window,
                        text="Blur Files",
                        command=blurFiles)


button_exit = Button(window,
                    text="Exit",
                    command=exit)


label_browse_files.grid(column=0, row=1)
button_browse_files.grid(column=0, row=2)
label_output_path.grid(column=0, row=3)
button_output_path.grid(column=0, row=4)
button_apply_blur.grid(column=0, row=5)
button_exit.grid(column=0, row=6)

window.mainloop()