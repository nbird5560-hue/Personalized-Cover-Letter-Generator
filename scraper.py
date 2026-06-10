import re
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Import selenium-stealth
from selenium_stealth import stealth

def get_job_description():
    def clean_url(url: str):
        if not isinstance(url, str):
            print("Input is not a string.")
            exit()
            
        # Check for LinkedIn
        if "linkedin.com" in url:
            match = re.search(r"currentJobId=(\d+)", url)
            if match:
                job_id = match.group(1)
                return f"https://www.linkedin.com/jobs/view/{job_id}", "linkedin"
            elif "/jobs/view/" in url:
                return url, "linkedin"
            else:
                print("LinkedIn Job ID not found in URL.")
                exit()
                
        # Check for Indeed
        elif "indeed.com" in url:
            match = re.search(r"[v]?jk=([a-zA-Z0-9]+)", url)
            if match:
                job_id = match.group(1)
                return f"https://www.indeed.com/viewjob?jk={job_id}", "indeed"
            elif "/viewjob" in url:
                return url, "indeed"
            else:
                print("Indeed Job ID (jk or vjk) not found in URL.")
                exit()

        # Check for Simplify
        elif "simplify.jobs" in url:
            match = re.search(r"jobId=([a-zA-Z0-9\-]+)", url)
            if match:
                job_id = match.group(1)
                return f"https://simplify.jobs/p/{job_id}", "simplify"
            elif "/p/" in url:
                return url, "simplify"
            else:
                print("Simplify Job ID not found in URL.")
                exit()
        else:
            print("Unsupported URL. Please provide a LinkedIn, Indeed, or Simplify URL.")
            exit()

    input_url = input("Enter LinkedIn, Indeed, or Simplify URL: ")
    job_url, platform = clean_url(input_url)

    # Anti-anti-scraper methods
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Masquarading as not bot
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    # Selenium-stealth configurations
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        print(f"Navigating to direct job page ({platform}): {job_url}")
        driver.get(job_url)
    
        time.sleep(random.uniform(4.0, 6.0))
    
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        title, company, description = None, None, None
    
        if platform == "linkedin":
            if "login" in driver.current_url or soup.find(id="username"):
                print("Blocked: LinkedIn redirected the headless browser to a login screen.")
                return None
            
            title_element = soup.select_one("h1.top-card-layout__title, h1.topcard__title")
            company_element = soup.select_one(
                'a[data-tracking-control-name="public_jobs_topcard-org-name"], '
                'span.topcard__flavor, a.topcard__flavor, '
                '.top-card-layout__first-subline a, .top-card-layout__first-subline'
            )
            description_element = soup.select_one("div.description__text--rich, div.show-more-less-html__markup")
        
        elif platform == "indeed":
            # Job Title Fallbacks
            title_element = soup.select_one(
                "h1.jobsearch-JobInfoHeader-title, "
                "h1[data-testid='simulated-headline'], "
                "div.jobsearch-JobInfoHeader-title-container h1, "
                "h1.css-1786v9r"
            )
            
            # Company Name Fallbacks
            company_element = soup.select_one(
                "[data-company-name='true'] > a, [data-company-name='true'], "
                "div[data-testid='inlineHeader-companyName'] a, "
                "div[data-testid='inlineHeader-companyName'], "
                ".jobsearch-InlineCompanyRating a, .jobsearch-InlineCompanyRating, "
                "div.css-1ioi40n a"
            )
            
            # Job Description Fallbacks
            description_element = soup.select_one(
                "div#jobDescriptionText, "
                "div.jobsearch-jobDescriptionText, "
                "div[id='jobDescriptionText']"
            )

        elif platform == "simplify":
            page_title = soup.title.get_text(strip=True) if soup.title else ""
            
            if "@" in page_title and "|" in page_title:
                title_part, remaining = page_title.split("@", 1)
                company_part = remaining.split("|")[0]
                
                title = title_part.strip()
                company = company_part.strip()
            else:
                # Fallbacks for on-page elements if structural changes occur
                title_element = soup.select_one("h1, [class*='title']")
                company_element = soup.select_one("[class*='company'], a[href*='/c/']")
                if title_element: title = title_element.get_text(strip=True)
                if company_element: company = company_element.get_text(strip=True)

            # Job Description Fallback selectors based on Simplify's page content
            description_element = soup.select_one(
                "div[class*='description'], "
                "section[class*='description'], "
                "main" # Fallback to core container if classes are obfuscated
            )

        if "title_element" in locals() and not title:
            title = re.sub(r'\s*-\s*job post$', '', title_element.get_text(strip=True), flags=re.IGNORECASE)
            
        if "company_element" in locals() and not company:
            company = company_element.get_text(strip=True)
            
        if "description_element" in locals():
            description = description_element.get_text(separator="\n", strip=True)

        return [description, title, company]

    finally:
        driver.quit()