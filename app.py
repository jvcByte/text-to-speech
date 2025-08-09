import streamlit as st
import streamlit.components.v1 as components
from newspaper import Article
import trafilatura
import requests
from bs4 import BeautifulSoup

# Page configuration
st.set_page_config(
    page_title="Crawl It 🔊",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, modern CSS with consistent styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* App background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    /* Main container */
    .main .block-container {
        padding: 1rem;
        max-width: 1000px;
        margin: 0 auto;
    }

    /* Hero header */
    .hero-container {
        text-align: center;
        padding: 2rem;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    /* Content cards */
    .content-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .section-header {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .section-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.3s ease;
        padding: 0.75rem 1.5rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        resize: vertical !important;
    }

    .stTextArea > div > div > textarea:focus {
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
    }

    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Alert styling */
    .stSuccess, .stError, .stInfo {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .content-card {
            padding: 1rem;
        }
        
        .main .block-container {
            padding: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero header
st.markdown('''
<div class="hero-container">
    <h1 class="hero-title">🔊 Crawl It 🔊</h1>
    <p class="hero-subtitle">Transform any article or text into natural-sounding speech</p>
    <p class="hero-subtitle">Copy and paste a link to any article or paste the raw text using the text input and listen to them instantly</p>
</div>
''', unsafe_allow_html=True)


def extract_content_multiple_methods(url):
    """Extract content from URL using multiple methods"""
    try:
        downloaded = trafilatura.fetch_url(url)
        content = trafilatura.extract(downloaded)
        if content and len(content.strip()) > 100:
            return {"method": "trafilatura", "content": content, "title": ""}
    except:
        pass

    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.text and len(article.text.strip()) > 100:
            return {"method": "newspaper3k", "content": article.text, "title": article.title}
    except:
        pass

    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()

        main_content = soup.find('main') or soup.find('article') or soup.find(
            'div', class_=['content', 'post', 'article'])
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content = '\n'.join(lines)
        title = soup.find('title').get_text() if soup.find('title') else ""

        return {"method": "beautifulsoup", "content": content, "title": title}
    except Exception as e:
        return {"method": "error", "content": f"Error extracting content: {str(e)}", "title": ""}


def create_tts_component():
    """Create the Text-to-Speech component"""
    return """
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }
        
        .tts-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            font-family: 'Inter', sans-serif;
            width: 100%;
            box-sizing: border-box;
        }

        .control-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-bottom: 1.5rem;
        }

        .tts-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .tts-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }

        .tts-btn.stop { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        .tts-btn.pause { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #2d3748; }
        .tts-btn.resume { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

        .status-display {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            color: white;
            font-weight: 500;
            margin-bottom: 1.5rem;
            min-height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .controls-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }

        .control-group {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .control-group label {
            color: white;
            font-weight: 500;
            display: block;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }

        .control-group select {
            width: 100%;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            color: white;
            padding: 8px 12px;
            font-size: 0.9rem;
            outline: none;
        }

        .control-group select:focus {
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
        }

        .control-group select option {
            background: #2d3748;
            color: white;
        }

        .range-container {
            position: relative;
        }

        .range-input {
            -webkit-appearance: none;
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.3);
            outline: none;
            margin: 8px 0;
        }

        .range-input::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            border: 2px solid white;
            transition: all 0.3s ease;
        }

        .range-input::-webkit-slider-thumb:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        }

        .range-input::-moz-range-thumb {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            border: 2px solid white;
        }

        .range-value {
            position: absolute;
            right: 0;
            top: -8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            min-width: 32px;
            text-align: center;
        }

        @media (max-width: 768px) {
            .control-grid {
                grid-template-columns: 1fr 1fr;
                gap: 8px;
            }
            
            .controls-section {
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }
            
            .tts-btn {
                padding: 10px 16px;
                font-size: 0.85rem;
            }
        }
    </style>

    <body>
        <div class="tts-container">
            <div class="control-grid">
                <button class="tts-btn" onclick="speakText()">🔊 Read Aloud</button>
                <button class="tts-btn stop" onclick="stopSpeaking()">⏹️ Stop</button>
                <button class="tts-btn pause" onclick="pauseSpeaking()">⏸️ Pause</button>
                <button class="tts-btn resume" onclick="resumeSpeaking()">▶️ Resume</button>
            </div>

            <div class="status-display" id="statusDisplay">
                Ready to read your content
            </div>

            <div class="controls-section">
                <div class="control-group">
                    <label for="voiceSelect">🎤 Voice Selection</label>
                    <select id="voiceSelect" onchange="updateVoice()">
                        <option value="">Default Voice</option>
                    </select>
                </div>

                <div class="control-group">
                    <label for="speedRange">⚡ Speed</label>
                    <div class="range-container">
                        <input type="range" class="range-input" id="speedRange" min="0.5" max="2" step="0.1" value="1" onchange="updateSpeed()">
                        <span class="range-value" id="speedValue">1.0</span>
                    </div>
                </div>

                <div class="control-group">
                    <label for="pitchRange">🎵 Pitch</label>
                    <div class="range-container">
                        <input type="range" class="range-input" id="pitchRange" min="0" max="2" step="0.1" value="1" onchange="updatePitch()">
                        <span class="range-value" id="pitchValue">1.0</span>
                    </div>
                </div>
            </div>
        </div>
    </body>

    <script>
    let currentUtterance = null;
    let voices = [];
    let selectedVoice = null;
    let speechRate = 1;
    let speechPitch = 1;
    let isPaused = false;
    let isPlaying = false;
    let textChunks = [];
    let currentChunkIndex = 0;

    function loadVoices() {
        voices = speechSynthesis.getVoices();
        const voiceSelect = document.getElementById('voiceSelect');
        voiceSelect.innerHTML = '<option value="">Default Voice</option>';

        voices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${voice.name} (${voice.lang})`;
            voiceSelect.appendChild(option);
        });
    }

    speechSynthesis.onvoiceschanged = loadVoices;
    loadVoices();

    function updateVoice() {
        const select = document.getElementById('voiceSelect');
        selectedVoice = voices[select.value] || null;
        updateStatus('🎤 Voice updated');
        setTimeout(() => updateStatus('Ready to read your content'), 2000);
    }

    function updateSpeed() {
        const range = document.getElementById('speedRange');
        speechRate = parseFloat(range.value);
        document.getElementById('speedValue').textContent = speechRate.toFixed(1);
        updateStatus('⚡ Speed adjusted');
        setTimeout(() => updateStatus('Ready to read your content'), 2000);
    }

    function updatePitch() {
        const range = document.getElementById('pitchRange');
        speechPitch = parseFloat(range.value);
        document.getElementById('pitchValue').textContent = speechPitch.toFixed(1);
        updateStatus('🎵 Pitch adjusted');
        setTimeout(() => updateStatus('Ready to read your content'), 2000);
    }

    function updateStatus(message) {
        const statusDiv = document.getElementById('statusDisplay');
        if (statusDiv) {
            statusDiv.textContent = message;
        }
    }

    function splitTextIntoChunks(text, maxLength = 200) {
        const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
        const chunks = [];
        let currentChunk = '';

        sentences.forEach(sentence => {
            if ((currentChunk + sentence).length > maxLength) {
                if (currentChunk) {
                    chunks.push(currentChunk.trim());
                    currentChunk = '';
                }
            }
            currentChunk += sentence;
        });

        if (currentChunk) {
            chunks.push(currentChunk.trim());
        }

        return chunks.length > 0 ? chunks : [text];
    }

    function speakNextChunk() {
        if (!isPlaying || currentChunkIndex >= textChunks.length) {
            if (currentChunkIndex >= textChunks.length) {
                isPlaying = false;
                updateStatus('✅ Reading completed!');
                setTimeout(() => updateStatus('Ready to read your content'), 3000);
            }
            return;
        }

        const chunk = textChunks[currentChunkIndex];
        updateStatus(`🗣️ Reading part ${currentChunkIndex + 1} of ${textChunks.length}...`);

        currentUtterance = new SpeechSynthesisUtterance(chunk);
        
        if (selectedVoice) currentUtterance.voice = selectedVoice;
        currentUtterance.rate = speechRate;
        currentUtterance.pitch = speechPitch;
        currentUtterance.volume = 1;

        currentUtterance.onend = function() {
            currentChunkIndex++;
            if (isPlaying) {
                setTimeout(() => {
                    if (isPlaying) speakNextChunk();
                }, 150);
            }
        };

        currentUtterance.onerror = function(event) {
            if (event.error === 'canceled') {
                isPlaying = false;
                return;
            }
            
            currentChunkIndex++;
            if (isPlaying && currentChunkIndex < textChunks.length) {
                setTimeout(() => speakNextChunk(), 300);
            } else {
                isPlaying = false;
                updateStatus('❌ Reading failed');
            }
        };

        if (isPlaying) {
            speechSynthesis.speak(currentUtterance);
        }
    }

    function speakText() {
        if (!('speechSynthesis' in window)) {
            updateStatus('❌ Text-to-speech not supported');
            return;
        }

        if (isPlaying) {
            updateStatus('⚠️ Already reading... Please stop first.');
            return;
        }

        let textToSpeak = '';
        
        // Get text from textarea - try multiple selectors
        const parentDoc = window.parent.document;
        
        // Try different ways to get the textarea
        let textElements = parentDoc.querySelectorAll('textarea[data-testid*="textArea"]');
        if (!textElements.length) {
            textElements = parentDoc.querySelectorAll('textarea');
        }
        
        for (let element of textElements) {
            if (element.value && element.value.trim().length > 5) {
                textToSpeak = element.value;
                break;
            }
        }

        // Fallback: try to get text from any visible textarea
        if (!textToSpeak) {
            const allTextareas = parentDoc.querySelectorAll('textarea');
            for (let textarea of allTextareas) {
                if (textarea.offsetParent !== null && textarea.value && textarea.value.trim().length > 5) {
                    textToSpeak = textarea.value;
                    break;
                }
            }
        }

        if (!textToSpeak || textToSpeak.trim().length < 5) {
            updateStatus('❌ No text found to read. Please enter some text first.');
            return;
        }

        speechSynthesis.cancel();
        
        setTimeout(() => {
            textChunks = splitTextIntoChunks(textToSpeak);
            currentChunkIndex = 0;
            isPlaying = true;
            isPaused = false;

            updateStatus(`🚀 Starting to read ${textChunks.length} parts...`);
            
            setTimeout(() => {
                if (isPlaying) speakNextChunk();
            }, 200);
        }, 300);
    }

    function stopSpeaking() {
        isPlaying = false;
        isPaused = false;
        speechSynthesis.cancel();
        updateStatus('⏹️ Reading stopped');
        
        setTimeout(() => {
            currentChunkIndex = 0;
            textChunks = [];
            currentUtterance = null;
            updateStatus('Ready to read your content');
        }, 500);
    }

    function pauseSpeaking() {
        if (speechSynthesis.speaking && !isPaused && isPlaying) {
            speechSynthesis.pause();
            isPaused = true;
            isPlaying = false;
            updateStatus('⏸️ Reading paused');
        } else {
            updateStatus('⚠️ Nothing to pause');
        }
    }

    function resumeSpeaking() {
        if (isPaused && speechSynthesis.paused) {
            speechSynthesis.resume();
            isPaused = false;
            isPlaying = true;
            updateStatus(`▶️ Resuming... (part ${currentChunkIndex + 1} of ${textChunks.length})`);
        } else {
            updateStatus('⚠️ Nothing to resume. Click "Read Aloud" to start.');
        }
    }

    window.addEventListener('beforeunload', function() {
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }
    });
    </script>
    """


# Main tabs
tab1, tab2 = st.tabs(["🌐 Web Content Extractor", "📝 Text Input"])

with tab1:
    st.markdown('''
    <div class="content-card">
        <div class="section-header">🌐 Web Content Extractor</div>
        <div class="section-subtitle">Enter a URL to extract and listen to article content</div>
    </div>
    ''', unsafe_allow_html=True)

    url_input = st.text_input(
        "",
        placeholder="https://example.com/article",
        label_visibility="collapsed",
        key="url_input"
    )

    if url_input:
        with st.spinner("🔍 Extracting content..."):
            result = extract_content_multiple_methods(url_input)

        if result["method"] != "error":
            st.success(f"✅ Content extracted using {result['method']}")
            
            if result["title"]:
                st.info(f"📄 **Title:** {result['title']}")

            st.markdown('''
            <div class="content-card">
                <div class="section-header">📝 Review & Edit Content</div>
                <div class="section-subtitle">Verify the content and make edits before reading</div>
            </div>
            ''', unsafe_allow_html=True)

            verified_content = st.text_area(
                "",
                value=result["content"],
                height=300,
                key="web_content",
                label_visibility="collapsed"
            )

            if verified_content:
                st.markdown("### 🎙️ Text-to-Speech Controls")
                components.html(create_tts_component(), height=600)

        else:
            st.error(f"❌ {result['content']}")

with tab2:
    st.markdown('''
    <div class="content-card">
        <div class="section-header">📝 Text Input</div>
        <div class="section-subtitle">Enter your text here to listen to it with text-to-speech</div>
    </div>
    ''', unsafe_allow_html=True)

    text_input = st.text_area(
        "",
        placeholder="Enter your text here...",
        label_visibility="collapsed",
        key="text_input",
        height=200
    )

    # Always show the TTS component
    st.markdown("### 🎙️ Text-to-Speech Controls")
    
    if text_input.strip():
        # Store text in session state for the component to access
        st.session_state.current_text = text_input
        components.html(create_tts_component(), height=600)
    else:
        # Show component even with no text, but with a message
        st.session_state.current_text = ""
        components.html(create_tts_component(), height=600)
        st.info("✏️ Enter text above to enable reading.")