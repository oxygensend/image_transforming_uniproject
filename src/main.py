from ImageProcessing import ImageProcessing as IP
from ImageTransformations import ImageTransformations as IT
from Menu import Menu





if __name__ == "__main__":



    while True:

        print("""Choose number of transformation from 0 to 4: 
        1. Affine transform defined by 4 values 
        2. Normalized filtration of entropy in a given window 
        3. Closing with a circular element with a given radius.
        4. Convex surroundings
        0. Exit
        """)


        choosen = int(input())

        if choosen == 1:
            Menu.affination()
        elif choosen == 2:
            Menu.entropyFilt()
        elif choosen == 3:
            Menu.closeWithCircle()
        elif choosen == 4:
            Menu.convexHull()
        else:
            Menu.exit()