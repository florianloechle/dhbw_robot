import cv2


class Camera:
    def __init__(self, video=None):
        # set capturing to video or to the default camera
        self.capture = cv2.VideoCapture(video if video else 0)
        # check if camera opening succeeded
        if not self.capture.isOpened():
            raise Exception(
                self.__class__.__name__ + ':' +
                    ' Could not open Videocapture. Please check default camera connection or video file.')

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # current frame
        self.frame = None

    def get_frame(self):
        hasFrame, self.frame = self.capture.read()
        return self.frame if hasFrame else None

    def dispose(self):
        self.capture.release()


