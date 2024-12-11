import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from spellchecker import SpellChecker

def new_file():
    text_area.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))

def exit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def find_text():
    find_string = simpledialog.askstring("Find", "Enter text to find:")
    text_area.tag_remove("found", "1.0", tk.END)
    if find_string:
        idx = "1.0"
        while True:
            idx = text_area.search(find_string, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            lastidx = f"{idx}+{len(find_string)}c"
            text_area.tag_add("found", idx, lastidx)
            idx = lastidx
        text_area.tag_config("found", foreground="white", background="blue")

def replace_text():
    find_string = simpledialog.askstring("Find", "Enter text to find:")
    replace_string = simpledialog.askstring("Replace", "Enter text to replace with:")
    text_area.tag_remove("found", "1.0", tk.END)
    if find_string and replace_string:
        idx = "1.0"
        while True:
            idx = text_area.search(find_string, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            lastidx = f"{idx}+{len(find_string)}c"
            text_area.delete(idx, lastidx)
            text_area.insert(idx, replace_string)
            idx = f"{idx}+{len(replace_string)}c"

def update_word_count(event=None):
    text = text_area.get(1.0, tk.END)
    words = len(text.split())
    status_bar.config(text=f"Word Count: {words}")

def change_font():
    font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
    font_size = simpledialog.askinteger("Font", "Enter font size (e.g., 12):")
    if font_family and font_size:
        text_area.config(font=(font_family, font_size))

def spell_check():
    spell = SpellChecker()
    text = text_area.get(1.0, tk.END).split()
    misspelled = spell.unknown(text)
    
    text_area.tag_remove("misspelled", "1.0", tk.END)
    for word in misspelled:
        start_idx = "1.0"
        while True:
            start_idx = text_area.search(word, start_idx, nocase=1, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(word)}c"
            text_area.tag_add("misspelled", start_idx, end_idx)
            start_idx = end_idx
    text_area.tag_config("misspelled", foreground="red", underline=1)

root = tk.Tk()
root.title("Notepad")

text_area = tk.Text(root, undo=True, wrap="word")
text_area.pack(fill=tk.BOTH, expand=1)
text_area.bind("<KeyRelease>", update_word_count)

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Replace", command=replace_text)
edit_menu.add_separator()
edit_menu.add_command(label="Spell Check", command=spell_check)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Font", command=change_font)
menu_bar.add_cascade(label="Format", menu=format_menu)

root.config(menu=menu_bar)

status_bar = tk.Label(root, text="Word Count: 0", anchor="w")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()