
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import subprocess

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        self.canvas_width = 320
        self.canvas_height = 240
        self.max_objects = 50
        self.object_list = []  # Lista de objetos com 'x', 'y', 'w', 'h', 'name', 'run'
        
        # Criar área de desenho
        self.canvas = tk.Canvas(root, bg="black", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=10)
        
        # Botões
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.new_button = tk.Button(button_frame, text="New", command=self.new_canvas)
        self.new_button.pack(side=tk.LEFT, padx=5)
        
        self.erase_button = tk.Button(button_frame, text="Erase", command=self.erase_last)
        self.erase_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(button_frame, text="Save", command=self.save_list)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = tk.Button(button_frame, text="Load", command=self.load_list)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Variáveis de controle do desenho
        self.current_rect = None
        self.start_x = None
        self.start_y = None
        self.temp_name = ""
        self.temp_run = ""
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def new_canvas(self):
        """Limpa a área de desenho e a lista de objetos."""
        self.canvas.delete("all")
        self.object_list = []
    
    def on_click(self, event):
        """Inicia o desenho de um retângulo."""
        if len(self.object_list) < self.max_objects:
            self.start_x = event.x
            self.start_y = event.y
            self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="white")
           
    
    def on_drag(self, event):
        """Atualiza o tamanho do retângulo enquanto o mouse é arrastado."""
        if self.current_rect:
            self.canvas.coords(self.current_rect, self.start_x, self.start_y, event.x, event.y)
    
    def on_release(self, event):
        """Finaliza o desenho e armazena o objeto."""
        if self.current_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.current_rect)
            w = abs(x2 - x1)
            h = abs(y2 - y1)
             # Solicitar nome e comando para o retângulo
            self.temp_name = input("Digite o nome do objeto: ")
            self.temp_run = input("Digite o comando shell a ser executado (opcional): ")
            # Adiciona retângulo à lista com as informações de nome e comando
            self.object_list.append({
                "x": min(x1, x2), "y": min(y1, y2), "w": w, "h": h, 
                "name": self.temp_name, "run": self.temp_run
            })
            self.current_rect = None
    
    def erase_last(self):
        """Apaga o último objeto desenhado, se houver algum."""
        if self.object_list:
            self.object_list.pop()  # Remove o último item da lista
            self.redraw_objects()   # Redesenha todos os objetos restantes
        else:
            messagebox.showinfo("Aviso", "Nenhum objeto para apagar!")
    
    def redraw_objects(self):
        """Redesenha todos os objetos no canvas."""
        self.canvas.delete("all")
        for obj in self.object_list:
            self.canvas.create_rectangle(obj["x"], obj["y"], obj["x"] + obj["w"], obj["y"] + obj["h"], outline="white")
            self.canvas.create_text(obj["x"] + obj["w"] / 2, obj["y"] + obj["h"] / 2, text=obj["name"], fill="white")
    
    def save_list(self):
        """Salva a lista de objetos em um arquivo CSV."""
        if not self.object_list:
            messagebox.showinfo("Aviso", "Nenhum objeto para salvar!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for obj in self.object_list:
                    writer.writerow([int(obj["x"]), int(obj["y"]), int(obj["w"]), int(obj["h"]), obj["name"], obj["run"]])
            messagebox.showinfo("Sucesso", "Lista salva com sucesso!")
    
    def load_list(self):
        """Carrega a lista de objetos de um arquivo CSV."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, newline='') as file:
                    reader = csv.reader(file)
                    self.object_list = []
                    for row in reader:
                        self.object_list.append({
                            "x": int(row[0]), "y": int(row[1]), "w": int(row[2]), 
                            "h": int(row[3]), "name": row[4], "run": row[5]
                        })
                self.redraw_objects()
                messagebox.showinfo("Sucesso", "Lista carregada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
