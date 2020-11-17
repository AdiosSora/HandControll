import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.layers.normalization import BatchNormalization
import matplotlib.pyplot as plt
import numpy as np

import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import buildPosesDataset as dataset

def train():
    batch_size = 128
    epochs = 10
    learning_rate = 0.01
    model_name = "cnn/models/hand_poses_wGarbage_" + str(epochs) + ".h5"

    # input image dimensions
    #入力画像の寸法
    img_rows, img_cols = 28, 28

    # the data, shuffled and split between train and test sets
    #列車とテストセット間でシャッフルおよび分割されたデータ
    x_train, y_train, x_test, y_test = dataset.load_data(poses=["all"])

    num_classes = len(np.unique(y_test))

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    #クラスベクトルをバイナリクラス行列に変換する
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    ####### Model structure #######
    #model building
    #モデル構築
    model = Sequential()
    #convolutional layer with rectified linear unit activation
    #正規化線形ユニットアクティベーションを使用した畳み込み層
    model.add(Conv2D(32, kernel_size=(3, 3),
                    activation='relu',
                    input_shape=input_shape))
    # 32 convolution filters used each of size 3x3
    # again
    #サイズ3x3のそれぞれを使用した32個の畳み込みフィルター
    model.add(Conv2D(64, (3, 3), activation='relu'))
    # 64 convolution filters used each of size 3x3
    # choose the best features via pooling
    #サイズ3x3のそれぞれを使用した64個の畳み込みフィルター
    #プーリングを介して最高の機能を選択します
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # randomly turn neurons on and off to improve convergence
    #収束を改善するためにニューロンをランダムにオン/オフします
    model.add(Dropout(0.25))
    # flatten since too many dimensions, we only want a classification output
    #次元が多すぎるため平坦化するため、分類出力のみが必要です
    model.add(Flatten())
    # fully connected to get all relevant data
    #すべての関連データを取得するために完全に接続されています
    model.add(Dense(128, activation='relu'))
    # one more dropout for convergence' sake :)
    #収束のためにもう1つドロップアウト:)
    model.add(Dropout(0.5))
    # output a softmax to squash the matrix into output probabilities
    #ソフトマックスを出力して、行列を出力確率に押しつぶします
    model.add(Dense(num_classes, activation='softmax'))
    # categorical ce since we have multiple classes (10)
    #複数のクラスがあるため、カテゴリカルce（10）
    model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer=keras.optimizers.Adam(lr=learning_rate),
                metrics=['accuracy'])

    ####### TRAINING #######
    hist = model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=2,
            validation_data=(x_test, y_test))
    # Evaluation
    #評価
    score = model.evaluate(x_test, y_test, verbose=1)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    model.save(model_name)

    # plotting the metrics
    #メトリックのプロット
    fig = plt.figure()
    plt.subplot(2,1,1)
    plt.plot(hist.history['acc'])
    plt.plot(hist.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='lower right')

    plt.subplot(2,1,2)
    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train()
