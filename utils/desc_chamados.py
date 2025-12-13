import customtkinter as CTK
from server import ChamadoTI
from utils.recolor_png import recolor_png
import CTkMessagebox

class desc_chamados(CTK.CTkToplevel):
    def __init__(self, master, user, chamado=None, refresh_callback=None):
        super().__init__(master)

        self.user = user
        self.chamado = chamado
        self.refresh_callback = refresh_callback

        self.title("Adicionar Chamado")
        self.geometry("520x560")
        self.resizable(False, False)
        self.grab_set()
        self.iconbitmap("assets/app.ico")

        # Título
        CTK.CTkLabel(
            self,
            text="Detalhes do chamado",
            font=("Arial", 26, "bold"),
            text_color="#2064f2"
        ).pack(pady=(15, 5))

        # Input do ID
        linha_id = self.criar_linha()
        linha_id.grid_columnconfigure(0, weight=0)
        linha_id.grid_columnconfigure(1, weight=1)

        img_id = CTK.CTkImage(
            light_image=recolor_png("assets/hash.png", (32, 100, 242)),
            dark_image=recolor_png("assets/hash.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_id,
            text="  ID:",
            text_color=("#1F1F1F", "#eceeff"),
            image=img_id,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))


        self.entry_id = CTK.CTkEntry(
            linha_id,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=40,
            width=80,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_id.grid(row=1, column=0, sticky="ew")

        # Input do solicitante
        img_solicitante = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (32, 100, 242)),
            dark_image=recolor_png("assets/user.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_id,
            text="  Solicitante:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_solicitante,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=1, sticky="w", pady=(0, 4), padx=(12, 0))


        self.entry_solicitante = CTK.CTkEntry(
            linha_id,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=40,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_solicitante.grid(row=1, column=1, sticky="ew", padx=(12, 0)) 

        # Input do setor
        linha_setor = self.criar_linha()
        img_setor = CTK.CTkImage(
            light_image=recolor_png("assets/setor.png", (32, 100, 242)),
            dark_image=recolor_png("assets/setor.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_setor,
            text="  Setor:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_setor,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.entry_setor = CTK.CTkEntry(
            linha_setor,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=40,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_setor.grid(row=1, column=0, sticky="ew")

        # Input do tecnico
        img_tecnico = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (32, 100, 242)),
            dark_image=recolor_png("assets/user.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_setor,
            text="  Técnico:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_tecnico,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=1, sticky="w", pady=(0, 4), padx=(12, 0))

        self.entry_tecnico = CTK.CTkEntry(
            linha_setor,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=40,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_tecnico.grid(row=1, column=1, sticky="ew", padx=(12, 0)) 

        # Dropdown de prioridade
        linha_prioridade = self.criar_linha()
        img_prioridade = CTK.CTkImage(
            light_image=recolor_png("assets/alert.png", (32, 100, 242)),
            dark_image=recolor_png("assets/alert.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_prioridade,
            text="  Prioridade:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_prioridade,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.prioridade_var = CTK.StringVar(value="")
        self.prioridade_dropdown = CTK.CTkOptionMenu(
            master=linha_prioridade,
            variable=self.prioridade_var,
            values=["Baixa", "Média", "Alta", "Crítica"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            text_color=("#1F1F1F", "#FFFFFF"),
            text_color_disabled=("#1F1F1F", "#FFFFFF"),
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.prioridade_dropdown.grid(row=1, column=0, sticky="ew")

        # Dropdown de status
        img_status = CTK.CTkImage(
            light_image=recolor_png("assets/tag.png", (32, 100, 242)),
            dark_image=recolor_png("assets/tag.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_prioridade,
            text="  Status:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_status,
            font=("Arial", 16),
            compound="left"
        ).grid(row=1, column=1, sticky="ew", padx=(12, 0)) 

        self.status_var = CTK.StringVar(value="")
        self.status_dropdown = CTK.CTkOptionMenu(
            master=linha_prioridade,
            variable=self.status_var,
            values=["Aberto", "Em andamento", "Resolvido", "Fechado"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            text_color=("#1F1F1F", "#FFFFFF"),
            text_color_disabled=("#1F1F1F", "#FFFFFF"),
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.status_dropdown.grid(row=1, column=1, sticky="ew", padx=(12, 0)) 

        # Input da abertura
        img_abertura = CTK.CTkImage(
            light_image=recolor_png("assets/calendar.png", (32, 100, 242)),
            dark_image=recolor_png("assets/calendar.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Data de abertura:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_abertura,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.entry_abertura = CTK.CTkEntry(
            self,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=40,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_abertura.pack(fill="x", padx=30, pady=8)

        # Input de descrição
        img_desc = CTK.CTkImage(
            light_image=recolor_png("assets/file-text.png", (32, 100, 242)),
            dark_image=recolor_png("assets/file-text.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Descrição:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_desc,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.text_descricao = CTK.CTkTextbox(
            self, 
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=100,
            font=("Arial", 14),
            corner_radius=20
        )
        self.text_descricao.pack(fill="x", padx=30, pady=8)
        self.preencher_dados()

    # Criar linha no grid
    def criar_linha(self):
        frame = CTK.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=30, pady=6)
        frame.grid_columnconfigure((0, 1), weight=1)
        return frame

    # Mostrar dados do chamado
    def preencher_dados(self):
        self.entry_id.insert(0, self.chamado.id)
        self.entry_solicitante.insert(0, self.chamado.solicitante)
        self.entry_setor.insert(0, self.chamado.setor)
        self.entry_abertura.insert(0, self.chamado.data_abertura.strftime('%d/%m/%Y %H:%M'))
        self.entry_tecnico.insert(0, self.chamado.TecnicoTI.nome if self.chamado.TecnicoTI else "Não atribuído")
        self.text_descricao.delete("1.0", "end")
        self.text_descricao.insert("1.0", self.chamado.descricao_problema)
        
        prioridade_reverse = {
            "baixa": "Baixa",
            "media": "Média",
            "alta": "Alta",
            "critica": "Crítica"
        }
        self.prioridade_var.set(prioridade_reverse[self.chamado.prioridade])

        status_reverse = {
            "aberto": "Aberto",
            "em andamento": "Em andamento",
            "resolvido": "Resolvido",
            "fechado": "Fechado"
        }
        self.status_var.set(status_reverse[self.chamado.status])

        self.entry_id.configure(state="disabled")
        self.entry_solicitante.configure(state="disabled")
        self.entry_setor.configure(state="disabled")
        self.entry_abertura.configure(state="disabled")
        self.entry_tecnico.configure(state="disabled")
        self.text_descricao.configure(state="disabled")
        self.prioridade_dropdown.configure(state="disabled")
        self.status_dropdown.configure(state="disabled")

