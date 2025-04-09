import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Dummy UI Window")
    root.geometry("400x200")  # Width x Height

    # Add a label
    label = tk.Label(root, text="Hello, this is a dummy UI window!")
    label.pack(pady=20)

    # Add a button
    button = tk.Button(root, text="Click Me", command=lambda: label.config(text="Button Clicked!"))
    button.pack()

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
