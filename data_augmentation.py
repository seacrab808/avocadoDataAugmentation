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

import cv2, sys
import numpy as np
import os
import random

# dataPath = os.path.join(os.getcwd(), 'data_augmentation')
dataOrg = os.path.join(os.getcwd(), 'org')
fileName = os.path.join(dataOrg, 'org_white.jpg')

img = cv2.imread('org/org_white.jpg')

if img is None:
    sys.exit("이미지를 불러오지 못했습니다.")

# 이미지 Resize
IMG = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

# 여기서부터 함수는 다 만들고 각자 폴더별로 저장하는 기능도 추가할 예정(폴더별 저장 기능 함수 따로 만들어서 내에서 호출)

# 랜덤으로 crop하는 함수
# : sizing에는 몇 배의 크기로 할지 0.1부터 0.9배까지 지정 가능. 0.8로 사용할 예정
def randomCrop(img, sizing, num_crops=10):
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
        
        # 크롭된 이미지를 저장
        createFile('org_white', 'randomCrop', crops)
    
    return crops


# hfilp 함수(좌우 반전)
def hFlip(img):
    flipped_img = cv2.flip(img, 1)
    return flipped_img

# vfilp 함수(상하 반전)
def vFlip(img):
    flipped_img = cv2.flip(img, 0)
    return flipped_img

# 좌우, 상하 반전
def vhFlip(img):
    flipped_img = cv2.flip(hFlip(img), 0)
    return flipped_img

# rotate 함수
def rotate(img, angle):
    # 이미지의 중심 좌표 구하기
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    
    # 회전 행렬 생성 (이미지 중심 기준으로 회전)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # 회전 적용
    rotated_img = cv2.warpAffine(img, rotation_matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)
    
    return rotated_img

# contrast 함수
# 0.5 ~ 1.5 사이 추천
def contrast(img, alpha):
    # param alpha : 대비 조정 비율 (1.0은 원본, 1.0 이상은 대비 증가, 1.0 이하는 대비 감소)
    
    # 이미지를 float32로 변환하여 계산 후 다시 unit8로 변환
    # 이미지 처리에서 더 높은 정확도를 위함. 
    # unit8은 0~255범위(소수점을 버리는 정수형 -> 계산 오차 발생 가능성)
    # float32는 소수점까지 계산하여 더 정밀한 결과를 제공
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
    return adjusted

# color shifting 함수
def colorShifting(img, shift_value=50):
    # param shift_value : 각 채널을 얼마나 이동시킬지 설정하는 값(양수, 음수 가능)
    
    # 이미지 복사
    shifted_img = img.astype(np.int32)
    
    # 각 채널에 대해 랜덤하게 값 더하기 또는 빼기
    for i in range(3):  # 0: Blue, 1: Green, 2: Red
        shift = random.randint(-shift_value, shift_value)  # -shift_value ~ shift_value 범위
        shifted_img[:, :, i] = np.clip(shifted_img[:, :, i] + shift, 0, 255)
        
     # 다시 uint8로 변환
    shifted_img = shifted_img.astype(np.uint8)
    
    return shifted_img

# 파일을 생성하는 함수(공통으로 적용할거임)
def createFile(filePath, folderName, arr):
    # param filePath: 저장된 파일 경로 (문자열)
    # param folderName : 파일 이름 (문자열)
    # param funcName : 함수의 이름 (문자열)
    # param arr: 저장할 이미지 데이터 (Numpy 배열)
    
    # 폴더가 없으면 생성
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    
    # 각 이미지에 대해 파일 이름 생성 및 저장
    for i, image in enumerate(arr):
        # 파일 이름 생성
        output_path = os.path.join(folderName, f"{filePath}_{folderName}_{i}.jpg")
        
        # 이미지 저장
        if cv2.imwrite(output_path, image):
            print(f"파일이 성공적으로 저장되었습니다: {output_path}")
        else:
            print(f"파일 저장에 실패했습니다: {output_path}")
    
# 이미지 show 함수(테스트용)
# cv2.imshow('org', IMG)
# cv2.imshow('color shifting', colorShifting(IMG))

randomCrop(IMG, 0.8)

cv2.waitKey()
cv2.destroyAllWindows()