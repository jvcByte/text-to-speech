# Speech-to-Text Web Application

A Streamlit-based web application that provides speech-to-text and text-to-speech functionality with a modern, responsive UI.

## Features

- **Speech-to-Text**: Convert spoken words into text using your device's microphone
- **Text-to-Speech**: Convert written text into natural-sounding speech
- **Responsive Design**: Works on both desktop and mobile devices
- **Modern UI**: Clean, intuitive interface with glassmorphism design elements
- **Article Summarization**: Extract and process text from web articles

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/speech-to-text-app.git
   cd speech-to-text-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Use the sidebar to navigate between different features:
   - **Text Input**: Type or paste text and have it read aloud
   - **Speech Input**: Record your voice and see it transcribed to text
   - **Article Summarization**: Enter a URL to extract and process article content

## Requirements

- Python 3.8+
- Modern web browser with Web Speech API support (Chrome, Firefox, Edge, Safari)
- Microphone (for speech input)
- Internet connection (for article summarization)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
