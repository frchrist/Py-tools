import customtkinter as CTK
class status:
	def __init__(parent):
		self.parent = parent

	def status_bar_widget(self):
        image_tab = self.parent.main_tab.tab(IMAGE_TAB)
        frame = CTK.CTkFrame(parent, fg_color="#F3FFF5", corner_radius=0)

        self.status_label = CTK.CTkLabel(frame, text="stable", )
        self.status_label.pack(side='left')


        frame.pack(fill="both", padx=3)

 

    def reset_status_bar(self, mil=3000):
        self.parent.root.after(mil, self.reset_bar)
    def reset_bar(self):
        self.status_label.configure(text="")
        # Pej6jMakj4