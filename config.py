import winsound
import threading
import os
from pathlib import Path
from pypdf import PdfReader
import docx
import inspect

class Chimes:
    @staticmethod
    def chime1():
        t1 = threading.Thread(target=winsound.Beep, args=(988, 250))
        t1.start()
        t1.join()

    @staticmethod
    def chime2():
        t2 = threading.Thread(target=winsound.Beep, args=(1976, 250))
        t2.start()
        t2.join()

    @classmethod
    def input_chime(cls):
        if not "AS_SUBPROCESS" in os.environ:
            cls.chime1()

    @classmethod
    def progress_chime(cls):
        if not "AS_SUBPROCESS" in os.environ:
            cls.chime2()
            cls.chime1()

    @classmethod
    def ending_chime(cls):
        cls.chime1()
        cls.chime2()

    @classmethod
    def terminal_chime(cls):
        cls.chime2()
        cls.chime1()
        cls.ending_chime()


def printss(string):
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    if not "AS_SUBPROCESS" in os.environ or  caller_module.__name__ == "task_manager.py": 
        print("\n----" + string + "----")


def extract_text_from_dir(path, setup_instruction="Run setup.py and follow the instructions as given."):
    if not (path.exists() and path.is_dir()):
        raise FileNotFoundError(f"The {path} directory does not exist.\n{setup_instruction}")
        
    combined_text = ""
    files_found = False

    # Process PDF Files
    for pdf_path in path.glob("*.pdf"):
        files_found = True
        sep = "-" * 20
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    combined_text += extracted + sep
        except Exception as e:
            print(f"Error reading PDF {pdf_path.name}: {e}")

    # Process TXT Files
    for txt_path in path.glob("*.txt"):
        files_found = True
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                combined_text += f.read() + sep
        except Exception as e:
            print(f"Error reading TXT {txt_path.name}: {e}")

    # Process DOCX Files
    for docx_path in path.glob("*.docx"):
        # Ignore temporary/lock files Word creates (e.g., ~$document.docx)
        if docx_path.name.startswith("~$"):
            continue
            
        files_found = True
        try:
            doc = docx.Document(docx_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            combined_text += "\n".join(full_text) + sep
        except Exception as e:
            print(f"Error reading DOCX {docx_path.name}: {e}")

    # If the folder was empty or lacked supported files
    if not files_found:
        raise FileNotFoundError(f"No supported files (.pdf, .txt, .docx) found in the {path} directory.")

    return combined_text

def nsep(*args):
    """
    Takes a variable number of arguments (or an unpacked list/tuple)
    and joins them into a string separated by newlines.
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        items = args[0]
    else:
        items = args
    return "\n".join(str(item) for item in args)    

def load_resume():
    path = Path("data/resume")
    return extract_text_from_dir(path)

def load_writing_samples():
    path = Path("data/writing_samples")
    return extract_text_from_dir(path)
