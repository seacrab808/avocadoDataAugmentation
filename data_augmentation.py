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

img = cv2.imread(fileName)

# 이미지 Resize
IMG = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

# 여기서부터 함수는 다 만들고 각자 폴더별로 저장하는 기능도 추가할 예정(폴더별 저장 기능 함수 따로 만들어서 내에서 호출)

# 랜덤으로 crop하는 함수
# : sizing에는 몇 배의 크기로 할지 0.1부터 0.9배까지 지정 가능. 0.8로 사용할 예정
def randomCrop(img, sizing):
    height, width, _ = img.shape
    
    # 이ㅑ미지 크기의 비율로 자를 크기 설정
    crop_height = random.randint(int(height * sizing), int(height * sizing))
    crop_width = random.randint(int(width * sizing), int(width * sizing))
    
    if height < crop_height or width < crop_width:
        raise ValueError("자르려는 사이즈가 이미지보다 큽니다.")
    
    # 랜덤으로 crop할 좌표 선택
    x = random.randint(0, width - crop_width)
    y = random.randint(0, height - crop_height)
    
    # 이미지 자르기
    cropped_img = img[y:y+crop_height, x:x+crop_width]
    
    return cropped_img

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

# contrast 함수

# color shifting 함수


# 이미지 show 함수(테스트용)
cv2.imshow('org', IMG)
cv2.imshow('h', hFlip(IMG))
cv2.imshow('v', vFlip(IMG))
cv2.imshow('h+v', vhFlip(IMG))



cv2.waitKey()
cv2.destroyAllWindows()