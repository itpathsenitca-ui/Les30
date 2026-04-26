import cv2
import os
import numpy as np
import pickle
from imutils import (
    paths,
)

dataset_path = "dataset"
faces = []
labels = []
label_map = {}
current_label = 0
for person_name in os.listdir(
    dataset_path
):
    person_folder = os.path.join(
        dataset_path,
        person_name,
    )

    label_map[
        current_label
    ] = person_name

    image_paths = list(
        paths.list_images(
            person_folder
        )
    )

    for image_path in image_paths:
        gray = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE,
        )
        resized = cv2.resize(
            gray,
            (
                200,
                200,
            ),
        )

        faces.append(
            resized
        )
        labels.append(
            current_label
        )

    current_label += 1
print(
    f"Загружено {len(faces)} изображений для {current_label} человек(а)."
)

# Создаём и обучаем LBPH-распознаватель
recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=2,
    neighbors=8,
    grid_x=8,
    grid_y=8,
    threshold=80,
)

print(
    "Обучение..."
)
recognizer.train(
    faces,
    np.array(
        labels
    ),
)

model_file = "persons.yml"
recognizer.write(
    model_file
)
print(
    f"Модель сохранена в {model_file}"
)

with (
    open(
        "labels.pickle",
        "wb",
    ) as f
):
    pickle.dump(
        label_map,
        f,
    )
