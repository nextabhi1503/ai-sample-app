import re

def parse_intent(text):
    text = text.lower()

    if "remind me to" in text:
        match = re.search(r"remind me to (.*?) at (\d+ ?[ap]m)", text)
        if match:
            return {"intent": "create_task", "task": match.group(1), "time": match.group(2)}
    
    elif "create task" in text:
        match = re.search(r"create task (.*?) at (\d+ ?[ap]m)", text)
        if match:
            return {"intent": "create_task", "task": match.group(1), "time": match.group(2)}

    elif "show my tasks" in text:
        return {"intent": "get_tasks"}
    
    elif "show task" in text:
        return {"intent": "get_tasks"}

    elif "weather" in text:
        match = re.search(r"weather(?: in ([a-zA-Z ]+))?", text)
        city = match.group(1).strip() if match and match.group(1) else None
        return {"intent": "get_weather", "location": city}
    
    elif "climate in" in text:
        match = re.search(r"weather in ([a-zA-Z ]+)", text)
        if match:
            return {"intent": "get_weather", "location": match.group(1).strip()}

    elif "create an event" in text:
        match = re.search(r"create an event (.*?) on (\d{4}-\d{2}-\d{2})", text)
        if match:
            return {"intent": "create_event", "event": match.group(1), "date": match.group(2)}

    elif "tell me a joke" in text:
        return {"intent": "tell_joke"}

    elif "save note" in text:
        match = re.search(r"save note: (.*)", text)
        if match:
            return {"intent": "save_note", "note": match.group(1)}
    
    elif "create note" in text:
        match = re.search(r"create note: (.*)", text)
        if match:
            return {"intent": "save_note", "note": match.group(1)}

    elif "show my notes" in text:
        return {"intent": "get_notes"}
    
    elif "show note" in text:
        return {"intent": "get_notes"}
    
    elif "delete task" in text:
        match = re.search(r"delete task (.*)", text)
        if match:
            return {"intent": "delete_task", "task": match.group(1)}

    elif "delete note" in text:
        match = re.search(r"delete note (.*)", text)
        if match:
            return {"intent": "delete_note", "note": match.group(1)}

    return {"intent": "unknown"}