import os
import random

names = [
    "John Smith","Alice Johnson","Michael Brown","Emma Davis","David Wilson",
    "Sophia Taylor","Daniel Anderson","Olivia Thomas","James Moore","Isabella Martin",
    "Ethan Jackson","Mia White","Alexander Harris","Charlotte Clark","Benjamin Lewis",
    "Amelia Walker","Lucas Hall","Harper Allen","Henry Young","Evelyn King",
    "Jack Wright","Abigail Scott","Samuel Green","Emily Baker","Matthew Adams",
    "Ella Nelson","Joseph Hill","Avery Carter","Andrew Mitchell","Scarlett Perez"
]

skills_pool = [
    "Python","Machine Learning","SQL","AWS","Docker",
    "TensorFlow","Deep Learning","Data Science","Java","Kubernetes"
]

educations = [
    "B.Tech Computer Science",
    "M.Tech Artificial Intelligence",
    "MS Data Science",
    "B.Sc Software Engineering"
]

os.makedirs("resumes", exist_ok=True)

for i, name in enumerate(names):

    skills = random.sample(skills_pool, 3)

    experience = random.randint(2,10)

    education = random.choice(educations)

    resume = f"""
{name}

Skills
{skills[0]}
{skills[1]}
{skills[2]}

Experience
{experience} years experience in software development and AI systems.

Education
{education}
"""

    with open(f"resumes/resume{i+1}.txt", "w") as f:
        f.write(resume)

print("30 resumes generated successfully.")