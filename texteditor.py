import tkinter as tk
from tkinter import filedialog, colorchooser, font, ttk, messagebox
from PIL import Image, ImageTk
import cohere
import os

# Store the API key in a separate variable
COHERE_API_KEY = 'dsUln49CQ0VTH4m73N0M5IAkAq8U0iJoKsrVKgXd'

class AIEnhancedTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Enhanced Text Editor")
        self.root.geometry("900x600")

        # Initialize Cohere client
        if not COHERE_API_KEY:
            messagebox.showerror("API Key Error", "Please set the COHERE_API_KEY.")
            root.destroy()
            return
        self.co = cohere.Client(COHERE_API_KEY)

        self.setup_ui()

    def setup_ui(self):
        # Main text area
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(expand=True, fill='both', pady=5)

        self.text_area = tk.Text(self.text_frame, wrap='word', undo=True)
        self.text_area.pack(side='left', expand=True, fill='both')

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # Toolbar
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side='top', fill='x')

        self.setup_toolbar_buttons()

        # AI Functions Frame
        self.ai_frame = tk.Frame(self.root)
        self.ai_frame.pack(side='right', fill='y')

        self.setup_ai_buttons()

        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", anchor='e')
        self.status_bar.pack(side='bottom', fill='x')

    def setup_toolbar_buttons(self):
        buttons = [
            ("New", self.new_file),
            ("Open", self.open_file),
            ("Save", self.save_file),
            ("Bold", self.toggle_bold),
            ("Italic", self.toggle_italic),
            ("Underline", self.toggle_underline),
            ("Color", self.change_text_color),
        ]

        for text, command in buttons:
            button = tk.Button(self.toolbar, text=text, command=command)
            button.pack(side='left', padx=2, pady=2)

    def setup_ai_buttons(self):
        ai_buttons = [
            ("Content Suggestion", self.content_suggestion),
            ("Vocabulary Enhancement", self.vocabulary_enhancement),
            ("Grammar Check", self.grammar_check),
            ("Text Improvement", self.text_improvement),
        ]

        for text, command in ai_buttons:
            button = tk.Button(self.ai_frame, text=text, command=command)
            button.pack(side='top', padx=2, pady=2, fill='x')

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.root.title("New File - AI-Enhanced Text Editor")
        self.status_bar.config(text="New File Created")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.root.title(f"{file_path} - AI-Enhanced Text Editor")
            self.status_bar.config(text=f"Opened {file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"{file_path} - AI-Enhanced Text Editor")
            self.status_bar.config(text=f"Saved {file_path}")

    def toggle_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
        self.text_area.tag_configure("bold", font=('TkDefaultFont', 10, 'bold'))

    def toggle_italic(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
        self.text_area.tag_configure("italic", font=('TkDefaultFont', 10, 'italic'))

    def toggle_underline(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
        self.text_area.tag_configure("underline", underline=True)

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_add("color", "sel.first", "sel.last")
            self.text_area.tag_configure("color", foreground=color)

    def content_suggestion(self):
        selected_text = self.text_area.get("sel.first", "sel.last")
        if selected_text:
            prompt = f"Based on the following text, suggest additional content or next points:\n\n{selected_text}\n\nSuggestion:"
            response = self.co.generate(
                model='command-nightly',
                prompt=prompt,
                max_tokens=50,  # Increased max tokens for more detailed content
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE')
            suggestion = response.generations[0].text.strip()
            self.show_ai_result("Content Suggestion", suggestion)
        else:
            self.status_bar.config(text="Please select text for content suggestion")

    def vocabulary_enhancement(self):
        selected_text = self.text_area.get("sel.first", "sel.last")
        if selected_text:
            prompt = f"Enhance the vocabulary of the following text by suggesting alternative words or phrases:\n\n{selected_text}\n\nEnhanced version:"
            response = self.co.generate(
                model='command-nightly',
                prompt=prompt,
                max_tokens=50,  # Increased max tokens for more vocabulary variation
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE')
            enhanced = response.generations[0].text.strip()
            self.show_ai_result("Vocabulary Enhancement", enhanced)
        else:
            self.status_bar.config(text="Please select text for vocabulary enhancement")

    def grammar_check(self):
        content = self.text_area.get(1.0, tk.END)
        response = self.co.generate(
            model='command-nightly',
            prompt=f"Check the following text for grammar issues and provide corrections:\n\n{content}\n\nGrammar check results:",
            max_tokens=50,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE')
        result = response.generations[0].text.strip()
        self.show_ai_result("Grammar Check", result)

    def text_improvement(self):
        content = self.text_area.get(1.0, tk.END)
        response = self.co.generate(
            model='command-nightly',
            prompt=f"Improve the following text by correcting errors and enhancing clarity:\n\n{content}\n\nImproved version:",
            max_tokens=200,  # Adjusted token limit for more thorough improvements
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE')
        result = response.generations[0].text.strip()
        self.show_ai_result("Text Improvement", result)

    def show_ai_result(self, title, result):
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("400x300")
        
        result_text = tk.Text(result_window, wrap='word')
        result_text.pack(expand=True, fill='both')
        result_text.insert(tk.END, result)
        result_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    editor = AIEnhancedTextEditor(root)
    root.mainloop()



