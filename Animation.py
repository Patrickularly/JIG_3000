import customtkinter as ctk
from PIL import Image
from os import walk

class AnimationButton(ctk.CTkButton):

    def __init__(self, parent, path):
        super().__init__(master = parent, text = 'AniButton')
        self.pack(expand=True)
        self.import_folders(path)

    def import_folders(self, path):
        for paths in (path):
            print(list(walk(paths)))

# window
window = ctk.CTk()
window.geometry('300x300')
window.title('Animation Test')

AnimationButton(window,'checkmark')

# run
window.mainloop()