# /backend/trader_app/app.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import csv
import os
import json
from PIL import Image, ImageTk

class TraderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trader Manager")
        self.root.geometry("900x700")

        self.mode = tk.StringVar(value="Nenhum")
        self.performance_data = [100, 105, 110, 95, 120]
        self.robot_status = {"Robô 1": "Inativo", "Robô 2": "Inativo", "Robô 3": "Inativo"}
        
        # Carregar imagens para ligar/desligar
        self.on_image = ImageTk.PhotoImage(Image.open("path_to_on_image.png").resize((40, 20)))
        self.off_image = ImageTk.PhotoImage(Image.open("path_to_off_image.png").resize((40, 20)))

        # ===== FRAME PRINCIPAL =====
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # ===== FRAMES =====
        self.create_control_frame()
        self.create_config_frame()
        self.create_log_frame()
        self.create_robot_frame()
        self.create_graph_frame()

        # Carregar configurações do arquivo JSON
        saved_config = self.load_config()
        self.mode.set(saved_config.get("mode", "Nenhum"))
        self.robot_status.update(saved_config.get("robot_status", {}))

    def create_control_frame(self):
        """Criação do frame de controle"""
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controle de Modos", padding=10)
        self.control_frame.grid(row=0, column=0, sticky="ew", pady=5)

        self.auto_mode_button = ttk.Button(self.control_frame, text="Modo Automático", command=self.switch_to_auto)
        self.auto_mode_button.grid(row=0, column=0, padx=5, pady=5)

        self.manual_mode_button = ttk.Button(self.control_frame, text="Modo Manual", command=self.switch_to_manual)
        self.manual_mode_button.grid(row=0, column=1, padx=5, pady=5)

        self.mode_label = ttk.Label(self.control_frame, text="Modo Atual: Nenhum", font=("Arial", 12))
        self.mode_label.grid(row=1, column=0, columnspan=2, pady=5)

    def create_config_frame(self):
        """Criação do frame de configurações"""
        self.config_frame = ttk.LabelFrame(self.main_frame, text="Configurações e Parâmetros", padding=10)
        self.config_frame.grid(row=1, column=0, sticky="ew", pady=5)

        self.param_label = ttk.Label(self.config_frame, text="Parâmetro (Modo Manual):")
        self.param_label.grid(row=0, column=0, pady=5, sticky="w")

        self.param_button = ttk.Button(self.config_frame, text="Enviar Parâmetro", command=self.ask_and_send_param)
        self.param_button.grid(row=0, column=2, padx=5, pady=5)

        self.stop_loss_label = ttk.Label(self.config_frame, text="Stop Loss:")
        self.stop_loss_label.grid(row=1, column=0, pady=5, sticky="w")

        self.stop_loss_entry = ttk.Entry(self.config_frame, width=25)
        self.stop_loss_entry.grid(row=1, column=1, pady=5)

        self.stop_win_label = ttk.Label(self.config_frame, text="Stop Win:")
        self.stop_win_label.grid(row=2, column=0, pady=5, sticky="w")

        self.stop_win_entry = ttk.Entry(self.config_frame, width=25)
        self.stop_win_entry.grid(row=2, column=1, pady=5)

        self.apply_limits_button = ttk.Button(self.config_frame, text="Aplicar Metas", command=self.apply_limits)
        self.apply_limits_button.grid(row=3, column=0, columnspan=3, pady=5)

    def create_log_frame(self):
        """Criação do frame de logs"""
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Logs", padding=10)
        self.log_frame.grid(row=2, column=0, sticky="nsew", pady=5)

        self.log_area = ScrolledText(self.log_frame, width=70, height=10, state='disabled', font=("Arial", 10))
        self.log_area.grid(row=0, column=0, padx=5, pady=5)

        self.export_log_button = ttk.Button(self.log_frame, text="Exportar Logs", command=self.export_logs)
        self.export_log_button.grid(row=1, column=0, pady=5)

    def create_robot_frame(self):
        """Criação do frame de gerenciamento de robôs"""
        self.robot_frame = ttk.LabelFrame(self.main_frame, text="Gerenciamento de Robôs", padding=10)
        self.robot_frame.grid(row=3, column=0, sticky="ew", pady=5)

        self.robot_buttons = {}  # Para armazenar referências aos botões de ligar/desligar

        for i, (robot, status) in enumerate(self.robot_status.items()):
            ttk.Label(self.robot_frame, text=f"{robot}:").grid(row=i, column=0, sticky="w")
            status_label = ttk.Label(self.robot_frame, text=status)
            status_label.grid(row=i, column=1, padx=5)

            toggle_button = ttk.Button(self.robot_frame, text="Ligar" if status == "Inativo" else "Desligar",
                                        command=lambda r=robot, s=status_label: self.toggle_robot(r, s))
            toggle_button.grid(row=i, column=2, padx=5)

            self.robot_buttons[robot] = toggle_button  # Armazenar referência do botão

    def create_graph_frame(self):
        """Criação do frame para gráficos"""
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Gráficos", padding=10)
        self.graph_frame.grid(row=4, column=0, sticky="ew", pady=5)

        self.show_graph_button = ttk.Button(self.graph_frame, text="Exibir Gráfico", command=self.show_graph)
        self.show_graph_button.grid(row=0, column=0, pady=5)

    def switch_to_auto(self):
        """Switch para modo automático"""
        self.mode.set("Automático")
        self.mode_label.config(text=f"Modo Atual: {self.mode.get()}")

    def switch_to_manual(self):
        """Switch para modo manual"""
        self.mode.set("Manual")
        self.mode_label.config(text=f"Modo Atual: {self.mode.get()}")

    def ask_and_send_param(self):
        """Solicita parâmetro ao usuário e envia"""
        param = simpledialog.askstring("Entrada", "Informe o parâmetro manual para o robô:")
        self.log(f"Parâmetro manual enviado: {param}")

    def apply_limits(self):
        """Aplica limites de stop loss e stop win"""
        try:
            stop_loss = float(self.stop_loss_entry.get())
            stop_win = float(self.stop_win_entry.get())
            self.log(f"Stop Loss: {stop_loss}, Stop Win: {stop_win}")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para Stop Loss e Stop Win.")

    def log(self, message):
        """Log de mensagens"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{timestamp} - {message}\n")
        self.log_area.config(state='disabled')
        self.log_area.yview(tk.END)

    def show_graph(self):
        """Exibe gráfico de performance"""
        fig, ax = plt.subplots()
        ax.plot(self.performance_data, label="Desempenho")
        ax.set_title("Gráfico de Performance")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().grid(row=1, column=0)
        canvas.draw()

    def export_logs(self):
        """Exporta logs para um arquivo CSV"""
        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_file = os.path.join("logs", "log.csv")
        with open(log_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Mensagem"])
            for i in range(self.log_area.index(tk.END) - 1):
                row = self.log_area.get(i).strip()
                writer.writerow([row.split(" ")[0], row.split(" ")[1]])

        self.log("Logs exportados com sucesso.")

    def toggle_robot(self, robot, status_label):
        """Alterna entre ligar e desligar o robô"""
        new_status = "Ativo" if self.robot_status[robot] == "Inativo" else "Inativo"
        self.robot_status[robot] = new_status
        status_label.config(text=new_status)
        
        # Exibindo mensagem de confirmação
        messagebox.showinfo("Status do Robô", f"{robot} agora está {new_status}.")
        self.log(f"{robot} agora está {new_status}.")
        status_label.config(text=new_status)

    def save_config(self, config_data):
        """Salva as configurações em arquivo JSON"""
        try:
            with open("config.json", "w") as file:
                json.dump(config_data, file)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as configurações: {str(e)}")

    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                return json.load(file)
        return {}

# Execução da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = TraderApp(root)
    root.mainloop()
