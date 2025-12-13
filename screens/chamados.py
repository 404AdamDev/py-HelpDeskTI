import customtkinter as CTK
from CTkMessagebox import *
from utils.ctktable import CTkTable
from tkinter import ttk
import server
import time
from utils.recolor_png import recolor_png
from utils.add_chamados import add_chamados
from utils.edit_chamados import edit_chamado_status
from utils.desc_chamados import desc_chamados
from PIL import Image

class chamados_screen(CTK.CTkFrame):
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

        self.prioridade_var = CTK.StringVar(value="Filtrar por prioridade")
        self.prioridade_filter = CTK.CTkOptionMenu(
            master=self.filter_frame,
            variable=self.prioridade_var,
            values=["Todos", "Baixa", "Média", "Alta", "Crítica"],
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
        self.prioridade_filter.pack(side="left", fill="x", padx=5, pady=8)


        self.status_var = CTK.StringVar(value="Filtrar por status")
        self.status_filter = CTK.CTkOptionMenu(
            master=self.filter_frame,
            variable=self.status_var,
            values=["Todos", "Aberto", "Em andamento", "Resolvido", "Fechado"],
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
        self.status_filter.pack(side="left", fill="x", padx=5, pady=8)

        self.search_entry.bind("<KeyRelease>", lambda e: self.load_table())
        self.prioridade_filter.configure(command=lambda _: self.load_table())
        self.status_filter.configure(command=lambda _: self.load_table())

        self.table_container = CTK.CTkFrame(self.content, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, padx=20)

        self.bottom_frame = CTK.CTkFrame(self.content, fg_color="transparent")
        self.bottom_frame.pack(fill="x", pady=10, padx=20)

        img_responder = CTK.CTkImage(
            light_image=recolor_png("assets/reply.png", (255, 255, 255)),
            dark_image=recolor_png("assets/reply.png", (255, 255, 255)),
            size=(18, 18)
        )

        self.btn_responder = CTK.CTkButton(
            self.bottom_frame,
            text="Responder Chamado",
            image=img_responder,
            compound="left",
            fg_color="#1a4dbf",
            hover_color="#1742a0",
            height=30,
            width=180,
            font=("Arial", 14, "bold"),
            corner_radius=20,
            command=self.responder_chamado
        )
        self.btn_responder.pack(side="right", padx=5)

        img_editar = CTK.CTkImage(
            light_image=recolor_png("assets/edit.png", (255, 255, 255)),
            dark_image=recolor_png("assets/edit.png", (255, 255, 255)),
            size=(18, 18)
        )

        self.btn_editar = CTK.CTkButton(
            self.bottom_frame,
            text="Editar Chamado",
            image=img_editar,
            compound="left",
            fg_color="#1a4dbf",
            hover_color="#1742a0",
            height=30,
            width=150,
            font=("Arial", 14, "bold"),
            corner_radius=20,
            command=self.editar_chamado
        )
        self.btn_editar.pack(side="right", padx=5)

        if self.user.role == "admin":
            img_add = CTK.CTkImage(
                light_image=recolor_png("assets/add.png", (255, 255, 255)),
                dark_image=recolor_png("assets/add.png", (255, 255, 255)),
                size=(18, 18)
            )

            self.btn_add_chamado = CTK.CTkButton(
                self.bottom_frame,
                text="Adicionar Chamado",
                image=img_add,
                compound="left",
                fg_color="#2064f2",
                hover_color="#1a4dbf",
                height=30,
                width=160,
                font=("Arial", 14, "bold"),
                corner_radius=20,
                command=self.adicionar_chamado
            )
            self.btn_add_chamado.pack(side="left")

    def load_table(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        map_prioridades = {
            "Baixa": "baixa",
            "Média": "media",
            "Alta": "alta",
            "Crítica": "critica"
        }

        map_status = {
            "Aberto": "aberto",
            "Em andamento": "em andamento",
            "Resolvido": "resolvido",
            "Fechado": "fechado"
        }

        search_text = self.search_entry.get().lower().strip()
        prioridade_filtro = self.prioridade_var.get()
        status_filtro = self.status_var.get()

        data = [["ID", "Solicitante", "Setor", "Prioridade", "Status", "Técnico"]]

        with server._Sessao() as s:
            query = s.query(server.ChamadoTI).order_by(server.ChamadoTI.id)

            chamados = query.all()

            for c in chamados:
                tecnico = c.TecnicoTI.nome if c.TecnicoTI else "—"
                searchable = f"{c.id} {c.solicitante} {c.setor} {tecnico}".lower()

                if search_text and search_text not in searchable:
                    continue
                if prioridade_filtro not in ["Todos", "Filtrar por prioridade"]:
                    prioridade_db = map_prioridades.get(prioridade_filtro)
                    if c.prioridade != prioridade_db:
                        continue
                if status_filtro not in ["Todos", "Filtrar por status"]:
                    status_db = map_status.get(status_filtro)
                    if c.status != status_db:
                        continue

                data.append([
                    c.id,
                    c.solicitante,
                    c.setor,
                    c.prioridade.capitalize(),
                    c.status.capitalize(),
                    tecnico
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
        self.colorir_status()
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
            self.detalhes_chamado()
            self.last_click_time = 0
            self.last_clicked_row = None
            return

        self.last_click_time = current_time
        self.last_clicked_row = row

    def detalhes_chamado(self):
        if not self.selected_row:
            return

        chamado_id = self.table.get(self.selected_row, 0)

        with server._Sessao() as s:
            chamado = s.query(server.ChamadoTI).filter_by(id=chamado_id).first()

            if not chamado:
                CTkMessagebox(
                    title="Erro",
                    message="Chamado não encontrado.",
                    icon="cancel"
                )
                return

        desc_chamados(
            master=self,
            user=self.user,
            chamado=chamado
        )

    def editar_chamado(self):
        if not self.selected_row:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um chamado primeiro",
                icon="warning"
            )
            return

        chamado_id = self.table.get(self.selected_row, 0)

        with server._Sessao() as s:
            chamado = s.query(server.ChamadoTI).filter_by(id=chamado_id).first()
            if chamado.TecnicoTI_id and chamado.TecnicoTI_id != self.user.id and self.user.role != "admin":
                CTkMessagebox(
                    title="Erro",
                    message=f"O chamado já está atribuido por {chamado.TecnicoTI.nome}",
                    icon="cancel"
                )
                return

        edit_chamado_status(
            master=self,
            chamado_id=chamado_id,
            user=self.user,
            refresh_callback=self.load_table
        )

    def responder_chamado(self):
        if not self.selected_row:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um chamado primeiro",
                icon="warning"
            )
            return

        chamado_id = self.table.get(self.selected_row, 0)

        with server._Sessao() as s:
            chamado = s.query(server.ChamadoTI).filter_by(id=chamado_id).first()

            if not chamado:
                CTkMessagebox(
                    title="Erro",
                    message="Chamado não encontrado.",
                    icon="cancel"
                )
                return
            
            if chamado.status == "fechado":
                CTkMessagebox(
                    title="Erro",
                    message="Não é possível atribuir chamados fechados.",
                    icon="cancel"
                )
                return

            if chamado.TecnicoTI_id is None:
                confirmar = CTkMessagebox(
                    title="Confirmar",
                    message="Deseja assumir este chamado?",
                    icon="question",
                    option_1="Sim",
                    option_2="Cancelar"
                )

                if confirmar.get() == "Sim":
                    server.ChamadoTI.atribuirChamado(
                        id=chamado_id,
                        tecnico=self.user.id
                    )

                    server.ChamadoTI.alterarStatus(
                        id=chamado_id,
                        valor="em andamento" if chamado.status == "aberto" else chamado.status
                    )

                    CTkMessagebox(
                        title="Sucesso",
                        message="Chamado atribuído a você!",
                        icon="check"
                    )

            elif chamado.TecnicoTI_id != self.user.id:
                CTkMessagebox(title="Aviso", message=f"Este chamado já está sendo atendido por {chamado.TecnicoTI.nome}.", icon="warning")
                return

            else:
                confirmar = CTkMessagebox(
                    title="Confirmar",
                    message="Você já é o técnico deste chamado.\nDeseja desassociá-lo?",
                    icon="question",
                    option_1="Sim",
                    option_2="Cancelar"
                )

                if confirmar.get() == "Sim":
                    server.ChamadoTI.desatribuirChamado(chamado_id)
                    CTkMessagebox(title="Sucesso", message="Chamado desassociado com sucesso.", icon="check")

        self.load_table()

    def colorir_status(self):
        for row in range(1, len(self.table.get())):
            status = self.table.get(row, 4).lower()

            if status in ["aberto", "não atendido"]:
                color = "#ff3b3b"
            elif status in ["resolvido", "atendido"]:
                color = "#00c851"
            elif status == "em andamento":
                color = "#ffbb33"
            else:
                color = "#ffffff"

            self.table.insert(
                row, 4,
                status.capitalize(),
                text_color=color
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

    def adicionar_chamado(self):
        add_chamados(
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
