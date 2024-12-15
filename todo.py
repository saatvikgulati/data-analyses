import tkinter as tk
from tkinter import filedialog,messagebox
import pickle as pk

root = tk.Tk()
root.title('analyser 1.0')
root.geometry('800x600')

frame_task = tk.Frame(root)
frame_task.pack()

entry_task = tk.Entry(root,width = 80)
entry_task.pack()

# ADD TASK
def add_task(event = 0):
    task = entry_task.get()
    # check if entry task is empty or white space
    if task == '':
        messagebox.showerror('Add Task','You must enter a task')
    else:
        list_box_tasks.insert(tk.END,task)
        entry_task.delete(0,tk.END)
        list_box_tasks.see(tk.END)

button_add_task = tk.Button(root,text = 'Add Task',width = 68,command = add_task)
button_add_task.pack()
root.bind('<Return>',add_task)

# DELETE TASK
def delete_task(event = 0):
    task_indexes = list_box_tasks.curselection()
    if not task_indexes:
        task_index = 0
    else:
        task_index = task_indexes[0]
    list_box_tasks.delete(task_index)
button_delete_task = tk.Button(root,text = 'Delete Task',width = 68,command = delete_task)
button_delete_task.pack()
root.bind('<Control-d>',delete_task)

# SAVED TASKS
def save_list():
    # filename = entry_task.get()
    filename = filedialog.asksaveasfilename(defaultextension='.pkl',filetypes=[('Pickle files','*.pkl*')])
    # filename = filename.strip()
    if filename:
        task_list = list_box_tasks.get(0,tk.END)
        pk.dump(task_list,open(f'{filename}','wb'))
        messagebox.showwarning('Success!!','File saved!!')
    else:
        messagebox.showerror('Could not save the file')
button_save_list = tk.Button(root,width = 68,text = 'Save Task',command = save_list)
button_save_list.pack()

# load task
def load_task():
    list_box_tasks.delete(0,tk.END)
    # filename = entry_task.get()
    filename = filedialog.askopenfilename(filetypes=[('Pickle files','*.pkl*')])
    if filename:
        loaded_tasks = pk.load(open(f'{filename}','rb'))
        for task in loaded_tasks:
            list_box_tasks.insert(tk.END,task)
        entry_task.delete(0,tk.END)

button_load_task = tk.Button(root,width = 68,text = 'Load Task',command = load_task)
button_load_task.pack()

# SCROLL BARS
scrollbar_task = tk.Scrollbar(frame_task,orient='vertical')
scrollbar_task.pack(side= tk.RIGHT,fill = tk.Y)

list_box_tasks = tk.Listbox(frame_task,height = 10,width = 80)
list_box_tasks.pack()

list_box_tasks.config(yscrollcommand=scrollbar_task.set)
scrollbar_task.config(command=list_box_tasks.yview)

root.mainloop()