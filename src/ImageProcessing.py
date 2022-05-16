import matplotlib.pyplot as plt
from numpy import ndarray
import numpy as np
from matplotlib.image import imread, imsave
from Image import Image
import PIL.Image

class ImageProcessing():

    @staticmethod
    def loadImage(path: str):

        try:
            image = PIL.Image.open(path)
            im_arr = np.asarray(image)
            if im_arr.shape[-1] == 4:
                im_arr = im_arr[:,:,2]
            return  Image(im_arr)
        except FileNotFoundError as e:
            print(e.strerror)
        
        

    @staticmethod
    def saveImage(image: Image, fileName: str):

        PIL.Image.fromarray(image.data).save(fileName)


    @staticmethod
    def plotImage(image: Image):
        plt.imshow(image.data)
        plt.show()

