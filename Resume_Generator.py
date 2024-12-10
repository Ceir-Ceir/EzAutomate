import openai
from datetime import date
from harvard_resume_formatter import (
    HarvardResumeFormatter,
    PersonalInfo,
    Education,
    Experience,
    Leadership,
    Skills,
)

# Set OpenAI API Key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def tailor_experience_with_ai(user_experience, job_description):
    """
    Tailor the 'Experience' section's bullet points to match the job description.
    """
    prompt = f"""
    You are a resume assistant. Rewrite the bullet points below to align with the following job description:
    Job Description: {job_description}
    Current Experience Bullet Points: {user_experience}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip().split("\n")

def generate_resume(user, job):
    """
    Generate a tailored resume using the HarvardResumeFormatter.
    """
    # Create PersonalInfo from user data
    personal_info = PersonalInfo(
        name=user["name"],
        street_address=user["address"]["street"],
        city=user["address"]["city"],
        state=user["address"]["state"],
        zip_code=user["address"]["zip"],
        email=user["email"],
        phone=user["phone"]
    )

    # Initialize the resume formatter
    resume = HarvardResumeFormatter(personal_info)

    # Add education
    for edu in user["education"]:
        resume.add_education(Education(
            institution=edu["institution"],
            location=edu["location"],
            degree=edu["degree"],
            gpa=edu.get("gpa"),
            graduation_date=date.fromisoformat(edu["graduation_date"]),
            relevant_coursework=edu.get("relevant_coursework"),
            additional_info=edu.get("additional_info")
        ))

    # Add experience with tailored bullet points
    for exp in user["experience"]:
        tailored_bullets = tailor_experience_with_ai(exp["description"], job["description"])
        resume.add_experience(Experience(
            company=exp["company"],
            location=exp["location"],
            title=exp["title"],
            start_date=date.fromisoformat(exp["start_date"]),
            end_date=date.fromisoformat(exp["end_date"]),
            description=tailored_bullets
        ))

    # Add leadership
    for lead in user["leadership"]:
        resume.add_leadership(Leadership(
            organization=lead["organization"],
            location=lead["location"],
            title=lead["title"],
            start_date=date.fromisoformat(lead["start_date"]),
            end_date=date.fromisoformat(lead["end_date"]),
            description=lead["description"]
        ))

    # Add skills
    resume.set_skills(Skills(
        technical=user["skills"]["technical"],
        language=user["skills"]["language"],
        interests=user["skills"]["interests"]
    ))

    # Generate formatted resume
    return resume.generate_resume()

def save_resume(resume_text, user, job):
    """
    Save the generated resume to the 'resumes' directory.
    """
    import os
    if not os.path.exists("resumes"):
        os.makedirs("resumes")

    file_name = f"resumes/{user['name']}_{job['title'].replace(' ', '_')}.txt"
    with open(file_name, "w") as f:
        f.write(resume_text)
    
    print(f"Resume saved to {file_name}")

# Example usage
if __name__ == "__main__":
    # Sample user and job data
    user = {
        "name": "John Doe",
        "address": {
            "street": "123 Main Street",
            "city": "Boston",
            "state": "MA",
            "zip": "02115"
        },
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "education": [
            {
                "institution": "Harvard University",
                "location": "Cambridge, MA",
                "degree": "A.B. Honors degree in History",
                "gpa": 3.73,
                "graduation_date": "2024-05-01",
                "relevant_coursework": ["International Political Economics", "European Community"],
                "additional_info": ["Varsity Soccer Team, 20 hours/week."]
            }
        ],
        "experience": [
            {
                "company": "TechCorp",
                "location": "San Francisco, CA",
                "title": "Software Engineer",
                "start_date": "2022-06-01",
                "end_date": "2024-08-01",
                "description": [
                    "Developed web applications using Python and Flask.",
                    "Collaborated with cross-functional teams to deliver scalable solutions."
                ]
            }
        ],
        "leadership": [
            {
                "organization": "Hackathon Club",
                "location": "Cambridge, MA",
                "title": "President",
                "start_date": "2021-09-01",
                "end_date": "2024-05-01",
                "description": [
                    "Organized 10+ hackathons, attracting over 500 participants.",
                    "Secured sponsorships from major tech companies."
                ]
            }
        ],
        "skills": {
            "technical": ["Python", "JavaScript", "SQL"],
            "language": ["English", "Spanish"],
            "interests": ["Chess", "Traveling", "AI Research"]
        }
    }

    job = {
        "title": "Data Scientist",
        "description": "Analyze data trends and build predictive models using Python, SQL, and machine learning tools."
    }

    # Generate and save resume
    tailored_resume = generate_resume(user, job)
    save_resume(tailored_resume, user, job)
