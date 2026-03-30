# ============================================
# summarizer.py - AI Summarization ka file
# OpenAI API use karta hai answer banane ke liye
# ============================================

from openai import OpenAI
import config

# OpenAI client banao
client = OpenAI(api_key=config.OPENAI_API_KEY)


def generate_answer(user_question, search_results):
    """
    Is function ka kaam:
    - User ka question aur search results leta hai
    - OpenAI se short summarized answer banata hai
    - Answer return karta hai
    """
    
    # Agar search results empty hain
    if not search_results:
        return "Maafi chahta hoon, internet search mein koi result nahi mila. Kripya apna sawaal dubara poochein."
    
    # Search results ko text mein convert karo
    search_text = ""
    for i, result in enumerate(search_results, 1):
        search_text += f"\nSource {i}: {result['title']}\n"
        search_text += f"Content: {result['body']}\n"
    
    # AI ko instructions do (prompt)
    prompt = f"""
    Tum ek helpful AI assistant ho. 
    Niche diye gaye search results ke basis par user ke sawaal ka jawab do.
    
    User ka Sawaal: {user_question}
    
    Search Results:
    {search_text}
    
    Instructions:
    - Short aur clear jawab do (2-3 paragraphs)
    - Simple language use karo
    - Important points bullet points mein likho
    - Agar koi information na mile to clearly batao
    - Sources ka mention karo jawab mein
    """
    
    try:
        # OpenAI API call karo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",      # AI model
            messages=[
                {
                    "role": "system", 
                    "content": "Tum ek helpful assistant ho jo internet search results ko summarize karta hai."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=500,             # Maximum response length
            temperature=0.7             # Creativity level (0=exact, 1=creative)
        )
        
        # Response text extract karo
        answer = response.choices[0].message.content
        return answer
        
    except Exception as e:
        return f"AI answer generate karne mein error aaya: {str(e)}"


def generate_simple_answer(user_question, search_results):
    """
    Backup function - Agar OpenAI fail ho to simple answer banata hai
    """
    
    if not search_results:
        return "Koi information nahi mili."
    
    # Pehle 3 results se answer banao
    answer = f"**'{user_question}' ke bare mein information:**\n\n"
    
    for i, result in enumerate(search_results[:3], 1):
        answer += f"**{i}. {result['title']}**\n"
        answer += f"{result['body'][:200]}...\n\n"  # First 200 characters
    
    return answer