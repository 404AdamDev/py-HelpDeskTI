import customtkinter as CTK
from CTkMessagebox import CTkMessagebox
from utils.recolor_png import recolor_png
import server
from PIL import Image

class login_screen(CTK.CTkFrame):
    def __init__(self, master, change_screen, user=None, **kwargs):
        super().__init__(master, **kwargs)
        self.change_screen = change_screen

        # Frame esquerdo com a Imagem
        self.left_frame = CTK.CTkFrame(self, width=400, fg_color="#2064f2", corner_radius=0)
        self.left_frame.pack(side="left", fill="both")

        self.img = Image.open("assets/login-bg.png")

        self.label_img = CTK.CTkLabel(self.left_frame, text="")
        self.label_img.pack(fill="both", expand=True)

        self.left_frame.bind("<Configure>", self.resize_image)

        # Frame direito com o formulário 
        self.card = CTK.CTkFrame(self, fg_color=("#dbdbdb", "#252525"), corner_radius=0)
        self.card.pack(side="right", fill="both", expand=True)

        self.login_content = CTK.CTkFrame(self.card, fg_color="transparent")
        self.login_content.pack(expand=True)

        # Titulos
        CTK.CTkLabel(
            self.login_content,
            text="Entrar no Help Desk TI!",
            font=("Arial", 32, "bold"),
            text_color="#2064f2"
        ).pack(pady=(0, 5))

        CTK.CTkLabel(
            self.login_content,
            text="Por favor, insira suas credenciais para continuar.",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=(0, 20))

        # Nome do técnico
        img_name = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (32, 100, 242)),
            dark_image=recolor_png("assets/user.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self.login_content,
            text="  Nome:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_name,
            font=("Arial", 16),
            compound="left"
        ).pack(pady=(10, 0))

        self.name_entry = CTK.CTkEntry(
            self.login_content,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            placeholder_text_color=("#9CA3AF", "#6F6F6F"),
            width=300,
            height=40,
            placeholder_text="Insira seu nome",
            font=("Arial", 14),
            corner_radius=20
        )
        self.name_entry.pack(pady=2)

        # Turno do técnico
        img_shift = CTK.CTkImage(
            light_image=recolor_png("assets/clock.png", (32, 100, 242)),
            dark_image=recolor_png("assets/clock.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self.login_content,
            text="  Turno:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_shift,
            font=("Arial", 16),
            compound="left"
        ).pack(pady=(10, 0))

        self.shift_var = CTK.StringVar(value="Escolha seu turno")
        self.shift_dropdown = CTK.CTkOptionMenu(
            master=self.login_content,
            variable=self.shift_var,
            values=["Manhã", "Tarde", "Noite", "Madrugada"],
            fg_color=("#F4F6F9", "#2C2C2C"),
            button_color=("#F4F6F9", "#2C2C2C"),
            button_hover_color=("#E5E7EB", "#3A3A3A"),
            text_color=("#1F1F1F", "#FFFFFF"),
            dropdown_fg_color=("#F4F6F9", "#2C2C2C"),
            dropdown_text_color=("#1F1F1F", "#FFFFFF"),
            dropdown_hover_color=("#E5E7EB", "#3A3A3A"),
            width=300,
            height=40,
            corner_radius=20,
            font=("Arial", 14),
        )
        self.shift_dropdown.pack(pady=2)

        # Botão de entrar
        CTK.CTkButton(
            self.login_content,
            text="Entrar",
            fg_color="#2064f2",
            hover_color="#1a4dbf",
            width=150,
            height=40,
            font=("Arial", 16, "bold"),
            corner_radius=20,
            command=self.login_action
        ).pack(pady=(20, 0))


    # Redimensionar a imagem
    def resize_image(self, event):
        sizeY = event.height
        bg_img = CTK.CTkImage(
            light_image=self.img,
            dark_image=self.img,
            size=(sizeY - 250, sizeY)
        )
        self.label_img.configure(image=bg_img)
        self.label_img.image = bg_img

    # Logar no sistema
    def login_action(self):
        nome = self.name_entry.get().strip()
        turno = self.shift_var.get().strip().lower()

        map_turnos = {
            "Manhã": "manha",
            "Tarde": "tarde",
            "Noite": "noite",
            "Madrugada": "madrugada"
        }

        turno_db = map_turnos.get(self.shift_var.get())

        if not nome or not turno_db:
            CTkMessagebox(title="Erro", message="Preencha todos os campos!", icon="warning")
            return

        usuario = server.TecnicoTI.autenticar(nome, turno_db)

        if usuario:
            print("Login autorizado:", usuario.nome, usuario.role)

            if self.change_screen:
                self.change_screen("home", user=usuario)
        else:
            CTkMessagebox(title="Login Inválido", message="Usuário ou turno incorretos!", icon="cancel")
