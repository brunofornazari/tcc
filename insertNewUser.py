import facialRecognition.faceCapture as capture
import facialRecognition.facial_trainer as trainer


def captureNewFace() :
    capture.captureNewFace()


def startTraining() :
    trainer.startTraining()


if __name__ == '__main__' :
    captureNewFace()
    startTraining()
