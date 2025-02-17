import cv2
import numpy as np

# 이미지 크기 (예: 640x480)
img_width, img_height = 640, 480

# YOLOv5가 출력했다고 가정한 예시 정규화된 바운딩 박스 좌표:
# (center_x, center_y, width, height) 모두 0~1 범위
bbox_norm = [0.5, 0.5, 0.2, 0.3]  # 이미지 중앙에 위치, 너비는 이미지의 20%, 높이는 이미지의 30%

# 정규화된 좌표를 픽셀 좌표로 변환
cx = int(bbox_norm[0] * img_width)
cy = int(bbox_norm[1] * img_height)
w = int(bbox_norm[2] * img_width)
h = int(bbox_norm[3] * img_height)

# 바운딩 박스의 좌측 상단 (x1, y1)와 우측 하단 (x2, y2) 좌표 계산
x1 = cx - w // 2
y1 = cy - h // 2
x2 = cx + w // 2
y2 = cy + h // 2

# 더미 이미지 생성 (검정색 배경)
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

# 바운딩 박스 그리기 (녹색 사각형)
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 바운딩 박스 좌표 정보 텍스트 출력 (원하는 경우 수정)
text = f"Center: ({cx}, {cy}), Size: ({w}, {h})"
cv2.putText(img, text, (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# OpenCV 창에 이미지 표시
cv2.imshow("Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

