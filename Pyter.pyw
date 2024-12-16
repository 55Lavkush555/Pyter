from tkinter import *
import sys
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess
import os
from tkinter import filedialog
import subprocess
import re
import webbrowser
import threading
from tkinter import scrolledtext
from tkinter.scrolledtext import ScrolledText


root = Tk()

filelist = os.listdir("C:\\Users\\Public\\Documents")
filedir = os.getcwd()

root.geometry('888x644')
root.title('Pyter')
root.iconbitmap('icon.ico')


class TextWithListbox:
    def __init__(self, root, h):
        self.root = root
        self.h = h
        
        
        self.suggestion_box = Listbox(root)
        self.suggestion_box.place_forget()

        text.bind('<KeyRelease>', self.provide_suggestions)
        self.suggestion_box.bind("<Double-1>", self.insert_suggestion)
        self.suggestion_box.bind("<Return>", self.insert_suggestion_r)

    def provide_suggestions(self, event):
        global word
        global suggestions

        suggestions = [
    'and', 'as', 'assert', 'async', 'await',
    'break', 'continue',
    'def', 'del',
    'elif', 'else', 'except',
    'False', 'finally', 'for', 'from',
    'global',
    'if', 'import', 'in', 'is', 'input',
    'lambda',
    'None', 'nonlocal', 'not',
    'or',
    'pass',
    'raise', 'return',
    'True', 'try',
    'while', 'with',
    'yield', 'print', 'open',
    'int', 'str', 'float',

    'class', 'self', 'super', 'staticmethod', 'classmethod',
    '__init__', '__new__', '__del__', '__str__', '__repr__',
    '__len__', '__getitem__', '__setitem__', '__delitem__',
    '__iter__', '__name__', '__next__', '__contains__', '__call__',
    '__eq__', '__ne__', '__lt__', '__le__', '__gt__', '__ge__',
    '__add__', '__sub__', '__mul__', '__truediv__', '__floordiv__',
    '__mod__', '__pow__', '__and__', '__or__', '__xor__', '__invert__',
    '__rshift__', '__lshift__', '__iadd__', '__isub__', '__imul__',
    '__itruediv__', '__ifloordiv__', '__imod__', '__ipow__',
    '__iand__', '__ior__', '__ixor__', '__ilshift__', '__irshift__',
   
    'getattr', 'setattr', 'hasattr', 'delattr', 'isinstance',
    'issubclass', 'type', 'id', 'dir', 'read', 'write'
]

        self.suggestion_box.delete(0, END)

        word = get_closest_word(text)

        for suggestion in suggestions:
            if suggestion.startswith(word):
                self.suggestion_box.insert(END, suggestion)

        cursor_index = text.index(INSERT)
        line, column = map(int, cursor_index.split('.'))

        bbox = text.bbox(f"{line}.{column}")
        if bbox:
            a, y, width, height = bbox
            self.suggestion_box.place(x=a+220, y=y+50 + height)
            self.suggestion_box.lift()
        else:
            self.suggestion_box.place_forget()

        highlight_functions(text)
        colour_words()

    def insert_suggestion(self, event):
        selected_suggestion = self.suggestion_box.get(ACTIVE)
        if selected_suggestion:
            selected_suggestion = selected_suggestion[len(word):len(selected_suggestion)]
            text.insert(INSERT, selected_suggestion)
            text.focus_set()
            self.suggestion_box.place_forget()
            colour_words()

    def insert_suggestion_r(self, event):
        selected_index = self.suggestion_box.curselection()
   
        if selected_index:
            selected_suggestion = self.suggestion_box.get(selected_index[0])
            selected_suggestion = selected_suggestion[len(word):len(selected_suggestion)]
            text.insert(INSERT, selected_suggestion)
            text.focus_set()
            self.suggestion_box.place_forget()
            colour_words()



def highlight_word(text_widget, word, color):
    text_widget.tag_remove(word, "1.0", END)

    text_widget.tag_configure(word, foreground=color)

    pattern = r'\b' + re.escape(word) + r'\b'

    text_content = text_widget.get("1.0", END)

    for match in re.finditer(pattern, text_content):
        start_index = f"1.0+{match.start()}c"
        end_index = f"1.0+{match.end()}c"
        
        text_widget.tag_add(word, start_index, end_index)

def list_files(directory):
    return os.listdir(directory)

def New():
    global file
    file = None
    text.delete(1.0, END)

def Open(event=None):
    global file
    try:
        file = askopenfilename(defaultextension='.py',
                                filetypes=[('All Files', '*.*'),
                                            ('Text Documents','*.txt')])
    
        if file == '':
            file = None
        else:
            text.delete(1.0,END)
            f = open(file, 'r')
            text.insert(1.0, f.read())
            f.close()    

    except:
        showinfo('Error', 'We could not open this file')

def openfolder():
    a = filedialog.askdirectory()
    return a

def open_folder(event=None):
    global file_
    global l
    global path

    l = False
    file_ = filedialog.askdirectory()

    with open('C:\\Users\\Public\\Documents\\path.txt', 'w') as f:
        f.write(file_)

    file_list.delete(0, END)
    b = 0
    path = file_
    file_ = list_files(file_)
    while b<len(file_):
        file_list.insert(END, file_[b])
        b+=1

    os.chdir(path)


def Save(event=None):
    global file
    if file == None:
        file = asksaveasfilename(initialfile='main.py', defaultextension='.py',
                             filetypes=[('All Files', '*.*'),
                                        ('Text Documents','*.txt')])
        
    if file =='':
        file = None

    else:
        f = open(file, 'w') 
        f.write(text.get(1.0, END))
        f.close()

def cut():
    text.event_generate(('<<Cut>>'))

def copy():
    text.event_generate(('<<Copy>>'))

def paste():
    text.event_generate(('<<Paste>>'))

def gethelp():
    webbrowser.open('http://55lavkush555.infinityfreeapp.com/')

def Terminal():
    subprocess.run(["start", "cmd"], shell=True)

def on_double_click(event):
    global file
    index = file_list.curselection()
    if index:
        item_text = file_list.get(index)

        try:
            text.delete(1.0, END)
            with open(f'{path}/{item_text}') as f:
                text.insert(1.0, f.read())
            file = f'{path}/{item_text}'
        except:
            os.startfile(f'{path}/{item_text}')

        colour_words()

def esc():
    sys.exit()

def on_bracket(event):
    if event.char == '(':
        text.insert(INSERT, "()")
        text.mark_set(INSERT, f"{text.index(INSERT)}-1c")
        return "break"

def on_collen(event):
    if event.char == "'":
        text.insert(INSERT, "''")
        text.mark_set(INSERT, f"{text.index(INSERT)}-1c")
        return "break"

def on_doublecollen(event):
    if event.char == '"':
        text.insert(INSERT, '""')
        text.mark_set(INSERT, f"{text.index(INSERT)}-1c")
        return "break"

def on_curli_bracket(event):
    if event.char == '{':
        text.insert(INSERT, '{}')
        text.mark_set(INSERT, f"{text.index(INSERT)}-1c")
        return "break"

def squaric_bracket(event):
    if event.char == '[':
        text.insert(INSERT, '[]')
        text.mark_set(INSERT, f"{text.index(INSERT)}-1c")
        return "break"

def get_closest_word(text_widget):
    cursor_position = text_widget.index("insert")
    
    line, column = map(int, cursor_position.split('.'))
    
    line_start = f"{line}.0"
    line_text = text_widget.get(line_start, cursor_position)

    words = re.findall(r'\b\w+\b', line_text)

    if words:
        return words[-1]
    else:
        return ""
    
def set_tab_size(text_widget, spaces=4):
    font_size = int(text_widget.cget("font").split()[1]) 
    tab_width = font_size * spaces
    text_widget.config(tabs=(tab_width,))

def highlight_functions(text_widget):
    global suggestions
    global h
    text_widget.tag_remove("function", "1.0", END)
    
    pattern = r'\bdef\b\s+(\w+)'

    text_content = text_widget.get("1.0", END)
    
    for match in re.finditer(pattern, text_content):

        start_index = f"1.0+{match.start(1)}c"
        end_index = f"1.0+{match.end(1)}c"
        
        text_widget.tag_add("function", start_index, end_index)

        h = text.get(start_index, end_index)

def colour_words():
    highlight_word(text, 'if', "red")
    highlight_word(text, 'else', "red")
    highlight_word(text, 'elif', "red")
    highlight_word(text, 'try', "red")
    highlight_word(text, 'except', "red")
    highlight_word(text, 'finally', "red")
    highlight_word(text, 'return', "red")
    highlight_word(text, 'def', "blue")
    highlight_word(text, 'True', "blue")
    highlight_word(text, 'False', "blue")
    highlight_word(text, 'None', "blue")
    highlight_word(text, 'break', "blue")
    highlight_word(text, 'and', "green")
    highlight_word(text, 'assert', "green")
    highlight_word(text, 'async', "green")
    highlight_word(text, 'await', "green")
    highlight_word(text, 'as', "orange")
    highlight_word(text, 'import', "orange")
    highlight_word(text, 'input', "orange")
    highlight_word(text, 'class', "orange")
    highlight_word(text, 'continue', "orange")
    highlight_word(text, 'del', "orange")
    highlight_word(text, 'from', "orange")
    highlight_word(text, 'or', "orange")
    highlight_word(text, 'not', "purple")
    highlight_word(text, 'for', "purple")
    highlight_word(text, 'while', "purple")
    highlight_word(text, 'with', "purple")
    highlight_word(text, 'yield', "purple")
    highlight_word(text, 'pass', "red")
    highlight_word(text, 'global', "green")
    highlight_word(text, 'nonlocal', "green")
    highlight_word(text, 'lambda', "orange")
    highlight_word(text, 'raise', "red")
    highlight_word(text, 'self', "orange")
    highlight_word(text, 'super', "orange")
    highlight_word(text, 'staticmethod', "orange")
    highlight_word(text, 'classmethod', "orange")
    highlight_word(text, '__init__', "orange")
    highlight_word(text, '__str__', "orange")
    highlight_word(text, '__repr__', "orange")
    highlight_word(text, '__len__', "orange")
    highlight_word(text, '__call__', "orange")
    highlight_word(text, '__name__', "orange")
    highlight_word(text, 'print', "brown")

def run_in_Turminal(event=None):
    output_window = Tk()
    output_window.title("output")

    output_area = scrolledtext.ScrolledText(output_window, wrap=WORD,font=("Arial", 12), state=DISABLED)
    output_area.pack(fill=BOTH, expand=1)

    code = text.get(1.0, END)
    with open(f"{path}/temp_script.py", "w") as temp_file:
        temp_file.write(code)
    
    result = subprocess.run(["python", f"{path}/temp_script.py"], capture_output=True,text=True)
    
    output_area.config(state=NORMAL)
    output_area.delete(1.0, END)
    output_area.insert(END, result.stdout)
    output_area.insert(END, result.stderr)
    output_area.config(state=DISABLED)

    output_window.mainloop()

def run(event=None):
    thread = threading.Thread(target=run_in_Turminal).start()
def run_r(event):
    thread = threading.Thread(target=run_in_Turminal).start()

def handle_newline(event):
    """Automatically add an indent after certain keywords."""
    current_line = text.get("insert linestart", "insert").strip()
    indent = get_current_indentation()

    if current_line.startswith(("if", "else", "elif", "def", "for", "while", "try", "except", "with", "class")):
        text.insert("insert", "\n" + "" * indent + "\t")
        global auto_tab
        auto_tab = True
        return "break"

    text.insert("insert", "\n" + "\t" * indent)
    return "break"

def get_current_indentation():
    """Get the current indentation of the line where the cursor is."""
    line = text.get("insert linestart", "insert")
    return len(line) - len(line.lstrip())

def reset_tab_flag(event):
    """Reset the auto_tab flag when the user moves to a new line."""
    global auto_tab
    if event.keysym in ("Return", "BackSpace"):
        auto_tab = False

def docs():
    os.startfile(f"{filedir}\\html\\index.html")

def show_context_menu(event):
    """Show the context menu on right-click."""
    try:
        index = file_list.nearest(event.y)
        file_list.selection_clear(0, END)
        file_list.selection_set(index)
        file_list.activate(index)

        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

def text_context_menu(event):
    """Show the context menu on right-click."""
    textcontext_menu.tk_popup(event.x_root, event.y_root)

def select_all():
    """Select all text in the text widget."""
    text.tag_add("sel", "1.0", "end")

        

if __name__ == "__main__":
    h = ''
    text_font = 'Areal 14'

    menubar = Menu(root)

    file = Menu(menubar, tearoff=0)
    file.add_command(label='New', command=New)
    file.add_command(label='Open', command=Open)
    file.add_command(label='Save', command=Save)
    file.add_command(label='Open folder', command=open_folder)
    file.add_separator()
    file.add_command(label='Exit', command=esc)
    menubar.add_cascade(label='File', menu = file)

    edit = Menu(menubar, tearoff=0)
    edit.add_command(label='cut', command=cut)
    edit.add_command(label='copy', command=copy)
    edit.add_command(label='paste', command=paste)
    menubar.add_cascade(label='Edit', menu = edit)

    Help = Menu(menubar, tearoff=0)
    Help.add_command(label='help',command=gethelp)
    Help.add_command(label='Terminal', command=Terminal)
    Help.add_command(label='Python Documentation', command=docs)
    menubar.add_cascade(label='Help', menu=Help)

    root.config(menu=menubar)

    file = None

    run = Button(root, text='Run', command=run, width=10).pack()

    Label(root, text='Files', font='lucida 10').pack(anchor=SW)
    files = Frame(root)

    file_list = Listbox(file, height=1000, width=35)
    try:
        with open('C:\\Users\\Public\\Documents\\path.txt') as f:
            path = f.read()
            file_ = list_files(path)
            os.chdir(path)
    except:
        file_ = list_files('\\')

    a = 0
    l = True

    while l==True and a<len(file_):
        file_list.insert(END, file_[a])
        a+=1

    file_list.pack(side=LEFT)
    file_list.bind("<Double-1>", on_double_click)
    files.pack(anchor=SW, fill='none')

    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="New", command=New)
    context_menu.add_command(label="Open new foler", command=open_folder)
    context_menu.add_command(label="Open", command=Open)

    frame = Frame(root, height=100000)

    wrap = "none"

    text = ScrolledText(frame, wrap=wrap, width=1000000, height=1000000, font=text_font, undo=True)
    text.pack(side=RIGHT, fill=X)
    app = TextWithListbox(root, h)

    frame.pack(anchor='se')

    textcontext_menu = Menu(root, tearoff=0)
    textcontext_menu.add_command(label="Undo", command=text.edit_undo)
    textcontext_menu.add_command(label="Redo", command=text.edit_redo)
    textcontext_menu.add_separator()
    textcontext_menu.add_command(label="Cut", command=cut)
    textcontext_menu.add_command(label="Copy", command=(copy))
    textcontext_menu.add_command(label="Paste", command=(paste))
    textcontext_menu.add_separator()
    textcontext_menu.add_command(label="Select All", command=select_all)

    text.bind("(", on_bracket)
    text.bind("'", on_collen)
    text.bind('"', on_doublecollen)
    text.bind('{', on_curli_bracket)
    text.bind('[', squaric_bracket)
    
    closest_word = get_closest_word(text)
    set_tab_size(text, spaces=4)
    text.tag_configure("function", foreground="green")
    highlight_functions(text)
    colour_words()
    text.bind("<Return>", handle_newline)
    text.bind("<Key>", reset_tab_flag)
    file_list.bind("<Button-3>", show_context_menu)
    text.bind("<Button-3>", text_context_menu)
    root.bind('<Control-s>', Save)
    root.bind('<Alt-r>', run_r)
    root.bind('<Control-f>', open_folder)
    root.bind('<Control-o>', Open)

    auto_tab = False

root.mainloop()
