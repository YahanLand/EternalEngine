import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtCore import QTimer

class GifModelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jerma Chat")

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top: Animated model area
        self.model_label = QLabel()
        self.model_label.setFixedSize(200, 200)
        
        # Load idle state as a static image (JPG)
        idle_pixmap = QPixmap("C:/Users/yagiz/project0/jermapic.jpg")
        if idle_pixmap.isNull():
            print("Idle image failed to load! Check the file path.")
        self.idle_pixmap = idle_pixmap  # store for later use
        self.model_label.setPixmap(self.idle_pixmap)
        self.model_label.setScaledContents(True)
        
        # Load an animated GIF for the "talking" state
        self.talking_movie = QMovie("C:/Users/yagiz/project0/jerma-handsome.gif")
        if not self.talking_movie.isValid():
            print("Talking GIF failed to load! Check the file path.")
        
        # Initially, we display the idle image.
        main_layout.addWidget(self.model_label)
        
        # Middle: Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        main_layout.addWidget(self.chat_display)
        
        # Bottom: User input and send button
        input_layout = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type your message here...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.prompt_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
        
    def send_message(self):
        prompt = self.prompt_input.text().strip()
        if not prompt:
            return
        
        # Display the user's message in the chat
        self.chat_display.append(f"You: {prompt}")
        self.prompt_input.clear()
        
        # Switch animation to talking GIF
        self.model_label.setMovie(self.talking_movie)
        self.talking_movie.start()
        
        # Simulate a response (here you would integrate your LLM)
        response = f"(Simulated response to '{prompt}')"
        self.chat_display.append(f"Model: {response}\n")
        
        # After 2 seconds, switch back to the idle image
        QTimer.singleShot(4000, self.switch_to_idle)
        
    def switch_to_idle(self):
        # Stop the talking animation and clear the movie from the label
        self.talking_movie.stop()
        self.model_label.setMovie(None)
        # Reset to the idle pixmap
        self.model_label.setPixmap(self.idle_pixmap)
        self.model_label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifModelWindow()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec())
