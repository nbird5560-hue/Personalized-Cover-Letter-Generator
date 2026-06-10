from scraper import get_job_description
from pick import pick
from config import Chimes

def load_job_description():
    Chimes.input_chime()
    options = ["url (LinkedIn, Indeed, Simplify)", "paste description into terminal"]
    selected, index = pick(options, "Chose Job Description")
    match index:
        case 0:
            return get_job_description()
        case 1:
            text = input("Paste description into terminal")
            if not text:
                raise ChildProcessError("Invalid input") 
            else:
                return text
