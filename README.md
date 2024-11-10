
# Beam - Illuminate What Matters 🌌

> *“The people who are crazy enough to think they can change the world are the ones who do.”*

Welcome to **Beam**.

[![Video Thumbnail](https://github.com/vididvidid/Beam/blob/main/Beam/YoutbeFreeDistraction.png)](https://youtu.be/f6VnDJXeXIc)


## Why Beam?
The world is full of distractions. Apps, websites, notifications—everywhere you turn, something is fighting for your attention. But let’s imagine a world where your technology is truly designed for you. A world where you choose your focus, and every interaction on your screen is precisely what you need, nothing more, nothing less.

**That’s Beam.** Beam isn’t just a tool; it’s a philosophy. It’s about **freedom**—freedom to focus, freedom to create, and freedom to do what matters most.

---

## What is Beam?
Beam gives you back control. No more wandering through endless feeds. Beam understands your focus, your goals, and creates a **personalized digital space** to keep you aligned with them. Every moment you spend with Beam is intentional, meaningful, and distraction-free.

---

### Beam Brings You:
1. **Real-Time Content Customization**  
   - Imagine opening YouTube, and seeing only what’s relevant to you. No clutter, no noise—just what matters.
   - 
   ![Screenshot 2024-11-10 095242](https://github.com/user-attachments/assets/bcf234ea-d0d0-4f30-8766-381b141b157a)

2. **Historical Chains of Your Work**  
   - Every project you start is seamlessly connected to your past work. Beam remembers, so you never waste time finding your way back.

   ![Screenshot 2024-11-10 100817](https://github.com/user-attachments/assets/d23abe9e-7cec-4050-8a74-4bb608a98283)


3. **Your Custom Interface**  
   - A workspace tailored to you: Study mode, Creative mode, Productivity mode—designed for your goals, your preferences, and your success.


4. **Smart Distraction Management with Deepfake Technology**  
   - Beam doesn’t just blur distractions; it transforms them. It’s like having your own assistant that clears the path so you can stay focused and energized.


---

## The Foundation of Beam’s Solution

### **Image-to-Text Conversion**
   - **Approach**: Initially, we considered building a custom model using TensorFlow. Given the diversity of image content, we opted for the **Ollama model**, which we hosted on **Cloudflare** for consistent processing.
   
   - **How it Works**:  
      1. Beam processes each image input, whether from photos or video frames.
      2. Beam extracts relevant text data that’s seamlessly integrated into your workspace.

   [![Video Thumbnail](https://github.com/vididvidid/Beam/blob/main/Beam/image%20and%20video.png)](https://github.com/vididvidid/Beam/blob/main/Beam/image%20to%20text.mkv)


   

---

### **Blurring the Irrelevant in Videos**

   - **Step-by-Step**:  
      1. Videos are divided into frames.
      2. Unique frames are identified and isolated.
      3. Frames are processed with a simple “Yes/No” filter.
      4. Beam reassembles the video, selectively blurring frames where unnecessary content is detected.

   **Input Video Sample**:
   ![Input Video](https://github.com/vididvidid/Beam/blob/main/Beam/SampleVideoInput.mov)

   **Prompt**:
   > “If Child Doing yoga Print Yes Otherwise NO”

   **Output Video Sample**:
   ![Output Video](https://github.com/vididvidid/Beam/blob/main/Beam/SampleVideoOutput.mp4)

---

### **Screen Overlay App for Focused Study with Hot Reloading**

   - **How It Works**:  
      1. **User Input**: Enter your focus topic.
      2. **Initial Screenshot**: Beam captures the initial screen state.
      3. **Content Analysis**: Beam evaluates each screen element based on the focus topic.
      4. **Overlay Creation**: Distracting content is softly covered to maintain focus.
      5. **Hot Reloading**: Beam continuously monitors the screen and updates overlays in real time.

   **Initial Screen**:
   ![Initial Screen](https://github.com/vididvidid/Beam/blob/main/Beam/Screenshot%202024-11-10%20100504.png)

   **Overlay in Progress**:
   ![Overlay in Progress](https://github.com/vididvidid/Beam/blob/main/Beam/OVerlaySample.png)

   **Final Screen with Overlay**:
   ![Final Screen](https://github.com/vididvidid/Beam/blob/main/Beam/ScreenOverlayDistractionFree.mkv)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/beam.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install opencv-python-headless pytesseract numpy pillow requests
   ```

3. **Configure Tesseract**:
   - Download and install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
   - Set the Tesseract path in `com2.py`:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

4. **Run Beam**:
   ```bash
   python com2.py
   ```

---

## Usage

Beam offers three core tools to keep you focused and distraction-free:

1. **Image-to-Text & Video-to-Text**  
   - Choose an input file, set a prompt, and let Beam turn visuals into meaningful, actionable text.

2. **Distraction-Free Video**  
   - Beam filters distractions in real-time, so you focus on relevant content only.

3. **Screen Overlay for Focused Study**  
   - Set your focus topic, and Beam automatically overlays white boxes on any irrelevant content on your screen.

---

## Contributing

We’re excited to welcome collaborators. Fork the repository, raise issues, and submit pull requests to enhance Beam.

## License
This project is licensed under the MIT License.

---

Welcome to Beam. It’s time to focus on what matters. 🌟

--- 
