
import customtkinter
from view.tl_view import TlView

from viewmodel.tl_viewmodel import TlViewModel
customtkinter.set_default_color_theme("dark-blue")



def main():
    view = TlView(customtkinter.CTk())
    viewmodel = TlViewModel(view=view)
    viewmodel.initialize_view()
    viewmodel.start()


if __name__ == '__main__':
    main()
