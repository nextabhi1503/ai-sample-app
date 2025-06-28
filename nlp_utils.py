### nlp_utils.py (GPT-based intent parser with fallback)
import openai
import os
import json
import re

openai.api_key = "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"

def parse_intent(text):
    system_prompt = """
You are an intent parsing agent. Convert user messages into structured JSON with the intent and any relevant fields. Possible intents include: create_task, get_tasks, get_weather, create_event, tell_joke, save_note, get_notes, delete_task, delete_note, unknown. Use snake_case for intent names and fields. If the input is ambiguous, use 'unknown'.
"""

    user_prompt = f"User message: {text}\nReturn JSON:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=150
        )
        output = response.choices[0].message['content'].strip()
        return json.loads(output)
    except Exception as e:
        print("GPT Intent Parsing Error:", e)
        return fallback_parse_intent(text)

def fallback_parse_intent(text):
    text = text.lower()
    # --- Helper
    def extract_time_or_fuzzy(text):
        # Extracts specific time or fuzzy time (e.g., "this evening")
        match = re.search(r"(?:at|by|around)? ?(\d{1,2}(?::\d{2})?\s?(?:am|pm)|tonight|this (morning|evening|afternoon)|tomorrow(?: (morning|evening)?)?)", text)
        return match.group(1).strip() if match else None

    # --- Create Task / Reminder ---
    match = re.search(r"(remind me to|set (a )?reminder to|i need to remember to|please remind me to|can you remind me to|create task|make a task to|add task to) (.*?)(?: at| by| around| on| tomorrow| tonight| this)?", text)
    if match:
        task = match.group(3).strip()
        time = extract_time_or_fuzzy(text)
        return {"intent": "create_task", "task": task, "time": time}

    # --- Show Tasks ---
    if re.search(r"(show|list|what are|tell me) (my )?(tasks|reminders|to[- ]?dos?)", text):
        return {"intent": "get_tasks"}

    # --- Delete Task ---
    match = re.search(r"(delete|remove|cancel) (?:the )?task (.*)", text)
    if match:
        return {"intent": "delete_task", "task": match.group(2).strip()}

    # --- Weather ---
    match = re.search(r"(?:what(?:'s| is) the )?(?:weather|climate)(?: (?:in|at))? ?([a-zA-Z ]+)?", text)
    if match:
        city = match.group(1).strip() if match.group(1) else None
        return {"intent": "get_weather", "location": city}

    # --- Create Event ---
    match = re.search(r"create (?:an )?event (.*?) on (\d{4}-\d{2}-\d{2})", text)
    if match:
        return {"intent": "create_event", "event": match.group(1).strip(), "date": match.group(2)}

    # --- Save Note ---
    match = re.search(r"(?:create|save|add|note down|jot down|write) (?:a )?note:? (.*)", text)
    if match:
        return {"intent": "save_note", "note": match.group(1).strip()}

    # --- Show Notes ---
    if re.search(r"(show|list|read|what are|display) (my )?(notes|memos|saved notes)", text):
        return {"intent": "get_notes"}

    # --- Delete Note ---
    match = re.search(r"(delete|remove|erase|discard) (?:the )?note[:]? (.*)", text)
    if match:
        return {"intent": "delete_note", "note": match.group(2).strip()}

    # --- Joke ---
    if re.search(r"(tell|say|give|crack) (me )?(a )?joke", text):
        return {"intent": "tell_joke"}

    return {"intent": "unknown"}