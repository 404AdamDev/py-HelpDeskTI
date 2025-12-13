import customtkinter as CTK
from typing import Callable
from screens.login import login_screen
from screens.home import home_screen
from screens.chamados import chamados_screen 
from screens.tecnicos import tecnicos_screen
from server import iniciar_servidor

externalScreen = None

class App(CTK.CTk):

    def __init__(self):
        super().__init__()

        self.title("Help Desk TI")
        self.geometry("1100x600")
        self.iconbitmap("assets/app.ico")

        #CTK.set_appearance_mode("light")

        self.current_frame = None

        # Mapeamento das telas
        self.screens = {
            "login": login_screen,
            "home": home_screen,
            "chamados": chamados_screen,
            "tecnicos": tecnicos_screen
        }

        self.change_screen("login")

    def change_screen(self, screen_name: str, user=None):
        if self.current_frame:
            self.current_frame.destroy()

        new_frame_class = self.screens[screen_name]
        self.current_frame = new_frame_class(self, self.change_screen, user)
        self.current_frame.pack(fill="both", expand=True)


def showExternalScreen(title: str, desc: str):
    global externalScreen

    if externalScreen:
        externalScreen.destroy()

    externalScreen = CTK.CTkToplevel()
    externalScreen.title(title)
    externalScreen.geometry("300x200")
    externalScreen.grab_set()

    CTK.CTkLabel(externalScreen, text=desc, font=("Arial", 20)).pack(pady=30)
    CTK.CTkButton(externalScreen, text="Fechar", command=externalScreen.destroy).pack(pady=10)

if __name__ == "__main__":
    print("\033[93mGeralmente vem com um administrador criado, tente logar com o nome 'HDTIAdmin' no turno 'Manhã'\033[0m.")
    iniciar_servidor()
    App().mainloop()