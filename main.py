import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QApplication, QInputDialog, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap
from PIL import Image

from PIL import ImageFilter
from PIL.ImageFilter import *

app = QApplication([])
win = QWidget()



win.resize(700, 400)
win.setWindowTitle('Easy Editor')
lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton("Сбросить фильтр")



row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
row1 = QHBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row1.addWidget(btn_left)
row1.addWidget(btn_right)
row1.addWidget(btn_flip)
row1.addWidget(btn_sharp)
row1.addWidget(btn_bw)
row1.addWidget(btn_save)
row1.addWidget(btn_reset)

col2.addLayout(row1)
row.addLayout(col1, 20)
row.addLayout(col2, 80)

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result            

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.original_image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def LoadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
        self.original_image = Image.open(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def resetImage(self):
        image_path = os.path.join(workdir, self.filename)
        self.image = Image.open(image_path)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.LoadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)



workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenameList():
    extensions = ['.jpg', '.jpeg', '.png', '.svg', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)



btn_dir.clicked.connect(showFilenameList)
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_reset.clicked.connect(workimage.resetImage)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)

#row.addWidget(btn_dir)
win.setLayout(row)
win.show()
app.exec_()
