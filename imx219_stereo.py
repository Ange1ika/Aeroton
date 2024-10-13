import cv2
import time
import os

# GStreamer пайплайны для IMX219 камер
gst_str_cam1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! nvvidconv flip-method=2 ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
gst_str_cam2 = 'nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! nvvidconv flip-method=2 ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# Открываем две камеры с использованием GStreamer пайплайнов
cam1 = cv2.VideoCapture(gst_str_cam1, cv2.CAP_GSTREAMER)
cam2 = cv2.VideoCapture(gst_str_cam2, cv2.CAP_GSTREAMER)

if not cam1.isOpened():
    print("Не удалось открыть камеру 1.")
if not cam2.isOpened():
    print("Не удалось открыть камеру 2.")

# Захват и сохранение фото
ret1, frame1 = cam1.read()
ret2, frame2 = cam2.read()

# Создаем папки для сохранения фото
if not os.path.exists('photos_cam1'):
    os.makedirs('photos_cam1')

if not os.path.exists('photos_cam2'):
    os.makedirs('photos_cam2')

# Количество фотографий
num_photos = 20

for i in range(num_photos):
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if ret1 and ret2:
        # Сохраняем фото
        cv2.imwrite(f'photos_cam1/photo_{i+1}.jpg', frame1)
        cv2.imwrite(f'photos_cam2/photo_{i+1}.jpg', frame2)

        print(f'Фото {i+1} сохранены.')

        # Задержка между фотографиями в 1.5 секунды
        time.sleep(1.5)
    else:
        print(f'Не удалось захватить изображения с камер на кадре {i+1}.')

# Закрываем камеры
cam1.release()
cam2.release()
cv2.destroyAllWindows()
