from utils import detector_utils as detector_utils
from utils import pose_classification_utils as classifier
import hand_gui as hgui
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
import PoseAction
import numpy as np
import gamma
import hand_gui
import eel
import base64

import traceback

frame_processed = 0
score_thresh = 0.18



# Create a worker thread that loads graph and
# does detection on images in an input queue and puts it on an output queue
#グラフをロードするワーカースレッドを作成し、
#入力キュー内の画像を検出し、出力キューに配置します

@eel.expose
def worker(input_q, output_q, cropped_output_q, inferences_q, pointX_q, pointY_q, cap_params, frame_processed):
    print(">> loading frozen model for worker")
    detection_graph, sess = detector_utils.load_inference_graph()
    sess = tf.Session(graph=detection_graph)

    print(">> loading keras model for worker")
    try:
        model, classification_graph, session = classifier.load_KerasGraph("cnn/models/hand_poses_wGarbage_10.h5")
    except Exception as e:
        print(e)
    while True:

        #print("> ===== in worker loop, frame ", frame_processed)
        frame = input_q.get()
        if (frame is not None):
            #実際の検出。 変数ボックスには、検出された手の境界ボックスの座標が含まれています。
            #スコアには、これらの各ボックスの信頼度が含まれています。
            #ヒント：len（boxes）> 1の場合、（スコアのしきい値内で）少なくとも片方の手を見つけたと見なすことができます。
            boxes, scores = detector_utils.detect_objects(
                frame, detection_graph, sess)

            #関心領域を取得
            #フレームの画像サイズを取得
            cropped_height,cropped_width,a = frame.shape[:3]
            res = detector_utils.get_box_image(cap_params['num_hands_detect'], cap_params["score_thresh"],
                scores, boxes, cropped_width,cropped_height, frame)

            #手の判定が一定値を超えたとき
            if (scores[0] > score_thresh):
                (left, right, top, bottom) = (boxes[0][1] * cropped_width, boxes[0][3] * cropped_width,
                                              boxes[0][0] * cropped_height, boxes[0][2] * cropped_height)

                #ウィンドウサイズを取得
                width,height = autopy.screen.size()

                #画面比率変数設定
                # wx = (width + (int(right)-int(left))*(width / cap_params['im_width'])) / cap_params['im_width']
                #
                # hx = (height + (int(bottom)-int(top))*(height / cap_params['im_height'])) / cap_params['im_height']
                # wx = (width + (int(right)-int(left))*(width / cropped_width)) / (cropped_width-20)
                #
                # hx = (height + (int(bottom)-int(top))*(height / cropped_height)) / (cropped_height-20)
                # p1 = int(left)*wx
                # p2 = int(bottom)*hx-(int(bottom)*hx-int(top)*hx)

                hx = (height / cropped_height)*1.2
                wx = (width / cropped_width)*1.2

                p1 = int(left)*wx
                p2 = int(top)*wx

                #判定した手の範囲を表示
                fp = (int(left),int(top))
                ep = (int(right),int(bottom))
                cv2.rectangle(frame, fp, ep, (77, 255, 9), 1, 1)

                #取得した座標(p1,p2)を挿入
                pointX_q.put(p1)
                pointY_q.put(p2)
            #手のポーズを分類する
            if res is not None:
                class_res = classifier.classify(model, classification_graph, session, res)
                inferences_q.put(class_res)

            #バウンディングボックスで注釈が付けられたフレームをキューに追加
            cropped_output_q.put(res)
            output_q.put(frame)
            frame_processed += 1
        else:
            output_q.put(frame)
    sess.close()


if __name__ == '__main__':
    flg_video = 0   #「1」でカメラが接続されていない
    flg_break = 0   #「1」で最初のループを抜け終了する⇒正常終了
    flg_restart = 0 #「1」でリスタートした際に hand_gui.py で eel が2度起動するのを防ぐ
    cnt_gui=0   #hand_guiにてeelを動かす用に使用（0:初回起動時、1:2回目以降起動時、2:カメラが切断された際にhtmlを閉じるために使用）

    while(True):    #カメラが再度接続するまでループ処理
        #try:
            #カメラが接続されていないフラグの場合
            if(flg_video == 1):
                #カメラが接続されているか確認
                cap2 = cv2.VideoCapture(0)
                ret2, frame2 = cap2.read()
                if(ret2 is True):
                    #カメラが接続されている場合
                    flg_video = 0
                    cnt_gui = 0
                    flg_restart = 1
                    print("webcamあったよ！！")
                    continue    #最初の while に戻る
                else:
                    #カメラが接続されていない場合
                    #print("webcamないよ！！！")
                    continue    #最初の while に戻る
            #正常終了のフラグの場合
            elif(flg_break == 1):
                break   #最初の while を抜けて正常終了
            #パーサを作る
            parser = argparse.ArgumentParser()

            #Webカメラの選択
            parser.add_argument(
                '-src',
                '--source',
                dest='video_source',
                type=int,
                default=0,
                # default=hand_gui.cam_source(),
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

            #ワーカーが同時に動く数を設定。
            parser.add_argument(
                '-num-w',
                '--num-workers',
                dest='num_workers',
                type=int,
                default=4,
                help='Number of workers.')

            #FIFO Queueの最大サイズを設定。
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

            pointX_q = Queue(maxsize=args.queue_size)#worker内のp1用
            pointY_q = Queue(maxsize=args.queue_size)#worker内のp2用

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
                        (input_q, output_q, cropped_output_q, inferences_q, pointX_q, pointY_q, cap_params, frame_processed))

            #pool2 = Pool(1,hand_gui.start_gui,(output_q, cropped_output_q))

            start_time = datetime.datetime.now()
            num_frames = 0
            fps = 0
            index = 0

            # 切り抜く色範囲の上限下限を設定
            lower_blue = np.array([0, 30, 60])
            upper_blue = np.array([30, 200, 255])

            cv2.namedWindow('Handpose', cv2.WINDOW_NORMAL)
            poseCount = [0,0,0,0,0,0,0]
            #cnt_gui=0   #hand_guiにてeelを動かす用に使用
            cnt_pose=0  #
            name_pose=""
            flg_end = 0#システム終了フラグ

            while True:
                frame = video_capture.read()
                frame = cv2.flip(frame, 1)

                index += 1
                gamma_config = 1.6

                if(frame is None):
                    #frame が None だと後述の frame = gamma.gamma_correction(frame,gamma_config) で
                    #cv2.error が発生するのでここで判定し、今の while を抜ける
                    traceback.print_exc()
                    #それぞれのフラグを立てて、システムを終了させ、最初の while に戻る
                    flg_video = 1
                    cnt_gui = 2
                    cnt_gui, flg_end, flg_restart = hand_gui.start_gui(output_frame, cnt_gui, cnt_pose, name_pose, flg_restart)
                    pool.terminate()
                    video_capture.stop()
                    cv2.destroyAllWindows()
                    break

                frame = gamma.gamma_correction(frame,gamma_config)
                # cv2.imwrite('Poses/Save/aaa' + str(num_frames) + '.png', frame)
                #画像切り取るかどうか
                frame_cropped_flag = False
                #画面サイズを縮小させ稼働領域の調整を行う
                #各パラメーターに値を入力することで画像サイズを小さくできる
                if(frame_cropped_flag == True):
                    # print(int(cap_params['im_width']))
                    # print(int(cap_params['im_height']))
                    left_params = int(cap_params['im_width'])//8
                    top_params = int(cap_params['im_height'])//8
                    right_params = int(cap_params['im_width'])-(int(cap_params['im_width'])//8)
                    bottom_params = int(cap_params['im_height'])-(int(cap_params['im_height'])//8)

                    #キャプチャした画像の切り取り
                    # frame = frame[top_params:bottom_params,left_params:right_params].copy()
                    frame = frame[100:200,100:200].copy()

                #背景切り抜きの為画像形式をBGRからHSVへ変更
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
                #設定した色範囲を塗りつぶしたマスク画像を生成
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                #生成したマスクで通常画像を切り抜き
                frame_masked = cv2.bitwise_and(hsv,hsv, mask=mask)

                # print(left_params,top_params,right_params,bottom_params)


                #マスク処理済の画像をHSV形式からRGB形式へ変換
                input_q.put(cv2.cvtColor(frame_masked, cv2.COLOR_HSV2RGB))

                # initialize the folder which contents html,js,css,etc

                output_frame = output_q.get()
                cropped_output = cropped_output_q.get()

                #hand_gui.start_gui(output_frame)
                output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
                #output_qの内容表示するためにhand_gui.start_guiへ
                cnt_gui, flg_end, flg_restart = hand_gui.start_gui(output_frame, cnt_gui, cnt_pose, name_pose, flg_restart)

                inferences      = None

                try:
                    inferences = inferences_q.get_nowait()
                except Exception as e:
                    pass

                elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
                num_frames += 1
                fps = num_frames / elapsed_time

                # Display inferences
                #ポーズの手の形の推測グラフを表示する
                if(inferences is not None):
                    #worker関数内のp1,p2の値を代入
                    x = pointX_q.get_nowait()
                    y = pointY_q.get_nowait()
                    gui.drawInferences(inferences,poseCount, poses)
                    #ポーズの形の信頼地が0.7を超えたらアクションを実行する
                    for i in range(len(poses)):
                        if(inferences[i] > 0.7):
                            poseCount = PoseAction.checkPose(x, y, poses,poses[i],poseCount)#testに7割越え識別したポーズの名称が代入される。
                            cnt_pose = poseCount[i] #全ポーズのゲージを取得したい場合は[i]を外す
                            name_pose = poses[i]
                if (cropped_output is not None):
                    #切り取った画像をBGR形式からRGB形式へ変更する。
                    cropped_output = cv2.cvtColor(cropped_output, cv2.COLOR_RGB2BGR)
                    if (args.display > 0):
                        cv2.namedWindow('Cropped', cv2.WINDOW_NORMAL)
                        cv2.resizeWindow('Cropped', 450, 300)
                        cv2.imshow('Cropped', cropped_output)

                        # cv2.imwrite('Poses/Seri/Seri_3/Seri_3' + str(num_frames) + '.png', cropped_output)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            flg_break = 1
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

        #            _, imencode_image = cv2.imencode('.jpg', output_frame)
        #            base64_image2 = base64.b64encode(imencode_image)
        #            eel.set_base64image2("data:image/jpg;base64," + base64_image2.decode("ascii"))

                    # output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
                    if (args.display > 0):
                        if (args.fps > 0):
                            detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                             output_frame)
                        cv2.imshow('Handpose', output_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            flg_break = 1
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
                    flg_break = 1
                    break

                if(flg_end == 1):
                    flg_break = 1
                    break

        #カメラが切断された際の例外処理(現状、全ての例外をキャッチしている)
#        except:# cv2.error as cv2_e:
#            traceback.print_exc()
            #それぞれのフラグを立てて、システムを終了させ、最初の while に戻る
#            flg_video = 1
#            cnt_gui = 2
#            cnt_gui, flg_end, flg_restart = hand_gui.start_gui(output_frame, cnt_gui, cnt_pose, name_pose, flg_restart)
#            pool.terminate()
#            video_capture.stop()
#            cv2.destroyAllWindows()

    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()
