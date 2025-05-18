import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
from datetime import datetime

class JogoMinaFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("💣 Mina Explosiva Premium")
        self.root.geometry("450x550")
        self.root.configure(bg="#FFEBEE")
        self.root.resizable(False, False)
        
        # Configurações do jogo
        self.linhas = 8
        self.colunas = 8
        self.num_minas = 10
        self.pontuacao = 0
        self.jogador_atual = "Jogador"
        self.arquivo_ranking = "ranking.json"
        
        # Emojis temáticos
        self.emoji_tema = {
            "mina": random.choice(["💣", "💥", "🔥", "☠️", "👾"]),
            "bandeira": random.choice(["🚩", "🏴", "🎌", "📍", "🚨"]),
            "vitoria": random.choice(["🎉", "🏆", "✨", "👑", "🥇"]),
            "reiniciar": random.choice(["🔁", "🔄", "♻️", "🆕", "🔃"])
        }
        
        # Cores vibrantes
        self.cores = {
            "fundo": "#FFEBEE",
            "botao": "#E3F2FD",
            "botao_hover": "#BBDEFB",
            "texto": "#212121",
            "mina": "#F44336",
            "bandeira": "#FF5722",
            "vazio": "#E8F5E9",
            "destaque": "#FF4081",
            "top1": "#FFD700",
            "top2": "#C0C0C0",
            "top3": "#CD7F32"
        }
        
        # Fontes
        self.fonte_titulo = ("Segoe UI Emoji", 18, "bold")
        self.fonte_normal = ("Segoe UI Emoji", 12)
        self.fonte_pequena = ("Segoe UI Emoji", 10)
        self.fonte_ranking = ("Segoe UI Emoji", 11)
        
        # Iniciar com menu principal
        self.mostrar_menu()

    def mostrar_menu(self):
        self.limpar_tela()
        
        # Frame do título
        frame_titulo = tk.Frame(self.root, bg=self.cores["fundo"])
        frame_titulo.pack(pady=20)
        
        tk.Label(
            frame_titulo,
            text="💣 MINA EXPLOSIVA PREMIUM 💥",
            bg=self.cores["fundo"],
            fg="#D32F2F",
            font=self.fonte_titulo
        ).pack()
        
        # Frame dos botões
        frame_botoes = tk.Frame(self.root, bg=self.cores["fundo"])
        frame_botoes.pack(pady=30)
        
        botoes_menu = [
            ("🎮 INICIAR PARTIDA", self.iniciar_partida),
            ("🏆 VER RANKING", self.mostrar_ranking),
            ("⭐ SOBRE O JOGO", self.mostrar_sobre),
            ("🚪 SAIR", self.root.quit)
        ]
        
        for texto, comando in botoes_menu:
            btn = tk.Button(
                frame_botoes,
                text=texto,
                bg=self.cores["botao"],
                fg=self.cores["texto"],
                activebackground=self.cores["botao_hover"],
                font=self.fonte_normal,
                width=25,
                height=2,
                command=comando
            )
            btn.pack(pady=5)
    
    def iniciar_partida(self):
        nome = simpledialog.askstring("Nome do Jogador", "Digite seu nome:", parent=self.root)
        self.jogador_atual = nome if nome else "Jogador"
        
        self.limpar_tela()
        self.pontuacao = 0
        self.jogo_ativo = True
        self.tabuleiro = []
        self.botoes = []
        self.minas_restantes = self.num_minas
        
        # Frame do cabeçalho
        frame_cabecalho = tk.Frame(self.root, bg=self.cores["fundo"])
        frame_cabecalho.pack(pady=10)
        
        tk.Label(
            frame_cabecalho,
            text=f"Jogador: {self.jogador_atual}",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fonte_normal
        ).pack()
        
        self.label_minas = tk.Label(
            frame_cabecalho,
            text=f"{self.emoji_tema['bandeira']} Minas: {self.minas_restantes}",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fonte_normal
        )
        self.label_minas.pack()
        
        # Frame do tabuleiro
        frame_tabuleiro = tk.Frame(self.root, bg=self.cores["fundo"])
        frame_tabuleiro.pack(pady=10)
        
        # Inicializar tabuleiro
        self.inicializar_tabuleiro(frame_tabuleiro)
        
        # Botão de menu
        tk.Button(
            self.root,
            text="🏠 VOLTAR AO MENU",
            bg=self.cores["botao"],
            fg=self.cores["texto"],
            font=self.fonte_normal,
            command=self.mostrar_menu
        ).pack(pady=10)
    
    def inicializar_tabuleiro(self, frame):
        # Posicionar minas
        self.tabuleiro = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]
        minas_posicionadas = 0
        
        while minas_posicionadas < self.num_minas:
            x, y = random.randint(0, self.linhas-1), random.randint(0, self.colunas-1)
            if self.tabuleiro[x][y] != -1:
                self.tabuleiro[x][y] = -1
                minas_posicionadas += 1
                
                # Atualizar vizinhos
                for i in range(max(0, x-1), min(self.linhas, x+2)):
                    for j in range(max(0, y-1), min(self.colunas, y+2)):
                        if self.tabuleiro[i][j] != -1:
                            self.tabuleiro[i][j] += 1
        
        # Criar botões
        self.botoes = []
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                btn = tk.Button(
                    frame,
                    text="",
                    width=3,
                    height=1,
                    bg=self.cores["botao"],
                    activebackground=self.cores["botao_hover"],
                    fg=self.cores["texto"],
                    font=self.fonte_normal,
                    relief=tk.RAISED,
                    command=lambda x=i, y=j: self.clicar(x, y)
                )
                btn.bind("<Button-3>", lambda event, x=i, y=j: self.marcar(x, y))
                btn.grid(row=i, column=j, padx=2, pady=2)
                linha.append(btn)
            self.botoes.append(linha)
    
    def clicar(self, x, y):
        if not self.jogo_ativo or self.botoes[x][y]["state"] == "disabled":
            return
            
        if self.tabuleiro[x][y] == -1:
            self.botoes[x][y].config(
                text=self.emoji_tema["mina"],
                bg="#FFCDD2",
                state="disabled"
            )
            self.fim_de_jogo(False)
            return
        
        self.revelar_quadrado(x, y)
        
        if self.verificar_vitoria():
            self.fim_de_jogo(True)
    
    def marcar(self, x, y):
        if not self.jogo_ativo or self.botoes[x][y]["state"] == "disabled":
            return
            
        btn = self.botoes[x][y]
        if btn["text"] == self.emoji_tema["bandeira"]:
            btn.config(text="")
            self.minas_restantes += 1
        else:
            btn.config(text=self.emoji_tema["bandeira"], fg=self.cores["bandeira"])
            self.minas_restantes -= 1
        
        self.label_minas.config(text=f"{self.emoji_tema['bandeira']} Minas: {self.minas_restantes}")
        self.pontuacao += 1
    
    def revelar_quadrado(self, x, y):
        if not (0 <= x < self.linhas) or not (0 <= y < self.colunas):
            return
        if self.botoes[x][y]["state"] == "disabled" or self.botoes[x][y]["text"] == self.emoji_tema["bandeira"]:
            return
            
        valor = self.tabuleiro[x][y]
        btn = self.botoes[x][y]
        
        if valor == 0:
            btn.config(
                text="",
                bg=self.cores["vazio"],
                state="disabled",
                relief=tk.SUNKEN
            )
            for i in range(max(0, x-1), min(self.linhas, x+2)):
                for j in range(max(0, y-1), min(self.colunas, y+2)):
                    if i != x or j != y:
                        self.revelar_quadrado(i, j)
        else:
            btn.config(
                text=str(valor),
                fg=self.cores_numeros()[valor-1],
                bg=self.cores["vazio"],
                state="disabled",
                relief=tk.SUNKEN
            )
        self.pontuacao += 1
    
    def cores_numeros(self):
        return [
            "#2196F3", "#4CAF50", "#F44336", "#9C27B0",
            "#FF9800", "#795548", "#607D8B", "#000000"
        ]
    
    def verificar_vitoria(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                btn = self.botoes[i][j]
                if self.tabuleiro[i][j] != -1 and btn["state"] != "disabled":
                    return False
        return True
    
    def fim_de_jogo(self, vitoria):
        self.jogo_ativo = False
        
        # Salvar resultado
        resultado = {
            "nome": self.jogador_atual,
            "pontuacao": self.pontuacao,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "resultado": "Vitória" if vitoria else "Derrota"
        }
        self.salvar_pontuacao(resultado)
        
        if vitoria:
            mensagem = f"PARABÉNS {self.jogador_atual}! {self.emoji_tema['vitoria']}\nPontuação: {self.pontuacao}"
        else:
            mensagem = f"BOOM! {self.emoji_tema['mina']}\nPontuação: {self.pontuacao}"
            self.revelar_todas_minas()
        
        # Mostrar mensagem e voltar ao menu após clicar em OK
        messagebox.showinfo("Fim de Jogo", mensagem)
        self.mostrar_menu()  # Adicionado esta linha para voltar ao menu automaticamente
    
    def revelar_todas_minas(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro[i][j] == -1:
                    self.botoes[i][j].config(
                        text=self.emoji_tema["mina"],
                        bg="#FFCDD2",
                        state="disabled"
                    )
    
    def salvar_pontuacao(self, resultado):
        try:
            with open(self.arquivo_ranking, "r") as f:
                ranking = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            ranking = []
        
        ranking.append(resultado)
        
        # Ordenar por MAIOR pontuação
        ranking = sorted(ranking, key=lambda x: x["pontuacao"], reverse=True)[:20]
        
        with open(self.arquivo_ranking, "w") as f:
            json.dump(ranking, f, indent=2)
    
    def mostrar_ranking(self):
        self.limpar_tela()
        
        tk.Label(
            self.root,
            text="🏆 RANKING TOP 20 🏆",
            bg=self.cores["fundo"],
            fg=self.cores["destaque"],
            font=self.fonte_titulo
        ).pack(pady=10)
        
        # Frame principal com scrollbar
        frame_principal = tk.Frame(self.root, bg=self.cores["fundo"])
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(frame_principal, bg=self.cores["fundo"], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.cores["fundo"])
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cabeçalho
        tk.Label(
            scroll_frame,
            text="POS | NOME          | PONTOS | RESULTADO | DATA",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fonte_ranking
        ).pack(pady=(0, 10))
        
        # Carregar ranking
        try:
            with open(self.arquivo_ranking, "r") as f:
                ranking = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            ranking = []
        
        # Mostrar ranking
        for i, item in enumerate(ranking[:20], 1):
            # Cores especiais para os top 3
            if i == 1:
                bg_color = self.cores["top1"]
                fg_color = "#000000"
            elif i == 2:
                bg_color = self.cores["top2"]
                fg_color = "#000000"
            elif i == 3:
                bg_color = self.cores["top3"]
                fg_color = "#000000"
            else:
                bg_color = self.cores["fundo"]
                fg_color = self.cores["texto"]
            
            tk.Label(
                scroll_frame,
                text=f"{i:2d}º {item['nome'][:12]:12s} {item['pontuacao']:6d} pts {item['resultado']:8s} {item['data'][:10]}",
                bg=bg_color,
                fg=fg_color,
                font=self.fonte_ranking,
                anchor="w",
                padx=10,
                pady=2
            ).pack(fill=tk.X, padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão de voltar
        tk.Button(
            self.root,
            text="⬅️ VOLTAR AO MENU",
            bg=self.cores["botao"],
            fg=self.cores["texto"],
            font=self.fonte_normal,
            command=self.mostrar_menu
        ).pack(pady=20)
    
    def mostrar_sobre(self):
        self.limpar_tela()
        
        sobre_texto = """
💣 MINA EXPLOSIVA PREMIUM 💥

A versão mais divertida do clássico jogo de minas!

🎮 COMO JOGAR:
- Clique ESQUERDO para revelar quadrados
- Clique DIREITO para colocar bandeiras
- Encontre todas as minas sem explodir!

📊 SISTEMA DE PONTUAÇÃO:
- Cada clique conta como 1 ponto
- Quanto MAIOR sua pontuação, MELHOR!
- Tente alcançar o topo do ranking

✏️ DESENVOLVIDO POR:

TONY LIMA - O MESTRE DOS EMOJIS!
"Transformando linhas de código em diversão"
Contato: +5586981192287

"""
        tk.Label(
            self.root,
            text=sobre_texto,
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fonte_pequena,
            justify="left"
        ).pack(pady=20, padx=20)
        
        tk.Button(
            self.root,
            text="⬅️ VOLTAR AO MENU",
            bg=self.cores["botao"],
            fg=self.cores["texto"],
            font=self.fonte_normal,
            command=self.mostrar_menu
        ).pack(pady=10)
    
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoMinaFinal(root)
    root.mainloop()