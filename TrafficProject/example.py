import tkinter as tk

def get_multiple_inputs():
    num_inputs = int(entry_num_inputs.get())
    if num_inputs > 0:
        input_dialog = tk.Toplevel(root)
        input_dialog.title("Multiple Inputs")
        
        input_entries = []
        for i in range(num_inputs):
            label = tk.Label(input_dialog, text=f"Input {i+1}:")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(input_dialog)
            entry.grid(row=i, column=1, padx=10, pady=5)
            input_entries.append(entry)
        
        def submit_inputs():
            inputs = [entry.get() for entry in input_entries]
            print("User entered:", inputs)
            input_dialog.destroy()
        
        submit_button = tk.Button(input_dialog, text="Submit", command=submit_inputs)
        submit_button.grid(row=num_inputs, columnspan=2, padx=10, pady=10)

root = tk.Tk()
root.title("Multiple Inputs Example")

label_num_inputs = tk.Label(root, text="Enter the number of inputs you want:")
label_num_inputs.pack(pady=5)

entry_num_inputs = tk.Entry(root)
entry_num_inputs.pack(pady=5)

button_get_inputs = tk.Button(root, text="Get Multiple Inputs", command=get_multiple_inputs)
button_get_inputs.pack(pady=10)

root.mainloop()