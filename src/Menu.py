from unittest import result
from ImageProcessing import ImageProcessing as IP
from ImageTransformations import ImageTransformations as IT
import numpy as np
class Menu:

    @staticmethod
    def affination():
        path = input("Input the path for image to be transformed: ")
        img = IP.loadImage(path)
        T = Menu._get_input()
        if(IT.affination(img, T)):
            print("Our image has been transformed, check in files for 'resultX_affine.png'")

    @staticmethod
    def closeWithCircle():
        path = input("Input the path for image(Only mono/bin): ")
        r = int(input("Enter radius: "))
        img = IP.loadImage(path)
        result = IT.closeWithCircle(img, r)
        if(result):
            print("Your image has been transformed, find in files 'result_closeWithCircle.png'")
        IP.saveImage(result, 'result_closeWithCircle.png')

    @staticmethod
    def entropyFilt():
        path = input("Input the path for image to filter: ")
        img = IP.loadImage(path)
        se = int(input("Enter mask(eg.2,5,4): "))
        result = IT.entropy_filter(img, se)
        if(result):
            print("Your image has been transformed, check in files for 'entropy_filter.png'")
        IP.saveImage(result, 'entropy_filter.png')

    @staticmethod
    def convexHull():
        path = input("Input path for image(only bin): ")
        img = IP.loadImage(path)
        result = IT.convex_hull(img)
        if(result):
            print("Your image has been transformed, check in files for 'convex_hull.png'")
        IP.saveImage(result, 'convex_hull.png')
    
    @staticmethod
    def exit():
        exit()

    @staticmethod
    def _get_input():
        print('Podaj 4 liczby(double) do przeształcenia afinicznego')
        return np.array([[ input(f"A[{j}][{i}] = ") for i in range(2)] for j in range(2)], dtype=np.float64)
