import subprocess
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import webbrowser
import pathlib
import threading
import queue
import json
import google.generativeai as genai
import logging
import base64  # Basic encryption

# Logging setup
logging.basicConfig(filename='gemini_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def install_python_if_needed():
    try:
        subprocess.run(["python", "--version"], check=True)
        logging.info("Python is already installed.")
        return True
    except subprocess.CalledProcessError:
        logging.warning("Python is not installed.")
        if os.name == 'nt':
            import urllib.request
            url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
            filename = "python-installer.exe"
            urllib.request.urlretrieve(url, filename)
            subprocess.run([filename, "/quiet", "InstallAllUsers=1", "Include_test=0", "Shortcuts=0", "Include_doc=0", "Include_pip=1", "PrependPath=1", "Include_tcltk=1"], check=True)
            os.remove(filename)
            logging.info("Python installed successfully. Please restart the script.")
            messagebox.showinfo("Python Installed", "Python installed successfully. Please restart the application.")
            return False
        else:
            messagebox.showinfo("Python Installation", "Please install Python 3.11.8 manually.")
            logging.error("Python installation is not automated for this OS.")
            return False

def create_virtual_environment():
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        logging.info("Virtual environment created.")
        return True
    except Exception as e:
        logging.error(f"Error creating virtual environment: {e}")
        return False

def install_dependencies():
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    try:
        result_upgrade = subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True, capture_output=True, text=True)
        logging.info(f"Pip upgrade output: {result_upgrade.stdout}")
        logging.info(f"Pip upgrade errors: {result_upgrade.stderr}")
        result_install = subprocess.run([venv_python, "-m", "pip", "install", "google-generativeai", "tkinter"], check=True, capture_output=True, text=True)
        logging.info(f"Install output: {result_install.stdout}")
        logging.info(f"Install errors: {result_install.stderr}")
        logging.info("Dependencies installed.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing dependencies: {e}")
        logging.error(f"Command output: {e.stdout}")
        logging.error(f"Command errors: {e.stderr}")
        return False

def encrypt_api_key(api_key):
    return base64.b64encode(api_key.encode()).decode()

def decrypt_api_key(encrypted_api_key):
    return base64.b64decode(encrypted_api_key.encode()).decode()

def load_api_key():
    try:
        with open("api_key.txt", "r") as f:
            return decrypt_api_key(f.read().strip())
    except FileNotFoundError:
        return None

def save_api_key(api_key):
    with open("api_key.txt", "w") as f:
        f.write(encrypt_api_key(api_key))

def run_application():
    try:
        API_KEY = load_api_key()
        if not API_KEY:
            import tkinter.simpledialog
            root = tk.Tk()
            root.withdraw()
            API_KEY = tkinter.simpledialog.askstring("API Key", "Enter your Gemini API key:")
            if not API_KEY:
                return
            save_api_key(API_KEY)
            root.destroy()
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        conversation_history = []
        execution_running = False

        def run_command(command, result_queue, cancel_flag):
            try:
                process = subprocess.Popen(['python', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
                while process.poll() is None:
                    if cancel_flag[0]:
                        process.terminate()
                        result_queue.put("Execution cancelled.")
                        return
                    stdout, stderr = process.communicate()
                    result_queue.put(f"Stdout: {stdout}\nStderr: {stderr}")
                stdout, stderr = process.communicate()
                result_queue.put(f"Stdout: {stdout}\nStderr: {stderr}")
            except subprocess.TimeoutExpired:
                result_queue.put("Command timed out.")
            except Exception as e:
                result_queue.put(f"Error: {e}")

        def generate_and_execute():
            nonlocal execution_running
            prompt = prompt_entry.get("1.0", tk.END).strip()
            if not prompt:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Please enter a prompt.")
                return

            if "search:" in prompt.lower():
                search_query = prompt.lower().replace("search:", "").strip()
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Search opened in browser.")
                return

            if "execute:" in prompt.lower():
                code = prompt.lower().replace("execute:", "").strip()
                result_queue = queue.Queue()
                cancel_flag = [False]
                execution_running = True
                cancel_button.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Executing...\n")

                thread = threading.Thread(target=run_command, args=(code, result_queue, cancel_flag))
                thread.start()

                def cancel_execution():
                    cancel_flag[0] = True
                    cancel_button.config(state=tk.DISABLED)

                cancel_button.config(command=cancel_execution)

                def update_result():
                    if not result_queue.empty():
                        result = result_queue.get()
                        result_text.insert(tk.END, result)
                        if not thread.is_alive():
                            nonlocal execution_running
                            execution_running = False
                            cancel_button.config(state=tk.DISABLED)
                    else:
                        root.after(100, update_result)

                update_result()
                return

            if "file:" in prompt.lower():
                filepath = prompt.lower().replace("file:", "").strip()
                try:
                    filepath = pathlib.Path(filepath).resolve()
                    if not str(filepath).startswith(str(pathlib.Path().resolve())):
                        result_text.delete("1.0", tk.END)
                        messagebox.showerror("File Access Denied", "File access outside of current directory is denied.")
                        return
                    with open(filepath, "r") as f:
                        file_contents = f.read()
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, file_contents)
                except FileNotFoundError:
                    messagebox.showerror("File Not Found", "The specified file does not exist.")
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, "File not found.")
                except Exception as e:
                    messagebox.showerror("File Error", f"An error occurred: {e}")
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, f"Error: {e}")
                return

            try:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "Generating response...\n")
                response = model.generate_content(prompt)
                result_text.insert(tk.END, response.text)
                conversation_history.append({"prompt": prompt, "response": response.text})
            except Exception as e:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Error: {e}")
                logging.error(f"Gemini API error: {e}")
                messagebox.showerror("Gemini Error", f"An error occurred: {e}")

        def open_file_dialog():
            filepath = filedialog.askopenfilename()
            if filepath:
                prompt_entry.insert(tk.END, f"file:{filepath}")

        def save_conversation():
            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filepath:
                with open(filepath, "w") as f:
                    json.dump(conversation_history, f)

        def load_conversation():
            nonlocal conversation_history
            filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if filepath:
                try:
                    with open(filepath, "r") as f:
                        conversation_history = json.load(f)
                    result_text.delete("1.0", tk.END)
                    for item in conversation_history:
                        result_text.insert(tk.END, f"Prompt: {item['prompt']}\nResponse: {item['response']}\n\n")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not load conversation: {e}")

        root = tk.Tk()
        root.title("Gemini Desktop Client")
        prompt_label = tk.Label(root, text="Enter Prompt:")
        prompt_label.pack()
        prompt_entry = scrolledtext.ScrolledText(root, height=10, width=80)
        prompt_entry.pack()
        generate_button = tk.Button(root, text="Generate/Execute", command=generate_and_execute)
        generate_button.pack()
        file_button = tk.Button(root, text="Open File", command=open_file_dialog)
        file_button.pack()
        cancel_button = tk.Button(root, text="Cancel Execution", state=tk.DISABLED)
        cancel_button.pack()
        save_button = tk.Button(root, text="Save Conversation", command=save_conversation)
        save_button.pack()
        load_button = tk.Button(root, text="Load Conversation", command=load_conversation)
        load_button.pack()
        result_text = scrolledtext.ScrolledText(root, height=20, width=80)
        result_text.pack()
        root.mainloop()

    except Exception as e:
        print(f"Application error: {e}")
        logging.critical(f"Application crash: {e}")

if install_python_if_needed():
    if create_virtual_environment():
        if install_dependencies():
            run_application()
        else:
            logging.error("Dependency installation failed.")
            print("Dependency installation failed.")
    else:
        logging.error("Virtual environment creation failed.")
        print("Virtual environment creation failed.")
else:
    logging.error("Python installation check failed.")
    print("Python installation check failed.")