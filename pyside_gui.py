import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTextEdit, QLineEdit, QPushButton
)

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
            encoding='utf-8',  # Use UTF-8 to decode the output
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
        self.setWindowTitle("AI Avatar MVP - PySide6")

        # Set up the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top area: Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Select Model:")
        self.model_combo = QComboBox()
        # Add available model names. Replace these with your actual model names.
        self.model_combo.addItems(["my_model", "another_model"])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        main_layout.addLayout(model_layout)

        # Middle area: Chat display (conversation text)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)  # Prevent the user from editing it
        main_layout.addWidget(self.chat_display)

        # Bottom area: User prompt input and Send button
        input_layout = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type your message here...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        # Also allow pressing Enter to send the message
        self.prompt_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

    def send_message(self):
        """
        Triggered when the user sends a message. It:
          - Retrieves the text from the input field.
          - Appends the user's message to the chat display.
          - Calls the get_llm_response function with the selected model and prompt.
          - Appends the model's response to the chat display.
        """
        prompt = self.prompt_input.text().strip()
        if not prompt:
            return  # Do nothing if the prompt is empty

        # Get the selected model from the dropdown
        model = self.model_combo.currentText()

        # Append the user's message to the chat display
        self.chat_display.append(f"You: {prompt}")
        self.prompt_input.clear()

        # Call the backend to get the model response (this call is blocking)
        response = get_llm_response(model, prompt)
        self.chat_display.append(f"Model ({model}): {response}\n")

        # Scroll to the bottom of the text display
        self.chat_display.moveCursor(self.chat_display.textCursor().End)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
