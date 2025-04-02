import tkinter as tk
from tkinter import scrolledtext
import random
import os
import datetime

# --- FakeWindow class with draggable title bar ---
class FakeWindow(tk.Frame):
    def __init__(self, parent, title="Window", width=400, height=300, x=50, y=50):
        super().__init__(parent, bd=2, relief="raised", bg="#1e1e1e")
        self.parent = parent
        self.width = width
        self.height = height

        # Title bar
        self.title_bar = tk.Frame(self, bg="#444", relief="raised", bd=1)
        self.title_bar.pack(side="top", fill="x")
        self.title_label = tk.Label(self.title_bar, text=title, bg="#444", fg="white", font=("Courier", 10))
        self.title_label.pack(side="left", padx=5)
        self.close_button = tk.Button(self.title_bar, text="X", bg="#444", fg="white", command=self.destroy, bd=0, padx=5)
        self.close_button.pack(side="right")
        
        # Make the title bar draggable
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        
        # Content area
        self.content = tk.Frame(self, bg="#1e1e1e")
        self.content.pack(expand=True, fill="both")
        
        # Place the fake window in the parent desktop area
        self.place(x=x, y=y, width=width, height=height)
    
    def start_move(self, event):
        # Record the offset of the click relative to the window
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_move(self, event):
        # Calculate new position
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y
        
        current_x = self.winfo_x()
        current_y = self.winfo_y()
        new_x = current_x + dx
        new_y = current_y + dy

        # Get parent's dimensions
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        # Ensure the window stays within parent's boundaries
        if new_x < 0:
            new_x = 0
        elif new_x + self.width > parent_width:
            new_x = parent_width - self.width

        if new_y < 0:
            new_y = 0
        elif new_y + self.height > parent_height:
            new_y = parent_height - self.height

        self.place_configure(x=new_x, y=new_y)

# --- Main RavenOS and apps ---
class PlayerStats:
    def __init__(self):
        self.name = "User123"
        self.level = 15
        self.experience = 1200
        self.health = 85
        self.strength = 40
        self.intelligence = 50
        self.money = 300000
        self.crypto = 2.345

    def update_stats(self, name, level, money, crypto):
        self.name = name
        self.level = level
        self.money = money
        self.crypto = crypto

class RavenOS:
    def __init__(self, root, player_stats):
        self.root = root
        self.root.title("RavenOS Desktop")
        self.root.geometry("1024x600")
        self.root.configure(bg="#1e1e1e")

        self.player_stats = player_stats  # Store player stats

        # Desktop area where all fake windows will appear
        self.desktop_area = tk.Frame(self.root, bg="#1e1e1e")
        self.desktop_area.pack(fill="both", expand=True)

        # Taskbar at the bottom
        self.taskbar = tk.Frame(self.root, bg="#333", height=40)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.taskbar, text="Terminal", bg="#555", fg="white", command=self.open_terminal).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.taskbar, text="Profile", bg="#555", fg="white", command=self.open_profile).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.taskbar, text="Dev Tools", bg="#555", fg="white", command=self.open_dev_tools).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.taskbar, text="Local Servers", bg="#555", fg="white", command=self.open_local_servers).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.taskbar, text="Shop", bg="#555", fg="white", command=self.open_shop).pack(side=tk.LEFT, padx=5, pady=5)

        self.create_desktop_icons()

    def create_desktop_icons(self):
        # Placeholder for desktop icons
        pass

    def open_terminal(self):
        Terminal(self.desktop_area, self.player_stats)

    def open_profile(self):
        Profile(self.desktop_area, self.player_stats)

    def open_dev_tools(self):
        DevTools(self.desktop_area, self.player_stats)

    def open_local_servers(self):
        LocalServers(self.desktop_area)

    def open_shop(self):
        ShopWindow(self.desktop_area, self.player_stats)

class ShopWindow:
    def __init__(self, parent, player_stats):
        self.window = FakeWindow(parent, title="Shop", width=500, height=400, x=100, y=100)
        self.player_stats = player_stats

        self.items = {
            "Health Potion": (50, "Restores 25 health."),
            "Sword": (200, "Increases strength by 10."),
            "Shield": (150, "Provides extra defense."),
            "Crypto Booster": (500, "Increases crypto holdings by 0.1 BTC.")
        }

        left_frame = tk.Frame(self.window.content, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.window.content, bg="#1e1e1e")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.items_listbox = tk.Listbox(left_frame, bg="#333", fg="white", font=("Courier", 12))
        self.items_listbox.pack(fill=tk.BOTH, expand=True)
        for item in self.items:
            price = self.items[item][0]
            self.items_listbox.insert(tk.END, f"{item} - ${price}")
        self.items_listbox.bind("<<ListboxSelect>>", self.show_item_details)

        self.item_name_label = tk.Label(right_frame, text="Item:", fg="white", bg="#1e1e1e", font=("Courier", 12))
        self.item_name_label.pack(anchor="w")
        self.price_label = tk.Label(right_frame, text="Price:", fg="white", bg="#1e1e1e", font=("Courier", 12))
        self.price_label.pack(anchor="w")
        self.description_label = tk.Label(right_frame, text="Description:", fg="white", bg="#1e1e1e", font=("Courier", 12), wraplength=200, justify="left")
        self.description_label.pack(anchor="w", pady=(0,10))

        self.buy_button = tk.Button(right_frame, text="Buy", bg="#555", fg="white", command=self.buy_item)
        self.buy_button.pack(pady=5)
        self.info_label = tk.Label(right_frame, text="", fg="white", bg="#1e1e1e", font=("Courier", 10))
        self.info_label.pack(pady=5)

    def show_item_details(self, event):
        selection = self.items_listbox.curselection()
        if selection:
            item_text = self.items_listbox.get(selection)
            item_name = item_text.split(" - $")[0]
            price, description = self.items[item_name]
            self.item_name_label.config(text=f"Item: {item_name}")
            self.price_label.config(text=f"Price: ${price}")
            self.description_label.config(text=f"Description: {description}")
            self.info_label.config(text="")

    def buy_item(self):
        selection = self.items_listbox.curselection()
        if selection:
            item_text = self.items_listbox.get(selection)
            item_name = item_text.split(" - $")[0]
            price, description = self.items[item_name]
            if self.player_stats.money >= price:
                self.player_stats.money -= price
                self.info_label.config(text=f"Purchased {item_name} for ${price}!")
            else:
                self.info_label.config(text="Insufficient funds!")
        else:
            self.info_label.config(text="Select an item first.")

class Profile:
    def __init__(self, parent, player_stats):
        self.window = FakeWindow(parent, title="Profile", width=400, height=400, x=150, y=150)
        self.player_stats = player_stats
        profile_text = self.get_profile_text()
        self.profile_info = tk.Label(self.window.content, text=profile_text, fg="white", bg="#1e1e1e",
                                     font=("Courier", 10), justify=tk.LEFT)
        self.profile_info.pack(pady=20)

    def get_profile_text(self):
        xp_needed = self.calculate_xp_to_next_level()
        profile_text = f"""
█████████████████████████████████████████████
█  Player Name: {self.player_stats.name:<20} 
█  Level: {self.player_stats.level:<27} 
█  Experience: {self.player_stats.experience:<17} 
█  XP to Next Level: {xp_needed:<13} 
█  Health: {self.player_stats.health:<21} 
█  Strength: {self.player_stats.strength:<19} 
█  Intelligence: {self.player_stats.intelligence:<14} 
█████████████████████████████████████████████

Crypto Holdings:
---------------------
█  Bitcoin (BTC): {self.player_stats.crypto:<15} 
█  Ethereum (ETH): {self.player_stats.crypto * 2:<15} 
█  Litecoin (LTC): {self.player_stats.crypto * 0.5:<15} 
█████████████████████████████████████████████

Money: ${self.player_stats.money}
        """
        return profile_text

    def calculate_xp_to_next_level(self):
        xp_per_level = 1000
        xp_needed = (self.player_stats.level + 1) * xp_per_level - self.player_stats.experience
        return xp_needed if xp_needed > 0 else 0

class DevTools:
    def __init__(self, parent, player_stats):
        self.window = FakeWindow(parent, title="Dev Tools", width=300, height=400, x=200, y=200)
        self.player_stats = player_stats

        tk.Label(self.window.content, text="Set Player Name:", fg="white", bg="#1e1e1e").pack(pady=5)
        self.name_entry = tk.Entry(self.window.content, bg="#333", fg="white")
        self.name_entry.insert(tk.END, self.player_stats.name)
        self.name_entry.pack(pady=5)

        tk.Label(self.window.content, text="Set Player Level:", fg="white", bg="#1e1e1e").pack(pady=5)
        self.level_entry = tk.Entry(self.window.content, bg="#333", fg="white")
        self.level_entry.insert(tk.END, str(self.player_stats.level))
        self.level_entry.pack(pady=5)

        tk.Label(self.window.content, text="Set Player Money ($):", fg="white", bg="#1e1e1e").pack(pady=5)
        self.money_entry = tk.Entry(self.window.content, bg="#333", fg="white")
        self.money_entry.insert(tk.END, str(self.player_stats.money))
        self.money_entry.pack(pady=5)

        tk.Label(self.window.content, text="Set Player Crypto (BTC):", fg="white", bg="#1e1e1e").pack(pady=5)
        self.crypto_entry = tk.Entry(self.window.content, bg="#333", fg="white")
        self.crypto_entry.insert(tk.END, str(self.player_stats.crypto))
        self.crypto_entry.pack(pady=5)

        tk.Button(self.window.content, text="Save Stats", bg="#555", fg="white", command=self.save_stats).pack(pady=10)

    def save_stats(self):
        name = self.name_entry.get()
        level = int(self.level_entry.get())
        money = float(self.money_entry.get())
        crypto = float(self.crypto_entry.get())
        self.player_stats.update_stats(name, level, money, crypto)
        self.window.destroy()
        Profile(self.window.master, self.player_stats)

class LocalServers:
    def __init__(self, parent):
        self.window = FakeWindow(parent, title="Local Servers", width=600, height=400, x=100, y=100)
        self.window.configure(bg="#1e1e1e")
        self.server_notes = {}

        left_frame = tk.Frame(self.window.content, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.server_listbox = tk.Listbox(left_frame, bg="#333", fg="white", font=("Courier", 12))
        self.server_listbox.pack(fill=tk.BOTH, expand=True)
        self.servers = [f"Server {i}: {random.choice(['Flux', 'Byte', 'Vortex', 'Neon', 'Delta', 'Grid', 'Matrix', 'Core', 'Quantum'])}" for i in range(1, 11)]
        for server in self.servers:
            self.server_listbox.insert(tk.END, server)
        self.server_listbox.bind("<<ListboxSelect>>", self.load_notes)

        right_frame = tk.Frame(self.window.content, bg="#1e1e1e")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(right_frame, text="Server Notes:", fg="white", bg="#1e1e1e", font=("Courier", 12)).pack(anchor="w")
        self.notes_text = tk.Text(right_frame, height=10, bg="#333", fg="white", font=("Courier", 10))
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        tk.Button(right_frame, text="Save Note", bg="#555", fg="white", command=self.save_note).pack(pady=5)
        tk.Button(right_frame, text="Connect", bg="#555", fg="white", command=self.connect_to_server).pack(pady=5)

    def load_notes(self, event):
        selection = self.server_listbox.curselection()
        if selection:
            server_name = self.server_listbox.get(selection)
            note = self.server_notes.get(server_name, "")
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(tk.END, note)

    def save_note(self):
        selection = self.server_listbox.curselection()
        if selection:
            server_name = self.server_listbox.get(selection)
            note = self.notes_text.get(1.0, tk.END).strip()
            self.server_notes[server_name] = note

    def connect_to_server(self):
        selection = self.server_listbox.curselection()
        if selection:
            server_name = self.server_listbox.get(selection)
            ServerTerminal(self.window.content, server_name)

class ServerTerminal:
    def __init__(self, parent, server_name):
        self.server_name = server_name
        self.window = FakeWindow(parent, title=f"Server Terminal - {server_name}", width=600, height=400, x=50, y=50)
        self.window.configure(bg="black")

        self.output_text = scrolledtext.ScrolledText(self.window.content, width=70, height=15, wrap=tk.WORD,
                                                      state=tk.DISABLED, bg="black", fg="white", font=("Courier", 10))
        self.output_text.pack(pady=10)
        self.input_box = tk.Entry(self.window.content, width=70, font=("Courier", 10))
        self.input_box.pack(pady=10)

        self.command_history = []
        self.history_index = -1

        self.input_box.bind("<Return>", self.execute_command)
        self.input_box.bind("<Up>", self.navigate_history_up)
        self.input_box.bind("<Down>", self.navigate_history_down)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"Welcome to the server terminal for {server_name}\n")
        self.output_text.config(state=tk.DISABLED)

    def execute_command(self, event=None):
        command = self.input_box.get()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"> {command}\n")
        self.output_text.yview(tk.END)
        self.input_box.delete(0, tk.END)
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.output_text.insert(tk.END, f"Executed: {command}\n")
        self.output_text.config(state=tk.DISABLED)

    def navigate_history_up(self, event=None):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_box.delete(0, tk.END)
            self.input_box.insert(tk.END, self.command_history[self.history_index])

    def navigate_history_down(self, event=None):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_box.delete(0, tk.END)
            self.input_box.insert(tk.END, self.command_history[self.history_index])

class Terminal:
    def __init__(self, parent, player_stats):
        self.player_stats = player_stats
        self.window = FakeWindow(parent, title="RavenOS Terminal", width=600, height=400, x=20, y=20)
        self.window.configure(bg="black")

        self.output_text = scrolledtext.ScrolledText(self.window.content, width=70, height=15, wrap=tk.WORD,
                                                      state=tk.DISABLED, bg="black", fg="white", font=("Courier", 10))
        self.output_text.pack(pady=10)
        self.input_box = tk.Entry(self.window.content, width=70, font=("Courier", 10))
        self.input_box.pack(pady=10)

        self.command_history = []
        self.history_index = -1

        self.files = {
            "file1.txt": "This is the content of file1.txt.",
            "file2.txt": "This is the content of file2.txt.",
            "secrets.txt": "Confidential data. Top secret information!"
        }
        self.directories = ["docs", "downloads", "images"]

        self.input_box.bind("<Return>", self.execute_command)
        self.input_box.bind("<Up>", self.navigate_history_up)
        self.input_box.bind("<Down>", self.navigate_history_down)

    def execute_command(self, event=None):
        user_input = self.input_box.get()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"> {user_input}\n")
        self.output_text.yview(tk.END)
        self.input_box.delete(0, tk.END)
        self.command_history.append(user_input)
        self.history_index = len(self.command_history)

        if user_input == "help":
            self.output_text.insert(tk.END, 
                "Available commands:\n"
                "- help                : Show this help message\n"
                "- exit                : Close the terminal\n"
                "- ls                  : List files and directories\n"
                "- cat <filename>      : Display file content\n"
                "- mkdir <dir>         : Create a directory\n"
                "- rm <filename>       : Remove a file\n"
                "- cp <source> <dest>   : Copy a file\n"
                "- mv <source> <dest>   : Move a file\n"
                "- clear / cls         : Clear the terminal\n"
                "- echo <text>         : Echo the input text\n"
                "- date                : Show current date and time\n"
                "- calc <expression>   : Evaluate an arithmetic expression\n"
                "- fortune             : Show a random fortune\n"
                "- random              : Output a random number (1-100)\n"
                "- weather             : Show a dummy weather message\n"
                "- whoami              : Show your username\n"
                "- pwd                 : Show current directory\n"
                "- about               : Show terminal version info\n"
                "\n")
        elif user_input == "exit":
            self.window.destroy()
        elif user_input in ("clear", "cls"):
            self.output_text.delete(1.0, tk.END)
        elif user_input == "ls":
            self.list_files_and_dirs()
        elif user_input.startswith("cat "):
            self.display_file_content(user_input)
        elif user_input.startswith("mkdir "):
            self.create_directory(user_input)
        elif user_input.startswith("rm "):
            self.remove_file(user_input)
        elif user_input.startswith("cp "):
            self.copy_file(user_input)
        elif user_input.startswith("mv "):
            self.move_file(user_input)
        elif user_input.startswith("echo "):
            self.output_text.insert(tk.END, user_input[5:] + "\n")
        elif user_input == "date":
            now = datetime.datetime.now()
            self.output_text.insert(tk.END, now.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        elif user_input.startswith("calc "):
            expr = user_input[5:]
            try:
                result = eval(expr, {"__builtins__": None}, {})
                self.output_text.insert(tk.END, str(result) + "\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
        elif user_input == "fortune":
            fortunes = ["You will have a great day!", "Beware of unexpected events.", "Today is your lucky day!", "Something amazing is about to happen.", "Patience is a virtue."]
            self.output_text.insert(tk.END, random.choice(fortunes) + "\n")
        elif user_input == "random":
            self.output_text.insert(tk.END, str(random.randint(1, 100)) + "\n")
        elif user_input == "weather":
            self.output_text.insert(tk.END, "The weather is sunny with a chance of code!\n")
        elif user_input == "whoami":
            self.output_text.insert(tk.END, f"You are {self.player_stats.name}\n")
        elif user_input == "pwd":
            self.output_text.insert(tk.END, "C:\\RavenOS\n")
        elif user_input == "about":
            self.output_text.insert(tk.END, "RavenOS Terminal v1.0\n")
        else:
            self.output_text.insert(tk.END, "Command not recognized. Type 'help' for a list of commands.\n")

        self.output_text.config(state=tk.DISABLED)

    def navigate_history_up(self, event=None):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_box.delete(0, tk.END)
            self.input_box.insert(tk.END, self.command_history[self.history_index])

    def navigate_history_down(self, event=None):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_box.delete(0, tk.END)
            self.input_box.insert(tk.END, self.command_history[self.history_index])

    def list_files_and_dirs(self):
        output = "Files and directories:\n"
        for file in self.files:
            output += f"- {file}\n"
        for dir in self.directories:
            output += f"DIR: {dir}/\n"
        self.output_text.insert(tk.END, output)

    def display_file_content(self, user_input):
        filename = user_input.split(" ")[1]
        if filename in self.files:
            self.output_text.insert(tk.END, f"{self.files[filename]}\n")
        else:
            self.output_text.insert(tk.END, f"File '{filename}' not found.\n")

    def create_directory(self, user_input):
        dir_name = user_input.split(" ")[1]
        if dir_name not in self.directories:
            self.directories.append(dir_name)
            self.output_text.insert(tk.END, f"Directory '{dir_name}' created.\n")
        else:
            self.output_text.insert(tk.END, f"Directory '{dir_name}' already exists.\n")

    def remove_file(self, user_input):
        filename = user_input.split(" ")[1]
        if filename in self.files:
            del self.files[filename]
            self.output_text.insert(tk.END, f"File '{filename}' deleted.\n")
        else:
            self.output_text.insert(tk.END, f"File '{filename}' not found.\n")

    def copy_file(self, user_input):
        parts = user_input.split(" ")
        source, dest = parts[1], parts[2]
        if source in self.files:
            self.files[dest] = self.files[source]
            self.output_text.insert(tk.END, f"File '{source}' copied to '{dest}'.\n")
        else:
            self.output_text.insert(tk.END, f"File '{source}' not found.\n")

    def move_file(self, user_input):
        parts = user_input.split(" ")
        source, dest = parts[1], parts[2]
        if source in self.files:
            self.files[dest] = self.files.pop(source)
            self.output_text.insert(tk.END, f"File '{source}' moved to '{dest}'.\n")
        else:
            self.output_text.insert(tk.END, f"File '{source}' not found.\n")

def main():
    player_stats = PlayerStats()
    root = tk.Tk()
    app = RavenOS(root, player_stats)
    root.mainloop()

if __name__ == "__main__":
    main()