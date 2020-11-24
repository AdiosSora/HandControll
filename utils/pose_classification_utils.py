import cv2
import numpy as np
from tensorflow import Graph, Session
import tensorflow as tf
import os; os.environ['KERAS_BACKEND'] = 'tensorflow'
import keras

#classification
#分類する
def load_KerasGraph(path):
    print("> ====== loading Keras model for classification")
    thread_graph = Graph()
    with thread_graph.as_default():
        thread_session = Session()
        with thread_session.as_default():
            model = keras.models.load_model(path)
            #model._make_predict_function()
            graph = tf.get_default_graph()
    print(">  ====== Keras model loaded")
    return model, graph, thread_session

def classify(model, graph, sess, im):

    #色変換
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    im = cv2.flip(im, 1)

    # Reshape
    #形を変える
    res = cv2.resize(im, (28,28), interpolation=cv2.INTER_AREA)

    # Convert to float values between 0. and 1.
    #0から1までの浮動小数点値に変換します。
    res = res.astype(dtype="float64")
    res = res / 255
    res = np.reshape(res, (1, 28, 28, 1))

    with graph.as_default():
        with sess.as_default():
            prediction= model.predict(res)

    return prediction[0]

def test_classify(model, im):
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    im = cv2.flip(im, 1)

    # Reshape
    #形を変える
    res = cv2.resize(im, (28,28), interpolation=cv2.INTER_AREA)

    # Convert to float values between 0. and 1.
    #0から1までの浮動小数点値に変換します。
    res = res.astype(dtype="float64")
    res = res / 255
    res = np.reshape(res, (1, 28, 28, 1))

    prediction= model.predict(res)

    return prediction[0]

if __name__ == "__main__":
    import keras

    print(">> loading keras model for pose classification")
    try:
        model = keras.models.load_model("cnn/models/hand_poses_win_wGarbage_10.h5")
    except Exception as e:
        print(e)


    # Palm
    print('<< Palm >>')
    im = cv2.imread("Poses/Palm/Palm_1/Palm_1_867.png")
    print(test_classify(model, im))
