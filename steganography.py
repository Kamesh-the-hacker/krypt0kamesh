import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import os

class SteganographyDecoder:
    def __init__(self, root):
        self.root = root
        self.root.title("KRYPT0KAMESH-DEVELOPED BY KAMESH")
        self.root.geometry("1000x800")
        
        # Load and set background image
        self.setup_background()
        
        # Variables
        self.image_path = tk.StringVar()
        self.decoded_text = tk.StringVar()
        self.image_display = None
        
        self.setup_ui()
    
    def setup_background(self):
        """Setup background image"""
        try:
            # Load and resize background image
            bg_image = Image.open("image.jpg")
            bg_image = bg_image.resize((1000, 800), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Create background label
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except FileNotFoundError:
            # If background image not found, use dark theme
            self.root.configure(bg='#1e1e1e')
        except Exception as e:
            print(f"Error loading background: {e}")
            self.root.configure(bg='#1e1e1e')
    
    def setup_ui(self):
        # Create main frame with semi-transparent background for better visibility
        main_frame = tk.Frame(self.root, bg='#2d2d2d', relief='raised', bd=2)
        main_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        # Configure style for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TLabelframe', background='#3d3d3d', foreground='white')
        style.configure('Dark.TLabel', background='#3d3d3d', foreground='white')
        style.configure('Dark.TButton', background='#4d4d4d', foreground='white')
        style.configure('Dark.TEntry', background='#4d4d4d', foreground='white')
        
        # Create inner container
        container = tk.Frame(main_frame, bg='#3d3d3d', padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(container, text="KryptKamesh Image Encoder/Decoder", 
                              font=('VT323', 20, 'bold'), bg='#3d3d3d', fg='white')
        title_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = tk.LabelFrame(container, text="Select Image", font=('VT323', 12), 
                                  bg='#3d3d3d', fg='white', padx=10, pady=10)
        file_frame.pack(fill='x', pady=(0, 10))
        
        path_frame = tk.Frame(file_frame, bg='#3d3d3d')
        path_frame.pack(fill='x')
        
        tk.Label(path_frame, text="Image Path:", bg='#3d3d3d', fg='white', font=('VT323', 10)).pack(side='left')
        
        path_entry = tk.Entry(path_frame, textvariable=self.image_path, state='readonly', 
                             bg='#4d4d4d', fg='white', width=50, font=('VT323', 10))
        path_entry.pack(side='left', padx=(5, 5), fill='x', expand=True)
        
        browse_btn = tk.Button(path_frame, text="Browse", command=self.browse_image,
                              bg='#5d5d5d', fg='white', activebackground='#6d6d6d', font=('VT323', 10))
        browse_btn.pack(side='right')
        
        # Control buttons frame
        control_frame = tk.Frame(container, bg='#3d3d3d')
        control_frame.pack(pady=10)
        
        encode_btn = tk.Button(control_frame, text="Encode Message", command=self.encode,
                              bg="#d22323", fg='white', activebackground='#005999', 
                              font=('VT323', 12, 'bold'), padx=20)
        encode_btn.pack(side='left', padx=(0, 10))
        
        decode_btn = tk.Button(control_frame, text="Decode Message", command=self.decode_message,
                              bg='#007acc', fg='white', activebackground='#005999', 
                              font=('VT323', 12, 'bold'), padx=20)
        decode_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(control_frame, text="Clear", command=self.clear_all,
                             bg="#6048E8", fg='white', activebackground='#6d6d6d', padx=20, font=('VT323', 12))
        clear_btn.pack(side='left', padx=(0, 10))
        
        save_btn = tk.Button(control_frame, text="Save Text", command=self.save_text,
                            bg="#60f233", fg='white', activebackground='#6d6d6d', padx=20, font=('VT323', 12))
        save_btn.pack(side='left')
        
        # Results frame
        results_frame = tk.LabelFrame(container, text="Results", font=('VT323', 12),
                                     bg='#3d3d3d', fg='white', padx=10, pady=10)
        results_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Create two-column layout
        left_frame = tk.Frame(results_frame, bg='#3d3d3d')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        right_frame = tk.Frame(results_frame, bg='#3d3d3d')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Image preview
        tk.Label(left_frame, text="Image Preview", bg='#3d3d3d', fg='white', 
                font=('VT323', 12, 'bold')).pack()
        
        self.image_frame = tk.Frame(left_frame, relief='sunken', borderwidth=2, bg='#2d2d2d')
        self.image_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.image_label = tk.Label(self.image_frame, text="No image selected", 
                                   bg='#2d2d2d', fg='white', font=('VT323', 11))
        self.image_label.pack(expand=True)
        
        # Message text area (single text area for both input and output)
        tk.Label(right_frame, text="Message (Input/Output)", bg='#3d3d3d', fg='white',
                font=('VT323', 12, 'bold')).pack()
        
        # Create frame for text area and scrollbar
        text_frame = tk.Frame(right_frame, bg='#3d3d3d')
        text_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        # Single text area for both encoding input and decoding output
        self.text_area = tk.Text(text_frame, height=25, width=40, wrap='word', 
                                font=('VT323', 11), bg='#2d2d2d', fg='white',
                                insertbackground='white')
        self.text_area.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for text area
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.text_area.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Enter message to encode or select image to decode")
        status_bar = tk.Label(container, textvariable=self.status_var, 
                             relief='sunken', anchor='w', bg='#2d2d2d', fg='white', font=('VT323', 10))
        status_bar.pack(fill='x', pady=(10, 5))
        
        # Footer with developer credit
        footer_frame = tk.Frame(container, bg='#3d3d3d')
        footer_frame.pack(fill='both', pady=(5, 0))
        
        footer_label = tk.Label(footer_frame, text="KRYPT0KAMESH - DEVELOPED BY KAMESH", 
                               font=('VT323', 11, 'italic'), bg="#3acb00", fg='#cccccc')
        footer_label.pack(pady=5)
    
    def browse_image(self):
        """Open file dialog to select an image"""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Image to Encode/Decode",
            filetypes=file_types
        )
        
        if filename:
            self.image_path.set(filename)
            self.load_image_preview(filename)
            self.status_var.set(f"Image loaded: {os.path.basename(filename)}")
    
    def load_image_preview(self, image_path):
        """Load and display image preview"""
        try:
            # Open and resize image for preview
            image = Image.open(image_path)
            
            # Calculate size to fit in preview area (max 300x300)
            max_size = 300
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.image_display = ImageTk.PhotoImage(image)
            
            # Update label
            self.image_label.configure(image=self.image_display, text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image preview:\n{str(e)}")
            self.image_label.configure(image="", text="Failed to load image")
    
    def decode_message(self):
        """Decode hidden message from the selected image"""
        if not self.image_path.get():
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        try:
            self.status_var.set("Decoding message... Please wait...")
            self.root.update()
            
            # Load the image
            image = Image.open(self.image_path.get())
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract hidden message
            decoded_message = self.extract_message(image)
            
            if decoded_message:
                # Clear the text area and display decoded message
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, decoded_message)
                self.status_var.set(f"Message decoded successfully! Length: {len(decoded_message)} characters")
            else:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, "No hidden message found or invalid format.")
                self.status_var.set("No message found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode message:\n{str(e)}")
            self.status_var.set("Decoding failed")
    
    def extract_message(self, image):
        """Extract message using LSB steganography"""
        width, height = image.size
        binary_message = ""
        
        # Extract bits from LSB of each color channel
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                
                # Extract LSB from each RGB channel
                for channel in range(3):  # R, G, B
                    binary_message += str(pixel[channel] & 1)
        
        # Convert binary to text
        message = ""
        delimiter = "1111111111111110"  # Common delimiter pattern
        
        # Look for delimiter to find end of message
        if delimiter in binary_message:
            binary_message = binary_message[:binary_message.find(delimiter)]
        
        # Convert binary to characters (8 bits = 1 character)
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                try:
                    char_code = int(byte, 2)
                    if char_code == 0:  # Null terminator
                        break
                    if 32 <= char_code <= 126 or char_code in [9, 10, 13]:  # Printable ASCII
                        message += chr(char_code)
                    else:
                        # Non-printable character might indicate end of message
                        break
                except ValueError:
                    break
        
        return message.strip() if message else None
    
    def clear_all(self):
        """Clear all fields and reset the interface"""
        self.image_path.set("")
        self.text_area.delete(1.0, tk.END)
        self.image_label.configure(image="", text="No image selected")
        self.image_display = None
        self.status_var.set("Ready - Enter message to encode or select image to decode")
    
    def save_text(self):
        """Save decoded text to a file"""
        text_content = self.text_area.get(1.0, tk.END).strip()
        
        if not text_content:
            messagebox.showwarning("Warning", "No text to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                messagebox.showinfo("Success", f"Text saved to:\n{filename}")
                self.status_var.set(f"Text saved: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def encode_message(self, image_path, message, output_path):
        """Encode message into image using LSB steganography"""
        img = Image.open(image_path)
        img = img.convert("RGB")
        
        binary_msg = ''.join([format(ord(c), '08b') for c in message]) + '1111111111111110'  # End marker
        data_index = 0
        img_data = list(img.getdata())
        new_data = []

        for pixel in img_data:
            r, g, b = pixel[:3]
            if data_index < len(binary_msg):
                r = (r & ~1) | int(binary_msg[data_index])
                data_index += 1
            if data_index < len(binary_msg):
                g = (g & ~1) | int(binary_msg[data_index])
                data_index += 1
            if data_index < len(binary_msg):
                b = (b & ~1) | int(binary_msg[data_index])
                data_index += 1
            new_data.append((r, g, b))
        
        img.putdata(new_data)
        img.save(output_path)
        return True

    def encode(self):
        """Encode message from text area into selected image"""
        if not self.image_path.get():
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        # Get message from the text area
        message = self.text_area.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encode in the text area!")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="Save Encoded Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if output_path:
            try:
                self.status_var.set("Encoding message...")
                self.root.update()
                
                success = self.encode_message(self.image_path.get(), message, output_path)
                if success:
                    messagebox.showinfo("Success", f"Message encoded and saved to:\n{output_path}")
                    self.status_var.set(f"Message encoded successfully: {os.path.basename(output_path)}")
                else:
                    messagebox.showerror("Error", "Failed to encode message.")
                    self.status_var.set("Encoding failed")
            except Exception as e:
                messagebox.showerror("Error", f"Encoding failed:\n{str(e)}")
                self.status_var.set("Encoding failed")

def main():
    root = tk.Tk()
    app = SteganographyDecoder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
