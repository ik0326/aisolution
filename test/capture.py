import cv2

filepath = "vtest.avi"
# cap = cv2.VideoCapture(filepath)
# Webカメラを使うときはこちら


class Capture:
    """
    Captureクラスは動画の動体検出をサポートするメソッドを提供します。
    """
    def __init__(self,movie_path:str|None=None,device:int=0) -> None:
        """initialize capture mode. and configs."""

        if not movie_path:
            self.cap = cv2.VideoCapture(device)
        else:
            try:
                if movie_path[-3:] != 'mp4':
                    raise "Non-mp4 files are not supported."
                self.cap = cv2.VideoCapture(movie_path)
            except:
                raise """cannot capture video. not found video.
                        arrow to capture 'mp4'.
                        """

        self.avg = None

    def motion_detection(self,reseption:float=0.8):
        while True:
            # 1フレームずつ取得する。
            ret, frame = self.cap.read()
            if not ret:
                break

            # グレースケールに変換
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 比較用のフレームを取得する
            if self.avg is None:
                self.avg = gray.copy().astype("float")
                continue

            # 現在のフレームと移動平均との差を計算
            cv2.accumulateWeighted(gray, self.avg, reseption)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))

            # デルタ画像を閾値処理を行う
            thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
            # 画像の閾値に輪郭線を入れる
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

            # 結果を出力
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(30)
            if key == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cc = Capture().motion_detection(reseption=0.5)