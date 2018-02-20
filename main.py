import sys

from PyQt5.QtWidgets import QApplication 

from MainWindow import MainWindow
from Glovox import Glovox

qdark_present = True
try:
    import qdarkstyle  
except ImportError:
    qdark_present = False

if __name__ == '__main__':

    app = QApplication(sys.argv)

	#The Model
    model = Glovox() 

    if qdark_present: # if this style has been imported, the GUI will use it
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    size = app.primaryScreen().size()

    #The View/Controller
    window = MainWindow(model, size) 

    sys.exit(app.exec_())