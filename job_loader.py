from scraper import get_job_description
from pick import pick
from config import Chimes

def load_job_description(link=None):

    if not link:
        Chimes.input_chime()
        options = ["url (LinkedIn, Indeed, Simplify)", "paste description into terminal"]
        selected, index = pick(options, "Chose Job Description")
    else:
        index = 0 
    match index:
        case 0:
            if link:
                return get_job_description(link)
            else:
                return get_job_description()
        case 1:
            text = input("Paste description into terminal")
            if not text:
                raise ChildProcessError("Invalid input") 
            else:
                return text
