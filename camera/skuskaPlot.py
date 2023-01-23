import tkinter as tk
from PIL import Image, ImageTk
import cv2

class MainWindow():
    def init(self, window, cap):
        self.window = window
        self.cap = cap
        self.width = 1048
        self.height = 200
        self.interval = 20 # Interval in ms to get the latest frame

        # Create canvas for image
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.configure(scrollregion=(0,0,0,480))
        self.canvas.pack(side="left",fill="both",expand=True)


        self.scrollbar = tk.Scrollbar(self.window, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        # Configure the canvas to use the scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Update image on canvas
        self.update_image()

    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format

        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)



if __name__ == '__main__':

    root = tk.Tk()
    frame = tk.Frame(root,width=1080,height=200,background="red")
    frame.pack()

    frame2 = tk.Frame(root,width=1080,height=300,background="green")
    frame2.pack(pady=(10,0))

    MainWindow(frame, cv2.VideoCapture(0))
    root.mainloop()