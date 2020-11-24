from utils import detector_utils as detector_utils
from utils import pose_classification_utils as classifier
import cv2
import tensorflow as tf
import multiprocessing
from multiprocessing import Queue, Pool
import time
from utils.detector_utils import WebcamVideoStream
import datetime
import argparse
import os;
os.environ['KERAS_BACKEND'] = 'tensorflow'
import keras
import gui
import autopy
import time

frame_processed = 0
score_thresh = 0.18

# Create a worker thread that loads graph and
# does detection on images in an input queue and puts it on an output queue
#グラフをロードするワーカースレッドを作成し、
#入力キュー内の画像を検出し、出力キューに配置します


def worker(input_q, output_q, cropped_output_q, inferences_q, cap_params, frame_processed):
    print(">> loading frozen model for worker")
    detection_graph, sess = detector_utils.load_inference_graph()
    sess = tf.Session(graph=detection_graph)

    print(">> loading keras model for worker")
    try:
        model, classification_graph, session = classifier.load_KerasGraph("cnn/models/hand_poses_wGarbage_10.h5")
    except Exception as e:
        print(e)
    p1 = 0
    p2 = 0
    p1_pre = 0
    p2_pre = 0
    p1_att = 0
    p2_att = 0
    while True:
        #print("> ===== in worker loop, frame ", frame_processed)
        frame = input_q.get()
        if (frame is not None):
            # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
            # while scores contains the confidence for each of these boxes.
            # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)
            #実際の検出。 変数ボックスには、検出された手の境界ボックスの座標が含まれています。
            #スコアには、これらの各ボックスの信頼度が含まれています。
            #ヒント：len（boxes）> 1の場合、（スコアのしきい値内で）少なくとも片方の手を見つけたと見なすことができます。
            boxes, scores = detector_utils.detect_objects(
                frame, detection_graph, sess)

            cv2.rectangle(frame, (int(cap_params['im_width'])//20,int(cap_params['im_height'])//20),
                        (int(cap_params['im_width'])-(int(cap_params['im_width'])//20),int(cap_params['im_height'])-(int(cap_params['im_height'])//20)),
                        (255, 9, 1), 1, 1)
            # get region of interest
            #関心領域を取得
            res = detector_utils.get_box_image(cap_params['num_hands_detect'], cap_params["score_thresh"],
                scores, boxes, cap_params['im_width'], cap_params['im_height'], frame)

            #手の判定が一定値を超えたとき
            if (scores[0] > score_thresh):
                (left, right, top, bottom) = (boxes[0][1] * cap_params['im_width'], boxes[0][3] * cap_params['im_width'],
                                              boxes[0][0] * cap_params['im_height'], boxes[0][2] * cap_params['im_height'])

                #ウィンドウサイズを取得
                width,height = autopy.screen.size()

                #画面比率変数設定
                wx = (width + ((int(right)-int(left)))*(width / cap_params['im_width'])) / cap_params['im_width']
                hx = (height + ((int(bottom)-int(top)))*(height / (cap_params['im_height']))) / cap_params['im_height']

                p1 = int(left)*wx
                p2 = int(top)*hx

                #判定した手の範囲を表示
                fp = (int(left),int(top))
                ep = (int(right),int(bottom))
                cv2.rectangle(frame, fp, ep, (77, 255, 9), 1, 1)
                #マウス操作
                try:
                    #座標間移動を何回行うか設定
                    i = 9
                    if(p1 > p1_pre):
                        p1_att = (p1-p1_pre) / i
                    else:
                        p1_att = (p1_pre-p1) / i

                    if(p2 > p2_pre):
                        p2_att = (p2-p2_pre) / i
                    else:
                        p2_att = (p2_pre-p2) / i

                    #座標間移動実行
                    for j in range(i):
                        autopy.mouse.move(p1_pre+p1_att*j,p2_pre+p2_att*j)

                    #座標移動実行
                    autopy.mouse.move(p1,p2)

                #座標がモニターの範囲外の場合のエラーキャッチ
                except ValueError:
                    print('Out of bounds')

            # classify hand pose
            #手のポーズを分類する
            if res is not None:
                class_res = classifier.classify(model, classification_graph, session, res)
                inferences_q.put(class_res)

            # add frame annotated with bounding box to queue
            #バウンディングボックスで注釈が付けられたフレームをキューに追加
            cropped_output_q.put(res)
            output_q.put(frame)
            frame_processed += 1
        else:
            output_q.put(frame)
    sess.close()


if __name__ == '__main__':
    #パーサを作る
    parser = argparse.ArgumentParser()

    #Webカメラの選択
    parser.add_argument(
        '-src',
        '--source',
        dest='video_source',
        type=int,
        default=0,
        help='Device index of the camera.')

    #手を識別する数
    parser.add_argument(
        '-nhands',
        '--num_hands',
        dest='num_hands',
        type=int,
        default=1,
        help='Max number of hands to detect.')

    #FPSを表示するか
    parser.add_argument(
        '-fps',
        '--fps',
        dest='fps',
        type=int,
        default=1,
        help='Show FPS on detection/display visualization')

    #ビデオストリームの横幅
    parser.add_argument(
        '-wd',
        '--width',
        dest='width',
        type=int,
        default=300,
        help='Width of the frames in the video stream.')

    #ビデオストリームの高さ
    parser.add_argument(
        '-ht',
        '--height',
        dest='height',
        type=int,
        default=200,
        help='Height of the frames in the video stream.')

    #OpenCVでのFPSの表示をするか否か
    parser.add_argument(
        '-ds',
        '--display',
        dest='display',
        type=int,
        default=1,
        help='Display the detected images using OpenCV. This reduces FPS')

    #???
    parser.add_argument(
        '-num-w',
        '--num-workers',
        dest='num_workers',
        type=int,
        default=4,
        help='Number of workers.')

    #???
    parser.add_argument(
        '-q-size',
        '--queue-size',
        dest='queue_size',
        type=int,
        default=5,
        help='Size of the queue.')

    #設定項目を変数argsに代入する。
    args = parser.parse_args()

    #各Queue変数の要素数の上限を設定
    input_q             = Queue(maxsize=args.queue_size)
    output_q            = Queue(maxsize=args.queue_size)
    cropped_output_q    = Queue(maxsize=args.queue_size)
    inferences_q        = Queue(maxsize=args.queue_size)

    #初期設定したargsパーサーからWebカメラの指定及びサイズを取得
    video_capture = WebcamVideoStream(
        src=args.video_source, width=args.width, height=args.height).start()

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = video_capture.size()
    print(cap_params['im_width'], cap_params['im_height'])
    cap_params['score_thresh'] = score_thresh

    # max number of hands we want to detect/track
    #検出/追跡する手の最大数
    cap_params['num_hands_detect'] = args.num_hands

    print(cap_params, args)

    # Count number of files to increment new example directory
    #新しいサンプルディレクトリをインクリメントするファイルの数を数える
    poses = []
    _file = open("poses.txt", "r")
    lines = _file.readlines()
    for line in lines:
        line = line.strip()
        if(line != ""):
            print(line)
            poses.append(line)


    # spin up workers to paralleize detection.
    #ワーカーをスピンアップして検出を並列化します。
    pool = Pool(args.num_workers, worker,
                (input_q, output_q, cropped_output_q, inferences_q, cap_params, frame_processed))

    start_time = datetime.datetime.now()
    num_frames = 0
    fps = 0
    index = 0

    cv2.namedWindow('Handpose', cv2.WINDOW_NORMAL)
    poseCount = [0,0,0,0]
    while True:
        frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        index += 1

        input_q.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        output_frame = output_q.get()
        cropped_output = cropped_output_q.get()

        inferences      = None

        try:
            inferences = inferences_q.get_nowait()
        except Exception as e:
            pass

        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        num_frames += 1
        fps = num_frames / elapsed_time

        # Display inferences
        #推論を表示する
        if(inferences is not None):
            gui.drawInferences(inferences,poseCount, poses)

        if (cropped_output is not None):
            cropped_output = cv2.cvtColor(cropped_output, cv2.COLOR_RGB2BGR)
            if (args.display > 0):
                cv2.namedWindow('Cropped', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Cropped', 450, 300)
                cv2.imshow('Cropped', cropped_output)

                #cv2.imwrite('image_' + str(num_frames) + '.png', cropped_output)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (num_frames == 400):
                    num_frames = 0
                    start_time = datetime.datetime.now()
                else:
                    print("frames processed: ", index, "elapsed time: ",
                          elapsed_time, "fps: ", str(int(fps)))


        # print("frame ",  index, num_frames, elapsed_time, fps)

        if (output_frame is not None):
            output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
            if (args.display > 0):
                if (args.fps > 0):
                    detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                     output_frame)
                cv2.imshow('Handpose', output_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (num_frames == 400):
                    num_frames = 0
                    start_time = datetime.datetime.now()
                else:
                    print("frames processed: ", index, "elapsed time: ",
                          elapsed_time, "fps: ", str(int(fps)))
        else:
            print("video end")
            break
    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()
