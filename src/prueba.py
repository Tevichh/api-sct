import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import pathlib
import cv2

import pathlib
from tensorflow.keras.preprocessing import image_dataset_from_directory

# Rutas y clases (ajustar según tu modelo)
tiposCancer = [
    "actinic keratosis",
    "basal cell carcinoma",
    "healthy",
    "invasive melanoma",
    "melanoma in situ",
    "nevus NOS",
    "seborrheic keratosis",
    "squamous cell carcinoma",
]
ruta_modelo = "src/modeloEntrenado/primerModeloV2.h5"

# Cargar el modelo
modelo = tf.keras.models.load_model(ruta_modelo)





# Función para graficar una imagen y su predicción
def graficar_imagen(imagen, predicciones, etiqueta_real, imagen_url):
    imagen = imagen[0]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(imagen)  # Mostrar la imagen

    etiqueta_prediccion = np.argmax(predicciones)
    color = "blue" if etiqueta_prediccion == etiqueta_real else "red"

    # Mostrar el nombre de la imagen y la predicción
    plt.xlabel(
        f"{tiposCancer[etiqueta_prediccion]} {100 * np.max(predicciones):2.0f}% ({tiposCancer[etiqueta_real]})\n{imagen_url}",
        color=color,
    )


# Función para graficar las probabilidades de las clases
def graficar_valor_arreglo(predicciones, etiqueta_real):
    plt.grid(False)
    plt.xticks(
        range(len(tiposCancer))
    )  # Cambia a range(len(tiposCancer)) si tienes más o menos clases
    plt.yticks([])
    grafica = plt.bar(range(len(tiposCancer)), predicciones, color="#777777")
    plt.ylim([0, 1])

    etiqueta_prediccion = np.argmax(predicciones)
    grafica[etiqueta_prediccion].set_color("red")
    grafica[etiqueta_real].set_color("blue")


# Función principal para consultar examen (obtener predicciones y graficar)
def examenConsulta(imagen_url):
    
    data_dir = pathlib.Path("src/muestrasPacientes/")

    dataset = image_dataset_from_directory(
        data_dir,
        image_size=(120, 120),
        batch_size=32,
        seed=123,
    )

    print(imagen_url)

    """ for images, labels in dataset.take(1):
    # Aquí asumimos que 'dataset.file_paths' es una lista de los nombres de archivo
        for i in range(len(images)):
            if(dataset.file_paths[i] == f"src/muestrasPacientes/examenes/{imagen_url}"):
                print(f"Nombre del archivo: {dataset.file_paths[i]}")
                predicciones = modelo.predict(images)
                print(tiposCancer[np.argmax(predicciones[i])]) """

    for images, labels in dataset.take(1):  # Tomamos un batch de imágenes
        for i in range(len(images)):  # Iteramos sobre las imágenes en el batch
            # Comparamos si la ruta de la imagen coincide con la imagen_url proporcionada
            if dataset.file_paths[i].endswith(imagen_url):  # Comparamos solo el nombre del archivo
                print(f"Nombre del archivo: {dataset.file_paths[i]}")
                
                # Hacemos la predicción para el batch completo
                predicciones = modelo.predict(images)
                
                # Obtener la clase predicha para la imagen actual (i) en el batch
                print(f"Predicción: {tiposCancer[np.argmax(predicciones[i])]}")
                return tiposCancer[np.argmax(predicciones[i])]


    return ""
