# /backend/trader_app/ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
from datetime import datetime

class TraderAppUI:
    def __init__(self, root, robots, history, update_robot_list, add_robot, remove_robot, view_history, toggle_robot, execute_trade):
        self.root = root
        self.robots = robots
        self.history = history
        self.update_robot_list = update_robot_list
        self.add_robot = add_robot
        self.remove_robot = remove_robot
        self.view_history = view_history
        self.toggle_robot = toggle_robot
        self.execute_trade = execute_trade
        
        # Carregando as imagens para os estados on/off
        self.on_image = ImageTk.PhotoImage(Image.open("path_to_on_image.png").resize((20, 20)))
        self.off_image = ImageTk.PhotoImage(Image.open("path_to_off_image.png").resize((20, 20)))

        self.setup_ui()

    def setup_ui(self):
        """Configura a interface gráfica com o menu, lista de robôs, botões, etc."""
        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        config_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Configurações", menu=config_menu)
        config_menu.add_command(label="Adicionar Robô", command=self.add_robot)
        config_menu.add_command(label="Remover Robô", command=self.remove_robot)

        # Lista de Robôs
        self.robot_listbox = tk.Listbox(self.root, width=50, height=10)
        self.robot_listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Botão para visualizar histórico
        self.view_history_button = tk.Button(self.root, text="Ver Histórico", command=self.view_history)
        self.view_history_button.grid(row=1, column=2, padx=10, pady=5)

        # Botão para executar operações
        self.execute_trade_button = tk.Button(self.root, text="Executar Operação", command=self.execute_trade)
        self.execute_trade_button.grid(row=2, column=2, padx=10, pady=5)

        # Atualizar a lista de robôs
        self.update_robot_list()

    def update_robot_list(self):
        """Limpa a lista de robôs e atualiza com o status atual de cada robô."""
        # Limpa a lista
        self.robot_listbox.delete(0, tk.END)

        # Adiciona robôs na lista
        row = 1  # Começando a adicionar os botões na segunda linha
        for robot_name, data in self.robots.items():
            status = data["status"]
            self.robot_listbox.insert(tk.END, f"{robot_name} - {status}")

            # Botão de toggle (on/off) para cada robô
            toggle_button = tk.Button(self.root, image=self.on_image if status == "on" else self.off_image,
                                      command=lambda name=robot_name: self.toggle_robot(name))
            toggle_button.grid(row=row, column=4, padx=5, pady=5)

            row += 1  # Avança para a próxima linha na grade

    def view_history(self):
        """Mostra o histórico em uma nova janela."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Histórico de Operações")
        history_listbox = tk.Listbox(history_window, width=50, height=10)
        history_listbox.pack(padx=10, pady=10)

        for entry in self.history:
            history_listbox.insert(tk.END, entry)

    def add_robot(self):
        """Solicita ao usuário que insira o nome de um novo robô e adiciona à lista."""
        new_robot_name = simpledialog.askstring("Novo Robô", "Digite o nome do novo robô:")
        if new_robot_name:
            # Adiciona o novo robô
            self.robots[new_robot_name] = {"status": "off"}
            self.update_robot_list()
            messagebox.showinfo("Sucesso", f"Robô {new_robot_name} adicionado com sucesso!")

    def remove_robot(self):
        """Remove o robô selecionado da lista."""
        selected_robot = self.robot_listbox.curselection()
        if selected_robot:
            robot_name = self.robot_listbox.get(selected_robot).split(" - ")[0]
            del self.robots[robot_name]
            self.update_robot_list()
            messagebox.showinfo("Sucesso", f"Robô {robot_name} removido com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione um robô para remover.")

    def toggle_robot(self, robot_name):
        """Alterna o status de um robô entre 'on' e 'off'."""
        robot_data = self.robots[robot_name]
        new_status = "off" if robot_data["status"] == "on" else "on"
        robot_data["status"] = new_status
        self.update_robot_list()
        messagebox.showinfo("Status Alterado", f"Robô {robot_name} agora está {new_status}.")

    def execute_trade(self):
        """Exemplo de execução de trade (essa função pode ser expandida para lógica real de trading)."""
        symbol = simpledialog.askstring("Entrada de Trade", "Digite o símbolo do ativo:")
        action = simpledialog.askstring("Entrada de Trade", "Digite a ação (compra/venda):")
        amount = simpledialog.askfloat("Entrada de Trade", "Digite o valor para a operação:")

        # Exemplo de execução de trade
        trade_response = self.execute_trade(symbol, action, amount)
        if trade_response:
            messagebox.showinfo("Operação Executada", f"Operação {action} no ativo {symbol} realizada com sucesso!")
            self.history.append(f"{datetime.now()} - {action.capitalize()} {amount} {symbol}")
            self.update_history()

    def update_history(self):
        """Atualiza o histórico de operações na interface gráfica."""
        # Atualiza o histórico na interface
        for entry in self.history:
            print(entry)  # Imprime no console ou exibe na interface (exemplo simples)

