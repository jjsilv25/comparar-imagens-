import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import pytesseract
import difflib

class TextDiffApp:
    def __init__(self, root):
        self.root = root
        self.image1_path = None
        self.image2_path = None
        self.text1 = ""
        self.text2 = ""
        self.diff = ""

        self.image1_label = tk.Label(
            self.root, text="Imagem 1 não selecionada")
        self.image1_label.pack()
        self.image1_button = tk.Button(
            self.root, text="Selecionar Imagem do laboratorio", command=self.browse_image1)
        self.image1_button.pack()

        self.image2_label = tk.Label(
            self.root, text="Imagem 2 não selecionada")
        self.image2_label.pack()
        self.image2_button = tk.Button(
            self.root, text="Selecionar Imagem do ensaque", command=self.browse_image2)
        self.image2_button.pack()

        self.compare_button = tk.Button(
            self.root, text="Comparar os texto das imagens", command=self.compare_images)
        self.compare_button.pack()

        self.text1_label = tk.Label(self.root, text="laboratorio:")
        self.text1_label.pack()
        self.text1_box = tk.Text(self.root, height=10, width=90)
        self.text1_box.pack()

        self.text2_label = tk.Label(self.root, text="ensaque:")
        self.text2_label.pack()
        self.text2_box = tk.Text(self.root, height=10, width=90)
        self.text2_box.pack()

        self.diff_label = tk.Label(self.root, text="Diferença:")
        self.diff_label.pack()
        self.diff_box = tk.Text(self.root, height=10, width=90)
        self.diff_box.pack()

        # Adiciona uma configuração para a tag "diff"
        self.diff_box.tag_configure("diff", foreground="red")

    def browse_image1(self):
        image_path = filedialog.askopenfilename()
        self.image1_label.config(text=image_path)
        self.image1_path = image_path

    def browse_image2(self):
        image_path = filedialog.askopenfilename()
        self.image2_label.config(text=image_path)
        self.image2_path = image_path

    def compare_images(self):
        highlighted1 = ""
        highlighted2 = ""
        if self.image1_path and self.image2_path:
            image1 = Image.open(self.image1_path)
            self.text1 = pytesseract.image_to_string(image1)
            self.text1_box.delete("1.0", tk.END)
            self.text1_box.insert(tk.END, self.text1)

            image2 = Image.open(self.image2_path)
            self.text2 = pytesseract.image_to_string(image2)
            self.text2_box.delete("1.0", tk.END)
            self.text2_box.insert(tk.END, self.text2)

            if self.text1 == self.text2:
                self.diff_box.delete("1.0", tk.END)
                self.diff_box.insert(tk.END, "Os textos são iguais.")
            else:
                diff1 = list(difflib.ndiff(self.text1, self.text2))
                diff2 = list(difflib.ndiff(self.text2, self.text1))

                for diff in diff1:
                    if diff[0] == ' ':
                        highlighted1 += diff[2]
                    elif diff[0] == '-':
                        highlighted1 += '{{{}}}'.format(diff[2])

                for diff in diff2:
                    if diff[0] == ' ':
                        highlighted2 += diff[2]
                    elif diff[0] == '-':
                        highlighted2 += '{{{}}}'.format(diff[2])

                self.diff = highlighted1
                self.diff_box.delete("1.0", tk.END)
                self.diff_box.insert(tk.END, highlighted1)
                self.diff_box.tag_add("diff", "1.0", "end")
if __name__ == "__main__":
    root = tk.Tk()
    app = TextDiffApp(root)
    root.mainloop()
