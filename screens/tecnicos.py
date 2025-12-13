import customtkinter as CTK
from CTkMessagebox import *
from utils.ctktable import CTkTable
from tkinter import ttk
import server
import time
from utils.recolor_png import recolor_png
from utils.add_tecnicos import add_tecnicos
from utils.edit_tecnicos import edit_tecnico
from utils.desc_tecnicos import desc_tecnicos
from PIL import Image

class tecnicos_screen(CTK.CTkFrame):
    def __init__(self, master, change_screen=None, user=None, **kwargs):
        super().__init__(master, **kwargs)
        self.last_click_time = 0
        self.last_clicked_row = None
        self.double_click_delay = 0.35
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
        self.criar_tabela()
        self.load_table()

    def criar_tabela(self):
        # Filtros
        self.filter_frame = CTK.CTkFrame(self.content, fg_color="transparent")
        self.filter_frame.pack(fill="x", pady=10, padx=20)

        self.search_entry = CTK.CTkEntry(
            self.filter_frame,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            placeholder_text_color=("#9CA3AF", "#6F6F6F"),
            height=40,
            width=200,
            placeholder_text="Pesquisar...",
            font=("Arial", 14),
            corner_radius=20
        )
        self.search_entry.pack(side="left", fill="x", padx=5, pady=8)

        self.turno_var = CTK.StringVar(value="Filtrar por turno")
        self.turno_filter = CTK.CTkOptionMenu(
            master=self.filter_frame,
            variable=self.turno_var,
            values=["Todos", "Manhã", "Tarde", "Noite", "Madrugada"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            button_hover_color=("#E5E7EB", "#3A3A3A"),
            text_color=("#1F1F1F", "#FFFFFF"),
            dropdown_fg_color=("#F4F6F9", "#2C2C2C"),
            dropdown_text_color=("#1F1F1F", "#FFFFFF"),
            dropdown_hover_color=("#E5E7EB", "#3A3A3A"),
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.turno_filter.pack(side="left", fill="x", padx=5, pady=8)


        self.role_var = CTK.StringVar(value="Filtrar por cargo")
        self.role_filter = CTK.CTkOptionMenu(
            master=self.filter_frame,
            variable=self.role_var,
            values=["Todos", "Admin", "User"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            button_hover_color=("#E5E7EB", "#3A3A3A"),
            text_color=("#1F1F1F", "#FFFFFF"),
            dropdown_fg_color=("#F4F6F9", "#2C2C2C"),
            dropdown_text_color=("#1F1F1F", "#FFFFFF"),
            dropdown_hover_color=("#E5E7EB", "#3A3A3A"),
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.role_filter.pack(side="left", fill="x", padx=5, pady=8)

        self.search_entry.bind("<KeyRelease>", lambda e: self.load_table())
        self.turno_filter.configure(command=lambda _: self.load_table())
        self.role_filter.configure(command=lambda _: self.load_table())

        self.table_container = CTK.CTkFrame(self.content, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, padx=20)

        self.bottom_frame = CTK.CTkFrame(self.content, fg_color="transparent")
        self.bottom_frame.pack(fill="x", pady=10, padx=20)

        img_editar = CTK.CTkImage(
            light_image=recolor_png("assets/edit.png", (255, 255, 255)),
            dark_image=recolor_png("assets/edit.png", (255, 255, 255)),
            size=(18, 18)
        )

        self.btn_editar = CTK.CTkButton(
            self.bottom_frame,
            text="Editar Técnico",
            image=img_editar,
            compound="left",
            fg_color="#1a4dbf",
            hover_color="#1742a0",
            height=30,
            width=150,
            font=("Arial", 14, "bold"),
            corner_radius=20,
            command=self.editar_tecnico
        )
        self.btn_editar.pack(side="right", padx=5)

        if self.user.role == "admin":
            img_add = CTK.CTkImage(
                light_image=recolor_png("assets/add.png", (255, 255, 255)),
                dark_image=recolor_png("assets/add.png", (255, 255, 255)),
                size=(18, 18)
            )

            self.btn_add_tecnico = CTK.CTkButton(
                self.bottom_frame,
                text="Adicionar Técnico",
                image=img_add,
                compound="left",
                fg_color="#2064f2",
                hover_color="#1a4dbf",
                height=30,
                width=160,
                font=("Arial", 14, "bold"),
                corner_radius=20,
                command=self.adicionar_tecnico
            )
            self.btn_add_tecnico.pack(side="left")

    def load_table(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        map_turno = {
            "Manhã": "manha",
            "Tarde": "tarde",
            "Noite": "noite",
            "Madrugada": "madrugada"
        }

        map_role = {
            "Admin": "admin",
            "User": "user",
        }

        search_text = self.search_entry.get().lower().strip()
        role_filtro = self.role_var.get()
        turno_filtro = self.turno_var.get()

        data = [["ID", "Nome", "Turno", "Cargo"]]

        with server._Sessao() as s:
            query = s.query(server.TecnicoTI).order_by(server.TecnicoTI.id)

            tecnicos = query.all()

            for c in tecnicos:
                searchable = f"{c.id} {c.nome}".lower()

                if search_text and search_text not in searchable:
                    continue
                if role_filtro not in ["Todos", "Filtrar por cargo"]:
                    role_db = map_role.get(role_filtro)
                    if c.role != role_db:
                        continue
                if turno_filtro not in ["Todos", "Filtrar por turno"]:
                    turno_db = map_turno.get(turno_filtro)
                    if c.turno != turno_db:
                        continue

                data.append([
                    c.id,
                    c.nome,
                    c.turno.capitalize(),
                    c.role.capitalize()
                ])

        tema = CTK.get_appearance_mode()
        colors_light = ["#B3B3B3", "#CFCFCF"]
        colors_dark = ["#2b2b2b", "#333333"]

        self.table = CTkTable(
            master=self.table_container,
            values=data,
            header_color=("#B3B3B3", "#2b2b2b"),
            colors=colors_dark if tema == "Dark" else colors_light,
            corner_radius=8,
            height=36,
            max_height=420,
            scroll_y=True,
            font=("Arial", 12),
            command=self.click_tabela
        )
        self.table.pack(fill="both", expand=True)

        self.estilizar_header()
        self.selected_row = None

    def click_tabela(self, cell):
        row = cell["row"]
        if row == 0: #Ignora o header
            return

        current_time = time.time()
        if self.selected_row:
            self.table.deselect_row(self.selected_row)

        self.table.select_row(row)
        self.selected_row = row

        if (self.last_clicked_row == row and current_time - self.last_click_time <= self.double_click_delay):
            self.detalhes_tecnico()
            self.last_click_time = 0
            self.last_clicked_row = None
            return

        self.last_click_time = current_time
        self.last_clicked_row = row

    def detalhes_tecnico(self):
        if not self.selected_row:
            return

        tecnico_id = self.table.get(self.selected_row, 0)

        with server._Sessao() as s:
            tecnico = s.query(server.TecnicoTI).filter_by(id=tecnico_id).first()

            if not tecnico:
                CTkMessagebox(
                    title="Erro",
                    message="Técnico não encontrado.",
                    icon="cancel"
                )
                return

        desc_tecnicos(
            master=self,
            user=self.user,
            tecnico=tecnico
        )

    def editar_tecnico(self):
        if not self.selected_row:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um técnico primeiro",
                icon="warning"
            )
            return

        tecnico_id = self.table.get(self.selected_row, 0)

        if tecnico_id == self.user.id:
            CTkMessagebox(
                title="Aviso",
                message="Você não pode editar seu próprio cargo.",
                icon="warning"
            )
            return

        edit_tecnico(
            master=self,
            tecnico_id=tecnico_id,
            user=self.user,
            refresh_callback=self.load_table
        )

    def estilizar_header(self, estilizar=True):
        if estilizar:
            for col in range(len(self.table.get_row(0))):
                self.table.insert(
                    0, col,
                    self.table.get(0, col),
                    font=("Arial", 13, "bold"),
                    text_color="#ffffff"
                )
        else:
            for col in range(len(self.table.get_row(0))):
                self.table.insert(
                    0, col,
                    self.table.get(0, col),
                    text_color="#ffffff"
                )

    def adicionar_tecnico(self):
        add_tecnicos(
            master=self,
            user=self.user,
            refresh_callback=self.load_table
        )

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
