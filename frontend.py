
import streamlit as st
from backend import handle_pdf_upload, handle_question

st.set_page_config(
    page_title="PDF Q&A System",
    page_icon="📚",
    layout="wide"
)

st.title("PDF Q&A System")
st.markdown("Upload any PDF and ask questions!")

# sidebar
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose PDF file",
        type="pdf"
    )

    process_btn = st.button("⚙️ Process PDF")

    if process_btn and uploaded_file:
        if st.session_state.get("current_pdf") != uploaded_file.name:
            with st.spinner("⏳ Processing PDF..."):
                vectorstore, msg = handle_pdf_upload(uploaded_file)
                if vectorstore is not None:
                    st.session_state.vectorstore = vectorstore
                    st.session_state.current_pdf = uploaded_file.name
                    st.session_state.history     = [] 
                    # st.success("✅ PDF Ready!")
                else:
                    st.error(f"❌ Error: {msg}")
        # else:
        #     st.info("✅ Same PDF already loaded!")

    # Status
    if "vectorstore" in st.session_state and st.session_state.vectorstore is not None:
        st.success(f"Loaded: {st.session_state.get('current_pdf', '')}")
    else:
        st.warning("⚠️ Upload PDF then click Process")

# questions input
question = st.text_input(
    "Type your question here...",
    placeholder="What is this document about?"
)

ask_button = st.button("🔍 Get Answer")

# ─── ANSWER ───────────────────────────────────
if ask_button and question:
    if "vectorstore" not in st.session_state or st.session_state.vectorstore is None:
        st.error("⚠️ Please upload PDF and click Process first!")
    else:
        with st.spinner("Finding answer..."):
            answer = handle_question(
                st.session_state.vectorstore,
                question
            )
        st.markdown("💡 Answer:")
        st.write(answer)

        # History save karo
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({
            "q": question,
            "a": answer
        })

# history
if "history" in st.session_state and st.session_state.history:
    st.markdown("---")
    st.markdown("### 📝 Previous Questions")
    for item in reversed(st.session_state.history):
        with st.expander(f"Q: {item['q'][:60]}..."):
            st.markdown(f"**Question:** {item['q']}")
            st.markdown(f"**Answer:** {item['a']}")