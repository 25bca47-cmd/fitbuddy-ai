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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>FitBuddy AI | Build. Train. Transform.</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: Arial, sans-serif;
            background: #050807;
            color: white;
            line-height: 1.6;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        /* NAVBAR */
        nav {
            position: sticky;
            top: 0;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 7%;
            background: rgba(3, 7, 6, 0.96);
            border-bottom: 1px solid #18231e;
        }

        .logo {
            font-size: 26px;
            font-weight: 900;
        }

        .logo span {
            color: #18ff8b;
        }

        .nav-links {
            display: flex;
            gap: 25px;
            align-items: center;
        }

        .nav-links a {
            color: #d8dedb;
            font-size: 15px;
        }

        .nav-links a:hover {
            color: #18ff8b;
        }

        .nav-button {
            border: 1px solid #18ff8b;
            color: #18ff8b !important;
            padding: 10px 20px;
            border-radius: 30px;
            font-weight: bold;
        }

        /* HERO */
        .hero {
            min-height: 720px;
            display: flex;
            align-items: center;
            padding: 70px 7%;

            background:
                linear-gradient(
                    90deg,
                    rgba(3,8,6,0.98) 0%,
                    rgba(3,8,6,0.88) 40%,
                    rgba(3,8,6,0.35) 75%,
                    rgba(3,8,6,0.70) 100%
                ),
                url("https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=1600&q=85")
                center/cover no-repeat;
        }

        .hero-content {
            max-width: 650px;
        }

        .eyebrow {
            color: #18ff8b;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }

        .hero h1 {
            font-size: clamp(55px, 9vw, 105px);
            line-height: 0.9;
            font-weight: 950;
            letter-spacing: -5px;
            margin-bottom: 25px;
        }

        .hero h1 span {
            color: #18ff8b;
        }

        .tagline {
            font-size: 34px;
            font-weight: 800;
            color: #18ff8b;
            margin-bottom: 18px;
        }

        .hero p {
            color: #d0d8d4;
            font-size: 19px;
            max-width: 560px;
            margin-bottom: 30px;
        }

        .main-button {
            display: inline-block;
            background: #18ff8b;
            color: #031008;
            padding: 17px 30px;
            border-radius: 35px;
            font-size: 17px;
            font-weight: 900;
            transition: 0.2s;
        }

        .main-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 35px rgba(24,255,139,0.25);
        }

        .trust-row {
            display: flex;
            gap: 35px;
            margin-top: 40px;
            color: #b8c3bd;
            font-size: 14px;
        }

        .trust-row strong {
            display: block;
            color: white;
            font-size: 15px;
        }

        /* FEATURES */
        .features {
            padding: 90px 7%;
            background: #070d0b;
        }

        .section-title {
            text-align: center;
            max-width: 800px;
            margin: 0 auto 55px;
        }

        .section-title small {
            color: #18ff8b;
            font-weight: 900;
            letter-spacing: 2px;
        }

        .section-title h2 {
            font-size: clamp(35px, 5vw, 60px);
            line-height: 1;
            margin: 15px 0;
        }

        .section-title p {
            color: #9eaaa4;
            font-size: 17px;
        }

        .feature-grid {
            max-width: 1200px;
            margin: auto;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .feature {
            background: #0b1310;
            border: 1px solid #1b2923;
            border-radius: 20px;
            padding: 30px;
            transition: 0.25s;
        }

        .feature:hover {
            transform: translateY(-5px);
            border-color: #18ff8b;
        }

        .icon {
            width: 55px;
            height: 55px;
            display: grid;
            place-items: center;
            border-radius: 50%;
            background: #18ff8b;
            color: #031008;
            font-size: 25px;
            margin-bottom: 20px;
        }

        .feature h3 {
            font-size: 21px;
            margin-bottom: 10px;
        }

        .feature p {
            color: #9da8a2;
            font-size: 15px;
        }

        /* CTA */
        .cta {
            padding: 100px 7%;
            text-align: center;

            background:
                linear-gradient(
                    rgba(3,8,6,0.85),
                    rgba(3,8,6,0.95)
                ),
                url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1600&q=85")
                center/cover no-repeat;
        }

        .cta h2 {
            font-size: clamp(40px, 7vw, 75px);
            line-height: 0.95;
            margin-bottom: 20px;
        }

        .cta h2 span {
            color: #18ff8b;
        }

        .cta p {
            color: #c3ccc7;
            margin-bottom: 30px;
            font-size: 18px;
        }

        /* FOOTER */
        footer {
            padding: 30px 7%;
            text-align: center;
            background: #030605;
            color: #78827d;
            font-size: 14px;
        }

        footer strong {
            color: #18ff8b;
        }

        /* MOBILE */
        @media (max-width: 800px) {

            nav {
                padding: 16px 5%;
            }

            .nav-links {
                display: none;
            }

            .hero {
                min-height: 650px;
                padding: 60px 6%;
                background-position: 65% center;
            }

            .hero h1 {
                font-size: 60px;
                letter-spacing: -3px;
            }

            .tagline {
                font-size: 26px;
            }

            .hero p {
                font-size: 16px;
            }

            .trust-row {
                gap: 15px;
                flex-wrap: wrap;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }

            .features {
                padding: 70px 6%;
            }

            .cta {
                padding: 80px 6%;
            }
        }
    </style>
</head>

<body>

    <nav>
        <div class="logo">
            FitBuddy <span>AI</span>
        </div>

        <div class="nav-links">
            <a href="/">Home</a>
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <a class="nav-button" href="/form">Get Started</a>
        </div>
    </nav>


    <section class="hero">

        <div class="hero-content">

            <div class="eyebrow">
                Your AI-Powered Fitness Partner
            </div>

            <h1>
                FITBUDDY <span>AI</span>
            </h1>

            <div class="tagline">
                Build. Train. Transform.
            </div>

            <p>
                Get personalized workout and fitness plans powered by AI.
                Train smarter, stay consistent and work toward your goals.
            </p>

            <a class="main-button" href="/form">
                ⚡ Create My Plan →
            </a>

            <div class="trust-row">

                <div>
                    <strong>✓ Personalized</strong>
                    Plans
                </div>

                <div>
                    <strong>⚡ AI Powered</strong>
                    Fitness
                </div>

                <div>
                    <strong>♥ Goal Focused</strong>
                    Training
                </div>

            </div>

        </div>

    </section>


    <section class="features" id="features">

        <div class="section-title">

            <small>POWERFUL FEATURES</small>

            <h2>
                Everything You Need
                for a Stronger You
            </h2>

            <p>
                FitBuddy AI brings your fitness journey together
                in one simple place.
            </p>

        </div>


        <div class="feature-grid">

            <div class="feature">
                <div class="icon">🏋️</div>

                <h3>AI Workout Plans</h3>

                <p>
                    Generate personalized 7-day workout plans
                    based on your goals and fitness level.
                </p>
            </div>


            <div class="feature">
                <div class="icon">🥗</div>

                <h3>Diet & Meal Plans</h3>

                <p>
                    Plan nutritious meals to support your
                    training and fitness goals.
                </p>
            </div>


            <div class="feature">
                <div class="icon">📊</div>

                <h3>Progress Tracking</h3>

                <p>
                    Keep track of workouts, measurements
                    and your fitness progress.
                </p>
            </div>


            <div class="feature">
                <div class="icon">🎯</div>

                <h3>Goal Setting</h3>

                <p>
                    Set clear goals and stay motivated
                    throughout your fitness journey.
                </p>
            </div>


            <div class="feature">
                <div class="icon">📱</div>

                <h3>Mobile Friendly</h3>

                <p>
                    Use FitBuddy AI comfortably on your
                    phone, tablet or computer.
                </p>
            </div>


            <div class="feature">
                <div class="icon">🚀</div>

                <h3>Built to Grow</h3>

                <p>
                    A strong foundation for future fitness
                    features and improvements.
                </p>
            </div>

        </div>

    </section>


    <section class="cta" id="about">

        <h2>
            LET'S BUILD A
            <span>STRONGER YOU</span>
        </h2>

        <p>
            Your next workout starts with one decision.
        </p>

        <a class="main-button" href="/form">
            ⚡ Create My Plan →
        </a>

    </section>


    <footer id="contact">

        <strong>FitBuddy AI</strong>
        — Build. Train. Transform.

        <br><br>

        General fitness information only.
        Listen to your body and seek qualified professional advice when needed.

    </footer>

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


    import time

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash"
    ]

    for model_name in models:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                text = response.text.strip()

                if text.startswith("```"):
                    text = text.replace("```json", "")
                    text = text.replace("```", "")
                    text = text.strip()

                data = json.loads(text)

                return data

            except Exception as e:
                print(
                    f"Gemini {model_name} attempt {attempt + 1} error:",
                    e
                )

                if attempt < 1:
                    time.sleep(5)

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
      
