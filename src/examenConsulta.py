import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
from PIL import Image


ruta_modelo = "src/modeloEntrenado/mejor_modelo_hmn.h5"


def examenConsulta(nombre_imagen):

    nombre_imagen = f"src/muestrasPacientes/{nombre_imagen}"

    print(nombre_imagen)

    modelo = tf.keras.models.load_model(ruta_modelo)

    img = Image.open(nombre_imagen)
    img = img.convert("RGB")
    img = np.array(img).astype(float) / 255
    img = cv2.resize(img, (224, 224))

    predicciones = modelo.predict(img.reshape(-1, 224, 224, 3))
    clase_predicha = np.argmax(predicciones[0], axis=-1)

    """ print(f"Clase predicha: {clase_predicha}")

    plt.imshow(img)
    plt.axis("off")
    plt.title("Imagen Cargada")
    plt.show() """

    return clase_predicha
