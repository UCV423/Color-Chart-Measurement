import sys
from UICRN_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
from torch import device, no_grad
import torchvision.transforms as transforms
from torch.autograd import Variable
from torch import jit

def img_input_proc(img):

    img = img / 255.0
    img = img.astype(np.float32)

    H, W, C = img.shape
    Wk = W
    Hk = H
    if W % 32:
        Wk = W + (32 * 6 - W % 32)
    if H % 32:
        Hk = H + (32 * 6 - H % 32)

    img = np.pad(img, ((0, Hk - H), (0, Wk - W), (0, 0)), 'reflect')
    #im_input = img / 255.0
    #im_input = (im_input - [0.062144067, 0.40411913, 0.50215524]) / [0.085818715, 0.18424582, 0.23216859]
    trans_torch = transforms.Compose([transforms.ToTensor(),
                                       transforms.Normalize([0.062144067, 0.40411913, 0.50215524],
                                                            [0.085818715, 0.18424582, 0.23216859])])

    img = transforms.ToTensor()(img)
    img.unsqueeze(0)
    # im_input = img / 255.0
    # im_input = im_input / im_input.max(axis=0)
    # im_input = np.expand_dims(np.rollaxis(im_input, 2), axis=0)
    return img, W, H

def img_output_proc(img):
    img = img.data[0].numpy()
    img = img * 255.
    img[img < 0] = 0
    img[img > 255.] = 255.
    np.transpose(img, (1, 2, 0))
    img = np.rollaxis(img, 0, 3)
    img = img.astype('uint8')
    return img

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.PB_open.clicked.connect(self.open_image)
        self.PB_run.clicked.connect(self.run_model)
        self.PB_load.clicked.connect(self.load_model)
        self.net = None
        #self.net = torch.nn.DataParallel(UW_model, device_ids=[0])
    def open_image(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(self, 'select images', '', 'Image files(*.jpg , *.png)')
            #print(openfile_name)
        except:
            return
        if openfile_name[0] != '':
            self.img_path = openfile_name[0]
            #print(self.img_path)
            try:
                self.ori_img = cv2.imread(self.img_path)
                self.img_to_run = cv2.resize(self.ori_img, (384, 384))
            except:
                self.label_status.setText("status: Failed to open image. Make sure the path has no Chinese.")
                return
            self.label_status.setText("status: image opened successfully")
            self.img_to_show = cv2.resize(self.ori_img, (480, 360))
            #print("alive")
            self.show_image(self.ori_label, self.img_to_show)

    def show_image(self, image_label, image, rgb=True):

        if rgb is True:
            rgb_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        else:
            rgb_image = image.copy()
        #rgb_image = cv2.resize(rgb_image, (self.width(), self.height()))
        label_image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        image_label.setPixmap(QPixmap.fromImage(label_image))

    def load_model(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(self, 'select model', '', 'Image files(*.pth , *.*)')
            # print(openfile_name)
        except:
            return
        if openfile_name[0] != '':
            model_path = openfile_name[0]
            print(model_path)

        try:
            UW_model = jit.load(model_path, map_location=device("cpu"))
        except:
            self.label_status.setText("status: model failed to load! Make sure the path has no Chinese.")
            return
        self.label_status.setText("status: model load successfully!")
        self.net = UW_model
        self.net.eval()
    def run_model(self):
        if self.net == None:
            self.label_status.setText("status: no model load!")
            return
        image_x, W, H = img_input_proc(self.img_to_run)

        with no_grad():
            image_x = Variable(image_x.unsqueeze(0))
            # if cuda.is_available():
            #     self.net.cuda()
            #     image_x = image_x.cuda()

            JR = self.net(image_x)

        output = JR
        output = output.cpu()

        im_restored = img_output_proc(output)
        im_restored = im_restored[0:H, 0:W, :]
        im_restored = im_restored.copy()
        im_restored = cv2.resize(im_restored, (480, 360))
        self.label_status.setText("status: done!")
        self.show_image(self.res_label, im_restored)
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)

    myWin = MyMainForm()

    myWin.show()

    sys.exit(app.exec_())