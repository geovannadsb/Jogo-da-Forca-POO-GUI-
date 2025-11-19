import tkinter as tk
from tkinter import ttk, messagebox, font
from Jogo_Forca.logica import JogoForca

try:
    from Jogo_Forca.palavras import PALAVRAS
except:
    PALAVRAS = None

PALETA = {
    'fundo': '#F9F4FB',
    'cartao': '#F3E9F7',
    'lilas': '#C9A3C5',
    'rosa': '#c07299',
    'roxo': '#9A72C1',
    'azul_bebe': '#A9D3E6',
    'azul_profundo': '#000000',
    'texto': '#4A3F55',
    'erro': '#BE6F8D',
    'acerto': '#205E8A'
}


class InterfaceForca:
    def __init__(self, root): #Interface gráfica do jogo da forca
        self.root = root
        root.title("Jogo da Forca")
        root.configure(bg=PALETA['fundo'])
        root.geometry("720x580")
        root.resizable(False, False)

        self.fonte_titulo = font.Font(family="Helvetica", size=28, weight="bold")
        self.fonte_palavra = font.Font(family="Helvetica", size=28, weight="bold")
        self.fonte_normal = font.Font(family="Helvetica", size=12)

        #Modelo
        self.jogo = JogoForca(lista_palavras=PALAVRAS or None, max_erros=6)

        #visual
        self._montar_topo()
        self._montar_cartao()
        self._montar_teclado()

        self.atualizar()


    def _montar_topo(self): #Seção superior da interface (título e botão de novo jogo)
        frame = tk.Frame(self.root, bg=PALETA['lilas'])
        frame.place(x=0, y=0, width=720, height=90)


        faixa = tk.Canvas(frame, width=720, height=90,
                          bg=PALETA['lilas'], highlightthickness=0)
        faixa.pack(fill="both")


        titulo = tk.Label(frame,
                          text="Jogo da Forca",
                          font=self.fonte_titulo,
                          bg=PALETA['lilas'],
                          fg=PALETA['azul_profundo'])
        titulo.place(relx=0.5, rely=0.5, anchor="center")


        botao = tk.Button(frame,
                          text="Novo Jogo",
                          command=self.novo_jogo,
                          bg=PALETA['roxo'],
                          fg="white",
                          bd=0,
                          padx=14,
                          pady=6,
                          font=("Helvetica", 12, "bold"),
                          activebackground=PALETA['rosa'])
        botao.place(x=580, y=28)


    def _montar_cartao(self): #Cartão central da interface
        self.cartao = tk.Frame(self.root, bg=PALETA['cartao'])
        self.cartao.place(x=20, y=110, width=680, height=300)


        self.canvas = tk.Canvas(self.cartao,
                                width=260,
                                height=260,
                                bg=PALETA['cartao'],
                                highlightthickness=0)
        self.canvas.place(x=10, y=10)


        self.lbl_palavra = tk.Label(self.cartao,
                                    text="",
                                    font=self.fonte_palavra,
                                    bg=PALETA['cartao'],
                                    fg=PALETA['texto'])
        self.lbl_palavra.place(x=310, y=20)


        self.lbl_erradas = tk.Label(self.cartao,
                                    text="Letras erradas:",
                                    font=self.fonte_normal,
                                    bg=PALETA['cartao'],
                                    fg=PALETA['erro'])
        self.lbl_erradas.place(x=310, y=100)


        self.lbl_tentativas = tk.Label(self.cartao,
                                       text="Tentativas restantes:",
                                       font=self.fonte_normal,
                                       bg=PALETA['cartao'],
                                       fg=PALETA['texto'])
        self.lbl_tentativas.place(x=310, y=140)


        self.lbl_msg = tk.Label(self.cartao,
                                text="",
                                font=("Helvetica", 12, "italic"),
                                bg=PALETA['cartao'],
                                fg=PALETA['texto'])
        self.lbl_msg.place(x=310, y=180)


    def _montar_teclado(self): #Teclado virtual da interface (botões de A–Z)
        frame = tk.Frame(self.root, bg=PALETA['fundo'])
        frame.place(x=20, y=420, width=680, height=100)

        self.botoes = {}

        linhas = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        y = 0
        for linha in linhas:
            x = 20
            for letra in linha:
                btn = tk.Button(frame, text=letra, width=3,
                                command=lambda c=letra: self.apertar(c),
                                bg=PALETA['azul_bebe'],
                                fg=PALETA['texto'],
                                bd=0,
                                font=("Helvetica", 11, "bold"))
                btn.place(x=x, y=10 + 32*y)
                self.botoes[letra] = btn
                x += 52
            y += 1


    def atualizar(self): # Atualizar todos os elementos da interface com o estado atual do jogo
        self.lbl_palavra.config(text=self.jogo.palavra_formatada())
        self.lbl_erradas.config(text="Letras erradas: " + self.jogo.letras_erradas_formatadas())
        self.lbl_tentativas.config(text=f"Tentativas restantes: {self.jogo.tentativas_restantes()}")


        for letra, btn in self.botoes.items():
            if letra in self.jogo.letras_certas or letra in self.jogo.letras_erradas:
                btn.config(state=tk.DISABLED, bg=PALETA['lilas'])
            else:
                btn.config(state=tk.NORMAL, bg=PALETA['azul_bebe'])

        self._desenhar_forca()

        if self.jogo.finalizado:
            if self.jogo.venceu():
                messagebox.showinfo("Vitória!", f"Você acertou! A palavra era: {self.jogo.revelar_palavra()}")
            else:
                messagebox.showinfo("Derrota", f"A palavra era: {self.jogo.revelar_palavra()}")

            for btn in self.botoes.values():
                btn.config(state=tk.DISABLED)


    def apertar(self, letra):
        resp = self.jogo.tentar_letra(letra)
        self.lbl_msg.config(text=resp['mensagem'])
        self.atualizar()


    def novo_jogo(self):
        self.jogo.reiniciar()
        for btn in self.botoes.values():
            btn.config(state=tk.NORMAL, bg=PALETA['azul_bebe'])
        self.lbl_msg.config(text="")
        self.atualizar()


    def _desenhar_forca(self):
        self.canvas.delete("all")
        cor = PALETA['azul_profundo']
        e = self.jogo.erros

        #estrutura
        self.canvas.create_line(10, 240, 200, 240, width=4, fill=cor)
        self.canvas.create_line(40, 240, 40, 20, width=4, fill=cor)
        self.canvas.create_line(40, 20, 140, 20, width=4, fill=cor)
        self.canvas.create_line(140, 20, 140, 44, width=4, fill=cor)

        #boneco
        if e > 0:
            self.canvas.create_oval(120, 44, 160, 84, width=3, outline=cor)
        if e > 1:
            self.canvas.create_line(140, 84, 140, 150, width=3, fill=cor)
        if e > 2:
            self.canvas.create_line(140, 100, 110, 120, width=3, fill=cor)
        if e > 3:
            self.canvas.create_line(140, 100, 170, 120, width=3, fill=cor)
        if e > 4:
            self.canvas.create_line(140, 150, 120, 190, width=3, fill=cor)
        if e > 5:
            self.canvas.create_line(140, 150, 160, 190, width=3, fill=cor)



if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceForca(root)
    root.mainloop()