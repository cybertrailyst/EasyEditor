import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QListWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageQt, ImageEnhance

class ImageProcessor:
    def __init__(self, image, file_name):
        self.image = image
        self.file_name = file_name
        
    def loadImage(self):
        self.image = Image.open(os.path.join(working_dir, self.file_name))
        
    def showImage(self):
        qt_image = ImageQt.ImageQt(self.image)
        pixmap = QPixmap.fromImage(qt_image)
        image_aspect_ratio = self.image.size[0] / self.image.size[1]
        label_aspect_ratio = image_label.size().width() / image_label.size().height()
        if image_aspect_ratio > label_aspect_ratio:
            pixmap = pixmap.scaledToWidth(image_label.size().width(), QtCore.Qt.SmoothTransformation)
        else:
            pixmap = pixmap.scaledToHeight(image_label.size().height(), QtCore.Qt.SmoothTransformation)
            
        image_label.setPixmap(pixmap)

    def do_left(self):
        self.image = self.image.rotate(90)
        self.showImage()

    def do_right(self):
        self.image = self.image.rotate(-90)
        self.showImage()

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage()

    def do_sharp(self):
        factor = 2
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(factor)
        self.showImage()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.showImage()
        
    def saveImage(self):
        self.image.save(os.path.join(working_dir, "modified", self.file_name))

def selectWorkdir():
    global working_dir
    working_dir = QFileDialog.getExistingDirectory()
    os.makedirs(os.path.join(working_dir, "modified"), exist_ok=True)
    file_list = [f for f in os.listdir(working_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    file_list_widget.clear()
    file_list_widget.addItems(file_list)
    
def showChosenImage(item):
    global workimage
    workimage = ImageProcessor(None, item.text())
    workimage.loadImage()
    workimage.showImage()

def showGrayImage(item):
    workimage.do_bw()

def LeftImage(item):
    workimage.do_left()

def RightImage(item):
    workimage.do_right()

def MirrorImage(item):
    workimage.do_mirror()

def SharpImage(item):
    workimage.do_sharp()

def SaveImage(item):
    workimage.saveImage()
    
app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
window.setWindowTitle("Easy Editor")

folder_button = QPushButton("Folder")
folder_button.clicked.connect(selectWorkdir)

file_list_widget = QListWidget()
file_list_widget.itemClicked.connect(showChosenImage)

image_label = QLabel()
image_label.setFixedSize(500, 500)

left_button = QPushButton("Left")
left_button.clicked.connect(LeftImage)
right_button = QPushButton("Right")
right_button.clicked.connect(RightImage)
mirror_button = QPushButton("Mirror")
mirror_button.clicked.connect(MirrorImage)
sharpening_button = QPushButton("Sharpening")
sharpening_button.clicked.connect(SharpImage)
bw_button = QPushButton("B&W")
bw_button.clicked.connect(showGrayImage)
save_button = QPushButton("Save")
save_button.clicked.connect(SaveImage)

h_layout = QHBoxLayout()
h_layout.addWidget(folder_button)
h_layout.addWidget(file_list_widget)

v_layout = QVBoxLayout()
v_layout.addLayout(h_layout)
v_layout.addWidget(image_label)
v_layout.addWidget(left_button)
v_layout.addWidget(right_button)
v_layout.addWidget(mirror_button)
v_layout.addWidget(sharpening_button)
v_layout.addWidget(bw_button)
v_layout.addWidget(save_button)

window.setLayout(v_layout)

window.show()

app.exec_()