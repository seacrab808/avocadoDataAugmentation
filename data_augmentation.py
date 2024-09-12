# 1. 배경: 흰색 책상, 우드 테이블
# 2. 데이터 증식 조건
#   2-0 스마트폰으로 사진 촬영 후 이미지 크기를 줄여주자(224x224)
#   2-1 rotate: 회전(15~20도)범위 안에서 어느 정도 각도를 넣어야 인식이 잘 되는가?
#   2-2 hfilp, vfilp: 도움이 되는가?
#   2-3 resize, crop: 가능하면 적용해 보자
#   2-4 파일명을 다르게 저장하자 cf) jelly_wood_rotate_30.jpg
#   2-5 클래스 별로 폴더를 생성
#   2-6 데이터를 어떻게 넣느냐에 따라 어떻게 동작되는지 1~2줄로 요약

# 구성 순서
# 1. 촬영
# 2. 이미지를 컴퓨터로 복사, resize
# 3. 육안으로 확인, 이렇게 사용해도 되는가?
# 4. 함수들을 만든다. resize, crop, hfilp, vfilp, 원본 파일명을 읽어서 파일명을 생성하는 기능은 모든 함수에 있어야 함
# 5. 단일 함수를 검증
# 6. 함수를 활용해서 기능 구현
# 7. 테스트(경우의 수)
# 8. 데이터셋을 teachable machine 사이트에 올려서 테스트
# 9. 인식이 잘 안 되는 케이스를 분석하고 케이스 추가 1~8에서 구현된 기능을 이용

import cv2
import sys
import numpy as np
import os
import random

# 이미지 불러오기
whiteorg = cv2.imread('org/org_white.jpg')
woodorg = cv2.imread('org/org_wood.jpg')

if whiteorg is None:
    sys.exit(f"{whiteorg} 이미지를 불러오지 못했습니다.")
if woodorg is None:
    sys.exit(f"{whiteorg} 이미지를 불러오지 못했습니다.")

# 이미지 Resize
org_white = cv2.resize(whiteorg, (224, 224), interpolation=cv2.INTER_AREA)
org_wood = cv2.resize(woodorg, (224, 224), interpolation=cv2.INTER_AREA)


def createFile(folderName, filePrefix, images):
    """
    여러 이미지 데이터를 주어진 폴더에 저장하는 함수.

    :param folderName: 저장할 폴더 이름 (문자열)
    :param filePrefix: 파일 이름에 붙일 접두사 (문자열)
    :param images: 저장할 이미지 데이터 (리스트)
    """
    # 폴더가 없으면 생성
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    
    # 각 이미지에 대해 파일 이름 생성 및 저장
    for i, image in enumerate(images):
        # 파일 이름 생성
        output_path = os.path.join(folderName, f"{filePrefix}_{i}.jpg")
        
        # 이미지 저장
        if cv2.imwrite(output_path, image):
            print(f"파일이 성공적으로 저장되었습니다: {output_path}")
        else:
            print(f"파일 저장에 실패했습니다: {output_path}")

def randomCrop(img, sizing, filePrefix, num_crops=10):
    height, width, _ = img.shape
    crops = []

    for _ in range(num_crops):
        # 이미지 크기의 비율로 자를 크기 설정
        crop_height = random.randint(int(height * sizing), height)
        crop_width = random.randint(int(width * sizing), width)

        if height < crop_height or width < crop_width:
            raise ValueError("자르려는 사이즈가 이미지보다 큽니다.")

        # 랜덤으로 crop할 좌표 선택
        x = random.randint(0, width - crop_width)
        y = random.randint(0, height - crop_height)

        # 이미지 자르기
        cropped_img = img[y:y+crop_height, x:x+crop_width]
        crops.append(cropped_img)
    
    # 크롭된 이미지 저장
    createFile('randomCrop', filePrefix, crops)
    
    return crops

def hFlip(img, filePrefix):
    flipped_img = cv2.flip(img, 1)
    
    # 플립된 이미지 저장
    createFile('hFlip', filePrefix, [flipped_img])
        
    return flipped_img

def vFlip(img, filePrefix):
    flipped_img = cv2.flip(img, 0)
    
    # 플립된 이미지 저장
    createFile('vFlip', filePrefix, [flipped_img])
    
    return flipped_img

def vhFlip(img, filePrefix):
    flipped_img = cv2.flip(img, -1)
    
    # 플립된 이미지 저장
    createFile('vhFlip', filePrefix, [flipped_img])
    
    return flipped_img

def rotate(img, filePrefix):
    rotated_images = []
    
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    
    for angle in range(10, 360, 10):
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_img = cv2.warpAffine(img, rotation_matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)
        rotated_images.append(rotated_img)
    
    # 회전된 이미지 저장
    createFile('rotate', filePrefix, rotated_images)
    
    return rotated_images

def contrast(img, filePrefix):
    contrasts = []
    
    for i in range(5, 15, 1):
        adjusted = cv2.convertScaleAbs(img, alpha=(i/10), beta=0)
        contrasts.append(adjusted)
        
    # 대비 조정된 이미지 저장
    createFile('contrast', filePrefix, contrasts)
    
    return contrasts

def colorShifting(img, filePrefix):
    shifted_images = []
    
    for value in range(10, 60, 10):
        shifted_img = img.astype(np.int32)
        
        for i in range(3):  # 0: Blue, 1: Green, 2: Red
            shift = random.randint(-value, value)
            shifted_img[:, :, i] = np.clip(shifted_img[:, :, i] + shift, 0, 255)
        
        shifted_img = shifted_img.astype(np.uint8)
        shifted_images.append(shifted_img)
    
    createFile('colorShifting', filePrefix, shifted_images)
    
    return shifted_images

def CreateImages(images, filePrefix):
    randomCrop(images, 0.8, filePrefix)
    hFlip(images, filePrefix)
    vFlip(images, filePrefix)
    vhFlip(images, filePrefix)
    rotate(images, filePrefix)
    contrast(images, filePrefix)
    colorShifting(images, filePrefix)
    print("이미지 생성이 완료되었습니다.")
    

def CreateAll():
    CreateImages(org_white, "org_white")
    CreateImages(org_wood, "org_wood")

CreateAll()

cv2.waitKey(0)
cv2.destroyAllWindows()
