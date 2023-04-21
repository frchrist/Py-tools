from viewmodel import tl_viewmodel
import customtkinter as CTK
from tkinter import filedialog as fd
import tkinter
import threading
from PIL import Image
from utils import decorators
import json

IMAGE_TAB = "Image process"
PDF_MERGE = "Pdf merge"
PDF_SPLIT  = "Pdf Split"
APP_VERSION = "1.0.0"
APP_TITLE = "Py tools {}".format(APP_VERSION)
APPLICATION_STATE_FILE = "./app_state.json"

IMAGE_PROCESS_ACTIONS = {
    "BG" : "Remove Image background",
    "IQ" : "Increase Image Quality"
}



my_image = CTK.CTkImage(light_image=Image.open("./view/assets/image.png"),
                                  dark_image=Image.open("./view/assets/image.png"),
                                  size=(200, 200))
arrow_image = CTK.CTkImage(light_image=Image.open("./view/assets/right.png"),
                                  dark_image=Image.open("./view/assets/right.png"),
                                  size=(50, 50))

def create_ctk_image_instance(filepath, size=(200, 200)):
    return CTK.CTkImage(light_image=Image.open(filepath),
                                  dark_image=Image.open(filepath),
                                  size=size)

def openfiledialog():
    filetypes = [('Image Files', '*.png *.jpg *.jpeg *.bmp *.gif')]
    name = fd.askopenfilename(title="Choose Image to transform", filetypes=filetypes)



    # if name != None:
    #     instance = create_ctk_image_instance(name)
    #     label.configure(image=instance)

    return name if isinstance(name, str) and name.strip() else None




class TlView:
    def __init__(self, root : CTK.CTk ):
        self.root :  CTK.CTk = root
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.geometry(self.read_application_state(key="geometry") or "550x400")
        # Set up the root window
        self.root.title(APP_TITLE)
        
        self._current_image_to_process = None
        # Set up the view model
        self.viewmodel : tl_viewmodel.TlViewModel = tl_viewmodel.TlViewModel(self)
        
        # Set up the main frame
        self.main_frame = CTK.CTkFrame(self.root, fg_color="#E5E5E5")
        self.main_tab = CTK.CTkTabview(self.main_frame, fg_color="#F3FFF5")
        self.main_tab.add(IMAGE_TAB)
        self.main_tab.add(PDF_SPLIT)
        self.main_tab.add(PDF_MERGE)
        self.main_tab.pack(expand=True, fill=CTK.BOTH, padx=5, pady=3)
        self.main_frame.pack(fill=CTK.BOTH, expand=True)
        self.image_processing_tab_widgets()

        self.status_bar_widget(self.root)
        self.reset_status_bar(2000)


    def status_bar_widget(self, parent):
        image_tab = self.main_tab.tab(IMAGE_TAB)
        frame = CTK.CTkFrame(parent, fg_color="#F3FFF5", corner_radius=0)

        self.status_label = CTK.CTkLabel(frame, text="stable", )
        self.status_label.pack(side='left')


        frame.pack(fill="both", padx=3)

 

    def reset_status_bar(self, mil=5000):
        self.root.after(mil, self.reset_bar)
    def reset_bar(self):
        self.status_label.configure(text="")
        self.root.after(5000, self.reset_bar)

    def get_current_image_to_process(self):
        return self._current_image_to_process

    def image_processing_tab_widgets(self):
        image_tab = self.main_tab.tab(IMAGE_TAB)
        frame = CTK.CTkFrame(image_tab, border_color="#F3FFF5", border_width=2)

        button = CTK.CTkButton(frame, text="Your Image" , command=self.set_loaded_image)
        button.pack(ipady=10, pady=10, padx=8, expand=False) 


        # What want you to do with you image
        w_frame =CTK.CTkFrame(frame,border_width=1)
        CTK.CTkLabel(w_frame, text="How to process your image ?").pack()


        action_vars = {}
        for key,action in IMAGE_PROCESS_ACTIONS.items():
            action_vars[key] = CTK.StringVar()


        # print(action_vars)
        for key,action in IMAGE_PROCESS_ACTIONS.items():
            # key_var = CTK.StringVar()
            CTK.CTkCheckBox(w_frame, text=action,offvalue=f"OFF{key}", onvalue=key,variable=action_vars[key],command = lambda key=key: self.image_actions_callback(action_vars[key]),
             border_width=1, border_color="#E5E5E5").pack(side="left", padx=6)
        # CTK.CTkCheckBox(w_frame, text="Increace Quality", onvalue="IQ").pack(side="left")



        w_frame.pack(pady=5, ipadx=3, ipady=3)

        # Image preview

        images_frame = CTK.CTkFrame(frame)

        self.selected_image = CTK.CTkLabel(images_frame, image=my_image, text="")
        self.selected_image.pack(side="left")

        CTK.CTkLabel(images_frame, image=arrow_image, text="").pack(side="left", padx=10)

        self.transformed_image = CTK.CTkLabel(images_frame, image=my_image, text="")
        self.transformed_image.pack(side="right")
        images_frame.pack(expand=True, pady=10)

        self.process_btn = CTK.CTkButton(frame, text="Process now.",  
            image=create_ctk_image_instance("./view/assets/engineering.png", (20,20)))
        self.process_btn.pack(pady=5,padx=4, side="left")
        self.process_btn.configure(state="disabled", command=self.image_process_thread)

        self.reset_btn = CTK.CTkButton(frame, text="reset", fg_color="transparent",hover=False,
            image=create_ctk_image_instance("./view/assets/undo.png", (20,20)), command=self.viewmodel.reset_image_tab_ui)
        self.reset_btn.pack(pady=5,padx=4, side="left")
        self.reset_btn.configure(state="disabled")
    

        frame.pack(expand=True, pady=3,ipadx=5, padx=3, fill="both")

    def image_tab_reset(self):
        self.selected_image.configure(image=my_image)
        self.transformed_image.configure(image=my_image)


    @decorators.log(message=None)
    def image_process_thread(self) -> None:
        threading.Thread(target = self.viewmodel.process_image, args=(self.status_label,)).start()
        # self.viewmodel.process_image()

    @decorators.log(message=None)
    def set_loaded_image(self):
        self._current_image_to_process = openfiledialog()
        if self._current_image_to_process != None:
            instance = create_ctk_image_instance(self._current_image_to_process)
            self.selected_image.configure(image=instance)
        self.enable_process_btn()

    @decorators.log(message=None)
    def set_transformed_image(self, image_path):
        image_ui_instance = create_ctk_image_instance(image_path)
        self.transformed_image.configure(image=image_ui_instance)



    @decorators.log(message=None)
    def enable_process_btn(self) -> None:
        self.process_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")


    @decorators.log(message=None)
    def image_actions_callback(self, var):
        self.viewmodel.on_image_process_actions_changed(var.get())
    @decorators.log(message=None)
    def set_viewmodel(self, viewmodel) -> None:
        self.viewmodel = viewmodel


    @decorators.log(message=None)
    def read_application_state(self,key, state_file = APPLICATION_STATE_FILE) -> str:
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
                return state[key]
        except (FileNotFoundError, json.JSONDecodeError):
            return None


    @decorators.log(message=None)
    def on_close(self) -> None:
        """
        Saves the current window state to `app_state.json` and destroys the Tkinter root window.

        The function creates a dictionary `state` with the current window geometry (position and size) and
        writes it to the file `./app_state.json` using the `json.dump` method. The file will be created
        if it does not already exist. The function then destroys the Tkinter root window.

        Args:
            self: The instance of the class that contains the `on_close` method.

        Returns:
            None
        """
        state = {'geometry': self.root.geometry()}
        with open('./app_state.json', 'w') as f:
            json.dump(state, f)
        self.root.destroy()






   
