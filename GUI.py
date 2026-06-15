import tkinter as tk
from tkinter import Text, Tk, simpledialog
from VM import VM


root = tk.Tk()
root.geometry('800x800')

def run():
    text = code.get('1.0', tk.END)
    VM.reset()

    VM.load(text)
    results = VM.run()
    output = ''
    for i in results:
        output = output + str(i) + '\n'
    var.set(output)


def VM_input():
    user_input = int(simpledialog.askinteger('input', 'Enter an Integer: ', parent=root))
    return user_input

VM = VM(input_function = VM_input)



root.title("ASSEMBLER")

var = tk.StringVar()
var.set("")

label = tk.Label(root, text="Write Your Code Below: ")
label.place(y=0)

code = tk.Text(root)
code.place(height=350, width=800, y=50)

submit = tk.Button(root, text='RUN', command=run)
submit.place(width=100, height=50, y=450)

output = tk.Label(root, textvariable=var)
output.place(height=350, width=800, y=500)


root.mainloop()
