import tkinter as tk
from model.tl_model import TlModel
from utils.http_requests import  remove_bg, enhance_image
from utils import decorators
import threading


class TlViewModel:
    def __init__(self, view):
        self.model = TlModel()
        self.view = view
        self._current_image_to_process = []


    def get_image_process_actions(self):
        return sorted(self._current_image_to_process)

    def add_image_process_action(self, action):
        self._current_image_to_process.append(action)

    def remove_image_process_action(self, action_to_remove_started_with_off):
        if action_to_remove_started_with_off == "__all__":
            self._current_image_to_process = []
            return
        self._current_image_to_process.remove(action_to_remove_started_with_off[3:])

    def on_image_process_actions_changed(self,item : str):
        if item.startswith("OFF"):
            self.remove_image_process_action(item)
        else:
            self.add_image_process_action(item)
        
    def set_view(self, view):
        self.view = view


    def reset_image_tab_ui(self):
        self.remove_image_process_action("__all__")
        self.view.image_tab_reset()
        # self.view.set_transformed_image()

        """


        """




    @decorators.log(message="Image processing.")
    def process_image(self, status_out) -> None:
        map = {
        "BG" : remove_bg,
        "IQ" : enhance_image
        }
        url = self.view.get_current_image_to_process()
        actions_to_perfom = self.get_image_process_actions()
        if(len(actions_to_perfom) <= 0):
            status_out.configure(text="please selected action to perform on the image before, process it.")
            return
        process_image_path = None
        try:
            for action in actions_to_perfom:

                process_image_path  = map.get(action)(url)

            self.view.set_transformed_image(process_image_path)
            status_out.configure(text="Process Done.")
        except ValueError as ev:
            status_out.configure(text=ev)
        except Exception as e:
            status_out.configure(text=e)
        finally:
            pass


        
    def initialize_view(self):
        # view = TlView(tk.Tk())
        # self.set_view(view)
        self.view.set_viewmodel(self)
        #self.view.root.mainloop()
        
    def start(self):
        self.view.root.mainloop()