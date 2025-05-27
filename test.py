import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Path model dan gambar test
model_path = 'model_klasifikasi_buah.h5'
test_image_path = 'download.jpg'  # Ganti dengan gambar yang mau dites

# Load model
model = load_model(model_path)

# Ukuran input gambar sesuai model
img_height, img_width = 100, 100

# Load dan preprocess gambar
img = image.load_img(test_image_path, target_size=(img_height, img_width))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)  # Tambahkan dimensi batch

# Mapping kelas dari hasil training
class_indices = {'apel hijau': 0, 'apel merah': 1, 'unknown': 2}  # Sesuaikan dengan training
index_to_class = {v: k for k, v in class_indices.items()}

# Prediksi
predictions = model.predict(img_array)
predicted_class_index = np.argmax(predictions[0])
predicted_class = index_to_class[predicted_class_index]
confidence = predictions[0][predicted_class_index]

print(f"Prediksi kelas: {predicted_class} dengan confidence: {confidence:.4f}")
