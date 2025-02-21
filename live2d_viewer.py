import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class Live2DWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live2D Animated Character")

        # Create a central widget and a layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
 
        # Create a QWebEngineView to load the local HTML file.
        self.web_view = QWebEngineView()
        
        # Use QUrl.fromLocalFile to construct a file URL.
        # Adjust the path to match where live2d.html is located in your project.
        local_html_path = QUrl.fromLocalFile("C:/Users/yagiz/project0/live2d.html")
        self.web_view.load(local_html_path)
        layout.addWidget(self.web_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Live2DWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
