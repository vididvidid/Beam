import cv2
import os
import requests
from PIL import Image, ImageChops, ImageFilter
import numpy as np
import time

# For GUI
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def append_log(message):
  """Appends a message to the log text area in the GUI."""
  log_text.insert(tk.END, message + '\n')
  log_text.see(tk.END)
  root.update_idletasks()

def video_to_frames(video_path, frames_folder, frame_rate=1):
  """Splits a video into frames, skipping identical consecutive frames."""
  if not os.path.exists(frames_folder):
      os.makedirs(frames_folder)

  cap = cv2.VideoCapture(video_path)
  fps = cap.get(cv2.CAP_PROP_FPS)
  frame_interval = int(fps / frame_rate)
  count = 0
  previous_frame = None
  frame_indices = []

  frame_number = 0
  while True:
      success, frame = cap.read()
      if not success:
          break

      if frame_number % frame_interval == 0:
          # Convert frame to grayscale for comparison
          current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          is_duplicate = False

          if previous_frame is not None:
              # Compare current frame with the previous frame
              diff = cv2.absdiff(previous_frame, current_frame_gray)
              non_zero_count = np.count_nonzero(diff)
              if non_zero_count == 0:
                  is_duplicate = True

          if not is_duplicate:
              frame_filename = os.path.join(frames_folder, f"frame_{count:04d}.jpg")
              cv2.imwrite(frame_filename, frame)
              frame_indices.append(frame_number)
              count += 1
              previous_frame = current_frame_gray

      frame_number += 1

  cap.release()
  append_log(f"Extracted {count} frames to '{frames_folder}'.")
  return frame_indices

def get_image_description(image_path, prompt):
  """
  Sends an image to the API endpoint and retrieves the description.
  """
  url = 'https://qa-pic.lizziepika.workers.dev/analyze-image'

  # Prepare the multipart form data
  with open(image_path, 'rb') as image_file:
      files = {
          'image': (os.path.basename(image_path), image_file, 'image/jpeg'),
          'text': (None, prompt),
      }

      headers = {
          'accept': '*/*',
          'origin': 'https://qa-pic.lizziepika.workers.dev',
          'referer': 'https://qa-pic.lizziepika.workers.dev/',
      }

      response = requests.post(url, headers=headers, files=files)

  if response.status_code == 200:
      data = response.json()
      description = data.get('response', '')
      return description
  else:
      append_log(f"Failed to get description for {image_path}: HTTP {response.status_code}")
      return 'No description available.'

def extract_yes_no(description):
  """Extracts 'yes' or 'no' from the API response."""
  description_lower = description.strip().lower()
  if 'yes' in description_lower:
      return 'yes'
  elif 'no' in description_lower:
      return 'no'
  else:
      # Default to 'no' if neither is found
      return 'no'

def blur_image(image_path):
  """Blurs the given image and saves it."""
  img = Image.open(image_path)
  blurred_img = img.filter(ImageFilter.GaussianBlur(radius=15))
  blurred_img.save(image_path)

def process_frames(frames_folder, prompt):
  """Processes each frame by sending it to the API and collecting responses."""
  frames = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])
  responses = []

  for i, frame in enumerate(frames):
      image_path = os.path.join(frames_folder, frame)
      description = get_image_description(image_path, prompt)
      
      response = extract_yes_no(description)
      responses.append((image_path, response))
      message = f"[{i+1}/{len(frames)}] Processed {frame}: {response}"
      append_log(message)
      
      # Optional: Delay to respect API rate limits
      time.sleep(1)  # Adjust the delay as appropriate

  return responses

def recreate_video(frames_folder, frame_indices, output_video_path, original_video_path, responses):
  """Recreates the video using processed frames and blurs frames based on responses."""
  # Get original video properties
  cap = cv2.VideoCapture(original_video_path)
  fps = cap.get(cv2.CAP_PROP_FPS)
  width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
  cap.release()

  # Prepare to write the video
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

  # Map frame indices to responses
  response_dict = dict(zip(frame_indices, responses))

  # Reconstruct the video
  cap = cv2.VideoCapture(original_video_path)
  frame_number = 0
  prev_frame = None
  while True:
      success, frame = cap.read()
      if not success:
          break

      if frame_number in response_dict:
          response = response_dict[frame_number][1]  # Get 'yes' or 'no' response

          if response == 'yes':
              # Keep the frame as is
              out.write(frame)
              prev_frame = frame
          else:
              # Blur the frame
              # Convert frame to PIL Image
              img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
              blurred_img = img.filter(ImageFilter.GaussianBlur(radius=15))
              # Convert back to OpenCV image
              frame_blurred = cv2.cvtColor(np.array(blurred_img), cv2.COLOR_RGB2BGR)
              out.write(frame_blurred)
              prev_frame = frame_blurred
      else:
          # Frame was skipped (identical to previous), so repeat the last processed frame
          if prev_frame is not None:
              out.write(prev_frame)
      frame_number += 1

  cap.release()
  out.release()
  append_log(f"Video recreated and saved to '{output_video_path}'.")

def process_image(image_path, prompt):
  """Processes a single image and displays the result."""
  description = get_image_description(image_path, prompt)
  response = description
  message = f"Processed {os.path.basename(image_path)}: {response}"
  append_log(message)

def run_application():
  """Runs the GUI application."""
  def select_input_file():
      filepath = filedialog.askopenfilename()
      input_file_var.set(filepath)

  def select_source_folder():
      folderpath = filedialog.askdirectory()
      source_folder_var.set(folderpath)

  def start_processing():
      input_file = input_file_var.get()
      source_folder = source_folder_var.get()
      prompt = prompt_text.get("1.0", tk.END).strip()
      processing_type = processing_type_var.get()

      if not input_file or not os.path.exists(input_file):
          messagebox.showerror("Error", "Please select a valid input file.")
          return
      if not source_folder or not os.path.exists(source_folder):
          messagebox.showerror("Error", "Please select a valid source folder.")
          return
      if not prompt:
          messagebox.showerror("Error", "Please enter a prompt.")
          return

      # Clear the log window before starting
      log_text.delete('1.0', tk.END)

      if processing_type == "Video":
          # Process video
          frames_folder = os.path.join(source_folder, "frames")
          output_video_path = os.path.join(source_folder, "processed_video.mp4")
          frame_indices = video_to_frames(input_file, frames_folder)
          responses = process_frames(frames_folder, prompt)
          recreate_video(frames_folder, frame_indices, output_video_path, input_file, responses)
          messagebox.showinfo("Success", f"Video processing complete. Output saved to {output_video_path}.")
      else:
          # Process image
          process_image(input_file, prompt)
          messagebox.showinfo("Success", f"Image processing complete.")

  # Create the main window
  global root
  root = tk.Tk()
  root.title("Beam")

  # Input file selection
  input_file_var = tk.StringVar()
  tk.Label(root, text="Input File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
  tk.Entry(root, textvariable=input_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
  tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

  # Source folder selection
  source_folder_var = tk.StringVar()
  tk.Label(root, text="Source Folder:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
  tk.Entry(root, textvariable=source_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
  tk.Button(root, text="Browse", command=select_source_folder).grid(row=1, column=2, padx=5, pady=5)

  # Prompt text
  tk.Label(root, text="Prompt:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
  prompt_text = tk.Text(root, width=50, height=5)
  prompt_text.grid(row=2, column=1, padx=5, pady=5)

  # Processing type (Video or Image)
  processing_type_var = tk.StringVar(value="Video")
  tk.Label(root, text="Processing Type:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
  ttk.Combobox(root, textvariable=processing_type_var, values=["Video", "Image"]).grid(row=3, column=1, padx=5, pady=5)

  # Start button
  tk.Button(root, text="Start Processing", command=start_processing).grid(row=4, column=1, padx=5, pady=20)

  # Display area for logs and outputs
  global log_text
  log_text = tk.Text(root, width=70, height=15)
  log_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

  root.mainloop()

if __name__ == '__main__':
  run_application()
