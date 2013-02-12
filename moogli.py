from PyQt4 import Qt,QtGui,QtCore
from canvas import GLCanvas
import sys

def Moogli():


    class GLApp(QtGui.QApplication):

        def __init__(self, args):
            QtGui.QApplication.__init__(self,args)
            self.window = GLWindow()
            self.canvas = self.window.canvas

        def show(self):
            #self.canvas.refresh_canvas()
            self.canvas.create_object_buffers()
            self.window.show()
            sys.exit(self.exec_())

    class GLWindow(QtGui.QMainWindow):

        def __init__(self, parent = None):
            super(GLWindow, self).__init__(parent)
            self.name = 'Moogli'
            self.setupUi(self)

        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.setWindowModality(QtCore.Qt.NonModal)
            MainWindow.resize(500, 500)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
            MainWindow.setSizePolicy(sizePolicy)
            self.centralwidget = QtGui.QWidget(MainWindow)
            self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setObjectName("verticalLayout")
            self.canvas = GLCanvas(self.centralwidget)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
            self.canvas.setSizePolicy(sizePolicy)
            self.canvas.setObjectName("canvas")
            self.verticalLayout.addWidget(self.canvas)
            MainWindow.setCentralWidget(self.centralwidget)
            MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", self.name, None, QtGui.QApplication.UnicodeUTF8))
    return GLApp(sys.argv)

if __name__ == "__main__":
    app = Moogli()
    app.canvas.drawObject1()
    app.show()
