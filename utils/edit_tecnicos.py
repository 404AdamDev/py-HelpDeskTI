import customtkinter as CTK
from CTkMessagebox import CTkMessagebox
import server
from utils.recolor_png import recolor_png

class edit_tecnico(CTK.CTkToplevel):
    def __init__(self, master, tecnico_id, user, refresh_callback=None):
        super().__init__(master)

        self.tecnico_id = tecnico_id
        self.user = user
        self.refresh_callback = refresh_callback

        self.title("Editar Tecnico")
        self.geometry("320x220")
        self.resizable(False, False)
        self.grab_set()  # trava a janela principal

        # Título
        CTK.CTkLabel(
            self,
            text=f"Técnico #{tecnico_id}",
            font=("Arial", 26, "bold"),
            text_color="#2064f2"
        ).pack(pady=(15, 5))

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

        self.role_var = CTK.StringVar(value="Escolha o novo cargo")
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

        # Botão salvar
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

    def salvar_tecnico(self):
        map_role = {
            "Admin": "admin",
            "User": "user",
        }
        novo_role = map_role.get(self.role_dropdown.get())

        with server._Sessao() as s:
            tecnico = s.query(server.TecnicoTI).filter_by(id=self.tecnico_id).first()

            if not tecnico:
                CTkMessagebox(
                    title="Erro",
                    message="Técnico não encontrado",
                    icon="cancel"
                )
                return

            tecnico.role = novo_role
            s.commit()

        if self.refresh_callback:
            self.refresh_callback()

        self.destroy()

