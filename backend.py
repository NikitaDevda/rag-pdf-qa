import tempfile
import os
from ml_logic import process_pdf, get_answer_from_rag

# pdf processing
def handle_pdf_upload(uploaded_file):
    """
    Frontend se PDF receive karo
    Temporary file mein save karo
    ML logic ko bhejo
    """
    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        vectorstore = process_pdf(temp_path)

        os.unlink(temp_path)

        return vectorstore, "PDF processed successfully!"

    except Exception as e:
        return None, f"Error: {str(e)}"


# question handling
def handle_question(vectorstore, question):
    """
    User ka question receive karo
    ML logic se answer lo
    Frontend ko return karo
    """
    try:
        if not vectorstore:
            return "Please upload PDF first!"

        if not question:
            return "Please enter a question!"

        answer = get_answer_from_rag(
            vectorstore,
            question
        )
        return answer

    except Exception as e:
        return f"Error getting answer: {str(e)}"


# session management
def save_to_history(session_state, question, answer):
    """
    Chat history save karo
    """
    if "history" not in session_state:
        session_state.history = []

    session_state.history.append({
        "question": question,
        "answer": answer
    })
    return session_state
