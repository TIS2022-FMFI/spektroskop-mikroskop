from tkinter.filedialog import askopenfilename, asksaveasfile, askdirectory, askopenfilenames
import cv2 as cv


class ImportModule:
    @staticmethod
    def importCameraImage():
        """returns path to the image"""
        return askopenfilename(filetypes=[('Images', '*.jpg *.jpeg *.png *.bmp')])


class ExportModule:
    @staticmethod
    def exportImage(image):
        """saves given image"""
        file = asksaveasfile(mode='w', defaultextension=".png")
        if file is None:
            return
        cv.imwrite(file.name, image)
