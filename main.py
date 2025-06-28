from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from nlp_utils import parse_intent
from db import init_db, add_task, get_tasks, add_note, get_notes
from api_clients.weather import get_weather
from api_clients.calendar import add_event_to_calendar
import random

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

init_db()

class UserInput(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(user_input: UserInput):
    intent_data = parse_intent(user_input.message)
    intent = intent_data.get("intent")

    if intent == "create_task":
        task = intent_data["task"]
        time = intent_data["time"]
        add_task(task, time)
        return {"response": f"Task '{task}' set for {time}."}

    elif intent == "get_tasks":
        tasks = get_tasks()
        if tasks:
            formatted = "\n".join([f"- {t['task']} at {t['time']}" for t in tasks])
            return {"response": f"Here are your tasks:\n{formatted}"}
        else:
            return {"response": "You have no tasks."}

    elif intent == "get_weather":
        city = intent_data["location"]
        weather = get_weather(city)
        return {"response": weather}

    elif intent == "create_event":
        event = intent_data["event"]
        date = intent_data["date"]
        response = add_event_to_calendar(event, date)
        return {"response": response}

    elif intent == "tell_joke":
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look sad? Because it had too many problems.",
            "I told my computer I needed a break, and it said 'no problem – I'll go to sleep!'"
        ]
        return {"response": random.choice(jokes)}

    elif intent == "save_note":
        note = intent_data["note"]
        add_note(note)
        return {"response": "Note saved."}

    elif intent == "get_notes":
        notes = get_notes()
        if notes:
            formatted = "\n".join([f"- {n}" for n in notes])
            return {"response": f"Here are your notes:\n{formatted}"}
        else:
            return {"response": "You don't have any saved notes."}

    else:
        return {"response": "Sorry, I didn’t understand that."}