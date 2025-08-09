import streamlit as st
import streamlit.components.v1 as components
from newspaper import Article
import trafilatura
import requests
from bs4 import BeautifulSoup

# Page configuration
st.set_page_config(
    page_title="Web Reader PWA 🔊",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add viewport meta tag for mobile responsiveness
st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    """,
    unsafe_allow_html=True
)

# Modern CSS with glassmorphism and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --bg-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Body and main container */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .main .block-container {
        padding: 1rem 1rem 2rem;
        max-width: 1200px;
        width: 100%;
        margin: 0 auto;
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    /* Header with glassmorphism */
    .hero-header {
        text-align: center;
        padding: 2rem;
        margin: 0 0 2rem 0;
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        box-shadow: var(--shadow);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 0;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 0 0.5rem;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        min-width: 120px;
        text-align: center;
    }
    
    @media (max-width: 480px) {
        .stTabs [data-baseweb="tab"] {
            min-width: 100%;
            margin-bottom: 4px;
        }
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        color: white;
        border-radius: 15px;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
        background: rgba(255, 255, 255, 0.15);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    /* Content containers */
    .content-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        width: 100%;
        box-sizing: border-box;
    }

    .content-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }

    /* Section headers */
    .section-header {
        color: white;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .section-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }

    .stTextInput > div > div > input:focus {
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-1px);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        min-height: 150px;
        resize: vertical;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
        resize: vertical !important;
    }

    .stTextArea > div > div > textarea:focus {
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px);
    }

    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Success/Error messages */
    .stSuccess, .stError, .stInfo {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Spinner */
    .stSpinner {
        color: white !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .streamlit-expanderContent {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .content-card {
            padding: 1.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 0 12px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero header
st.markdown('''
<div class="hero-header">
    <h1 class="hero-title">🔊 Web Reader PWA</h1>
    <p class="hero-subtitle">Transform any article or text into natural-sounding speech with AI</p>
</div>
''', unsafe_allow_html=True)


def extract_content_multiple_methods(url):
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
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
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


def create_modern_tts_component():
    return """
    <style>
        .tts-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            # width: 100%;
            # max-width: 100%;
            # box-sizing: border-box;
            # max-height: 100vh;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        
        @media (min-width: 768px) {
            .tts-container {
                display: flex;
                flex-direction: row;
                flex-wrap: wrap;
                align-items: flex-start;
            }
            
            .control-group {
                flex: 1;
                min-width: 200px;
                margin: 0.5rem;
            }
            
            .status-display {
                width: 100%;
            }
        }

        .control-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin-bottom: 1.5rem;
            width: 100%;
            flex-shrink: 0;
        }
        
        @media (max-width: 768px) {
            .control-grid {
                grid-template-columns: 1fr 1fr;
                gap: 8px;
            }
            
            .controls-section {
                grid-template-columns: 1fr;
                gap: 1.2rem;
            }
            
            .tts-btn {
                padding: 10px 12px !important;
                font-size: 0.85rem !important;
            }
            
            # .tts-container {
            #     min-height: 400px;
            #     padding: 1.2rem;
            # }
            
            .control-group {
                width: 100%;
            }
        }
        
        @media (max-width: 480px) {
            .control-grid {
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }
            
            .content-card {
                padding: 1rem !important;
            }
            
            .section-header {
                font-size: 1.5rem !important;
            }
            
            .section-subtitle {
                font-size: 0.9rem !important;
            }
            
            .controls-section {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .control-group {
                padding: 0.75rem;
            }
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
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }

        .tts-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .tts-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.3);
        }

        .tts-btn:hover::before {
            left: 100%;
        }

        .tts-btn:active {
            transform: translateY(-1px);
        }

        .tts-btn.stop {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }

        .tts-btn.pause {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #2d3748;
        }

        .tts-btn.resume {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }

        .status-display {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            color: white;
            font-weight: 500;
            margin: 0.5rem 0 1.5rem;
            min-height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            flex-shrink: 0;
        }

        .controls-section {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            width: 100%;
            box-sizing: border-box;
        }
        
        .control-group {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            width: 100%;
            box-sizing: border-box;
        }
        
        @media (min-width: 768px) {
            .controls-section {
                flex-direction: row;
                flex-wrap: wrap;
            }
            
            .control-group {
                flex: 1;
                min-width: 200px;
            }
        }
        
        # .control-group {
        #     min-width: 0; /* Prevents flex items from overflowing */
        # }

        .control-group {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            # width: 100%;
            # box-sizing: border-box;
            max-width: 100%;
        }

        .control-group label {
            color: white;
            font-weight: 500;
            display: block;
            margin-bottom: 8px;
        }

        .control-group select {
            width: 90%;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            padding: 8px 12px;
            font-size: 0.9rem;
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
            height: 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.2);
            outline: none;
            transition: all 0.3s ease;
        }

        .range-input::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .range-input::-webkit-slider-thumb:hover {
            transform: scale(1.2);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }

        .range-value {
            position: absolute;
            right: 0;
            top: -2px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        @media (max-width: 768px) {
            .control-grid {
                grid-template-columns: 1fr 1fr;
            }

            .tts-btn {
                padding: 10px 16px;
                font-size: 0.85rem;
            }

            .controls-section {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <div class="tts-container">
        <div class="control-grid">
            <button class="tts-btn" onclick="speakText()">
                🔊 Read Aloud
            </button>
            <button class="tts-btn stop" onclick="stopSpeaking()">
                ⏹️ Stop
            </button>
            <button class="tts-btn pause" onclick="pauseSpeaking()">
                ⏸️ Pause
            </button>
            <button class="tts-btn resume" onclick="resumeSpeaking()">
                ▶️ Resume
            </button>
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
        document.getElementById(
            'speedValue').textContent = speechRate.toFixed(1);
        updateStatus('⚡ Speed adjusted');
        setTimeout(() => updateStatus('Ready to read your content'), 2000);
    }

    function updatePitch() {
        const range = document.getElementById('pitchRange');
        speechPitch = parseFloat(range.value);
        document.getElementById(
            'pitchValue').textContent = speechPitch.toFixed(1);
        updateStatus('🎵 Pitch adjusted');
        setTimeout(() => updateStatus('Ready to read your content'), 2000);
    }

    function updateStatus(message) {
        const statusDiv = document.getElementById('statusDisplay');
        if (statusDiv) {
            statusDiv.textContent = message;
            statusDiv.style.transform = 'scale(1.05)';
            setTimeout(() => {
                statusDiv.style.transform = 'scale(1)';
            }, 200);
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
                updateStatus('✅ Reading completed successfully!');
                setTimeout(() => updateStatus('Ready to read your content'), 3000);
            }
            return;
        }

        const chunk = textChunks[currentChunkIndex];
        updateStatus(`🗣️ Reading part ${currentChunkIndex + 1} of ${textChunks.length}...`);

        try {
            currentUtterance = new SpeechSynthesisUtterance(chunk);

            if (selectedVoice) {
                currentUtterance.voice = selectedVoice;
            }
            currentUtterance.rate = speechRate;
            currentUtterance.pitch = speechPitch;
            currentUtterance.volume = 1;

            currentUtterance.onstart = function() {
                console.log(`✓ Started chunk ${currentChunkIndex + 1}/${textChunks.length}`);
            };

            currentUtterance.onend = function() {
                currentChunkIndex++;
                if (isPlaying) {
                    setTimeout(() => {
                        if (isPlaying) {
                            speakNextChunk();
                        }
                    }, 150);
                }
            };

            currentUtterance.onerror = function(event) {
                if (event.error === 'canceled') {
                    isPlaying = false;
                    return;
                }

                if (event.error === 'interrupted') {
                    currentChunkIndex++;
                    if (isPlaying && currentChunkIndex < textChunks.length) {
                        setTimeout(() => {
                            if (isPlaying) {
                                speakNextChunk();
                            }
                        }, 300);
                    }
                    return;
                }

                console.error('Speech error:', event.error);
                currentChunkIndex++;
                if (isPlaying && currentChunkIndex < textChunks.length) {
                    setTimeout(() => speakNextChunk(), 500);
                } else {
                    isPlaying = false;
                    updateStatus('❌ Reading failed');
                }
            };

            if (isPlaying) {
                speechSynthesis.speak(currentUtterance);
            }

        } catch (error) {
            console.error('Error creating utterance:', error);
            updateStatus('❌ Error in speech synthesis');
            isPlaying = false;
        }
    }

    function speakText() {
        if (!('speechSynthesis' in window)) {
            updateStatus('❌ Text-to-speech not supported in this browser');
            return;
        }

        if (isPlaying) {
            updateStatus('⚠️ Already reading... Please stop first.');
            setTimeout(() => updateStatus('Ready to read your content'), 2000);
            return;
        }

        // Get text from the textarea or session state
        let textToSpeak = '';
        
        // Try to get text from the textarea first
        const textElements = parent.document.querySelectorAll('textarea');
        for (let element of textElements) {
            if (element.value && element.value.trim().length > 5) {
                textToSpeak = element.value;
                break;
            }
        }
        
        // If no text in textarea, try to get from session state
        if (!textToSpeak) {
            try {
                // This is a way to access Streamlit's session state from JavaScript
                const streamlitDoc = window.parent.document;
                if (streamlitDoc) {
                    // This is a bit of a hack to get the session state
                    // It works because Streamlit stores the component's args in a script tag
                    const scripts = streamlitDoc.getElementsByTagName('script');
                    for (let script of scripts) {
                        if (script.textContent.includes('setFrameValue')) {
                            const match = script.textContent.match(/setFrameValue\([^,]+,\s*([^)]+)\)/);
                            if (match && match[1]) {
                                const state = JSON.parse(match[1]);
                                if (state && state.tts_text) {
                                    textToSpeak = state.tts_text;
                                    break;
                                }
                            }
                        }
                    }
                }
            } catch (e) {
                console.error('Error accessing session state:', e);
            }
        }

        if (!textToSpeak || textToSpeak.trim().length < 5) {
            updateStatus('❌ No text found to read. Please enter some text first.');
            setTimeout(() => updateStatus('Ready to read your content'), 3000);
            return;
        }

        updateStatus('🔄 Preparing to read...');

        speechSynthesis.cancel();

        setTimeout(() => {
            textChunks = splitTextIntoChunks(textToSpeak);
            currentChunkIndex = 0;
            isPlaying = true;
            isPaused = false;

            updateStatus(`🚀 Starting to read ${textChunks.length} parts...`);

            setTimeout(() => {
                if (isPlaying) {
                    speakNextChunk();
                }
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
            setTimeout(() => updateStatus('Ready to read your content'), 2000);
        }
    }

    function resumeSpeaking() {
        if (isPaused && speechSynthesis.paused) {
            speechSynthesis.resume();
            isPaused = false;
            isPlaying = true;
            updateStatus(`▶️ Resuming... (part ${currentChunkIndex + 1} of ${textChunks.length})`);
        } else if (!isPaused && !isPlaying) {
            updateStatus('⚠️ Nothing to resume. Click "Read Aloud" to start.');
            setTimeout(() => updateStatus('Ready to read your content'), 3000);
        }
    }

    window.addEventListener('beforeunload', function() {
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }
    });
    </script>
    """


# Main tabs with content cards
tab1, tab2 = st.tabs(["🌐 Web Content Extractor", "📝 Text Input"])

with tab1:
    st.markdown('''
    <div class="content-card">
        <div class="section-header">
            🌐 Web Content Extractor
        </div>
        <div class="section-subtitle">
            Enter a URL to extract and listen to article content with AI-powered extraction
        </div>
    </div>
    ''', unsafe_allow_html=True)

    url_input = st.text_input(
        "",
        placeholder="https://example.com/article",
        label_visibility="collapsed",
        key="url_input"
    )

    if url_input:
        with st.spinner("🔍 Extracting content with AI..."):
            result = extract_content_multiple_methods(url_input)

        if result["method"] != "error":
            st.success(
                f"✅ Content extracted successfully using {result['method']}")
            if result["title"]:
                st.info(f"📄 **Title:** {result['title']}")

            st.markdown('''
            <div class="content-card">
                <div class="section-header">
                    📝 Review & Edit Content
                </div>
                <div class="section-subtitle">
                    Verify the extracted content and make any necessary edits before reading
                </div>
            </div>
            ''', unsafe_allow_html=True)

            verified_content = st.text_area(
                "",
                value=result["content"],
                height=350,
                key="web_content",
                label_visibility="collapsed"
            )

            if verified_content:
                st.markdown("### 🎙️ Text-to-Speech Controls")
                components.html(create_modern_tts_component(), height=750)

        else:
            st.error(f"❌ {result['content']}")

with tab2:
    st.markdown('''
    <div class="content-card">
        <div class="section-header">
            📝 Text Input
        </div>
        <div class="section-subtitle">
            Enter your text here to listen to it with AI-powered text-to-speech
        </div>
    </div>''', unsafe_allow_html=True)

    # Text input area with responsive height
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='responsive-textarea-container'>",
                    unsafe_allow_html=True)
        text_input = st.text_area(
            "",
            placeholder="Enter your text here...",
            label_visibility="collapsed",
            key="text_input",
            height=200
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Add some space
    st.write("")

    # TTS Controls
    if text_input.strip():
        st.markdown("### 🎙️ Text-to-Speech Controls")

        # Store the text in the session state to make it accessible to the TTS component
        if 'tts_text' not in st.session_state:
            st.session_state.tts_text = ""
        st.session_state.tts_text = text_input

        # Add the TTS component with responsive height
        st.markdown("<div class='responsive-tts-container'>",
                    unsafe_allow_html=True)
        components.html(create_modern_tts_component(), height=500)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(
            "✏️ Click here after entering the text above to enable the Text-to-Speech controls.")

    # Add responsive styles
    st.markdown("""
    <style>
        .responsive-textarea-container {
            width: 100%;
            margin-bottom: 1.5rem;
        }
        
        .responsive-tts-container {
            width: 100%;
            margin: 0 auto;
        }
        
        @media (max-width: 768px) {
            .responsive-textarea-container {
                margin-bottom: 1rem;
            }
            
            .responsive-tts-container {
                height: auto !important;
            }
            
            iframe {
                min-height: 400px;
            }
        }
        
        @media (max-width: 480px) {
            .responsive-textarea-container textarea {
                min-height: 200px !important;
            }
            
            .responsive-tts-container iframe {
                min-height: 450px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
