import streamlit as st
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.document_processor import extract_text_from_txt

# --- Load API Key ---
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# --- Page config ---
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 2rem;
        border-radius: 10px;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stTextInput>div>div>input {
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("<h1 style='text-align: center;'>🤖 Fine-Tuned RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Ask questions and get responses based on your uploaded document!</p>", unsafe_allow_html=True)

# --- Initialize session state ---
if 'chunks' not in st.session_state:
    st.session_state.chunks = []
if 'vectorizer' not in st.session_state:
    st.session_state.vectorizer = None
if 'chunk_vectors' not in st.session_state:
    st.session_state.chunk_vectors = None
if 'file_loaded' not in st.session_state:
    st.session_state.file_loaded = False

# --- Sidebar ---
st.sidebar.header("📂 File Input")
txt_file_path = st.sidebar.text_input("Enter the .txt filename (from 'data/' folder)", value="document.txt")

# Load file when path changes or Load button is clicked
load_file = st.sidebar.button("📂 Load File")

if load_file or (txt_file_path and not st.session_state.file_loaded):
    if txt_file_path:
        try:
            st.session_state.chunks = extract_text_from_txt(txt_file_path)
            
            # Pre-compute vectorization for better performance
            if st.session_state.chunks:
                st.session_state.vectorizer = TfidfVectorizer()
                st.session_state.chunk_vectors = st.session_state.vectorizer.fit_transform(st.session_state.chunks)
                st.session_state.file_loaded = True
                st.sidebar.success("✅ File loaded successfully!")
            else:
                st.sidebar.warning("⚠️ No text chunks found in the file.")
                
        except FileNotFoundError:
            st.sidebar.error("❌ File not found in the 'data/' folder.")
            st.session_state.file_loaded = False
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")
            st.session_state.file_loaded = False

# Model Info
MODEL_NAME = "gpt-4"
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Model Info")
st.sidebar.write(f"**Current Model:** {MODEL_NAME}")
st.sidebar.write(f"**Indexed Chunks:** {len(st.session_state.chunks)}")
st.sidebar.write(f"**File Status:** {'✅ Loaded' if st.session_state.file_loaded else '❌ Not Loaded'}")

# --- Main Content ---
st.markdown("### 💬 Ask Your Question:")

# Create columns for better layout
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input("Type your question here...", key="query_input")

with col2:
    search_button = st.button("🔍 Search", key="search_btn")

# Alternative: Use form for better UX (Enter key support)
with st.form("search_form"):
    query_form = st.text_input("Or use this input with Enter key support:", key="query_form")
    search_form_button = st.form_submit_button("🔍 Search with Form")

# Handle search from either input method
current_query = query if search_button else (query_form if search_form_button else "")
perform_search = (search_button or search_form_button) and current_query.strip()

# Validation and Search Logic
if perform_search:
    if not st.session_state.file_loaded:
        st.error("❌ Please load a file first before searching.")
    elif not st.session_state.chunks:
        st.error("❌ No content available to search. Please check your file.")
    else:
        try:
            with st.spinner("🔍 Searching for relevant content..."):
                # Use pre-computed vectors for better performance
                query_vector = st.session_state.vectorizer.transform([current_query])
                similarities = cosine_similarity(query_vector, st.session_state.chunk_vectors)
                
                # Get top chunks (ensure we have enough chunks to work with)
                num_results = min(5, len(st.session_state.chunks))  # Get top 5 or all available chunks
                indices = similarities.argsort()[0][-num_results:][::-1]
                similarity_scores = similarities[0][indices]
                
                st.markdown("### 📄 Top Relevant Chunks:")
                
                # Show at least 3 results, but filter very low similarity scores
                results_shown = 0
                min_results = 3
                
                for i, (idx, score) in enumerate(zip(indices, similarity_scores)):
                    # Show result if it meets threshold OR we haven't shown minimum results yet
                    if score > 0.05 or results_shown < min_results:
                        results_shown += 1
                        
                        # Color code based on relevance
                        if score > 0.3:
                            border_color = "#4CAF50"  # Green for high relevance
                            relevance_label = "High"
                        elif score > 0.1:
                            border_color = "#FF9800"  # Orange for medium relevance
                            relevance_label = "Medium"
                        else:
                            border_color = "#9E9E9E"  # Gray for low relevance
                            relevance_label = "Low"
                        
                        st.markdown(f"**Result {results_shown}:** (Similarity: {score:.3f} - {relevance_label} Relevance)")
                        st.markdown(
                            f"<div style='background-color: #ffffff; padding: 1rem; border-radius: 5px; "
                            f"border-left: 4px solid {border_color}; margin: 10px 0; text-align: justify;'>"
                            f"{st.session_state.chunks[idx]}</div>",
                            unsafe_allow_html=True
                        )
                        
                        if results_shown < len(indices) and results_shown < num_results:
                            st.markdown("<hr>", unsafe_allow_html=True)
                        
                        # Stop after showing reasonable number of results
                        if results_shown >= 5:
                            break
                
                if results_shown == 0:
                    st.warning("⚠️ No content found for your query. Try rephrasing your question.")
                elif results_shown < min_results and len(st.session_state.chunks) < min_results:
                    st.info(f"ℹ️ Only {len(st.session_state.chunks)} chunks available in the document.")
                    
        except Exception as e:
            st.error(f"❌ Error during similarity search: {e}")
            st.error("Please check your input and try again.")

# Instructions for users
if not st.session_state.file_loaded:
    st.info("📝 **Instructions:**\n1. Enter your .txt filename in the sidebar\n2. Click 'Load File' to process the document\n3. Ask questions using either search method above")

# Debug information (can be removed in production)
if st.checkbox("🔧 Show Debug Info", key="debug_checkbox"):
    st.write("**Debug Information:**")
    st.write(f"- Chunks loaded: {len(st.session_state.chunks)}")
    st.write(f"- File loaded status: {st.session_state.file_loaded}")
    st.write(f"- Vectorizer initialized: {st.session_state.vectorizer is not None}")
    st.write(f"- Current query: '{current_query}'")
    st.write(f"- Perform search: {perform_search}")