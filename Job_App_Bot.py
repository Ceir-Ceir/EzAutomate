from playwright.sync_api import sync_playwright
import os

def apply_to_job(job, user, resume_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless
        page = browser.new_page()

        # Navigate to job application URL
        page.goto(job['url'])

        # Fill in application fields
        page.fill('input[name="name"]', user['name'])
        page.fill('input[name="email"]', user['email'])
        page.fill('input[name="phone"]', user['phone'])

        # Upload resume
        page.set_input_files('input[type="file"]', resume_path)

        # Submit the form
        page.click('button[type="submit"]')

        # Log application success or failure
        print(f"Application submitted for {user['name']} to {job['title']} at {job['company']}")

        browser.close()
