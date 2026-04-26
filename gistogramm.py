import cv2
import matplotlib.pyplot as plt

# 1. Загружаем обученную модель
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(
    "trained_model_persons.yml"
)

# 2. Извлекаем гистограммы и метки
histograms = recognizer.getHistograms()  # список numpy массивов
labels = recognizer.getLabels()  # список меток (чисел)

print(
    f"Найдено {len(histograms)} классов (людей)."
)
print(
    f"Размер одной гистограммы: {histograms[0].shape}"
)

# 3. Строим гистограмму для первого класса (например)
first_hist = histograms[
    0
].flatten()  # это уже одномерный массив частот

plt.figure(
    figsize=(
        12,
        4,
    )
)
plt.bar(
    range(
        len(
            first_hist
        )
    ),
    first_hist,
    width=1.0,
)
plt.title(
    f"Гистограмма LBP для класса {labels[0]}"
)
plt.xlabel(
    "Индекс бинарного паттерна (по ячейкам)"
)
plt.ylabel(
    "Частота"
)
plt.show()
