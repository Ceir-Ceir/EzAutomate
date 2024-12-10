from Job_Matcher import match_jobs_to_users
from Resume_Generator import generate_resume
from Job_App_Bot import apply_to_job

matches = match_jobs_to_users()

for user, job in matches:
    resume_text = generate_resume(user, job)
    resume_path = f"resumes/{user['name']}_{job['title']}.txt"
    with open(resume_path, "w") as f:
        f.write(resume_text)

    # Apply to the matched job
    apply_to_job(job, user, resume_path)
