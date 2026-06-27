from groq import Groq
import config

def generate_ai_summary(selected_item_name, combined_data):
    """
    Sends the aggregated raw data to Groq's Llama 3.1 8B Instant model
    and returns a professionally formatted Markdown deep research report.
    """
    if not config.GROQ_API_KEY:
        print("⚠️ Groq API Key not configured! Cannot generate AI summary.")
        return "AI Summary is unavailable (Groq API Key not configured)."

    try:
        client = Groq(api_key=config.GROQ_API_KEY)
        
        prompt = f"""Nee oru expert research analyst. Keela irukira raw data-va analyze panni oru professional deep research report generate pannu.

Topic: {selected_item_name}

Raw Data:
{combined_data}

Report Format:
1. 📌 OVERVIEW (2-3 lines summary)
2. 📊 KEY FACTS (bullet points)
3. 📞 CONTACT INFORMATION (Phone, Email, Website, Address)
4. ⭐ RATINGS & REVIEWS (Google rating, review highlights)
5. 🏢 COMPANY/ORGANIZATION DETAILS (from LinkedIn)
6. 📰 LATEST NEWS (recent updates)
7. 🎥 RECOMMENDED VIDEOS (YouTube links)
8. 📱 SOCIAL MEDIA LINKS
9. 💡 ADDITIONAL INSIGHTS

Make it professional, well-structured, and easy to read."""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        
        response_text = chat_completion.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"⚠️ Groq AI summary generation failed: {e}")
        return f"Failed to generate report due to an error: {e}"

def _trim_text(text, max_chars):
    """Trims text to max_chars, cutting at the last newline before the limit."""
    if not text or len(text) <= max_chars:
        return text
    trimmed = text[:max_chars]
    last_newline = trimmed.rfind('\n')
    if last_newline > max_chars * 0.5:
        trimmed = trimmed[:last_newline]
    return trimmed + "\n...[trimmed for size]"


def chat_with_groq(selected_item_name, combined_data, user_question, chat_history=None, live_research_data=""):
    """
    Answers a user question about the researched entity.
    Aggressively trims data to stay within Groq free tier token limits.
    Prioritizes live research data (most relevant) over pre-collected data.
    """
    if not config.GROQ_API_KEY:
        return "AI Chat is unavailable (Groq API Key not configured)."
        
    if chat_history is None:
        chat_history = []
        
    try:
        client = Groq(api_key=config.GROQ_API_KEY)
        
        # Aggressively trim data to fit within ~6000 token limit
        # ~4 chars per token roughly, so ~5500 tokens max for data = ~22000 chars
        # But free tier TPM is only 6000, so we need to be much more aggressive
        # Keep total prompt under ~4000 tokens = ~16000 chars including instructions
        
        has_live = bool(live_research_data and live_research_data.strip())
        
        if has_live:
            # When live data exists, prioritize it heavily
            live_trimmed = _trim_text(live_research_data, 4000)
            raw_trimmed = _trim_text(combined_data, 2500)
        else:
            live_trimmed = ""
            raw_trimmed = _trim_text(combined_data, 5500)
        
        # Build compact system prompt
        data_sections = ""
        if live_trimmed:
            data_sections += f"\n[LIVE WEB DATA - freshly searched for this question]\n{live_trimmed}\n"
        
        data_sections += f"\n[PRE-COLLECTED DATA]\n{raw_trimmed}\n"
        
        system_prompt = f"""You are DeepDig AI assistant for: {selected_item_name}.
{data_sections}
RULES: Answer from the data above. Extract names, contacts, numbers, emails, designations. Be detailed and comprehensive. Use bullet points. If info is partial, show what you found. Never say "not found" without checking thoroughly."""

        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add only the last 2 exchanges from history to save tokens
        recent_history = chat_history[-4:] if len(chat_history) > 4 else chat_history
        for msg in recent_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            # Trim long history messages too
            messages.append({"role": role, "content": _trim_text(content, 500)})
            
        # Add the current question
        messages.append({"role": "user", "content": user_question})
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
        )
        
        response_text = chat_completion.choices[0].message.content
        return response_text
    except Exception as e:
        print(f"⚠️ Groq chat failed: {e}")
        return f"Failed to get a response from chat assistant: {e}"
