# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.py'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene, QMessageBox, QGraphicsPixmapItem
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap
import anime
from my_utils import utils
from my_utils.request import WorkThread


class MyMainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = anime.Ui_Dialog()
        self.ui.setupUi(self)
        # 检查图库位置
        self.check_picture_home()
        # "线上获取"槽函数绑定
        self.ui.u_btn_submit.clicked.connect(self.check_submit_btn)
        # "线下随机"槽函数绑定
        self.ui.u_btn_randomGet.clicked.connect(self.random_get)


    def check_picture_home(self):
        """
        检查图库位置
        :return:
        """
        if not os.path.exists("pictures/"):
            os.makedirs("pictures/")

    def show_error_message(self, desc, message):
        """
        自定义错误弹窗
        :param message:
        :return: None
        """
        QMessageBox.critical(self, desc, message)

    def show_download_message(self, desc, message):
        """
        下载弹窗提示，5秒后自动关闭
        :param message:
        :return: None
        """
        dwn_msg = QMessageBox()
        dwn_msg.setText(message)
        dwn_msg.setWindowTitle(desc)
        dwn_msg.setStandardButtons(QMessageBox.Ok)
        dwn_msg.show()
        dwn_msg.button(QMessageBox.Ok).animateClick(5 * 1000)
        dwn_msg.exec_()

    def random_get(self):
        """
        随机获取一张图片，并显示
        :return: None
        """
        try:
            self.show_picture(utils.get_random_picture())
        except:
            self.show_error_message("错误", "本地图库无图片！")

    def check_submit_btn(self):
        """
        检查"线上获取"按钮是否能触发
        :return: bool
        """
        state = self.get_radio_btn_state()
        if state == -1:
            # 弹出报错信息框
            self.show_error_message("未选择图片类型和填写图片描述！")
            return False
        try:
            content = self.parser_tag_content()
            # 多线程调API获取图片，并下载保存
            download_task = WorkThread(state, content)
            download_task.start()
            # 下载图片提示
            self.show_download_message("下载", "图片正在下载，请稍等")
            download_task.join()
            pic_name = download_task.get_result()
            # 显示图片
            self.show_picture(pic_name)
        except:
            self.show_error_message("错误", "图片下载失败！请再次尝试")
            return False
        return True

    def get_radio_btn_state(self):
        """
        检查radio button是否被点击
        :return: int -1为未选择，0为非r-18，1为r-18，2为混合
        """
        state = -1
        if self.ui.u_radioBtn_noero.isChecked():
            state = 0
        elif self.ui.u_radioBtn_ero.isChecked():
            state = 1
        elif self.ui.u_radioBtn_both.isChecked():
            state = 2
        return state

    def parser_tag_content(self):
        """
        解析tagInput中的内容
        targetInput中的属性用空格分隔
        :return: list
        """
        try:
            tag_list = self.ui.u_text_tagInput.toPlainText().replace('\n', '').split()
            return tag_list
        except Exception as e:
            print("tag描述格式错误！")
            raise e

    def show_picture(self, picture_name):
        """
        通过图片名称加载图片
        :param picture_name: 图片名称
        :return: None
        """
        try:
            # todo: 加载正常图片size，不覆盖框
            scene = QGraphicsScene()
            img_show = QPixmap()
            img_show.load(utils.get_file_path(picture_name))
            img_showItem = QGraphicsPixmapItem()
            img_showItem.setPixmap(QPixmap(img_show))
            # img_showItem.setPixmap(QPixmap(img_show).scaled(8000,  8000))    //自己设定尺寸
            scene.addItem(img_showItem)
            self.ui.u_graghView_picture.setScene(scene)
            self.ui.u_graghView_picture.fitInView(QGraphicsPixmapItem(QPixmap(img_show)))
        except Exception as e:
            print("图片加载失败")
            raise e


if __name__ == "__main__":
    # 支持高清分辨率
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myDialog = MyMainDialog()
    myDialog.show()
    sys.exit(app.exec_())

