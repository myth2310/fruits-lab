import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Direktori dataset (ubah sesuai folder dataset kamu)
train_dir = 'dataset/train'   # folder training dengan subfolder kelas
val_dir = 'dataset/validation'  # folder validation

# Parameter input gambar
img_height, img_width = 100, 100
batch_size = 32

# --- Buat ImageDataGenerator dengan augmentasi untuk training ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

# --- Load dataset dari folder dan otomatis deteksi kelas ---
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'  # untuk klasifikasi multi kelas pakai categorical
)

validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical'
)

# --- Cek kelas dan jumlah kelas dari data yang dimuat ---
class_indices = train_generator.class_indices
print("Mapping kelas:", class_indices)

num_classes = len(class_indices)
print("Jumlah kelas:", num_classes)

# --- Bangun model CNN ---
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')  # output sesuai jumlah kelas
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# --- Training model ---
epochs = 50
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator
)

# --- Simpan model ---
model.save('model_klasifikasi_buah.h5')
print("Model disimpan sebagai model_klasifikasi_buah.h5")
