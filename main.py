import cv2
from mtcnn import MTCNN
import threading
import time

# Функция для чтения кадров из видеопотока
def read_frames():
    global frame, video_cap

    while True:
        ret, frame = video_cap.read()
        if not ret:
            break

# Функция для обработки и отображения кадров
def process_frames():
    global frame

    detector = MTCNN(scale_factor=0.5, min_face_size=20)  # Настройки для ускорения MTCNN

    while True:
        if frame is not None:
            start_time = time.time()

            # Уменьшаем разрешение видеопотока
            frame_resized = cv2.resize(frame, (640, 480))

            res = detector.detect_faces(frame_resized)
            for face in res:
                box = face['box']
                cv2.rectangle(frame_resized, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)

            cv2.imshow('FaceRec', frame_resized)

            # Подождем, чтобы убедиться, что частота кадров не ниже 30 кадров в секунду
            elapsed_time = time.time() - start_time
            if elapsed_time < 1 / 30:
                time.sleep((1 / 30) - elapsed_time)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


# Глобальная переменная для хранения кадра
frame = None

# Запускаем видеопоток и создаем потоки для чтения и обработки кадров
video_cap = cv2.VideoCapture(0)
read_thread = threading.Thread(target=read_frames)
process_thread = threading.Thread(target=process_frames)

# Запускаем потоки
read_thread.start()
process_thread.start()

# Ожидаем завершения потоков
read_thread.join()
process_thread.join()

# Освобождаем ресурсы и закрываем окно OpenCV
video_cap.release()
cv2.destroyAllWindows()
