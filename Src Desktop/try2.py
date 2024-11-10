import tkinter as tk
from tkinter import messagebox
import threading
import time
import pytesseract
from PIL import ImageGrab, Image
import numpy as np

# If necessary, set the tesseract command path. Adjust based on your installation
# Uncomment and modify the following line for your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class DistractionBlockerApp:
  def __init__(self, root):
      self.root = root
      self.root.title("Distraction Blocker")
      self.focus_topic = ''
      self.monitoring = False

      # Create GUI elements
      self.prompt_label = tk.Label(root, text="Enter your focus topic:")
      self.prompt_label.pack(pady=10)

      self.prompt_entry = tk.Entry(root, width=50)
      self.prompt_entry.pack(pady=5)

      self.start_button = tk.Button(root, text="Start", command=self.start_monitoring)
      self.start_button.pack(pady=10)

      self.status_label = tk.Label(root, text="Status: Idle")
      self.status_label.pack(pady=5)

  def start_monitoring(self):
      self.focus_topic = self.prompt_entry.get()
      if not self.focus_topic.strip():
          messagebox.showwarning("Input Required", "Please enter your focus topic.")
          return

      self.status_label.config(text="Status: Monitoring screen for distractions...")
      self.monitoring = True

      # Start the monitoring in a separate thread
      monitoring_thread = threading.Thread(target=self.monitor, daemon=True)
      monitoring_thread.start()

  def monitor(self):
      # Capture initial screenshot
      baseline_screenshot = ImageGrab.grab()

      # Main monitoring loop
      while self.monitoring:
          time.sleep(2)  # Adjust the interval as needed

          # Capture new screenshot
          new_screenshot = ImageGrab.grab()

          # Compare screenshots
          if self.screens_are_different(baseline_screenshot, new_screenshot):
              # Screenshots are different; process changes
              self.process_changes(new_screenshot)
              # Update baseline screenshot
              baseline_screenshot = new_screenshot

  def screens_are_different(self, img1, img2):
      # Resize images to reduce comparison time
      img1_small = img1.resize((100, 100)).convert('L')
      img2_small = img2.resize((100, 100)).convert('L')

      # Convert images to numpy arrays
      arr1 = np.array(img1_small)
      arr2 = np.array(img2_small)

      # Calculate difference
      diff = np.sum(np.abs(arr1 - arr2))
      return diff > 0  # Returns True if there is any difference

  def process_changes(self, screenshot):
      # Convert the screenshot to grayscale for OCR
      gray_image = screenshot.convert('L')

      # Use pytesseract to extract text data with bounding boxes
      data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)

      distraction_boxes = []

      num_boxes = len(data['level'])
      for i in range(num_boxes):
          text = data['text'][i]
          if text.strip() == '':
              continue  # Skip empty text

          # Check if the text is related to the focus topic
          if self.focus_topic.lower() not in text.lower():
              # Get bounding box of the text
              x = data['left'][i]
              y = data['top'][i]
              w = data['width'][i]
              h = data['height'][i]

              distraction_boxes.append((x, y, w, h))

      # Overlay white boxes over distractions
      if distraction_boxes:
          self.overlay_distractions(distraction_boxes)
          # Update the status label
          self.status_label.config(text="Status: Blocking detected distractions.")
      else:
          # No distractions found
          self.status_label.config(text="Status: No distractions detected.")

  def overlay_distractions(self, boxes):
      # Create an overlay window
      overlay = tk.Toplevel(self.root)
      overlay.attributes("-fullscreen", True)
      overlay.attributes("-topmost", True)
      overlay.config(bg='black')
      overlay.attributes('-alpha', 0.1)  # Almost transparent

      # Create a canvas to draw the overlays
      screen_width = overlay.winfo_screenwidth()
      screen_height = overlay.winfo_screenheight()
      canvas = tk.Canvas(overlay, width=screen_width, height=screen_height, highlightthickness=0)
      canvas.pack()

      # Draw transparent rectangles over the entire screen
      canvas.create_rectangle(0, 0, screen_width, screen_height, fill='black', outline='')

      # Cut out holes in the overlay where there are no distractions
      for box in boxes:
          x1, y1, w, h = box
          x2 = x1 + w
          y2 = y1 + h
          canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='')

      # Update the canvas to apply changes
      canvas.update()

      # Keep the overlay open until the next screen change
      # Destroy the overlay after 2 seconds
      overlay.after(2000, overlay.destroy)

if __name__ == "__main__":
  root = tk.Tk()
  app = DistractionBlockerApp(root)
  root.mainloop()
