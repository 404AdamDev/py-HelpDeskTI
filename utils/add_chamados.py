import customtkinter as CTK
from server import ChamadoTI
from utils.recolor_png import recolor_png
import CTkMessagebox

class add_chamados(CTK.CTkToplevel):
    def __init__(self, master, user, refresh_callback=None):
        super().__init__(master)

        self.user = user
        self.refresh_callback = refresh_callback

        self.title("Adicionar Chamado")
        self.geometry("420x580")
        self.resizable(False, False)
        self.grab_set()
        self.iconbitmap("assets/app.ico")

        # Título
        CTK.CTkLabel(
            self,
            text="Novo Chamado",
            font=("Arial", 26, "bold"),
            text_color="#2064f2"
        ).pack(pady=(15, 5))

        # Input do solicitante
        img_solicitante = CTK.CTkImage(
            light_image=recolor_png("assets/user.png", (32, 100, 242)),
            dark_image=recolor_png("assets/user.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Solicitante:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_solicitante,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.entry_solicitante = CTK.CTkEntry(
            self,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            placeholder_text_color=("#9CA3AF", "#6F6F6F"),
            height=40,
            placeholder_text="Insira o nome do solicitante",
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_solicitante.pack(fill="x", padx=30, pady=8)

        # Input do setor
        img_setor = CTK.CTkImage(
            light_image=recolor_png("assets/setor.png", (32, 100, 242)),
            dark_image=recolor_png("assets/setor.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Setor:",
            text_color=("#1F1F1F", "#eceeff"),
            anchor="w",
            image=img_setor,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.entry_setor = CTK.CTkEntry(
            self,
            fg_color=("#F4F6F9", "#2C2C2C"),
            border_color=("#D0D5DD", "#2E2E2E"),
            text_color=("#1F1F1F", "#FFFFFF"),
            placeholder_text_color=("#9CA3AF", "#6F6F6F"),
            height=40,
            placeholder_text="Insira o setor",
            font=("Arial", 14),
            corner_radius=20
        )
        self.entry_setor.pack(fill="x", padx=30, pady=8)

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
        placeholder = "Descreva o problema aqui"
        self.text_descricao.insert("1.0", placeholder)
        self.text_descricao.configure(text_color=("#9CA3AF", "#6F6F6F"))

        def on_focus_in(event):
            if self.text_descricao.get("1.0", "end-1c") == placeholder:
                self.text_descricao.delete("1.0", "end")
                self.text_descricao.configure(text_color=("#1F1F1F", "#FFFFFF"))

        def on_focus_out(event):
            if not self.text_descricao.get("1.0", "end-1c").strip():
                self.text_descricao.insert("1.0", placeholder)
                self.text_descricao.configure(text_color=("#9CA3AF", "#6F6F6F"))

        self.text_descricao.bind("<FocusIn>", on_focus_in)
        self.text_descricao.bind("<FocusOut>", on_focus_out)

        # Dropdown de prioridade
        img_prioridade = CTK.CTkImage(
            light_image=recolor_png("assets/alert.png", (32, 100, 242)),
            dark_image=recolor_png("assets/alert.png", (32, 100, 242)),
            size=(24, 24)
        )

        CTK.CTkLabel(
            self,
            text="  Prioridade:",
            text_color=("#1F1F1F", "#eceeff"),
            width=300,
            anchor="w",
            image=img_prioridade,
            font=("Arial", 16),
            compound="left"
        ).pack(fill="x", pady=(10, 0), padx=30)

        self.prioridade_var = CTK.StringVar(value="Escolha a prioridade")
        self.prioridade_dropdown = CTK.CTkOptionMenu(
            master=self,
            variable=self.prioridade_var,
            values=["Baixa", "Média", "Alta", "Crítica"],
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
        self.prioridade_dropdown.pack(fill="x", padx=30, pady=8)

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

    # Salvar chamado no banco
    def salvar_chamado(self):
        solicitante = self.entry_solicitante.get().strip()
        setor = self.entry_setor.get().strip()
        descricao = self.text_descricao.get("1.0", "end-1c").strip()

        map_prioridades = {
            "Baixa": "baixa",
            "Média": "media",
            "Alta": "alta",
            "Crítica": "critica"
        }
        prioridade = map_prioridades.get(self.prioridade_dropdown.get())

        if not solicitante or not setor or not descricao or not prioridade:
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message="Preencha todos os campos corretamente!",
                icon="warning"
            )
            return

        try:
            ChamadoTI().adicionarChamado(
                solicitante=solicitante,
                setor=setor,
                descricao_problema=descricao,
                prioridade=prioridade,
                status="aberto"
            )

            CTkMessagebox.CTkMessagebox(
                title="Sucesso",
                message="Chamado criado com sucesso!",
                icon="check"
            )

            if self.refresh_callback:
                self.refresh_callback()

            self.destroy()

        except Exception as e:
            CTkMessagebox.CTkMessagebox(
                title="Erro",
                message=f"Erro ao salvar chamado:\n{e}",
                icon="cancel"
            )