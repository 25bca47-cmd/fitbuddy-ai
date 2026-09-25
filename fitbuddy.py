import os
import json
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from google import genai

app = FastAPI()

# Gemini client
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FitBuddy - AI Fitness Coach</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }

            body {
                background: #07110c;
                color: white;
                min-height: 100vh;
            }

            .container {
                max-width: 1100px;
                margin: auto;
                padding: 25px;
            }

            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 0;
            }

            .logo {
                font-size: 25px;
                font-weight: bold;
                color: #39ff88;
            }

            .badge {
                border: 1px solid #39ff88;
                padding: 8px 14px;
                border-radius: 20px;
                color: #39ff88;
                font-size: 13px;
            }

            .hero {
                text-align: center;
                padding: 90px 15px 70px;
            }

            .hero h1 {
                font-size: 55px;
                line-height: 1.1;
                margin-bottom: 20px;
            }

            .hero h1 span {
                color: #39ff88;
            }

            .hero p {
                color: #aab5ae;
                font-size: 18px;
                max-width: 650px;
                margin: auto;
                line-height: 1.7;
            }

            .btn {
                display: inline-block;
                margin-top: 35px;
                padding: 16px 30px;
                background: #39ff88;
                color: #061009;
                text-decoration: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
            }

            .features {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-top: 30px;
            }

            .feature {
                background: #0d1b13;
                border: 1px solid #1d3526;
                border-radius: 18px;
                padding: 28px;
            }

            .feature h3 {
                color: #39ff88;
                margin-bottom: 10px;
            }

            .feature p {
                color: #9ba79f;
                line-height: 1.6;
            }

            @media(max-width: 700px) {
                .hero h1 {
                    font-size: 40px;
                }

                .features {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>

    <body>
        <div class="container">

            <nav>
                <div class="logo">FitBuddy</div>
                <div class="badge">AI FITNESS COACH</div>
            </nav>

            <section class="hero">
                <h1>Your Personal<br><span>AI Fitness Coach</span></h1>

                <p>
                    Create a personalized 7-day fitness plan using
                    Generative AI based on your goals, body details
                    and workout preferences.
                </p>

                <a href="/form" class="btn">Create My Fitness Plan →</a>
            </section>

            <section class="features">
                <div class="feature">
                    <h3>🤖 AI Generated</h3>
                    <p>
                        Gemini AI creates a personalized weekly
                        workout plan based on your information.
                    </p>
                </div>

                <div class="feature">
                    <h3>🎯 Goal Based</h3>
                    <p>
                        Choose your fitness goal and workout intensity
                        to generate a suitable plan.
                    </p>
                </div>

                <div class="feature">
                    <h3>📅 7-Day Plan</h3>
                    <p>
                        Get a structured weekly schedule with exercises,
                        sets, repetitions and recovery days.
                    </p>
                </div>
            </section>

        </div>
    </body>
    </html>
    """


# ---------------------------------------------------------
# FORM PAGE
# ---------------------------------------------------------
@app.get("/form", response_class=HTMLResponse)
def form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FitBuddy - Enter Details</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }

            body {
                background: #07110c;
                color: white;
            }

            .container {
                max-width: 850px;
                margin: auto;
                padding: 25px;
            }

            .top {
                text-align: center;
                padding: 35px 10px;
            }

            .logo {
                color: #39ff88;
                font-size: 25px;
                font-weight: bold;
                margin-bottom: 15px;
            }

            h1 {
                font-size: 38px;
                margin-bottom: 10px;
            }

            .subtitle {
                color: #9ba79f;
                line-height: 1.6;
            }

            form {
                background: #0d1b13;
                border: 1px solid #1d3526;
                border-radius: 20px;
                padding: 30px;
            }

            .section-title {
                color: #39ff88;
                font-size: 17px;
                margin: 25px 0 15px;
            }

            .section-title:first-child {
                margin-top: 0;
            }

            label {
                display: block;
                margin-bottom: 8px;
                color: #dbe5df;
                font-size: 14px;
            }

            input, select, textarea {
                width: 100%;
                padding: 14px;
                background: #07110c;
                border: 1px solid #294632;
                border-radius: 10px;
                color: white;
                outline: none;
                margin-bottom: 18px;
            }

            input:focus, select:focus, textarea:focus {
                border-color: #39ff88;
            }

            textarea {
                min-height: 100px;
                resize: vertical;
            }

            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 18px;
            }

            button {
                width: 100%;
                padding: 16px;
                border: none;
                border-radius: 12px;
                background: #39ff88;
                color: #061009;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 10px;
            }

            button:hover {
                opacity: 0.9;
            }

            .note {
                margin-top: 18px;
                padding: 15px;
                border-radius: 10px;
                background: #111f17;
                color: #9ba79f;
                font-size: 13px;
                line-height: 1.5;
            }

            @media(max-width: 650px) {
                .grid {
                    grid-template-columns: 1fr;
                    gap: 0;
                }

                h1 {
                    font-size: 31px;
                }
            }
        </style>
    </head>

    <body>

        <div class="container">

            <div class="top">
                <div class="logo">FitBuddy • AI FITNESS COACH</div>
                <h1>Tell Us About You</h1>
                <p class="subtitle">
                    Enter your details and let AI create your personalized
                    7-day fitness plan.
                </p>
            </div>

            <form action="/generate" method="post">

                <div class="section-title">01 — Personal Details</div>

                <div class="grid">
                    <div>
                        <label>Name</label>
                        <input type="text" name="name"
                               placeholder="Enter your name" required>
                    </div>

                    <div>
                        <label>Age</label>
                        <input type="number" name="age"
                               min="13" max="100"
                               placeholder="Your age" required>
                    </div>
                </div>

                <div class="grid">
                    <div>
                        <label>Gender</label>
                        <select name="gender" required>
                            <option value="">Select gender</option>
                            <option>Male</option>
                            <option>Female</option>
                            <option>Other</option>
                        </select>
                    </div>

                    <div>
                        <label>Height (cm)</label>
                        <input type="number" name="height"
                               min="100" max="250"
                               placeholder="Example: 175" required>
                    </div>
                </div>

                <label>Weight (kg)</label>
                <input type="number" name="weight"
                       min="25" max="300"
                       placeholder="Example: 60" required>


                <div class="section-title">02 — Fitness Goal</div>

                <label>What is your main goal?</label>

                <select name="goal" required>
                    <option value="">Choose your goal</option>
                    <option>Weight Gain</option>
                    <option>Weight Loss</option>
                    <option>Muscle Building</option>
                    <option>General Fitness</option>
                    <option>Strength</option>
                    <option>Endurance</option>
                </select>


                <div class="section-title">03 — Workout Preference</div>

                <label>Workout Intensity</label>

                <select name="intensity" required>
                    <option value="">Choose intensity</option>
                    <option>Beginner</option>
                    <option>Moderate</option>
                    <option>Advanced</option>
                </select>


                <div class="section-title">04 — Additional Information</div>

                <label>
                    Medical history / injuries / other important details
                </label>

                <textarea name="medical"
                          placeholder="Optional — mention anything important for the plan"></textarea>


                <button type="submit">
                    ✨ Generate My AI Fitness Plan
                </button>

                <div class="note">
                    ⚠️ FitBuddy provides general fitness information and
                    is not a replacement for professional medical advice.
                </div>

            </form>

        </div>

    </body>
    </html>
    """


# ---------------------------------------------------------
# GEMINI AI PLAN GENERATION
# ---------------------------------------------------------
def generate_ai_plan(name, age, gender, height, weight,
                     goal, intensity, medical):

    if client is None:
        return None

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe, realistic and beginner-friendly 7-day general fitness
plan using the following user information:

Name: {name}
Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}
Medical history / other details: {medical if medical else "None provided"}

IMPORTANT:
- Do not diagnose medical conditions.
- Do not recommend dangerous or extreme exercise.
- Do not prescribe medication.
- If the user mentions an injury or medical condition, keep the plan
  conservative and recommend consulting a qualified healthcare professional.
- Include rest/recovery where appropriate.
- Keep the plan practical for a normal person.
- Do not give extreme dieting or restrictive eating instructions.

Return ONLY valid JSON.

Use exactly this structure:

{{
  "summary": "Short personalized summary",
  "days": [
    {{
      "day": "Day 1",
      "title": "Workout title",
      "focus": "Main focus",
      "exercises": [
        {{
          "name": "Exercise name",
          "sets": "3",
          "reps": "10",
          "rest": "60 sec"
        }}
      ],
      "tip": "Useful workout tip"
    }}
  ]
}}

The days array must contain exactly 7 days.
"""


    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove accidental markdown JSON fences
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)

        return data

    except Exception as e:
        print("Gemini error:", e)
        return None


# ---------------------------------------------------------
# RESULT PAGE
# ---------------------------------------------------------
@app.post("/generate", response_class=HTMLResponse)
def generate(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    height: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    medical: str = Form("")
):

    plan = generate_ai_plan(
        name,
        age,
        gender,
        height,
        weight,
        goal,
        intensity,
        medical
    )

    # Fallback if Gemini is unavailable
    if not plan:
        plan = {
            "summary": "Your AI plan could not be generated right now. Please check your Gemini API setup and try again.",
            "days": [
                {
                    "day": "Day 1",
                    "title": "Full Body",
                    "focus": "General fitness",
                    "exercises": [
                        {
                            "name": "Bodyweight Squats",
                            "sets": "3",
                            "reps": "10",
                            "rest": "60 sec"
                        },
                        {
                            "name": "Wall Push-ups",
                            "sets": "3",
                            "reps": "10",
                            "rest": "60 sec"
                        }
                    ],
                    "tip": "Start slowly and focus on good form."
                }
            ]
        }

    days_html = ""

    for day in plan.get("days", []):

        exercises_html = ""

        for exercise in day.get("exercises", []):

            exercises_html += f"""
            <div class="exercise">
                <div>
                    <strong>{exercise.get("name", "Exercise")}</strong>
                    <span>
                        {exercise.get("sets", "-")} sets ×
                        {exercise.get("reps", "-")} reps
                    </span>
                </div>

                <small>
                    Rest: {exercise.get("rest", "-")}
                </small>
            </div>
            """

        days_html += f"""
        <div class="day-card">

            <div class="day-number">
                {day.get("day", "Day")}
            </div>

            <h2>{day.get("title", "Workout")}</h2>

            <div class="focus">
                Focus: {day.get("focus", "Fitness")}
            </div>

            <div class="exercise-list">
                {exercises_html}
            </div>

            <div class="tip">
                💡 {day.get("tip", "")}
            </div>

        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>FitBuddy - Your AI Plan</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>

            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}

            body {{
                background: #07110c;
                color: white;
            }}

            .container {{
                max-width: 1050px;
                margin: auto;
                padding: 25px;
            }}

            .header {{
                text-align: center;
                padding: 30px 10px;
            }}

            .logo {{
                color: #39ff88;
                font-size: 25px;
                font-weight: bold;
                margin-bottom: 15px;
            }}

            .header h1 {{
                font-size: 38px;
                margin-bottom: 10px;
            }}

            .header p {{
                color: #9ba79f;
            }}

            .profile {{
                background: #0d1b13;
                border: 1px solid #1d3526;
                border-radius: 18px;
                padding: 22px;
                margin-bottom: 25px;
            }}

            .profile-title {{
                color: #39ff88;
                margin-bottom: 15px;
                font-weight: bold;
            }}

            .profile-grid {{
                display: grid;
                grid-template-columns:
                    repeat(5, 1fr);
                gap: 12px;
            }}

            .profile-item {{
                background: #07110c;
                border-radius: 10px;
                padding: 13px;
            }}

            .profile-item small {{
                display: block;
                color: #7e8b83;
                margin-bottom: 5px;
            }}

            .profile-item strong {{
                color: white;
            }}

            .summary {{
                background: #102318;
                border: 1px solid #285638;
                border-radius: 18px;
                padding: 25px;
                margin-bottom: 25px;
            }}

            .summary h2 {{
                color: #39ff88;
                margin-bottom: 10px;
            }}

            .summary p {{
                color: #c4d0c8;
                line-height: 1.6;
            }}

            .days {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}

            .day-card {{
                background: #0d1b13;
                border: 1px solid #1d3526;
                border-radius: 18px;
                padding: 23px;
                position: relative;
            }}

            .day-number {{
                color: #39ff88;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 10px;
                text-transform: uppercase;
            }}

            .day-card h2 {{
                margin-bottom: 7px;
            }}

            .focus {{
                color: #829088;
                font-size: 14px;
                margin-bottom: 18px;
            }}

            .exercise {{
                background: #07110c;
                border-radius: 10px;
                padding: 12px;
                margin-bottom: 9px;
                display: flex;
                justify-content: space-between;
                gap: 10px;
            }}

            .exercise strong {{
                display: block;
                margin-bottom: 4px;
            }}

            .exercise span,
            .exercise small {{
                color: #89968e;
                font-size: 12px;
            }}

            .tip {{
                margin-top: 15px;
                padding: 12px;
                background: #111f17;
                border-radius: 9px;
                color: #aab5ae;
                font-size: 13px;
                line-height: 1.5;
            }}

            .actions {{
                text-align: center;
                margin: 35px 0 20px;
            }}

            .btn {{
                display: inline-block;
                background: #39ff88;
                color: #061009;
                text-decoration: none;
                padding: 15px 25px;
                border-radius: 11px;
                font-weight: bold;
            }}

            .safety {{
                text-align: center;
                color: #718078;
                font-size: 12px;
                line-height: 1.5;
                margin: 20px auto;
                max-width: 700px;
            }}

            @media(max-width: 750px) {{

                .profile-grid {{
                    grid-template-columns: 1fr 1fr;
                }}

                .days {{
                    grid-template-columns: 1fr;
                }}

                .header h1 {{
                    font-size: 31px;
                }}
            }}

            @media(max-width: 430px) {{

                .profile-grid {{
                    grid-template-columns: 1fr;
                }}

                .container {{
                    padding: 15px;
                }}
            }}

        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">
                <div class="logo">
                    FitBuddy • AI FITNESS COACH
                </div>

                <h1>Your Personalized 7-Day Plan</h1>

                <p>
                    Generated with Gemini AI based on your fitness details.
                </p>
            </div>


            <div class="profile">

                <div class="profile-title">
                    YOUR DETAILS
                </div>

                <div class="profile-grid">

                    <div class="profile-item">
                        <small>Name</small>
                        <strong>{name}</strong>
                    </div>

                    <div class="profile-item">
                        <small>Age</small>
                        <strong>{age}</strong>
                    </div>

                    <div class="profile-item">
                        <small>Height</small>
                        <strong>{height} cm</strong>
                    </div>

                    <div class="profile-item">
                        <small>Weight</small>
                        <strong>{weight} kg</strong>
                    </div>

                    <div class="profile-item">
                        <small>Goal</small>
                        <strong>{goal}</strong>
                    </div>

                </div>

            </div>


            <div class="summary">

                <h2>✨ AI Summary</h2>

                <p>
                    {plan.get("summary", "Personalized fitness plan generated by AI.")}
                </p>

            </div>


            <div class="days">

                {days_html}

            </div>


            <div class="actions">

                <a href="/form" class="btn">
                    + Create Another Plan
                </a>

            </div>


            <div class="safety">

                ⚠️ FitBuddy provides general fitness information.
                Listen to your body, use proper form and seek qualified
                professional advice when needed, especially for medical
                conditions or injuries.

            </div>

        </div>

    </body>

    </html>
    """
      