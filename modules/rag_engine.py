"""
Smart Campus Intelligence System — RAG Query Engine
Uses LangChain + Google Gemini to answer teacher queries about students using vector DB context.
"""
import config
from modules import database
from datetime import date


def _build_student_context() -> str:
    """
    Pull all student records and attendance data from ChromaDB
    and format as a text document for the LLM context.
    """
    # Get all enrolled students
    students = database.get_all_students()
    
    context_parts = []
    context_parts.append("=== ENROLLED STUDENTS DATABASE ===\n")
    
    if not students['ids']:
        context_parts.append("No students are currently enrolled in the system.\n")
    else:
        for i, sid in enumerate(students['ids']):
            meta = students['metadatas'][i] if students['metadatas'] else {}
            context_parts.append(
                f"Student: {meta.get('name', 'Unknown')}\n"
                f"  Registration ID: {sid}\n"
                f"  Email: {meta.get('email', 'N/A')}\n"
                f"  Department: {meta.get('department', 'N/A')}\n"
                f"  Enrolled Date: {meta.get('enrolled_date', 'N/A')}\n"
            )
    
    # Get all attendance records
    all_attendance = database.get_all_attendance()
    
    context_parts.append("\n=== ATTENDANCE RECORDS ===\n")
    
    if not all_attendance['ids']:
        context_parts.append("No attendance records found.\n")
    else:
        # Group by student
        student_records = {}
        all_dates = set()
        
        for i, record_id in enumerate(all_attendance['ids']):
            meta = all_attendance['metadatas'][i]
            sid = meta.get("student_id", "")
            d = meta.get("date", "")
            time = meta.get("time", "")
            name = meta.get("name", "")
            
            if sid not in student_records:
                student_records[sid] = {"name": name, "records": []}
            student_records[sid]["records"].append({"date": d, "time": time})
            all_dates.add(d)
        
        total_days = len(all_dates)
        context_parts.append(f"Total class days recorded: {total_days}\n")
        context_parts.append(f"Dates: {', '.join(sorted(all_dates))}\n\n")
        
        for sid, info in student_records.items():
            days_present = len(set(r["date"] for r in info["records"]))
            percentage = round(days_present / total_days * 100, 1) if total_days > 0 else 0
            
            context_parts.append(
                f"Attendance for {info['name']} ({sid}):\n"
                f"  Days Present: {days_present}/{total_days} ({percentage}%)\n"
                f"  Status: {'Good Standing' if percentage >= 75 else 'AT RISK - Below 75%'}\n"
                f"  Records:\n"
            )
            for rec in sorted(info["records"], key=lambda x: x["date"]):
                context_parts.append(f"    - {rec['date']} at {rec['time']}\n")
            context_parts.append("\n")
    
    # Today's summary
    today = date.today().isoformat()
    today_records = database.get_today_attendance()
    today_present = set()
    for meta in today_records.get('metadatas', []):
        today_present.add(meta.get("student_id", ""))
    
    context_parts.append(f"\n=== TODAY'S SUMMARY ({today}) ===\n")
    context_parts.append(f"Students present today: {len(today_present)}\n")
    if today_present:
        for sid in today_present:
            # Find name from student records
            for meta in students.get('metadatas', []):
                if meta.get('student_id', '') == sid or sid in students.get('ids', []):
                    name_idx = students['ids'].index(sid) if sid in students['ids'] else -1
                    if name_idx >= 0:
                        context_parts.append(
                            f"  - {students['metadatas'][name_idx].get('name', sid)} ({sid})\n"
                        )
                    break
    
    total_enrolled = len(students['ids']) if students['ids'] else 0
    absent_today = total_enrolled - len(today_present)
    context_parts.append(f"Students absent today: {absent_today}\n")
    
    return "".join(context_parts)


def query(question: str) -> str:
    """
    Answer a teacher's natural language question about students using RAG.
    
    Pulls all student + attendance data from ChromaDB as context,
    then sends to Gemini with a carefully crafted prompt.
    
    Args:
        question: Teacher's question in natural language
        
    Returns:
        str: AI-generated answer based on the database context
    """
    if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "your_gemini_api_key_here":
        return (
            "⚠️ **Gemini API key not configured.**\n\n"
            "Please add your Gemini API key to the `.env` file:\n"
            "```\nGOOGLE_API_KEY=your_actual_key_here\n```\n\n"
            "Get a free key at: https://aistudio.google.com/apikey"
        )
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
    except ImportError as e:
        return f"⚠️ Missing dependency: {e}. Please install: `pip install langchain-google-genai`"
    
    # Build context from the vector database
    context = _build_student_context()
    
    # Craft the RAG prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are the AI assistant for the Smart Campus Intelligence System. 
Your job is to answer questions about students, their attendance, and academic performance 
based ONLY on the data provided below from our ChromaDB vector database.

IMPORTANT RULES:
- Only use information from the provided context. Do not make up data.
- If the data doesn't contain enough information to answer, say so clearly.
- Format your responses in a clear, readable way using markdown.
- Use tables when showing multiple students' data.
- Highlight students with attendance below 75% as "At Risk".
- Be helpful and professional — you are assisting a teacher.
- Today's date is {today}.

=== DATABASE CONTEXT ===
{context}
=== END CONTEXT ==="""),
        ("human", "{question}")
    ])
    
    # Try primary model, then fallbacks if rate-limited
    models_to_try = [config.GEMINI_MODEL] + getattr(config, "GEMINI_FALLBACK_MODELS", [])
    
    last_error = None
    for model_name in models_to_try:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=config.GOOGLE_API_KEY,
                temperature=0.3
            )
            chain = prompt_template | llm | StrOutputParser()
            response = chain.invoke({
                "context": context,
                "question": question,
                "today": date.today().isoformat()
            })
            return response
        except Exception as e:
            last_error = e
            err_str = str(e)
            # Only try next model on rate limit or not-found errors
            if any(x in err_str for x in ("429", "RESOURCE_EXHAUSTED", "quota", "NOT_FOUND", "404")):
                continue
            # For any other error, fail immediately
            return f"❌ Error querying Gemini: {err_str}\n\nPlease check your API key and internet connection."
    
    return (
        f"❌ All Gemini models are currently rate-limited.\n\n"
        f"**Last error:** {last_error}\n\n"
        f"Please wait a minute and try again, or check your quota at https://ai.dev/rate-limit"
    )


def get_context_preview() -> str:
    """
    Get a preview of the context that would be sent to the LLM.
    Useful for debugging and showing what data the AI has access to.
    """
    return _build_student_context()
