# Utilities for object detector.
import numpy as np
import sys
import tensorflow as tf
import os
import pyautogui
from threading import Thread
from datetime import datetime
import cv2
from utils import label_map_util
from collections import defaultdict


detection_graph = tf.Graph()
sys.path.append("..")

# score threshold for showing bounding boxes.
#バウンディングボックスを表示するためのスコアしきい値。
_score_thresh = 0.27

MODEL_NAME = 'hand_inference_graph'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
#凍結検出グラフへのパス。 これは、オブジェクトの検出に使用される実際のモデルです。
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
#各ボックスに正しいラベルを追加するために使用される文字列のリスト。
PATH_TO_LABELS = os.path.join(MODEL_NAME, 'hand_label_map.pbtxt')

NUM_CLASSES = 1
# load label map
#ラベルマップをロード
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Load a frozen infrerence graph into memory
#凍結された推論グラフをメモリにロードする
def load_inference_graph():
    # load frozen tensorflow model into memory
    #凍結されたテンソルフローモデルをメモリにロードする
    print("> ====== loading HAND frozen graph into memory")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    print(">  ====== Hand Inference graph loaded.")
    return detection_graph, sess


# draw the detected bounding boxes on the images
# You can modify this to also draw a label.
#draw the detected bounding boxes on the images
# You can modify this to also draw a label.
#検出された境界ボックスを画像に描画します
#これを変更して、ラベルを描画することもできます。
def draw_box_on_image(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np):
    for i in range(num_hands_detect):
        if (scores[i] > score_thresh):
            (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                          boxes[i][0] * im_height, boxes[i][2] * im_height)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            #print(left)
            #print(top)
            #print(right)
            #print(bottom)

            p3 = ((int(left)+((int(right)-int(left))//2)),(int(top)+((int(bottom)-int(top))//2)))
            p4 = ((int(left)+((int(right)-int(left))//2))+1,(int(top)+((int(bottom)-int(top))//2))+1)

            pyautogui.moveTo((int(left)+((int(right)-int(left))//2)),(int(top)+((int(bottom)-int(top))//2)))
            cv2.rectangle(image_np, p3, p4, (77, 255, 9), 3, 1)

def get_box_image(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np):
    for i in range(num_hands_detect):
        if (scores[i] > score_thresh):
            (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                          boxes[i][0] * im_height, boxes[i][2] * im_height)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))

            return image_np[int(top):int(bottom), int(left):int(right)].copy()


# Show fps value on image.
#画像にfps値を表示します。
def draw_fps_on_image(fps, image_np):
    cv2.putText(image_np, fps, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77, 255, 9), 2)


# Actual detection .. generate scores and bounding boxes given an image
#実際の検出..画像を指定してスコアとバウンディングボックスを生成します
def detect_objects(image_np, detection_graph, sess):
    # Definite input and output Tensors for detection_graph
    #Detection_graphの明確な入力および出力テンソル
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    #各ボックスは、特定のオブジェクトが検出された画像の一部を表します。
    detection_boxes = detection_graph.get_tensor_by_name(
        'detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    #各スコアは、各オブジェクトの信頼度を表します。
     #スコアは、クラスラベルとともに結果画像に表示されます。
    detection_scores = detection_graph.get_tensor_by_name(
        'detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores,
            detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    return np.squeeze(boxes), np.squeeze(scores)


# Code to thread reading camera input.
# Source : Adrian Rosebrock
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
#読み取りカメラ入力をスレッド化するコード。
#出典：エイドリアンローズブロック
#https：//www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
class WebcamVideoStream:
    def __init__(self, src, width, height):
        # initialize the video camera stream and read the first frame
        # from the stream
        #ビデオカメラストリームを初期化し、最初のフレームを読み取ります
        #ストリームから
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        #スレッドがすべきかどうかを示すために使用される変数を初期化します
        #停止する

        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        #スレッドを開始して、ビデオストリームからフレームを読み取ります
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        #スレッドが停止するまで無限にループし続けます
        while True:
            # if the thread indicator variable is set, stop the thread
            #スレッドインジケータ変数が設定されている場合は、スレッドを停止します
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            #それ以外の場合は、ストリームから次のフレームを読み取ります
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        #最近読んだフレームを返す
        return self.frame

    def size(self):
        # return size of the capture device
        #キャプチャデバイスの戻りサイズ
        return self.stream.get(3), self.stream.get(4)

    def stop(self):
        # indicate that the thread should be stopped
        #スレッドを停止する必要があることを示します
        self.stopped = True
