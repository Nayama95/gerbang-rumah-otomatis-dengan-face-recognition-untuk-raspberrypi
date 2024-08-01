import os
import tkinter as tk

def tampilkan_file():
    # Ganti path dengan path direktori yang ingin Anda tampilkan
    path = "db"
    # Hapus semua widget pada frame
    for widget in frame.winfo_children():
        widget.destroy()
    # Tampilkan semua file dalam direktori
    for i, file in enumerate(os.listdir(path)):
        label = tk.Label(frame, text=file)
        label.grid(row=i, column=0)

root = tk.Tk()
root.title("File Manager")
root.geometry("400x400")

button = tk.Button(root, text="Tampilkan File", command=tampilkan_file)
button.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

root.mainloop()