

import numpy as np


class Image:
    
    def __init__(self, data: np.ndarray) -> None:
        self.data = data
        self.width = data.shape[1]
        self.height = data.shape[0]
        self.isRgb = True if len(data.shape) == 3 else False
        self.isArgb = True if data.shape[-1] == 4 else False
    
    def getPixel(self,x,y):

        return self.data[x,y] if not self.isArgb else self.data[x,y][-2]
    
    def setPixel(self, x,y, pixel):
        self.data[x,y] = pixel if not self.isArgb else [pixel, pixel, pixel, 255]