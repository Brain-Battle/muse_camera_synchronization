import tkinter as tk
from tkinter import messagebox, ttk
from connection import LumixConnection, GoProConnection, MuseConnection, SocketConnection
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Connection and Recording")

        self.entities = ["Lumix", "Android_WiFi", "Muse", "GoPro"]
        self.table_data = []
        self.connections = []

        instructions = (
            "Instructions:\n"
            "1) Click add device at the bottom\n"
            "2) Double click on the row in a table to modify the row\n"
            "3) Add parameters like IP address, IP address and port or name of a Muse device\n"
            "4) Connect\n"
            "5) Start recording\n"
            "6) Stop recording\n"
        )
        self.instructions_label = tk.Label(root, text=instructions, justify=tk.LEFT)
        self.instructions_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        self.style.configure("Treeview", font=('Arial', 10), rowheight=25)
        self.style.map("Treeview", background=[('selected', '#347083')], foreground=[('selected', 'white')])

        # Configure striped row colors
        self.style.configure("Treeview", background="#f0f0ff", fieldbackground="#f0f0ff")
        self.style.map("Treeview", background=[('selected', '#347083'), ('!selected', '#f0f0ff')])

        self.create_table()

        self.add_row_button = tk.Button(root, text="Add Device", command=self.add_row)
        self.add_row_button.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew')

        self.delete_row_button = tk.Button(root, text="Delete Device", command=self.delete_last_row)
        self.delete_row_button.grid(row=3, column=0, columnspan=4, pady=10, sticky='ew')

        self.add_row_button = tk.Button(root, text="Connect devices", command=self.connect_devices)
        self.add_row_button.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')

        self.add_row_button = tk.Button(root, text="Start recordings", command=self.start_recordings)
        self.add_row_button.grid(row=5, column=0, columnspan=4, pady=10, sticky='ew')

        self.add_row_button = tk.Button(root, text="Stop recordings", command=self.stop_recordings)
        self.add_row_button.grid(row=6, column=0, columnspan=4, pady=10, sticky='ew')


    def delete_last_row(self):
        if self.table_data:
            last_row_id = len(self.table_data) - 1
            self.tree.delete(last_row_id)
            del self.table_data[last_row_id]
            self.update_tree()
        else:
            messagebox.showinfo("Delete Device", "No devices to delete.")

    def create_table(self):
        self.tree = ttk.Treeview(self.root, columns=("Device", "Parameters"), show='headings')
        self.tree.heading("Device", text="Device")
        self.tree.heading("Parameters", text="Parameters")
        self.tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        self.tree.tag_configure('oddrow', background='#f0f0ff')
        self.tree.tag_configure('evenrow', background='#ffffff')

        self.tree.bind("<Double-1>", self.on_double_click)

    def add_row(self):
        row_id = len(self.table_data)
        self.table_data.append({"device": tk.StringVar(), "parameters": tk.StringVar()})

        tag = 'evenrow' if row_id % 2 == 0 else 'oddrow'
        self.tree.insert('', 'end', iid=row_id, values=("Select Device", "Enter Parameters"), tags=(tag,))
        self.update_tree()

    def on_double_click(self, event):
        if len(self.tree.selection()) == 0:
            return
        item = self.tree.selection()[0]
        row_id = int(item)
        self.edit_row(row_id)

    def edit_row(self, row_id):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Row")

        tk.Label(edit_window, text="Entity:").grid(row=0, column=0, padx=10, pady=5)
        entity_menu = ttk.Combobox(edit_window, textvariable=self.table_data[row_id]["device"])
        entity_menu['values'] = self.entities
        entity_menu.grid(row=0, column=1, padx=10, pady=5)
        entity_menu.set(self.tree.item(row_id, 'values')[0])

        tk.Label(edit_window, text="Parameters:").grid(row=1, column=0, padx=10, pady=5)
        param_entry = tk.Entry(edit_window, textvariable=self.table_data[row_id]["parameters"])
        param_entry.grid(row=1, column=1, padx=10, pady=5)
        param_entry.insert(0, self.tree.item(row_id, 'values')[1])

        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_row(row_id, edit_window))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def save_row(self, row_id, edit_window):
        self.update_tree()
        edit_window.destroy()

    def update_tree(self):
        for row_id, data in enumerate(self.table_data):
            self.tree.item(row_id, values=(data["device"].get(), data["parameters"].get()))

    def connect_devices(self):
        device_list = self.get_device_list()
        self.connections = []
        for entity in device_list:
            device = entity[0]
            params = entity[1]
            if device == "Lumix":
                self.connections.append(LumixConnection(params).connect())
            elif device == "Android_WiFi":
                l = params.split(":")
                ip = l[0]
                if len(l) == 1:
                    port = 3000
                else:
                    port = int(l[1])
                self.connections.append(SocketConnection(ip, port).connect())
            elif device == "Muse":
                self.connections.append(MuseConnection(params).connect())
            elif device == "GoPro":
                self.connections.append(GoProConnection().connect())
            else:
                assert False
        #GoProConnection.refresh()

        print("Connecting devices:", device_list)
        messagebox.showinfo("Connect Devices", f"Connecting devices: {device_list}")

    def start_recordings(self):
        for connection in self.connections:
            connection.start_recording()
        print("Starting recordings")
        messagebox.showinfo("Start Recordings", "Starting recordings...")

    def stop_recordings(self):
        for connection in self.connections:
            connection.stop_recording()
        print("Stopping recordings")
        messagebox.showinfo("Stop Recordings", "Stopping recordings...")

    def get_device_list(self):
        return [(data["device"].get(), data["parameters"].get()) for data in self.table_data]



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
