import math
import time

import cv2 as cv
import mediapipe as mp
from mediapipe.tasks.python import vision

from visualization import draw_manual, print_RSP_result


MODEL_PATH = "hand_landmarker.task"


def calculate_distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
        + (point1.z - point2.z) ** 2
    )


def is_finger_open(hand_landmarks, tip_index, pip_index):
    wrist = hand_landmarks[0]
    tip = hand_landmarks[tip_index]
    pip = hand_landmarks[pip_index]

    tip_distance = calculate_distance(tip, wrist)
    pip_distance = calculate_distance(pip, wrist)

    return tip_distance > pip_distance


def classify_rps(hand_landmarks):
    index_open = is_finger_open(hand_landmarks, 8, 6)
    middle_open = is_finger_open(hand_landmarks, 12, 10)
    ring_open = is_finger_open(hand_landmarks, 16, 14)
    pinky_open = is_finger_open(hand_landmarks, 20, 18)

    # Rock
    if (
        not index_open
        and not middle_open
        and not ring_open
        and not pinky_open
    ):
        return 0

    # Paper
    if (
        index_open
        and middle_open
        and ring_open
        and pinky_open
    ):
        return 1

    # Scissors
    if (
        index_open
        and middle_open
        and not ring_open
        and not pinky_open
    ):
        return 2

    return None


def create_hand_landmarker():
    base_options = mp.tasks.BaseOptions(
        model_asset_path=MODEL_PATH
    )

    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    return vision.HandLandmarker.create_from_options(options)


def main():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    hand_landmarker = create_hand_landmarker()
    start_time = time.time()

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("카메라 영상을 가져올 수 없습니다.")
                break

            frame = cv.flip(frame, 1)

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame,
            )

            timestamp_ms = int((time.time() - start_time) * 1000)

            detection_result = hand_landmarker.detect_for_video(
                mp_image,
                timestamp_ms,
            )

            rps_result = None

            if detection_result.hand_landmarks:
                hand_landmarks = detection_result.hand_landmarks[0]

                rps_result = classify_rps(hand_landmarks)

                frame = draw_manual(
                    frame,
                    detection_result,
                )

            frame = print_RSP_result(
                frame,
                rps_result,
            )

            cv.imshow("RPS Game", frame)

            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        hand_landmarker.close()
        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()