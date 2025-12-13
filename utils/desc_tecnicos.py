import customtkinter as CTK
from server import TecnicoTI
from utils.recolor_png import recolor_png
import CTkMessagebox

class desc_tecnicos(CTK.CTkToplevel):
    def __init__(self, master, user, tecnico=None, refresh_callback=None):
        super().__init__(master)

        self.user = user
        self.tecnico = tecnico
        self.refresh_callback = refresh_callback

        self.title("Adicionar Técnico")
        self.geometry("520x240")
        self.resizable(False, False)
        self.grab_set()
        self.iconbitmap("assets/app.ico")

        # Título
        CTK.CTkLabel(
            self,
            text="Detalhes do técnico",
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

        # Input do nome
        img_nome = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (32, 100, 242)),
            dark_image=recolor_png("assets/user.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_id,
            text="  Nome:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_nome,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=1, sticky="w", pady=(0, 4), padx=(12, 0))


        self.entry_nome = CTK.CTkEntry(
            linha_id,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            height=40,
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_nome.grid(row=1, column=1, sticky="ew", padx=(12, 0)) 

        # Dropdown de turno
        linha_turno = self.criar_linha()
        img_turno = CTK.CTkImage(
            light_image=recolor_png("assets/clock.png", (32, 100, 242)),
            dark_image=recolor_png("assets/clock.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_turno,
            text="  Turno:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_turno,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.turno_var = CTK.StringVar(value="")
        self.turno_dropdown = CTK.CTkOptionMenu(
            master=linha_turno,
            variable=self.turno_var,
            values=["Manhã", "Tarde", "Noite", "Madrugada"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            text_color=("#1F1F1F", "#FFFFFF"),
            text_color_disabled=("#1F1F1F", "#FFFFFF"),
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.turno_dropdown.grid(row=1, column=0, sticky="ew")

        # Dropdown de role
        img_role = CTK.CTkImage(
            light_image=recolor_png("assets/cargo.png", (32, 100, 242)),
            dark_image=recolor_png("assets/cargo.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            linha_turno,
            text="  Cargo:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_role,
            font=("Arial", 16),
            compound="left"
        ).grid(row=0, column=1, sticky="ew", padx=(12, 0)) 

        self.role_var = CTK.StringVar(value="")
        self.role_dropdown = CTK.CTkOptionMenu(
            master=linha_turno,
            variable=self.role_var,
            values=["Aberto", "Em andamento", "Resolvido", "Fechado"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            text_color=("#1F1F1F", "#FFFFFF"),
            text_color_disabled=("#1F1F1F", "#FFFFFF"),
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.role_dropdown.grid(row=1, column=1, sticky="ew", padx=(12, 0))
        self.preencher_dados()

    # Criar linha no grid
    def criar_linha(self):
        frame = CTK.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=30, pady=6)
        frame.grid_columnconfigure((0, 1), weight=1)
        return frame

    # Mostrar dados do técnico
    def preencher_dados(self):
        self.entry_id.insert(0, self.tecnico.id)
        self.entry_nome.insert(0, self.tecnico.nome)
        
        turno_reverse = {
            "manha": "Manhã",
            "tarde": "Tarde",
            "noite": "Noite",
            "madrugada": "Madrugada"
        }
        self.turno_var.set(turno_reverse[self.tecnico.turno])

        role_reverse = {
            "admin": "Admin",
            "user": "User",
        }
        self.role_var.set(role_reverse[self.tecnico.role])

        self.entry_id.configure(state="disabled")
        self.entry_nome.configure(state="disabled")
        self.turno_dropdown.configure(state="disabled")
        self.role_dropdown.configure(state="disabled")

