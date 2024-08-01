import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import shutil
import os

class ProjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project App")
        self.root.configure(bg='#2e2e2e')  # Dark background color

        # Set default window size
        self.root.geometry("1000x800")  # Width x Height

        # Create a Canvas widget for scrolling
        self.canvas = tk.Canvas(self.root, bg='#2e2e2e')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Create a vertical scrollbar
        self.v_scroll = tk.Scrollbar(self.root, orient='vertical', command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky='ns')

        # Create a horizontal scrollbar
        self.h_scroll = tk.Scrollbar(self.root, orient='horizontal', command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky='ew')

        # Create a frame inside the canvas that will hold all the widgets
        self.scrollable_frame = tk.Frame(self.canvas, bg='#2e2e2e')
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Create a window inside the canvas to hold the frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.config(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Set grid weights for the canvas and scrollbars
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create widgets and add them to the scrollable frame
        self.create_widgets()

        # Bind mouse wheel event for scrolling
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def create_widgets(self):
        # Radio buttons for Photo or Video
        self.file_type = tk.StringVar(value="Photo")

        radio_frame = tk.Frame(self.scrollable_frame, bg='#2e2e2e')
        radio_frame.grid(row=0, column=0, columnspan=3, sticky='w')

        tk.Radiobutton(radio_frame, text="Photo", variable=self.file_type, value="Photo",
                       bg='#2e2e2e', fg='white', selectcolor='#3e3e3e', indicatoron=0,
                       relief='flat').pack(side='left', padx=5)
        tk.Radiobutton(radio_frame, text="Video", variable=self.file_type, value="Video",
                       bg='#2e2e2e', fg='white', selectcolor='#3e3e3e', indicatoron=0,
                       relief='flat').pack(side='left', padx=5)

        # Radio button indicator label
        self.radio_label = tk.Label(self.scrollable_frame, text="Selected: Photo", bg='#2e2e2e', fg='white')
        self.radio_label.grid(row=0, column=2, sticky='w')

        # Text boxes for Title and Comment
        tk.Label(self.scrollable_frame, text="Project Title:", bg='#2e2e2e', fg='white').grid(row=1, column=0, sticky='w')
        self.title_entry = tk.Entry(self.scrollable_frame, bg='#3e3e3e', fg='white', insertbackground='white')
        self.title_entry.grid(row=1, column=1, sticky='ew')

        tk.Label(self.scrollable_frame, text="Project Comment:", bg='#2e2e2e', fg='white').grid(row=2, column=0, sticky='w')
        self.comment_entry = tk.Text(self.scrollable_frame, height=5, bg='#3e3e3e', fg='white')
        self.comment_entry.grid(row=2, column=1, sticky='ew')

        # Drag and drop or Browse for Thumbnail
        tk.Label(self.scrollable_frame, text="Thumbnail:", bg='#2e2e2e', fg='white').grid(row=3, column=0, sticky='w')
        self.thumbnail_entry = tk.Entry(self.scrollable_frame, bg='#3e3e3e', fg='white', insertbackground='white')
        self.thumbnail_entry.grid(row=3, column=1, sticky='ew')
        self.thumbnail_button = tk.Button(self.scrollable_frame, text="Browse", command=self.browse_thumbnail, bg='#4e4e4e', fg='white')
        self.thumbnail_button.grid(row=3, column=2, sticky='ew')
        self.thumbnail_label = tk.Label(self.scrollable_frame, bg='#2e2e2e')
        self.thumbnail_label.grid(row=4, column=1, pady=10)

        # Drag and drop or Browse for Content
        tk.Label(self.scrollable_frame, text="Content:", bg='#2e2e2e', fg='white').grid(row=5, column=0, sticky='w')
        self.content_entry = tk.Entry(self.scrollable_frame, bg='#3e3e3e', fg='white', insertbackground='white')
        self.content_entry.grid(row=5, column=1, sticky='ew')
        self.content_button = tk.Button(self.scrollable_frame, text="Browse", command=self.browse_content, bg='#4e4e4e', fg='white')
        self.content_button.grid(row=5, column=2, sticky='ew')
        self.content_label = tk.Label(self.scrollable_frame, bg='#2e2e2e')
        self.content_label.grid(row=6, column=1, pady=10)

        # Submit button
        self.submit_button = tk.Button(self.scrollable_frame, text="Submit", command=self.submit, bg='#4e4e4e', fg='white')
        self.submit_button.grid(row=7, columnspan=3, pady=10)

    def on_frame_configure(self, event):
        # Update scroll region after the frame is configured
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        # Scroll the canvas based on the mouse wheel movement
        if event.num == 5 or event.delta == -120:  # For down scrolling
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:  # For up scrolling
            self.canvas.yview_scroll(-1, "units")

    def browse_thumbnail(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.thumbnail_entry.delete(0, tk.END)
            self.thumbnail_entry.insert(0, file_path)
            self.display_image(file_path, self.thumbnail_label)

    def browse_content(self):
        file_types = [("PNG files", "*.png"), ("MP4 files", "*.mp4")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.content_entry.delete(0, tk.END)
            self.content_entry.insert(0, file_path)
            if file_path.lower().endswith('.png'):
                self.display_image(file_path, self.content_label)
            else:
                self.content_label.config(image='')

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith('.png'):
                if not self.thumbnail_entry.get():
                    self.thumbnail_entry.delete(0, tk.END)
                    self.thumbnail_entry.insert(0, file)
                    self.display_image(file, self.thumbnail_label)
                else:
                    self.content_entry.delete(0, tk.END)
                    self.content_entry.insert(0, file)
                    self.display_image(file, self.content_label)
            elif file.lower().endswith('.mp4'):
                self.content_entry.delete(0, tk.END)
                self.content_entry.insert(0, file)
                self.content_label.config(image='')
            else:
                messagebox.showerror("Error", "Unsupported file format")

    def display_image(self, file_path, label):
        img = Image.open(file_path)
        width, height = img.size
        img = img.resize((int(width * 0.35), int(height * 0.35)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

    def submit(self):
        project_type = self.file_type.get()
        title = self.title_entry.get()
        comment = self.comment_entry.get("1.0", tk.END).strip()
        thumbnail = self.thumbnail_entry.get()
        content = self.content_entry.get()

        if not title or not thumbnail or not content:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # For now, we'll just print the collected information to the console
        print(f"Project Type: {project_type}")
        print(f"Title: {title}")
        print(f"Comment: {comment}")
        print(f"Thumbnail: {thumbnail}")
        print(f"Content: {content}")

    # Non-ChatGPT code **************************************************
        # Image/Video Copying Logic
        if thumbnail.split('/')[-1] not in os.listdir('./images/Blender Pics/') and content.split('/')[-1] not in os.listdir('./images/Blender Pics/'):
            if thumbnail == content:
                shutil.copy(thumbnail, './images/Blender Pics/')
            else:
                shutil.copy(thumbnail, './images/Blender Pics/')
                shutil.copy(content, './images/Blender Pics/')
        else:
            messagebox.showerror("Error",  "File already exists.")
            return
        
        if title + '.txt' not in os.listdir('./descriptions/'):
            with open('./descriptions/' + title + '.txt', 'w') as f:
                f.write(comment)
            f.close()
        else:
            messagebox.showerror("Error", "Description File already exists.")
            return
        

    # *******************************************************************

        # Add your logic here to handle the data
        messagebox.showinfo("Success", "Project submitted successfully!")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ProjectApp(root)
    root.mainloop()