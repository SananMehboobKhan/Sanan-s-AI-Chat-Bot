# ============================================
# history.py - Chat History ka file
# Saari conversation save karta hai
# ============================================

from datetime import datetime


def initialize_history():
    """
    Naya empty chat history banata hai
    """
    return []


def add_message(history, role, content):
    """
    History mein naya message add karta hai
    
    role = "user" (aap) ya "assistant" (AI)
    content = message ka text
    """
    
    message = {
        'role': role,                           # Kisne bola
        'content': content,                     # Kya bola
        'timestamp': datetime.now().strftime("%H:%M:%S")  # Kab bola
    }
    
    history.append(message)
    return history


def get_formatted_history(history):
    """
    History ko readable format mein return karta hai
    """
    
    if not history:
        return "Abhi koi conversation nahi hai."
    
    formatted = ""
    for msg in history:
        if msg['role'] == 'user':
            formatted += f"[{msg['timestamp']}] Aap: {msg['content']}\n\n"
        else:
            formatted += f"[{msg['timestamp']}] AI: {msg['content']}\n\n"
    
    return formatted


def clear_history():
    """
    Chat history clear karta hai
    """
    return []


def get_message_count(history):
    """
    Total messages count return karta hai
    """
    return len(history)


def export_history_text(history):
    """
    History ko text file ke liye format karta hai
    """
    
    export_text = f"Chat History - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    export_text += "=" * 50 + "\n\n"
    
    for msg in history:
        if msg['role'] == 'user':
            export_text += f"[{msg['timestamp']}] YOU: {msg['content']}\n"
        else:
            export_text += f"[{msg['timestamp']}] AI: {msg['content']}\n"
        export_text += "-" * 30 + "\n"
    
    return export_text