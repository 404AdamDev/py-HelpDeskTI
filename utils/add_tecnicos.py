import customtkinter as CTK
from server import TecnicoTI, _Sessao
from utils.recolor_png import recolor_png
import CTkMessagebox

class add_tecnicos(CTK.CTkToplevel):
    def __init__(self, master, user, refresh_callback=None):
        super().__init__(master)

        self.user = user
        self.refresh_callback = refresh_callback

        self.title("Adicionar Técnico")
        self.geometry("420x420")
        self.resizable(False, False)
        self.grab_set()
        self.iconbitmap("assets/app.ico")

        # Título
        CTK.CTkLabel(
            self,
            text="Novo Técnico",
            font=("Arial", 26, "bold"),
            text_color="#2064f2"
        ).pack(pady=(15, 5))

        # Input do nome
        img_nome = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (32, 100, 242)),
            dark_image=recolor_png("assets/user.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Nome:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_nome,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.entry_nome = CTK.CTkEntry(
            self,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            placeholder_text_color=("#9CA3AF", "#6F6F6F"),
            height=40,
            placeholder_text="Insira o nome do técnico",
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_nome.pack(fill="x", padx=30, pady=8)

        # Dropdown de turno
        img_turno = CTK.CTkImage(
            light_image=recolor_png("assets/clock.png", (32, 100, 242)),
            dark_image=recolor_png("assets/clock.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Turno:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_turno,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.turno_var = CTK.StringVar(value="Escolha o turno")
        self.turno_dropdown = CTK.CTkOptionMenu(
            master=self,
            variable=self.turno_var,
            values=["Manhã", "Tarde", "Noite", "Madrugada"],
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
        self.turno_dropdown.pack(fill="x", padx=30, pady=8)

        # Dropdown do role
        img_role = CTK.CTkImage(
            light_image=recolor_png("assets/cargo.png", (32, 100, 242)),
            dark_image=recolor_png("assets/cargo.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Cargo:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_role,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.role_var = CTK.StringVar(value="Escolha o cargo")
        self.role_dropdown = CTK.CTkOptionMenu(
            master=self,
            variable=self.role_var,
            values=["Admin", "User"],
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
        self.role_dropdown.pack(fill="x", padx=30, pady=8)

        CTK.CTkButton(
            self,
            text="Salvar Técnico",
            fg_color="#2064f2",
            hover_color="#1a4dbf",
            height=40,
            width=200,
            font=("Arial", 16, "bold"),
            corner_radius=20,
            command=self.salvar_tecnico
        ).pack(padx=30, pady=(10, 0))

    # Salvar tecnico no banco
    def salvar_tecnico(self):
        nome = self.entry_nome.get().strip()

        map_turnos = {
            "Manhã": "manha",
            "Tarde": "tarde",
            "Noite": "noite",
            "Madrugada": "madrugada"
        }
        turno = map_turnos.get(self.turno_dropdown.get())

        map_role = {
            "Admin": "admin",
            "User": "user",
        }
        role = map_role.get(self.role_dropdown.get())

        if not nome:
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message="Preencha todos os campos corretamente!",
                icon="warning"
            )
            return
        
        tecnico = TecnicoTI.autenticar(nome, turno)
        if tecnico:
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message=f"Já existe um técnico com esse nome.",
                icon="cancel"
            )
            return

        try:
            TecnicoTI().criarTecnico(
                nome=nome,
                turno=turno,
                role=role,
            )

            CTkMessagebox.CTkMessagebox(
                title="Sucesso",
                message="Técnico criado com sucesso!",
                icon="check"
            )

            if self.refresh_callback:
                self.refresh_callback()

            self.destroy()

        except Exception as e:
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message=f"Erro ao salvar técnico:\n{e}",
                icon="cancel"
            )