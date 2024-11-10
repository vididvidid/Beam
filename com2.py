import cv2
import os
import requests
import threading
import time
import pytesseract
from PIL import Image, ImageChops, ImageFilter, ImageGrab
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class CombinedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Suite")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.beam_frame = ttk.Frame(self.notebook)
        self.distraction_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.beam_frame, text='Beam')
        self.notebook.add(self.distraction_frame, text='Distraction Blocker')
        
        # Initialize both applications
        self.setup_beam_tab()
        self.setup_distraction_blocker_tab()

    def setup_beam_tab(self):
        # Input file selection
        self.input_file_var = tk.StringVar()
        tk.Label(self.beam_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(self.beam_frame, textvariable=self.input_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.beam_frame, text="Browse", command=self.select_input_file).grid(row=0, column=2, padx=5, pady=5)

        # Source folder selection
        self.source_folder_var = tk.StringVar()
        tk.Label(self.beam_frame, text="Source Folder:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(self.beam_frame, textvariable=self.source_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.beam_frame, text="Browse", command=self.select_source_folder).grid(row=1, column=2, padx=5, pady=5)

        # Prompt text
        tk.Label(self.beam_frame, text="Prompt:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.prompt_text = tk.Text(self.beam_frame, width=50, height=5)
        self.prompt_text.grid(row=2, column=1, padx=5, pady=5)

        # Processing type
        self.processing_type_var = tk.StringVar(value="Video")
        tk.Label(self.beam_frame, text="Processing Type:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Combobox(self.beam_frame, textvariable=self.processing_type_var, values=["Video", "Image"]).grid(row=3, column=1, padx=5, pady=5)

        # Start button
        tk.Button(self.beam_frame, text="Start Processing", command=self.start_beam_processing).grid(row=4, column=1, padx=5, pady=20)

        # Log text
        self.log_text = tk.Text(self.beam_frame, width=70, height=15)
        self.log_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def setup_distraction_blocker_tab(self):
        self.focus_topic = ''
        self.monitoring = False

        # Create GUI elements for distraction blocker
        self.prompt_label = tk.Label(self.distraction_frame, text="Enter your focus topic:")
        self.prompt_label.pack(pady=10)

        self.prompt_entry = tk.Entry(self.distraction_frame, width=50)
        self.prompt_entry.pack(pady=5)

        self.start_button = tk.Button(self.distraction_frame, text="Start", command=self.start_monitoring)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(self.distraction_frame, text="Status: Idle")
        self.status_label.pack(pady=5)

    # Beam tab methods
    def append_log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def select_input_file(self):
        filepath = filedialog.askopenfilename()
        self.input_file_var.set(filepath)

    def select_source_folder(self):
        folderpath = filedialog.askdirectory()
        self.source_folder_var.set(folderpath)

    def video_to_frames(self, video_path, frames_folder, frame_rate=1):
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
                current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                is_duplicate = False

                if previous_frame is not None:
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
        self.append_log(f"Extracted {count} frames to '{frames_folder}'.")
        return frame_indices

    def get_image_description(self, image_path, prompt):
        url = 'https://qa-pic.lizziepika.workers.dev/analyze-image'

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
            self.append_log(f"Failed to get description for {image_path}: HTTP {response.status_code}")
            return 'No description available.'

    def extract_yes_no(self, description):
        description_lower = description.strip().lower()
        if 'yes' in description_lower:
            return 'yes'
        elif 'no' in description_lower:
            return 'no'
        else:
            return 'no'

    def process_frames(self, frames_folder, prompt):
        frames = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])
        responses = []

        for i, frame in enumerate(frames):
            image_path = os.path.join(frames_folder, frame)
            description = self.get_image_description(image_path, prompt)
            
            response = self.extract_yes_no(description)
            responses.append((image_path, response))
            message = f"[{i+1}/{len(frames)}] Processed {frame}: {response}"
            self.append_log(message)
            
            time.sleep(1)

        return responses

    def recreate_video(self, frames_folder, frame_indices, output_video_path, original_video_path, responses):
        cap = cv2.VideoCapture(original_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        response_dict = dict(zip(frame_indices, responses))

        cap = cv2.VideoCapture(original_video_path)
        frame_number = 0
        prev_frame = None
        while True:
            success, frame = cap.read()
            if not success:
                break

            if frame_number in response_dict:
                response = response_dict[frame_number][1]

                if response == 'yes':
                    out.write(frame)
                    prev_frame = frame
                else:
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=15))
                    frame_blurred = cv2.cvtColor(np.array(blurred_img), cv2.COLOR_RGB2BGR)
                    out.write(frame_blurred)
                    prev_frame = frame_blurred
            else:
                if prev_frame is not None:
                    out.write(prev_frame)
            frame_number += 1

        cap.release()
        out.release()
        self.append_log(f"Video recreated and saved to '{output_video_path}'.")

    def process_image(self, image_path, prompt):
        description = self.get_image_description(image_path, prompt)
        response = description
        message = f"Processed {os.path.basename(image_path)}: {response}"
        self.append_log(message)

    def start_beam_processing(self):
        input_file = self.input_file_var.get()
        source_folder = self.source_folder_var.get()
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        processing_type = self.processing_type_var.get()

        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid input file.")
            return
        if not source_folder or not os.path.exists(source_folder):
            messagebox.showerror("Error", "Please select a valid source folder.")
            return
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt.")
            return

        self.log_text.delete('1.0', tk.END)

        if processing_type == "Video":
            frames_folder = os.path.join(source_folder, "frames")
            output_video_path = os.path.join(source_folder, "processed_video.mp4")
            frame_indices = self.video_to_frames(input_file, frames_folder)
            responses = self.process_frames(frames_folder, prompt)
            self.recreate_video(frames_folder, frame_indices, output_video_path, input_file, responses)
            messagebox.showinfo("Success", f"Video processing complete. Output saved to {output_video_path}.")
        else:
            self.process_image(input_file, prompt)
            messagebox.showinfo("Success", f"Image processing complete.")

    # Distraction Blocker tab methods
    def start_monitoring(self):
        self.focus_topic = self.prompt_entry.get()
        if not self.focus_topic.strip():
            messagebox.showwarning("Input Required", "Please enter your focus topic.")
            return

        self.status_label.config(text="Status: Monitoring screen for distractions...")
        self.monitoring = True

        monitoring_thread = threading.Thread(target=self.monitor, daemon=True)
        monitoring_thread.start()

    def monitor(self):
        baseline_screenshot = ImageGrab.grab()

        while self.monitoring:
            time.sleep(2)
            new_screenshot = ImageGrab.grab()

            if self.screens_are_different(baseline_screenshot, new_screenshot):
                self.process_changes(new_screenshot)
                baseline_screenshot = new_screenshot

    def screens_are_different(self, img1, img2):
        img1_small = img1.resize((100, 100)).convert('L')
        img2_small = img2.resize((100, 100)).convert('L')

        arr1 = np.array(img1_small)
        arr2 = np.array(img2_small)

        diff = np.sum(np.abs(arr1 - arr2))
        return diff > 0

    def process_changes(self, screenshot):
        gray_image = screenshot.convert('L')
        data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)

        distraction_boxes = []

        num_boxes = len(data['level'])
        for i in range(num_boxes):
            text = data['text'][i]
            if text.strip() == '':
                continue

            if self.focus_topic.lower() not in text.lower():
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                distraction_boxes.append((x, y, w, h))

        if distraction_boxes:
            self.overlay_distractions(distraction_boxes)
            self.status_label.config(text="Status: Blocking detected distractions.")
        else:
            self.status_label.config(text="Status: No distractions detected.")

    def overlay_distractions(self, boxes):
        overlay = tk.Toplevel(self.root)
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-topmost", True)
        overlay.config(bg='black')
        overlay.attributes('-alpha', 0.1)

        screen_width = overlay.winfo_screenwidth()
        screen_height = overlay.winfo_screenheight()
        canvas = tk.Canvas(overlay, width=screen_width, height=screen_height, highlightthickness=0)
        canvas.pack()

        canvas.create_rectangle(0, 0, screen_width, screen_height, fill='black', outline='')

        for box in boxes:
            x1, y1, w, h = box
            x2 = x1 + w
            y2 = y1 + h
            canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='')

        canvas.update()
        overlay.after(2000, overlay.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedApp(root)
    root.mainloop()
