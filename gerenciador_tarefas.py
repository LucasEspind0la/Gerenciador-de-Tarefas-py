import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import json
import os

# ------------------------------
# Configurações de estilo
# ------------------------------
BG_COLOR = "#0D0D0D"          # Preto profundo
FG_COLOR = "#F5F5F5"          # Cinza claro
ACCENT_COLOR = "#D4AF37"      # Dourado
HIGHLIGHT_COLOR = "#2A2A2A"   # Cinza escuro
FONT_DEFAULT = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")

# ------------------------------
# Persistência: carregar/salvar JSON
# ------------------------------
ARQUIVO_DADOS = "tarefas.json"

def carregar_tarefas():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar tarefas:\n{e}")
        return []

def salvar_tarefas(tarefas):
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar tarefas:\n{e}")

# ------------------------------
# Classe principal da aplicação
# ------------------------------
class GerenciadorTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.root.configure(bg=BG_COLOR)

        # Dados
        self.tarefas = carregar_tarefas()

        # Interface
        self.criar_widgets()
        self.atualizar_lista()

    def criar_widgets(self):
        # === Frame principal ===
        frame_principal = tk.Frame(self.root, bg=BG_COLOR)
        frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        titulo = tk.Label(
            frame_principal,
            text="Gerenciador de Tarefas",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT_COLOR,
            bg=BG_COLOR
        )
        titulo.pack(pady=(0, 15))

        # Entrada + categoria + data
        input_frame = tk.Frame(frame_principal, bg=BG_COLOR)
        input_frame.pack(fill="x", pady=(0, 15))

        # Campo de tarefa
        self.entry_tarefa = tk.Entry(
            input_frame,
            width=30,
            font=FONT_DEFAULT,
            bg="#1A1A1A",
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
            relief="flat"
        )
        self.entry_tarefa.pack(side="left", padx=(0, 10), ipady=5)
        self.entry_tarefa.bind("<Return>", lambda e: self.adicionar_tarefa())

        # Combobox de categoria
        self.combo_categoria = ttk.Combobox(
            input_frame,
            values=["Pessoal", "Estudo", "Trabalho"],
            state="readonly",
            width=10,
            font=("Segoe UI", 10)
        )
        self.combo_categoria.set("Estudo")
        self.combo_categoria.pack(side="left", padx=(0, 10))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="#1A1A1A",
                        background="#1A1A1A",
                        foreground=FG_COLOR,
                        selectbackground=HIGHLIGHT_COLOR)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#1A1A1A")],
                  selectbackground=[("readonly", HIGHLIGHT_COLOR)])

        # Data (hoje por padrão)
        hoje = date.today().strftime("%Y-%m-%d")
        self.entry_data = tk.Entry(
            input_frame,
            width=10,
            font=("Segoe UI", 10),
            bg="#1A1A1A",
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
            relief="flat"
        )
        self.entry_data.pack(side="left", padx=(0, 10), ipady=3)
        self.entry_data.insert(0, hoje)

        # Botão Adicionar
        self.botao_adicionar = tk.Button(
            input_frame,
            text="➕ Adicionar",
            command=self.adicionar_tarefa,
            bg=ACCENT_COLOR,
            fg=BG_COLOR,
            font=FONT_BOLD,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.botao_adicionar.pack(side="left")
        self.botao_adicionar.bind("<Enter>", lambda e: self.botao_adicionar.config(bg="#C19A2F"))
        self.botao_adicionar.bind("<Leave>", lambda e: self.botao_adicionar.config(bg=ACCENT_COLOR))

        # Lista de tarefas
        list_frame = tk.Frame(frame_principal, bg=BG_COLOR)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox_tarefas = tk.Listbox(
            list_frame,
            width=60,
            height=15,
            font=("Segoe UI", 10),
            bg="#121212",
            fg=FG_COLOR,
            selectbackground=HIGHLIGHT_COLOR,
            activestyle="none",
            relief="flat",
            bd=0,
            yscrollcommand=scrollbar.set,
            highlightthickness=0
        )
        self.listbox_tarefas.pack(fill="both", expand=True, padx=2)
        scrollbar.config(command=self.listbox_tarefas.yview)

        # Botões de ação
        btn_frame = tk.Frame(frame_principal, bg=BG_COLOR)
        btn_frame.pack(fill="x")

        self.criar_botao(btn_frame, "🗑️ Remover", self.remover_tarefa)
        self.criar_botao(btn_frame, "🧹 Limpar Concluídas", self.limpar_concluidas)
        self.criar_botao(btn_frame, "✅ Marcar como Concluída", self.marcar_concluida, ACCENT_COLOR)

    def criar_botao(self, parent, texto, comando, cor_bg=HIGHLIGHT_COLOR):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cor_bg,
            fg=FG_COLOR,
            font=FONT_DEFAULT,
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2"
        )
        btn.pack(side="left", padx=5, pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg="#3A3A3A" if cor_bg == HIGHLIGHT_COLOR else "#C19A2F"))
        btn.bind("<Leave>", lambda e: btn.config(bg=cor_bg))
        return btn

    def formatar_tarefa_para_exibicao(self, tarefa):
        desc = tarefa["descricao"]
        cat = tarefa["categoria"]
        data = tarefa["data"]
        concluida = tarefa["concluida"]
        status = "✓" if concluida else "○"
        return f"{status} [{cat}] {desc} — {data}"

    def atualizar_lista(self):
        self.listbox_tarefas.delete(0, tk.END)
        for i, t in enumerate(self.tarefas):
            texto = self.formatar_tarefa_para_exibicao(t)
            self.listbox_tarefas.insert(tk.END, texto)
            if t["concluida"]:
                self.listbox_tarefas.itemconfig(i, {"fg": "#666666", "selectforeground": "#888888"})

    def adicionar_tarefa(self):
        desc = self.entry_tarefa.get().strip()
        if not desc:
            messagebox.showwarning("Aviso", "Digite uma tarefa!")
            return

        categoria = self.combo_categoria.get()
        data = self.entry_data.get().strip()
        if not data:
            data = date.today().strftime("%Y-%m-%d")

        nova_tarefa = {
            "descricao": desc,
            "categoria": categoria,
            "data": data,
            "concluida": False
        }
        self.tarefas.append(nova_tarefa)
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()
        self.entry_tarefa.delete(0, tk.END)
        self.entry_tarefa.focus()

    def remover_tarefa(self):
        try:
            idx = self.listbox_tarefas.curselection()[0]
            self.tarefas.pop(idx)
            salvar_tarefas(self.tarefas)
            self.atualizar_lista()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

    def marcar_concluida(self):
        try:
            idx = self.listbox_tarefas.curselection()[0]
            self.tarefas[idx]["concluida"] = not self.tarefas[idx]["concluida"]
            salvar_tarefas(self.tarefas)
            self.atualizar_lista()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")

    def limpar_concluidas(self):
        self.tarefas = [t for t in self.tarefas if not t["concluida"]]
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()
        messagebox.showinfo("Limpeza", "Tarefas concluídas removidas.")

# ------------------------------
# Execução
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorTarefas(root)
    root.mainloop()