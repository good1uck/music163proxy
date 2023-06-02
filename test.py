import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

def generate_list():
    input_text = text_entry.get("1.0", "end-1c")
    ip_list = input_text.split("\n")
    ip_list = [ip.strip() for ip in ip_list if ip.strip()]
    output_text = "\n".join(ip_list)
    output_text_formatted = "[\n" + ",\n".join(["    '" + ip + "'" for ip in ip_list]) + "\n]"
    output_text_box.configure(state="normal")
    output_text_box.delete("1.0", tk.END)
    output_text_box.insert(tk.END, output_text_formatted)
    output_text_box.configure(state="disabled")
    clipboard_button.configure(state="normal")
    clipboard_text.set(output_text_formatted)  # Use the formatted output text for copying

def copy_to_clipboard():
    window.clipboard_clear()
    clipboard_content = clipboard_text.get()  # Copy the formatted output text
    window.clipboard_append(clipboard_content)
    messagebox.showinfo("Copy Successful", "The generated content has been copied to the clipboard.")

# Create the GUI window
window = tk.Tk()
window.title("IP List Generator")

# Create and position the text entry field
text_entry = tk.Text(window, height=10, width=30)
text_entry.grid(row=0, column=0, padx=10, pady=10)

# Create the generate button
generate_button = tk.Button(window, text="Generate List", command=generate_list)
generate_button.grid(row=1, column=0, padx=10, pady=5)

# Create the output label
output_text_box = scrolledtext.ScrolledText(window, height=10, width=30, state="disabled", wrap=tk.WORD)
output_text_box.grid(row=2, column=0, padx=10, pady=5)

# Create the copy button
clipboard_text = tk.StringVar()
clipboard_button = ttk.Button(window, text="Copy", command=copy_to_clipboard, state="disabled")
clipboard_button.grid(row=3, column=0, padx=10, pady=5)

# Run the GUI event loop
window.mainloop()
