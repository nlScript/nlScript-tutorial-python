import requests
from PIL import Image, ImageFilter
from io import BytesIO
import matplotlib.pyplot as plt


class Preprocessing:
    def __init__(self, img):
        self._img = img
        self._fig = None
        self._ax = None
        self._pixelWidth = 1
        self._units = "pixel"

    def open(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        self.setImage(img)

    def show(self):
        self._fig, self._ax = plt.subplots()
        self._ax.imshow(self._img)
        plt.ion()
        plt.show()

    def update(self):
        self._ax.imshow(self._img)
        plt.draw()

    def setImage(self, img):
        self._img = img

    def getImage(self):
        return self._img

    def setPixelWidth(self, pw, units):
        self._pixelWidth = pw
        self._units = units

    def getPixelWidth(self):
        return self._pixelWidth

    def getUnits(self):
        return self._units

    def gaussianBlur(self, sigma):
        img2 = self._img.filter(ImageFilter.GaussianBlur(radius=sigma))
        self._img.paste(img2, (0, 0))
        self.update()

    def medianFilter(self, radius):
        img2 = self._img.filter(ImageFilter.MedianFilter(size=2 * radius + 1))
        self._img.paste(img2, (0, 0))
        self.update()

    def intensityNormalization(self):
        pass

    def subtractBackground(self, radius):
        pass

