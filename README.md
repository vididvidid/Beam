# Beam - Illuminate What Matters 🌟

## Introduction
Beam is designed to transform the way we interact with technology, steering it away from distractions and toward growth and empowerment. Today’s platforms often prioritize engagement over purpose, making it challenging for users to maintain focus on their real goals. Beam is here to change that. By providing a distraction-free environment tailored to individual needs, Beam enhances focus, productivity, and personal growth.

## Key Features
Beam is a suite that includes the following essential tools:

- **Image-to-Text Conversion**: Seamlessly converts images into text, aiding in quick content extraction and analysis.
- **Video-to-Text Conversion**: Automatically extracts textual content from videos, making it easier to document and summarize information.
- **Distraction-Free Video**: Removes irrelevant content to keep your focus on what matters most.
- **Distraction Overlay**: Identifies and overlays distracting elements on your screen, allowing you to stay on track with your goals.

## Vision
*Beam* is designed not only as a tool but as a personal ally in your digital journey. Imagine an AI that crafts an environment aligned with your intentions, gently guiding you when focus drifts. Beam doesn’t just block distractions; it reshapes the digital experience to empower you to achieve more.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/beam.git
   ```
2. **Install Dependencies**:
   Ensure you have `cv2`, `pytesseract`, `numpy`, `tkinter`, and `requests` installed.
   ```bash
   pip install opencv-python-headless pytesseract numpy pillow requests
   ```

3. **Tesseract Configuration**:
   - Download and install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
   - Update the path in `com2.py`:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

4. **Run the Software**:
   ```bash
   python com2.py
   ```

## Usage
Beam offers a distraction-free experience through the following modules:

### 1. Image-to-Text & Video-to-Text
- **Select Input File**: Choose an image or video for text extraction.
- **Source Folder**: Specify a location for output files.
- **Prompt Entry**: Enter any specific instruction or context.
- **Processing Type**: Choose between 'Image' or 'Video' processing.
  
### 2. Distraction-Free Video
Beam automatically filters distractions in videos, allowing you to focus only on relevant content.

### 3. Distraction Overlay
Stay aligned with your focus topic. Beam identifies unrelated content on your screen and overlays a faint blur, helping maintain focus.

## Contribution
We welcome contributions to enhance Beam’s functionality. Feel free to fork the repository, raise issues, and submit pull requests.

## License
Distributed under the MIT License.
