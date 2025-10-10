# create simple calculator using GUI 

# deploy in window desktop application using exe 
# for GUI we have to use tkinter library 
import tkinter as tk

def click(event):
    global expression
    expression += str(event.widget["text"])
    input_text.set(expression)

def clear():
    global expression
    expression = ""
    input_text.set(expression)

def evaluate():
    global expression
    try:
        result = str(eval(expression))
        input_text.set(result)
        expression = result
    except Exception as e:
        input_text.set("Error")
        expression = ""

# Create main window
root = tk.Tk()
root.title("Simple Calculator")

expression = ""
input_text = tk.StringVar()

# Input field
input_frame = tk.Frame(root, bd=2, relief=tk.RIDGE)
input_frame.pack(pady=10)

input_field = tk.Entry(input_frame, textvariable=input_text, font=('arial', 20, 'bold'), bd=5, relief=tk.SUNKEN, justify='right')
input_field.pack(ipadx=8, ipady=8)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

for row in buttons:
    row_frame = tk.Frame(btn_frame)
    row_frame.pack()
    for btn in row:
        button = tk.Button(row_frame, text=btn, font=('arial', 18), width=4, height=2)
        button.pack(side='left', padx=2, pady=2)
        if btn == '=':
            button.bind('<Button-1>', lambda e: evaluate())
        else:
            button.bind('<Button-1>', click)

# Clear button
clear_btn = tk.Button(root, text='Clear', font=('arial', 16), width=18, command=clear)
clear_btn.pack(pady=10)

root.mainloop()


# pyinstaller --onefile --windowed pythonbasic\CalculatorGUI.py