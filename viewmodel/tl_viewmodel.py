import tkinter as tk
from model.tl_model import TlModel
from utils.http_requests import  remove_bg
import threading


class TlViewModel:
    def __init__(self, view):
        self.model = TlModel()
        self.view = view
        
    def set_view(self, view):
        self.view = view

    def process_image(self) -> None:
        url = self.view.get_current_image_to_process()
        process_image_path = remove_bg(url)

        self.view.set_transformed_image(process_image_path)

        
    def initialize_view(self):
        # view = TlView(tk.Tk())
        # self.set_view(view)
        self.view.set_viewmodel(self)
        #self.view.root.mainloop()
        
    def start(self):
        self.view.root.mainloop()