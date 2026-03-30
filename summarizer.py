# ============================================
# summarizer.py - AI Summarization
# Using Groq API (FREE - faster than OpenAI!)
# ============================================

from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)


def generate_answer(user_question, search_results):

    if not search_results:
        return "Sorry, no internet search results were found. Please try rephrasing your question."

    search_text = ""
    for i, result in enumerate(search_results, 1):
        search_text += f"\nSource {i}: {result['title']}\n"
        search_text += f"Content: {result['body']}\n"

    prompt = f"""You are a helpful AI assistant.
Answer the user's question based on the search results below.

User Question: {user_question}

Search Results:
{search_text}

Instructions:
- ALWAYS respond in ENGLISH only
- Give a clear, well-structured answer
- Use bullet points for key facts when helpful
- Keep it concise (2-3 paragraphs max)
- Be direct and informative
"""

    try:
        response = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that ONLY responds in English. You summarize internet search results into clear answers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=600,
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg:
            return "Invalid Groq API key. Please check config.py"
        elif "429" in error_msg:
            return "Too many requests. Please wait a moment and try again."
        else:
            return f"Error: {error_msg}"

