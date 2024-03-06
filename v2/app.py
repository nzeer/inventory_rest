import os
import glob

from flask import Flask, render_template

app = Flask(__name__)

# Directory where Ansible inventory files are stored
INVENTORY_DIR = "/inventory/arch/"

def glob_files(location: str = "/inventory", file_extension: str = "*.list", is_recursive: bool = True) -> set:
    """
    Search for files with a specific file extension in a given location.

    Args:
        location (str, optional): The location to search for files. Defaults to "./".
        file_extension (str, optional): The file extension to match. Defaults to "*.list".
        is_recursive (bool, optional): Whether to search recursively in subdirectories. Defaults to True.

    Returns:
        set: A set of file paths matching the given criteria.
    """
    glob_listfiles_path = "%s/**/%s" % (location, file_extension)
    return set(glob.glob(glob_listfiles_path, recursive=is_recursive))

def read_inventory(inv_dir: str = INVENTORY_DIR):
    files:list = glob_files()
    print(f"Files: {files}")
    inventory: dict = {}
    if not inv_dir or not os.path.isdir(inv_dir):
        return inventory
    
    try:
        for filepath in files:
            if not os.path.isfile(filepath):
                raise Exception(f"File {filepath} is not a file.")
            
            print(f"Reading inventory file: {filepath}")
            with open(filepath, "r") as file:
                section:str = None
                for line in file:
                    line = line.strip()
                    print(f"Line: {line}")
                    if line.startswith("[") and line.endswith("]"):
                        section = line[1:-1]
                        print(f"Section: {section}")
                        if ":" in section:
                            section, subsection = section.split(":", 1)
                            print(f"Subsection: {section}\nSubsection: {subsection}")
                            if section not in inventory:
                                print(f"Creating Section as dict: {section}")
                                inventory[section] = {}
                            print(f"Creating Subsection as list: {subsection}")
                            inventory[section][subsection] = []
                        else:
                            print(f"Creating Section as list: {section}")
                            inventory[section] = []
                    elif section and line:
                        if ":" in section:
                            print(f"Appending {line} to Subsection: {section}")
                            inventory[section][subsection].append(line)
                        else:
                            print(f"Appending {line} to Section: {section}")
                            try:
                                inventory[section].append(line)
                            except:
                                print(f"Appending {line} to Subsection: {section}")
                                inventory[section][subsection].append(line)
    except Exception as e:
        print(f"Error reading inventory: {e}\n")
        print(f"Inventory: {inventory}")
    return inventory


@app.route("/")
def index():
    inventory = read_inventory(INVENTORY_DIR)
    return render_template("index.html", inventory=inventory)


"""if __name__ == "__main__":
    DICT_HOSTS = load_hosts_csv(HOSTS_CSV)
    app.run(host='0.0.0.0', port=5000, debug=True)"""
