import streamlit as st
import requests
import json
import datetime

# Set page config
st.set_page_config(
    page_title="தமிழ் AI கவிதை & கதை ஜெனரேட்டர்",
    page_icon="📜",
    layout="wide"
)

# Custom CSS with Tamil font support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap');
    
    body, .generated-text, textarea, input {
        font-family: 'Noto Sans Tamil', 'Latha', 'Arial Unicode MS', sans-serif !important;
    }
    
    .title {
        color: #2e7d32;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    
    .generated-text {
        font-size: 18px;
        line-height: 1.8;
        white-space: pre-line;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #2e7d32;
        color: #212529 !important;
        margin-top: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        font-size: 16px;
        padding: 8px 20px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Mistral API configuration
MISTRAL_API_KEY = "kikzWsaFDjKcHiV6gUCkp3jyUx6ojNqt"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def generate_text(title, poem_type, prompt, genre, max_length=300):
    """Generate Tamil text using Mistral API"""
    try:
        if genre == "கவிதை":
            system_prompt = """You are a Tamil poet. Write beautiful Tamil poems with rhyme and rhythm."""
            user_prompt = f"""பின்வரும் தலைப்பில் {poem_type} வகை தமிழ் கவிதை எழுதுக:
            தலைப்பு: {title}
            விளக்கம்: {prompt}
            • 4-6 வரிகள்
            • அழகான தமிழ்
            • ஓசை நயம்"""
        else:
            system_prompt = """You are a Tamil storyteller. Write engaging Tamil stories with simple language and interesting endings."""
            user_prompt = f"""பின்வரும் தலைப்பில் {poem_type} வகை தமிழ் கதை எழுதுக:
            தலைப்பு: {title}
            விளக்கம்: {prompt}
            • 5-10 வாக்கியங்கள்
            • எளிய தமிழ்
            • சுவாரஸ்யமான முடிவு"""
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "open-mistral-7b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_length,
            "top_p": 0.9
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"பிழை: {str(e)}")
        return None

def create_html_file(title, genre, poem_type, content):
    """Create HTML content with proper styling"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ta">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap');
            body {{
                font-family: 'Noto Sans Tamil', sans-serif;
                line-height: 1.8;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1 {{
                color: #2e7d32;
                text-align: center;
                border-bottom: 2px solid #2e7d32;
                padding-bottom: 10px;
            }}
            .meta {{
                text-align: center;
                font-style: italic;
                margin-bottom: 30px;
                color: #555;
            }}
            .content {{
                white-space: pre-line;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="meta">
            <p>வகை: {genre} ({poem_type})</p>
            <p>உருவாக்கப்பட்ட தேதி: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        <div class="content">
            {content}
        </div>
    </body>
    </html>
    """
    return html_content

def download_file(content, filename):
    """Create download button for the file"""
    st.download_button(
        label="கோப்பை பதிவிறக்குக",
        data=content.encode('utf-8'),
        file_name=filename,
        mime="text/html"
    )

# Main app
def main():
    st.markdown("<h1 class='title'>தமிழ் AI கவிதை & கதை ஜெனரேட்டர்</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("அமைப்புகள்")
        genre = st.radio("தேர்வு செய்க:", ("கவிதை", "கதை"), index=0)
        
        if genre == "கவிதை":
            poem_type = st.selectbox(
                "கவிதை வகை:",
                ("எண்சீர் விருத்தம்", "குறளடி", "வெண்பா", "ஆசிரியப்பா", "மரபற்ற கவிதை")
            )
        else:
            poem_type = st.selectbox(
                "கதை வகை:",
                ("நீதிக் கதை", "அறிவியல் புனைகதை", "காதல் கதை", "திகில் கதை", "வரலாற்று கதை")
            )
        
        length = st.slider("உரையின் நீளம்:", 100, 500, 250, 50)
        
        st.markdown("---")
        st.markdown("""
        **வழிமுறைகள்:**  
        1. வகையை தேர்ந்தெடுக்கவும்  
        2. தலைப்பு மற்றும் விளக்கத்தை உள்ளிடவும்  
        3. "உருவாக்கு" பொத்தானை அழுத்தவும்  
        4. HTML கோப்பாக பதிவிறக்கலாம்
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("தலைப்பு:", placeholder="எ.கா: கடலின் அழகு")
    with col2:
        prompt = st.text_input("விளக்கம்:", placeholder="எ.கா: கடலின் அழகை பற்றிய கவிதை")
    
    if st.button("உருவாக்கு", type="primary"):
        if not title.strip() or not prompt.strip():
            st.warning("தயவு செய்து தலைப்பு மற்றும் விளக்கத்தை உள்ளிடவும்!")
        else:
            with st.spinner(f"AI உங்கள் {genre} உருவாக்குகிறது..."):
                generated_text = generate_text(title, poem_type, prompt, genre, length)
                
                if generated_text:
                    st.markdown("---")
                    st.subheader(f"உங்கள் {genre}:")
                    st.markdown(f'<div class="generated-text">{generated_text}</div>', unsafe_allow_html=True)
                    
                    # Create HTML file
                    html_content = create_html_file(title, genre, poem_type, generated_text)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"tamil_{genre}_{timestamp}.html"
                    
                    # Download buttons
                    st.markdown("---")
                    st.subheader("பதிவிறக்கம்")
                    download_file(html_content, filename)
                else:
                    st.error("உரை உருவாக்கத்தில் பிழை ஏற்பட்டுள்ளது")

if __name__ == "__main__":
    main()