import customtkinter as CTK
from CTkMessagebox import CTkMessagebox
import server
from utils.recolor_png import recolor_png

class edit_chamado_status(CTK.CTkToplevel):
    def __init__(self, master, chamado_id, user, refresh_callback=None):
        super().__init__(master)

        self.chamado_id = chamado_id
        self.user = user
        self.refresh_callback = refresh_callback

        self.title("Editar Chamado")
        self.geometry("320x220")
        self.resizable(False, False)
        self.grab_set()  # trava a janela principal

        # Título
        CTK.CTkLabel(
            self,
            text=f"Chamado #{chamado_id}",
            font=("Arial", 26, "bold"),
            text_color="#2064f2"
        ).pack(pady=(15, 5))

        # Dropdown de status
        img_status = CTK.CTkImage(
            light_image=recolor_png("assets/tag.png", (32, 100, 242)),
            dark_image=recolor_png("assets/tag.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Status:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_status,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.status_var = CTK.StringVar(value="Escolha o novo status")
        self.status_dropdown = CTK.CTkOptionMenu(
            master=self,
            variable=self.status_var,
            values=["Aberto", "Em andamento", "Resolvido", "Fechado"],
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
        self.status_dropdown.pack(fill="x", padx=30, pady=8)

        # Botão salvar
        CTK.CTkButton(
            self,
            text="Salvar Chamado",
            fg_color="#2064f2",
            hover_color="#1a4dbf",
            height=40,
            width=200,
            font=("Arial", 16, "bold"),
            corner_radius=20,
            command=self.salvar_chamado
        ).pack(padx=30, pady=(10, 0))

    def salvar_chamado(self):
        map_status = {
            "Aberto": "aberto",
            "Em andamento": "em andamento",
            "Resolvido": "resolvido",
            "Fechado": "fechado"
        }
        novo_status = map_status.get(self.status_dropdown.get())

        with server._Sessao() as s:
            chamado = s.query(server.ChamadoTI).filter_by(id=self.chamado_id).first()
            if not chamado:
                CTkMessagebox(
                    title="Erro",
                    message="Chamado não encontrado",
                    icon="cancel"
                )
                return

            chamado.status = novo_status
            s.commit()

        if self.refresh_callback:
            self.refresh_callback()

        self.destroy()

