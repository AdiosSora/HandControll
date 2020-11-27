import numpy as np
import cv2

def gamma_correction(image,gamma):

        """ガンマ補正を利用して、画像を明るくしたり暗くしたりする


                Args:
            image(obj): イメージ画像
            gamma(float): ガンマ値  0〜1までは、暗くする、1以上は明るくする

        Returns:
           ガンマ補正後のイメージ画像

        """
        # 整数型で2次元配列を作成[256,1]
        lookup_table = np.zeros((256, 1), dtype = 'uint8')
        for loop in range(256):
            # γテーブルを作成
            lookup_table[loop][0] = 255 * pow(float(loop)/255, 1.0/gamma)

        # lookup Tableを用いて配列を変換
        image_gamma = cv2.LUT(image, lookup_table)

        return image_gamma
