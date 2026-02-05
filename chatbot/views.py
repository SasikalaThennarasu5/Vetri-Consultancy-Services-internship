import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jobs.models import Job

HF_API_KEY = "PASTE_YOUR_HUGGINGFACE_API_KEY"
MODEL = "google/flan-t5-base"


def chat_ui(request):
    return render(request, "chatbot/chat.html")


def extract_details(text):
    prompt = f"""
Extract skills and preferred job location.
Return ONLY JSON.

Example:
{{"skills":["django"],"location":"Chennai"}}

Text:
{text}
"""

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": prompt},
        timeout=30
    )

    result = response.json()

    if isinstance(result, dict) and "error" in result:
        return None

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    return None


@csrf_exempt
def chat_api(request):
    data = json.loads(request.body)
    user_input = data.get("message", "")

    intent = detect_intent(user_input)

    # 9️⃣ Application process
    if intent == "apply":
        return JsonResponse({
            "reply": (
                "📄 Vetri Consultancy Application Process:\n"
                "1. Submit resume\n"
                "2. Skill screening\n"
                "3. Technical interview\n"
                "4. HR discussion\n"
                "5. Offer letter"
            )
        })

    # 8️⃣ Interview preparation
    if intent == "interview":
        return JsonResponse({
            "reply": (
                "🎤 Common Interview Questions:\n"
                "1. What is Django ORM?\n"
                "2. Explain REST API\n"
                "3. Difference between GET and POST\n"
                "4. What is middleware?\n"
                "5. Explain MVC vs MVT"
            )
        })

    # 7️⃣ Salary estimation
    if intent == "salary":
        return JsonResponse({
            "reply": (
                "💰 Approximate Salary Ranges:\n"
                "Python Developer: ₹4–8 LPA\n"
                "Java Developer: ₹3–7 LPA\n"
                "Frontend Developer: ₹3–6 LPA"
            )
        })

    # 4️⃣ Resume tips
    if intent == "resume":
        return JsonResponse({
            "reply": (
                "📝 Resume Improvement Tips:\n"
                "• Add real-time project details\n"
                "• Mention tools & technologies clearly\n"
                "• Keep resume to 1–2 pages\n"
                "• Add GitHub or portfolio link"
            )
        })

    # ---------------- JOB SEARCH FLOW ---------------- #

    extracted = extract_details(user_input)

    # ✅ Fallback if AI fails
    if not extracted:
        parts = user_input.lower().split(",")
        skills = [p.strip() for p in parts[:-1]]
        location = parts[-1].strip() if parts else ""
    else:
        try:
            info = json.loads(extracted)
            skills = info.get("skills", [])
            location = info.get("location", "")
        except:
            skills = []
            location = ""

    if not skills or not location:
        return JsonResponse({
            "reply": "Please enter skills and location like: django, chennai"
        })

    # 6️⃣ Job role suggestion
    role_map = {
        "python": "Backend Developer",
        "django": "Backend Developer",
        "java": "Java Developer",
        "html": "Frontend Developer",
        "css": "Frontend Developer",
        "javascript": "Frontend Developer",
    }

    roles = {role_map[s] for s in skills if s in role_map}

    # 1️⃣ 2️⃣ 3️⃣ Job matching
    jobs = Job.objects.filter(location__icontains=location)

    matched = []
    for job in jobs:
        score = sum(skill.lower() in job.skills.lower() for skill in skills)
        if score > 0:
            matched.append((score, job))

    if not matched:
        return JsonResponse({"reply": "❌ No matching jobs found."})

    matched.sort(reverse=True, key=lambda x: x[0])

    reply = "✅ Recommended Jobs:\n\n"

    for score, job in matched[:3]:
        job_skills = set(job.skills.lower().split(","))
        user_skills = set(skills)

        matched_skills = job_skills & user_skills
        missing_skills = job_skills - user_skills

        reply += (
            f"🔹 {job.title} ({job.location})\n"
            f"✔ Matches because you know: {', '.join(matched_skills)}\n"
        )

        if missing_skills:
            reply += f"📌 Suggested skills: {', '.join(list(missing_skills)[:2])}\n"

        reply += "\n"

    if roles:
        reply += f"🎯 Suitable roles: {', '.join(roles)}\n"

    reply += (
        "\n📝 Resume Tip: Highlight projects clearly.\n"
        "📈 Skill Tip: Learn REST APIs & Git."
    )

    return JsonResponse({"reply": reply})


def detect_intent(text):
    text = text.lower()

    if "resume" in text:
        return "resume"
    if "interview" in text:
        return "interview"
    if "salary" in text or "package" in text:
        return "salary"
    if "apply" in text:
        return "apply"

    return "job_search"
