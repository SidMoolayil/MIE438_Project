import cv2
import numpy as np

# TODO: need to determine these bounds via an "color recognize mode". This color recognize mode should distribute each
# TODO: new color into a bin evenly.


def color_test():
    lowerBound = np.array([10, 50, 50])
    upperBound = np.array([20, 255, 255])

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cam.read()

        img = cv2.resize(img, (340, 220))
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, lowerBound, upperBound)

        kernelOpen = np.ones((5,5))
        kernelClose = np.ones((20,20))

        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
        maskFinal = maskClose

        conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img, conts, -1, (255, 0, 0), 3)

        for i in range(len(conts)):
            x, y, w, h = cv2.boundingRect(conts[i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img,
                        str(i + 1),
                        (x, y + h),
                        font,
                        4,
                        (0, 255, 255))

        cv2.imshow("maskClose", maskClose)
        cv2.imshow("maskOpen", maskOpen)
        cv2.imshow("mask", mask)
        cv2.imshow("cam", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    color_test()