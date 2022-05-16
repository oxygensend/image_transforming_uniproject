from calendar import c
from enum import unique
from os import setpgid
from turtle import width
from Image import Image
import numpy as np
from ImageProcessing import ImageProcessing as IP
import math

class ImageTransformations:

    @classmethod
    def affination(cls,image: Image, T: np.ndarray):
        

        affArr = np.linalg.inv(T)

        k = 3 if image.isRgb else 1

        temp = [0, 0, 0]
        for l in range(k):
            temp[l] = 1
            output_img = Image(np.zeros_like(image.data))
            for i in range(image.height):
                for j in range(image.width):
                    x = int(j* affArr[0,0] + i * affArr[1,0])
                    y = int(j * affArr[0,1] + i * affArr[1,1])

                    if (x>=0 and x < image.width)  and (y>=0 and y < image.height):
                        px = image.getPixel(y,x);

                        if(image.isRgb):
                            output_img.setPixel(i,j, px * temp)
                        else:
                            output_img.setPixel(i,j,px) 

            temp[l] = 0
            IP.saveImage(output_img, f'result{l}_affine.png');
        return 1

    @classmethod
    def dilate(cls,image: Image, se: np.ndarray):

        outImage = Image(np.zeros_like(image.data))

        
        half_height_se = se.shape[0] //2
        half_width_se = se.shape[1] //2

        for i in range(image.height):
            for j in range(image.width):
                max = 0

                for k in range(se.shape[0]):
                    if (i+k-half_height_se) < 0 or (i+k-half_height_se) >= image.height:
                        continue

                    for l in range(0, se.shape[1]):
                        
                        if (k == i and l == j) or se[k][l] != 1:
                            continue
                        if (j+l-half_width_se) < 0 or (j+l-half_width_se) >= image.width:
                            continue
                        if image.getPixel(i+k-half_height_se, j+l-half_width_se) > max:
                            max = image.getPixel(i+k-half_height_se, j+l-half_width_se)

                outImage.setPixel(i,j,max)


        return outImage

    @classmethod
    def erode(cls, image: Image, se: np.ndarray):

        outImage = Image(np.zeros_like(image.data))

        half_height_se = se.shape[0] //2
        half_width_se = se.shape[1] //2
        
        for i in range(image.height):
            for j in range(image.width):
                min = 255

                for k in range(se.shape[0]):
                    if (i+k-half_height_se) < 0 or (i+k-half_height_se) >= image.height:
                        continue

                    for l in range(0, se.shape[1]):
                        
                        if (k == i and l == j) or se[k][l] != 1:
                            continue
                        if (j+l-half_width_se) < 0 or (j+l-half_width_se) >= image.width:
                            continue

                        if image.getPixel(i+k-half_height_se, j+l-half_width_se) < min:
                            min = image.getPixel(i+k-half_height_se, j+l-half_width_se)


                outImage.setPixel(i,j, min)



        return outImage
   

    @classmethod
    def closeWithCircle(cls, image: Image,r):

        se = np.array( [[  int(np.sqrt( (r-i)**2 + (r-j)**2 ) <= r)  for i in range(0, 2*r+1) ] for j in range(0,2*r+1)  ])

        image = cls.dilate(image,se)
        image = cls.erode(image,se)

        return image


    @staticmethod
    def calculate_hist(src):

        histogram = np.zeros(256)
        for y in src:
            histogram[y]+=1

        return histogram
        
    @classmethod
    def entropy(cls,image: Image):
        
        N = image.width * image.height

        histogram = 0
        if image.isRgb:
            for i in range(3):
                histogram += cls.calculate_hist(image.data[:,:,i].flatten())
            histogram = histogram/(N*3)
        else:
            histogram = cls.calculate_hist(image.data.flatten())/N


        histogram = histogram[histogram > 0]
        return - np.sum(np.multiply(np.log(histogram), histogram))

    @classmethod
    def entropy_filter(cls,image: Image, mask):
        
        mask_half = math.floor(mask/2)
        result_image = np.zeros((image.height, image.width))

        for i in range(image.height):
            for j in range(image.width):

                kx =  np.max([0, j- mask_half])
                lx = np.min([image.width, j + mask_half])
                ky = np.max([0, i - mask_half])
                ly = np.min([image.height, i + mask_half])
                region = image.data[ky:ly, kx:lx]

                res = cls.entropy(Image(region))
                result_image[i, j] = res

        # Normalization
        entropyMin = min(result_image.flatten())
        entropyMax = max(result_image.flatten())
        result_image = (result_image - entropyMin) / (entropyMax - entropyMin) * 255
        result_image = result_image.astype(np.uint8)

        return Image(result_image)

    # For hit_miss purpose
    @classmethod
    def erode2(cls,image, se):
   
        result_image = np.zeros_like(image)
        height, width = image.shape
        mask_y, mask_x = se.shape
        mask_half_x = mask_x // 2
        mask_half_y = mask_y // 2

        for i in range(math.ceil(mask_y / 2), height -  mask_half_y):
            for j in range(math.ceil(mask_x / 2), width - mask_half_x):

                cut = image[i - mask_half_y:i + mask_half_y + 1, j - mask_half_x: j + mask_half_x+ 1]
                result_image[i, j] = min(cut[ se ==1])

        return result_image

    @classmethod
    def convex_hull(cls,image: Image):
       
        se1 = np.array([[1, 1, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int)
        se2 = np.array([[1, 1, 1], [1, -1, 0], [0, -1, 0]], dtype=np.int)


        compare = np.zeros(image.data.shape)
        result_image = image.data

        while not np.array_equal(result_image, compare):
            compare = result_image

            for i in range(4):
                result_image = result_image | cls.hit_miss(result_image, se1)
                result_image = result_image | cls.hit_miss(result_image, se2)
                se1 = np.rot90(se1)
                se2 = np.rot90(se2)


        return Image(result_image)

    @classmethod
    def hit_miss(cls,image_data: np.ndarray, se):
    
        true_mask = se * (se == 1)
        false_mask = se * (se == -1) * -1

        result_image = cls.erode2(image_data, true_mask) & cls.erode2(~image_data, false_mask)

        return result_image



       