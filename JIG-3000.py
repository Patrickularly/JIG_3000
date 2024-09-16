import customtkinter as ctk
import sqlite3
from tkinter import messagebox

connection = sqlite3.connect('JIG-3000.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS "jig-3000"(
                            id INTEGER PRIMARY KEY,
                            problems TEXT,
                            objects TEXT)''')

root = ctk.CTk()
root.geometry('500x500')
root.title('JIG-3000')
root.resizable(False, False)

custom_colors = {
                'gen1': '#05AFD3',
                'gen2': '#2FCCEB',
                'bg': '',
                'fg': '#44109F',
                'btns': '#05AFD3',
                'none': 'transparent'
}

fonts = {
    'gen': ('Rockwell',17,'bold'),
    'btns': ('Krungthep',15),
    'lbl': ('Arial',10,'bold'),
    'head': ('Rockwell',35, 'bold'),
}

def center_window(root, width, height):
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f'{width}x{height}+{x}+{y}')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)  # No expansion for columns

################################
#         Warning popup        #
################################

def open_messeagebox(warning_type):
    if warning_type == 'problem':
        messagebox.showwarning(message='This problem already exists!')
    elif warning_type == 'object':
        messagebox.showwarning(message='This object already exists!')
    elif warning_type == 'empty_problem':
        messagebox.showwarning(message='You need to enter a problem!')
    elif warning_type == 'empty_object':
        messagebox.showwarning(message='You need to enter an object!')

################################
#       Buttons function       #
################################

def on_button_click(button_id):
    if button_id == 'edit':
        popup = ctk.CTkToplevel(master=root)
        popup.title('Editor')

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_rowconfigure(1, weight=1)
        
        popup.update_idletasks()
        width = popup.winfo_reqwidth()
        height = popup.winfo_reqheight()
        popup.geometry(f'{width}x{height}')

        lbox = ctk.CTkScrollableFrame(popup)
        lbox.grid(row=3, column=0, pady=5, padx=5)
        
        cursor.execute('''SELECT * FROM "jig-3000"''')
        rows = cursor.fetchall()
        for row in rows:
            entry_label = ctk.CTkLabel(lbox, text=f'{row[0]}. {row[1]} {row[2]}')
            entry_label.pack(pady=5, padx=5, anchor='w')  # Pack each entry into the frame
        

        label = ctk.CTkLabel(master=popup, wraplength=360, justify='left', text='Which entry do you want to edit?')
        label.grid(row=0, column=0, pady=20, padx=20, sticky='nesw', columnspan=2)

        button_save = ctk.CTkButton(master=popup, fg_color=custom_colors['btns'], text='SAVE')
        s_button = ctk.CTkButton(master=popup, fg_color='green', text='Object')
        close_button = ctk.CTkButton(master=popup, fg_color='blue', text='Quit', command=popup.destroy)

        button_save.grid(row=1, column=0, padx=20, pady=(0,20))
        s_button.grid(row=1, column=1, padx=20, pady=(0,20))
        close_button.grid(row=2, column=0, padx=20, pady=(0,20))

        popup.update_idletasks()
        width = popup.winfo_reqwidth()
        height = popup.winfo_reqheight()
        popup.geometry(f'{width}x{height}')

    elif button_id == 'generate':
        cursor.execute('''SELECT objects FROM "jig-3000" ORDER BY RANDOM() LIMIT 1''')
        object = cursor.fetchone()[0]
        cursor.execute('''SELECT problems FROM "jig-3000" ORDER BY RANDOM() LIMIT 1''')
        problem = cursor.fetchone()[0]
        label_output.configure(text=f'PROBLEM:{problem} OBJECT: {object}')

    elif button_id == 'problem':

        if not entry_problem.get():
            open_messeagebox('empty_problem')
            return
        
        user_input = entry_problem.get().strip().upper()
        cursor.execute('''SELECT COUNT(*) FROM "jig-3000" WHERE problems = ?''', (user_input,))
        entry_check = cursor.fetchone()[0]

        if entry_check > 0:
            open_messeagebox('problem')
            entry_problem.delete(0, ctk.END)

        else:
            cursor.execute('''SELECT id FROM "jig-3000" WHERE problems IS NULL LIMIT 1''')
            empty_row = cursor.fetchone()

            if empty_row:
                cursor.execute('''UPDATE "jig-3000" SET problems = ? WHERE id = ?''', (user_input, empty_row[0]))
            else:
                cursor.execute('''INSERT INTO "jig-3000" (problems) VALUES(?)''', (user_input,))
            
            connection.commit()
            entry_problem.delete(0, ctk.END)

    elif button_id == 'object':

        if not entry_object.get():
            open_messeagebox('empty_object')
            return

        user_input = entry_object.get().strip().upper()
        cursor.execute('''SELECT COUNT(*) FROM "jig-3000" WHERE objects = ?''', (user_input,))
        entry_check = cursor.fetchone()[0]

        if entry_check > 0:
            open_messeagebox('object')
            entry_object.delete(0, ctk.END)
        else:
            cursor.execute('''SELECT id FROM "jig-3000" WHERE objects IS NULL LIMIT 1''')
            empty_row = cursor.fetchone()

            if empty_row:
                cursor.execute('''UPDATE "jig-3000" SET objects = ? WHERE id = ?''', (user_input, empty_row[0]))

            else:
                cursor.execute('''INSERT INTO "jig-3000" (objects) VALUES(?)''', (user_input,))

            connection.commit()
            entry_object.delete(0, ctk.END)

    elif button_id == 'faq':
        popup = ctk.CTkToplevel(master=background)
        popup.geometry('600x500')
        popup.title('How to use the JIG-3000')

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_rowconfigure(1, weight=1)

        label_summary = ctk.CTkLabel(master=popup, 
                            wraplength=400, 
                            justify='left',
                            font=('Arial',15),
                            text = ("The JIG-3000 stimulates creativity by connecting unrelated problems "
                                    "and objects. Based on Arthur Koestler's bi-sociative thinking model, "
                                    "it encourages humorous or absurd objects by pairing problems with "
                                    "random objects, breaking conventional thought patterns."
                                    ))
        label_summary.grid(row=0, column=0, pady=20, padx=20, sticky='nesw')

        label = ctk.CTkLabel(master=popup, 
                            wraplength=400, 
                            justify='left',
                            font=('Arial',15,'bold'),
                            text='1. Enter a specific PROBLEM and a random OBJECT.*\n\n'\
                                '2. Press generate.\n\n'\
                                '3. Try solving the PROBLEM with the OBJECT.**')
        label.grid(row=1, column=0, pady=(0,20), padx=20, sticky='nesw')

        label_example = ctk.CTkLabel(master=popup,
                                    wraplength=400,
                                    justify='left',
                                    text=("EXAMPLE:\n"
                                    "When the PROBLEM is 'Global warming' and the OBJECT is 'Tablecloths,' you might suggest covering "
                                    "the world in white tablecloths to reflect sunlight and cool the planet. This could boost textile "
                                    "industries and avoid color clashes. To prevent interference with photosynthesis, use lace tablecloths "
                                    "and let tree branches poke through. Embrace the absurdity fully!"))

        label_example.grid(row=2, column=0, pady=(0,20), padx=20, sticky='nesw')

        close_button = ctk.CTkButton(master=popup, fg_color='blue', text='Quit', command=popup.destroy)
        close_button.grid(row=3, column=0, padx=20, pady=(0,20))

        label = ctk.CTkLabel(master=popup, 
                    wraplength=400, 
                    justify='left',
                    font=('Arial',10),
                    text='* Repeat as many times as you want. Try to keep the piles equal in numbers.\n'\
                        '** Your answer doesn\'t have to be logical, or even follow the laws of physics.')
        
        label.grid(row=4, column=0, pady=(0,20), padx=20, sticky='nesw')

        popup.update_idletasks()
        width = popup.winfo_reqwidth()
        height = popup.winfo_reqheight()
        popup.geometry(f'{width}x{height}')
    
    elif button_id == 'quit':
        connection.close()  # Close the SQLite connection
        root.destroy() 

background = ctk.CTkFrame(root, fg_color='#7E30FA')
for i in range(7):
    background.grid_rowconfigure(i, weight=1)
for j in range(2):
    background.grid_columnconfigure(j, weight=1)

label_header = ctk.CTkLabel(master=background, text_color='white', fg_color=custom_colors['none'], font=fonts['head'], text='JIG-3000')

label_frame = ctk.CTkFrame(master=background,fg_color=custom_colors['fg'])
label_frame.grid_columnconfigure(0,weight=1)
label_frame.grid_rowconfigure(0,weight=1)

label_output = ctk.CTkLabel(master=label_frame, fg_color=custom_colors['none'], font=fonts['lbl'],text_color='white', text='Generate a random pair')

entry_frame = ctk.CTkFrame(background, fg_color=custom_colors['fg'])
for i in range(3):
    entry_frame.grid_columnconfigure(i,weight=1)
for j in range(2):
    entry_frame.grid_rowconfigure(j,weight=1)

entry_problem = ctk.CTkEntry(master=entry_frame, text_color='black', height=35,width=230, fg_color='white', placeholder_text='Enter a problem', placeholder_text_color='darkgrey')
entry_problem.bind('<Return>', lambda event: on_button_click('problem'))
entry_object = ctk.CTkEntry(master=entry_frame, text_color='black', height=35, width=230, fg_color='white', placeholder_text='Enter a object', placeholder_text_color='darkgrey')
entry_object.bind('<Return>', lambda event: on_button_click('object'))

button_faq = ctk.CTkButton(master=background, font=fonts['btns'], text='FAQ', text_color='white', fg_color=custom_colors['gen1'], hover_color=custom_colors['gen2'], command=lambda: on_button_click('faq'))
button_edit = ctk.CTkButton(master=background,font=fonts['btns'], text='EDIT', text_color='white', fg_color=custom_colors['gen1'], hover_color=custom_colors['gen2'], command=lambda: on_button_click('edit'))
button_enter_1 = ctk.CTkButton(master=entry_frame, font=fonts['btns'], text='ADD PROBLEM', text_color='white', fg_color=custom_colors['gen1'], hover_color=custom_colors['gen2'], command=lambda: on_button_click('problem'))
button_enter_2 = ctk.CTkButton(master=entry_frame, font=fonts['btns'], text='ADD OBJECT', text_color='white', fg_color=custom_colors['gen1'], hover_color=custom_colors['gen2'],command=lambda: on_button_click('object'))
button_generate = ctk.CTkButton(master=background, border_spacing=15, corner_radius=250, border_width=5, border_color=custom_colors['fg'],text_color=custom_colors['fg'], font=fonts['gen'], fg_color='white', text='GENERATE NEW PAIR', hover_color='#E2CDB4', command=lambda: on_button_click('generate'))
button_quit = ctk.CTkButton(master=background, font=fonts['btns'], text='QUIT', text_color='white', fg_color=custom_colors['gen1'], hover_color=custom_colors['gen2'], command=lambda: on_button_click('quit'))

background.grid(row=0, column=0, pady=15, padx=15, sticky='nesw')

background.grid_rowconfigure(0, weight=0)
for i in range(1,4):
    background.grid_rowconfigure(i, weight=1)
for j in range(4):
    background.grid_columnconfigure(j,weight=1)

label_header.grid(row=0, column=0, pady=(15,0), padx=10, ipady=10, columnspan=4, sticky='ew')
label_frame.grid(row=3,column=0, columnspan=4, sticky='ew', padx=15)
label_output.grid(row=0, column=0, pady=10, padx=20, columnspan=4, sticky='ew')

entry_frame.grid(row=1,column=0,columnspan=4, padx=15, pady=(20,0), sticky='nesw')
entry_problem.grid(row=0, column=0, pady=(20,5), padx=(20,0), ipady=5, sticky='nesw', columnspan=2)
entry_object.grid(row=1, column=0, pady=(5,20), padx=(20,0), ipady=5, sticky='nesw', columnspan=2)

button_faq.grid(row=4, column=0, pady=20, padx=20, ipady=5, sticky='nesw')
button_edit.grid(row=4, column=1, pady=20, padx=20, ipady=5, sticky='nesw')
button_enter_1.grid(row=0, column=2, pady=(20,5), padx=(0,20), ipady=5, sticky='e')
button_enter_2.grid(row=1, column=2, pady=(5,20), padx=(0,20), ipady=5, sticky='e')
button_generate.grid(row=2, column=0, pady=(20), padx=100, columnspan=4, sticky='ew')
button_quit.grid(row=4,column=2, pady=20, padx=20, ipady=5, sticky='nesw')

root.mainloop()