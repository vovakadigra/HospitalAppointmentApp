import pandas as pd
import random

# Define the survey questions
questions = [
    "1. How many years of experience do you have as a doctor?",
    "2. Have you published any research papers? If yes, please provide details.",
    "3. How often do you attend medical conferences to update your knowledge and skills?",
    "4. Do you engage in teaching or mentoring activities? If yes, please provide details.",
    "5. On a scale of 1-10, rate your overall performance as a doctor.",
    "6. Have you received positive feedback or testimonials from patients or colleagues?",
    "7. Are you involved in any medical committees or professional organizations?"
]

# Create a dictionary for autofill values
autofill_values = {
    "years_of_experience": [1, 2, 3, 4, 5],
    "research_papers": ["Yes", "No"],
    "conference_attendance": ["Never", "Rarely", "Sometimes", "Frequently", "Always"],
    "teaching_mentoring": ["Yes", "No"],
    "performance_rating": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "feedback_testimonials": ["Yes", "No"],
    "committees_organizations": ["Yes", "No"]
}

# Generate the surveys and assign salary_bonus_decision
num_surveys = 100000 # Number of surveys to generate

generated_surveys = []

for _ in range(num_surveys):
    # Generate random survey answers
    answers = [
        random.choice(autofill_values["years_of_experience"]),
        random.choice(autofill_values["research_papers"]),
        random.choice(autofill_values["conference_attendance"]),
        random.choice(autofill_values["teaching_mentoring"]),
        random.choice(autofill_values["performance_rating"]),
        random.choice(autofill_values["feedback_testimonials"]),
        random.choice(autofill_values["committees_organizations"])
    ]

    # Calculate the score for question 1
    q1_score = 0
    if answers[0] in [1, 2, 3]:
        q1_score = 0.25
    elif answers[0] in [4, 5]:
        q1_score = 0.5

    # Calculate the score for question 2
    q2_score = 1 if answers[1] == "Yes" else 0

    # Calculate the score for question 3
    q3_score = 0
    if answers[2] == "Never":
        q3_score = 0
    elif answers[2] == "Rarely":
        q3_score = 0.25
    elif answers[2] == "Sometimes":
        q3_score = 0.5
    elif answers[2] == "Frequently":
        q3_score = 0.75
    elif answers[2] == "Always":
        q3_score = 1

    # Calculate the score for question 4
    q4_score = 1 if answers[3] == "Yes" else 0

    # Calculate the score for question 5
    q5_score = 0
    if answers[4] < 5:
        q5_score = 0
    elif answers[4] == 5:
        q5_score = 1
    elif answers[4] in [6, 7]:
        q5_score = 1.25
    elif answers[4] == 8:
        q5_score = 1.5
    elif answers[4] == 9:
        q5_score = 1.75
    elif answers[4] == 10:
        q5_score = 2

    # Calculate the score for question 6
    q6_score = 1 if answers[5] == "Yes" else 0

    # Calculate the score for question 7
    q7_score = 0.5 if answers[6] == "Yes" else 0

    # Calculate the total score
    total_score = q1_score + q2_score + q3_score + q4_score + q5_score + q6_score + q7_score

    # Assign salary_bonus_decision based on the total score
    salary_bonus_decision = "Yes" if total_score >= 0.64 * 7 else "No"

    # Add the survey data to the list
    generated_surveys.append(answers + [salary_bonus_decision])

# Create a DataFrame from the generated surveys
columns = questions + ["salary_bonus_decision"]
df = pd.DataFrame(generated_surveys, columns=columns)

# Save the DataFrame to a CSV file
df.to_csv("generated_surveys.csv", index=False)
