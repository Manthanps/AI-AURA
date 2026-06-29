import os
import shutil
import webbrowser
import json

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def create_folder(name):
    os.makedirs(name, exist_ok=True)
    return f"Folder '{name}' created"

def delete_folder(name):
    shutil.rmtree(name)
    return f"Folder '{name}' deleted"

def create_file(name):
    open(name, "w").close()
    return f"File '{name}' created"

def delete_file(name):
    os.remove(name)
    return f"File '{name}' deleted"

def open_website(site):
    memory = load_memory()

    if site in memory:
        browser = memory[site]
        print(f"Opening {site} in your preferred browser: {browser}")
    else:
        browser = input(f"Which browser should I use for {site}? ")
        memory[site] = browser
        save_memory(memory)

    url = f"https://www.google.com/search?q={site}"
    webbrowser.open(url)
    return f"Opened {site}"
