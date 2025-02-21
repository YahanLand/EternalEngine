import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTextEdit, QLineEdit, QPushButton
)
from PySide6.QtGui import QMovie, QPixmap, QTextCursor
from PySide6.QtCore import QTimer

def get_installed_models():
    """
    Runs the 'ollama list' command to get a list of installed models.
    
    Returns:
        list: A list of model names (strings).
    """
    try:
        # Run the 'ollama list' command.
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        output = result.stdout.strip()
        models = []
        # Assume each line represents one model.
        # If there's a header line (e.g., "NAME  VERSION ..."), you might need to skip it.
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            # If the first line is a header, skip it.
            if line.lower().startswith("name"):
                continue
            # Assume the model name is the first token in the line.
            model_name = line.split()[0]
            models.append(model_name)
        return models if models else ["no_models"]
    except subprocess.CalledProcessError as e:
        print("Error getting installed models:", e)
        print("Standard Error Output:", e.stderr)
        # Fallback to a default model name if the command fails.
        return ["no_models"]

def get_llm_response(model, prompt):
    """
    Sends the prompt to the local model via Ollama and returns the response.
    
    Parameters:
        model (str): The name of the model to run.
        prompt (str): The user’s text input.
    
    Returns:
        str: The generated response from the model.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error communicating with the local model:", e)
        print("Standard Error Output:", e.stderr)
        return "Sorry, I couldn't get a response from the model."

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Game Engine")
        
        # Set up the central widget and layout.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top area: Model selection.
        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_combo = QComboBox()

        # Populate the dropdown with models retrieved from 'ollama list'.
        models = get_installed_models()
        self.model_combo.addItems(models)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        main_layout.addLayout(model_layout)

        # Create a QLabel that will display our avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(200, 200)

        # Load the idle state image as a QPixmap
        idle_path = ("C:/Users/yagiz/project0/jermapic.jpg")
        self.idle_pixmap = QPixmap(idle_path)
        if self.idle_pixmap.isNull():
            print("Error: Idle image failed to load! Check path:", idle_path)
        self.avatar_label.setPixmap(self.idle_pixmap)
        self.avatar_label.setScaledContents(True)

        # Load the talking state animated GIF using QMovie
        talking_path = ("C:/Users/yagiz/project0/jerma-handsome.gif")
        self.talking_movie = QMovie(talking_path)
        if not self.talking_movie.isValid():
            print("Error: Talking GIF failed to load! Check path:", talking_path)

        # Add the avatar label to the layout.
        main_layout.addWidget(self.avatar_label)
        
        # Middle area: Chat display (conversation text).
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        main_layout.addWidget(self.chat_display)
        
        # Bottom area: User prompt input and Send button.
        input_layout = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type your message here...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        # Bind the Enter key to send the message.
        self.prompt_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
    
    def send_message(self):
        """
        Triggered when the user sends a message. It retrieves the prompt,
        appends it to the chat display, calls the backend function, and displays the response.
        """
        prompt = self.prompt_input.text().strip()
        if not prompt:
            return  # Do nothing if the prompt is empty

        # Get the selected model from the dropdown.
        model = self.model_combo.currentText()

        # Append the user's message to the chat display.
        self.chat_display.append(f"You: {prompt}")
        self.prompt_input.clear()

        # Switch the avatar to the talking animation.
        self.avatar_label.setMovie(self.talking_movie)
        self.talking_movie.start()

        # Call the backend to get the model response.
        response = get_llm_response(model, prompt)
        self.chat_display.append(f"Model ({model}): {response}\n")
        self.chat_display.moveCursor(QTextCursor.End)

        # After a delay, switch back to the idle image
        QTimer.singleShot(2000, self.switch_to_idle)

    def switch_to_idle(self):
        # Stop the talking animation and remove it from the label
        self.talking_movie.stop()
        self.avatar_label.setMovie(None)
        # Reset the avatar label to display the idle pixmap
        self.avatar_label.setPixmap(self.idle_pixmap)
        self.avatar_label.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
