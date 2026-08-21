"""
Computer Vision(opencv:Open Source Computer Vision 라이브러리 사용)
"""

# 설치 코드 -> pip install opencv-python
# 안되면 conda install opencv-python
import cv2

print(cv2.__version__)
#5.0.0
img1 = cv2.imread('test18john.jpeg')
print(type(img1))
#<class 'numpy.ndarray'>

cv2.imshow('image test: ',img1)
cv2.waitKey()
cv2.destroyAllWindows()
print('end')

#이미지 다른 이름으로 저장
cv2.imwrite('test18Mayer.jpg',img1)
cv2.imwrite('test18jm.jpg',img1,[cv2.IMWRITE_JPEG_QUALITY,1])
cv2.imwrite('test18jmcp.jpg',img1,[cv2.IMWRITE_JPEG2000_COMPRESSION_X1000,150000])


#이미지 크기 조정
img2 =cv2.resize(img1,(300,100),interpolation=cv2.INTER_AREA)
cv2.imwrite('test18cut.jpg',img2)


#밝기 상하좌우 회전 자르기 다 가능