"""
# @ Color Chart Difference
# @Author  : UAC
# @Time    : 2021/6/15
"""

import sys
from CC_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QFileDialog, QApplication
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
from imutils.perspective import four_point_transform
import CC_IQA


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.PB_open.clicked.connect(self.open_image)
        self.PB_4points.clicked.connect(self.get_cc_points)
        self.PB_reset.clicked.connect(self.reset)
        self.PB_rot.clicked.connect(self.rot_rect)
        self.PB_cal.clicked.connect(self.cal_diff)
        self.PB_ok.clicked.connect(self.get_scale)
        self.img_path = ""
        self.cc_points = []
        self.get_p = False
        self.scale = 0.5

    def open_image(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(self, 'select images', '', 'Excel files(*.jpg , *.png)')
            #print(openfile_name)
        except:
            return
        if openfile_name[0] != '':
            self.cc_image.reselect()
            self.img_path = openfile_name[0]
            self.ori_cc_img = cv2.imread(self.img_path)
            self.resize_cc_img = cv2.resize(self.ori_cc_img, (640, 480))
            self.cc_image.show_image(self.resize_cc_img)

    def get_cc_points(self):
        self.get_p = True
        self.cc_points = self.cc_image.return_points(self.ori_cc_img, self.get_p)
        if self.cc_points == False:
            QMessageBox.information(self, 'error', 'The number of selected points is insufficient',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        #print(self.cc_points)
        rect = four_point_transform(self.ori_cc_img.copy(), np.array(self.cc_points))
        #cv2.imwrite("tmp_cc.jpg", rect)
        self.rect_img = cv2.cvtColor(rect.copy(), cv2.COLOR_BGR2RGB)
        self.rect_img = cv2.resize(self.rect_img, (self.area_image.width(), self.area_image.height()))
        self.show_image(self.area_image, self.rect_img, rgb=False)

    def reset(self):
        self.cc_image.reselect()

    def show_image(self, image_label, image, rgb=True):
        # 参数image为np.array类型
        if rgb is True:
            rgb_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        else:
            rgb_image = image.copy()
        #rgb_image = cv2.resize(rgb_image, (self.width(), self.height()))
        label_image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        image_label.setPixmap(QPixmap.fromImage(label_image))

    def rot_rect(self):
        img = cv2.transpose(self.rect_img)
        img = cv2.flip(img, 0)
        self.rect_img = img.copy()
        self.rect_img = cv2.resize(self.rect_img, (self.area_image.width(), self.area_image.height()))
        self.show_image(self.area_image, self.rect_img, rgb=False)

    def get_scale(self):
        tmp = self.scale_text.text()
        self.scale = float(tmp)

    def cal_diff(self):

        m_C, m_E, rect_drawed = CC_IQA.cc_task(self.rect_img, self.scale)
        self.show_image(self.area_image, rect_drawed, rgb=False)
        self.label_C.setText("mean C: {:.4f}".format(m_C))
        self.label_E.setText("mean E: {:.4f}".format(m_E))

if __name__ == "__main__":

    app = QApplication(sys.argv)

    myWin = MyMainForm()

    myWin.show()

    sys.exit(app.exec_())