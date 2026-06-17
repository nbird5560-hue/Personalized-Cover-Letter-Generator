# OVERVIEW:

This tool is designed to help job seekers by analyzing and interpreting the user's writing style, and create personalized cover letters highlighting the intersection of the user's experience/projects and job descriptions provided to the machine. The tool follows a multi-model, multi-pass, pipelined local LLM-driven process, intended to optimize the user's cover letters in the eyes of a prospective hiring manager.

This is a work in progress, and I will continue to update this project to include more features, a front-end, and greater compatabilities. It is my intention to keep this project locally hosted to avoid token credit costs associated with larger commercial LLMs.

# FEATURES:

`·` Supports extracting job descriptions and relevant information from LinkedIn.com, Indeed.com, and simplify.com (more to come).

`·` Supports the upload of multiple tailored résumés, resulting in greater breadth of highlightable skills and cover letter coverage.

`·` Supports automated job link `→` cover letter queuing with custom keybind ctrl + alt + c on highlighted text.

# HOW TO USE:

## Setup:

Upon installation, run setup.py. This script will establish the system's file structure and preform some optimizing data precompilation; populate the "resumes" and "writing_samples" subdirectories under "data" as prompted, then continue through the setup script as instructed.

This will:
`·` Compile any uploaded resumes into a single amalgamation, reducing processing time during usage.
`·` Create a writing style profile for the user, also aimed at reducing processing time.

If the user updates the résumés or writing samples within the projects files, the setup.py structure should be rerun.

## Usage:

This program may be run in one of two ways, writing a standalone cover letter, or initialzing a queue of cover letters to be written in succession.

### Batches of Cover Letters:

Within the context of queued batches cover letters, we will refer to a batch of links (each translating to an individual cover letter) sent to the system as a 'job', and individual links within a job as 'tasks'.

To start, run the 'SaveJobLink.ahk' file in the 'auxiliary' subdirectory (if the AutoHotkey v2 session is not yet initialized from previous use); this enables a custom keybind ctrl + alt + c, which allows the user to send highlighted text directly to the job docket. The user may then skim job sites (LinkedIn, Indeed, Simplify), highlighting job-search platform links (dirty links accepted) and using the custom keybind (ctrl + alt + c) to queue these listings within the job docket.

When the user is satisfied with the contents of then docket, they should run 'task_manager.py' which will load these links from the job docket to an internal queuing system. This initializes the 'job', allowing the user to partition sets of cover letters into output batches. The user will be prompted with a choice of a universal output format (.docx (recommended), .pdf, .txt, at terminal) for cover letter outputs.

Please note that cover letters can safely removed from or changed within the 'output' subdirectory at any time while the job continues with other tasks.

In the case that the prior job was prematurely aborted, uncompleted tasks will not be lost! Upon starting a new job, the user will be prompted as to how they wish to resolve the positioning of the uncompleted tasks within the new job docket.

### Standalone Cover Letter:

Run the 'main.py' script and select your choice of providing a copied job description or url directly to the terminal, then follow through by pasting your respective choice into the terminal. At time of output, you will be prompted with a choice of output format (.docx (recommended), .pdf, .txt, at terminal).

## Outputs:

Outputted cover letters can be found in the 'outputs' subdirectory, and will be named "\[Company_Name\] - \[Role_Title\] - Cover Letter.\[chosen_extension\]" by default. Output files produced from a job will also populate a list of chronologically appended output names sorted in a text file found at "./data/processes/completed.txt", as well as a cleaned link to the job-search page where the application should be submitted.

When processing batches of documents in succession of one another, if completed.txt contains any contents, the user will be asked whether they would like to clear the completed log or not. To clear this log, completed.txt may be manually deleted or may be dynamically updated, even while a job is in progress, by running 'update_completed.py' in another terminal.

## Chime Tones Windows (OS):

Chime tones are used to mark progression through the system's processing, as depending on hardware constraints, each task may take several minutes to complete.

In the case of queued cover letters, Chime tones will mark the completion of a 'task' (completed cover letter) and the completion of the 'job'. A low tone to a high tone will mark the completion of a single cover letter, and a sequence of four tones in the sequence of high `→` low `→` low `→` high will denote the completion of the job.

In the case of a procuding a standalone cover letter, a single low chime marks the need for user input, high tone `→` low tone will indicate progression past computationally intensive processes, and low tone `→` high tone will indicate task completion.
