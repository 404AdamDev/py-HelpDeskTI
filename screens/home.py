import customtkinter as CTK
from utils.recolor_png import recolor_png
from PIL import Image
import server

class home_screen(CTK.CTkFrame):
    def __init__(self, master, change_screen=None, user=None, **kwargs):
        super().__init__(master, **kwargs)
        self.change_screen = change_screen
        self.user = user

        # Navbar (barra superior)
        self.navbar = CTK.CTkFrame(
            self,
            height=60,
            fg_color=("#2064f2"),
            corner_radius=0
        )
        self.navbar.pack(fill="x", side="top")

        img_menu = CTK.CTkImage(
            light_image=recolor_png("assets/menu.png", (255, 255, 255)),
            dark_image=recolor_png("assets/menu.png", (255, 255, 255)),
            size=(24, 24)
        )

        # Botão que abre/fecha a sidebar
        self.menu_button = CTK.CTkButton(
            self.navbar,
            text="",
            image=img_menu,
            width=40,
            height=40,
            fg_color="transparent",
            hover_color=("#407dff"),
            command=self.toggle_sidebar
        )
        self.menu_button.pack(side="left", padx=10)

        # Título da página
        self.title_label = CTK.CTkLabel(
            self.navbar,
            text="Home",
            font=("Arial", 18, "bold"),
            text_color="#eceeff"
        )
        self.title_label.pack(side="left")

        # Bem-vindo usuário
        img_bemvindo = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (255, 255, 255)),
            dark_image=recolor_png("assets/user.png", (255, 255, 255)),
            size=(24, 24)
        )

        self.bem_vindo = CTK.CTkLabel(
            self.navbar,
            text=f"Bem-vindo, {self.user.nome}  ",
            font=("Arial", 16, "bold"),
            image=img_bemvindo,
            compound="right",
            text_color="#eceeff"
        )
        self.bem_vindo.pack(side="right", padx=10)

        # Sidebar (menu lateral)
        self.sidebar_width = 230
        self.sidebar_open = True

        self.sidebar = CTK.CTkFrame(
            self,
            width=self.sidebar_width,
            fg_color=("#1848af"),
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        # Botões da sidebar
        img_home = CTK.CTkImage(
            light_image=recolor_png("assets/house.png", (255, 255, 255)),
            dark_image=recolor_png("assets/house.png", (255, 255, 255)),
            size=(24, 24)
        )

        self.btn_home = CTK.CTkButton(
            self.sidebar,
            text="Home",
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            hover_color=("#2064f2"),
            image=img_home,
            compound="left",
            command=lambda: self.change_screen("home", user=self.user)
        )
        self.btn_home.pack(fill="x", padx=10, pady=5)

        img_chamados = CTK.CTkImage(
            light_image=recolor_png("assets/headset.png", (255, 255, 255)),
            dark_image=recolor_png("assets/headset.png", (255, 255, 255)),
            size=(24, 24)
        )

        self.btn_chamados = CTK.CTkButton(
            self.sidebar,
            text="Chamados",
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            hover_color=("#2064f2"),
            image=img_chamados,
            compound="left",
            command=lambda: self.change_screen("chamados", user=self.user)
        )
        self.btn_chamados.pack(fill="x", padx=10, pady=5)

        img_tecnicos = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (255, 255, 255)),
            dark_image=recolor_png("assets/user.png", (255, 255, 255)),
            size=(24, 24)
        )

        self.btn_tecnicos = CTK.CTkButton(
            self.sidebar,
            text="Técnicos",
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            hover_color=("#2064f2"),
            image=img_tecnicos,
            compound="left",
            command=lambda: self.change_screen("tecnicos", user=self.user)
        )
        self.btn_tecnicos.pack(fill="x", padx=10, pady=5)

        if self.user.role != "admin":
            self.btn_tecnicos.pack_forget()

        img_logout = CTK.CTkImage(
            light_image=recolor_png("assets/log-out.png", (255, 255, 255)),
            dark_image=recolor_png("assets/log-out.png", (255, 255, 255)),
            size=(24, 24)
        )

        self.btn_logout = CTK.CTkButton(
            self.sidebar,
            text="Sair",
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            hover_color=("#f22020"),
            image=img_logout,
            compound="left",
            command=lambda: self.change_screen("login")
        )
        self.btn_logout.pack(fill="x", side="bottom", padx=10, pady=5)

        # Conteúdo da aba
        self.content = CTK.CTkFrame(
            self,
            fg_color=("#dbdbdb", "#252525")
        )
        self.content.pack(side="left", fill="both", expand=True)
        self.carregar_dashboard()

    # Abrir e fechar a sidebar
    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar.pack_forget()
            self.sidebar_open = False
        else:
            self.content.pack_forget()
            self.sidebar.pack(side="left", fill="y")
            self.content.pack(side="left", fill="both", expand=True)
            self.sidebar_open = True

    # Carregar os dados do dashboard
    def carregar_dashboard(self):
        with server._Sessao() as sessao:
            total = sessao.query(server.ChamadoTI).count()
            abertos = sessao.query(server.ChamadoTI).filter_by(status="aberto").count()
            criticos = sessao.query(server.ChamadoTI).filter_by(prioridade="critica").count()
            resolvidos = sessao.query(server.ChamadoTI).filter_by(status="resolvido").count()
            meus = sessao.query(server.ChamadoTI).filter_by(TecnicoTI_id=self.user.id).count()

        # Criação dos cards
        self.add_card("Chamados Totais", "#2064f2", "assets/headphones.png", (255, 255, 255), total)
        self.add_card("Abertos", "#f22020", "assets/headset.png", (255, 255, 255), abertos)
        self.add_card("Criticos", "#f29e20", "assets/alert.png", (255, 255, 255), criticos)
        self.add_card("Resolvidos", "#27f220", "assets/laptop-solved.png", (255, 255, 255), resolvidos)
        self.add_card("Meus Chamados", "#2064f2", "assets/laptop.png", (255, 255, 255), meus)

    # Função para adicionar um card ao dashboard
    def add_card(self, titulo, line_color, img_url, img_color, valor):
        card = CTK.CTkFrame(self.content, fg_color=("#C9C9C9", "#424242"), corner_radius=8)
        card.pack(pady=(20, 10), padx=20, fill="x")

        line = CTK.CTkFrame(card, fg_color=line_color, height=12, width=5)
        line.pack(fill="y", side="left")

        if img_url:
            img = CTK.CTkImage(
                light_image=recolor_png(img_url, img_color),
                dark_image=recolor_png(img_url, img_color),
                size=(24, 24)
            )
            CTK.CTkLabel(card, text=f"  {titulo}", font=("Arial", 14, "bold"), text_color=("#1F1F1F", "#eceeff"), image=img, compound="left").pack(anchor="w", padx=10, pady=5)
        else:
            CTK.CTkLabel(card, text=titulo, font=("Arial", 14, "bold"), text_color=("#1F1F1F", "#eceeff")).pack(anchor="w", padx=10, pady=5)
        CTK.CTkLabel(card, text=str(valor), font=("Arial", 26, "bold"), text_color=("#1F1F1F", "#eceeff")).pack(anchor="w", padx=10, pady=5)

