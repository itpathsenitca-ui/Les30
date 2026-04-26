#!/usr/bin/env python3

import cv2
from cvzone.FaceDetectionModule import (
    FaceDetector,
)
import os
import time

MAX_IMAGES = 100
person_name = "Maxim"

dataset_path = "dataset"
save_dir = os.path.join(
    dataset_path,
    person_name,
)
os.makedirs(
    save_dir,
    exist_ok=True,
)

cap = cv2.VideoCapture(
    0
)
detector = FaceDetector(
    minDetectionCon=0.7
)
img_counter = 0
last_saved = time.time()
save_interval = 0.3

while True:
    (
        success,
        img,
    ) = cap.read()

    (
        img,
        bboxs,
    ) = detector.findFaces(
        img
    )

    if bboxs:
        bbox = bboxs[
            0
        ][
            "bbox"
        ]
        (
            x,
            y,
            w,
            h,
        ) = bbox
        x = max(
            0,
            x,
        )
        y = max(
            0,
            y,
        )
        w = min(
            w,
            img.shape[
                1
            ]
            - x,
        )
        h = min(
            h,
            img.shape[
                0
            ]
            - y,
        )
        face = img[
            y : y
            + h,
            x : x
            + w,
        ]
        current_time = time.time()
        if (
            current_time
            - last_saved
            >= save_interval
        ):
            filename = f"{person_name}_{img_counter}.jpg"
            filepath = os.path.join(
                save_dir,
                filename,
            )
            cv2.imwrite(
                filepath,
                face,
            )
            print(
                f"Сохранено: {filename}"
            )
            img_counter += 1
            last_saved = current_time
            if (
                img_counter
                == MAX_IMAGES
            ):
                break

        cv2.putText(
            img,
            f"Collected: {img_counter}",
            (
                10,
                30,
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (
                0,
                255,
                0,
            ),
            2,
        )

    cv2.imshow(
        "Collecting Faces",
        img,
    )
    cv2.waitKey(
        1
    )
