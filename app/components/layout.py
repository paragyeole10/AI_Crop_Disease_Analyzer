import streamlit as st
import os

def inject_custom_css():
    """
    Injects custom CSS styling for premium SaaS aesthetics.
    """
    st.markdown("""
    <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        /* Apply globally */
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Clean layout changes */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Hero section styling */
        .hero-container {
            background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
            border-radius: 16px;
            padding: 3rem 2.5rem;
            color: white;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 25px rgba(46, 125, 50, 0.15);
            position: relative;
            overflow: hidden;
        }
        .hero-container::after {
            content: '';
            position: absolute;
            bottom: -50px;
            right: -50px;
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 50%;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        .hero-subtitle {
            font-size: 1.25rem;
            font-weight: 300;
            opacity: 0.9;
            max-width: 700px;
            line-height: 1.5;
        }
        
        /* Modern card styles */
        .feature-card {
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
            border-color: #2E7D32;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        .feature-title {
            font-weight: 600;
            font-size: 1.15rem;
            color: #1E293B;
            margin-bottom: 0.5rem;
        }
        .feature-text {
            font-size: 0.95rem;
            color: #64748B;
            line-height: 1.4;
        }
        
        /* Dashboard Results card styles */
        .result-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        .badge-healthy {
            background-color: #E8F5E9;
            color: #2E7D32;
        }
        .badge-diseased {
            background-color: #FFEBEE;
            color: #C62828;
        }
        
        .metric-value {
            font-size: 2.25rem;
            font-weight: 700;
            color: #1E293B;
            line-height: 1.1;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #2E7D32;
        }
        
        /* Card details in results */
        .details-box {
            background: #F8FAF8;
            border-left: 4px solid #2E7D32;
            padding: 1.25rem;
            border-radius: 0 12px 12px 0;
            margin-bottom: 1rem;
        }
        .details-box-title {
            font-weight: 600;
            font-size: 1.05rem;
            color: #1E293B;
            margin-bottom: 0.4rem;
        }
        .details-box-content {
            font-size: 0.95rem;
            color: #475569;
            line-height: 1.4;
        }
        
        /* Marketplace custom styles */
        .recommendation-banner {
            background: linear-gradient(135deg, #1E3A8A 0%, #2E7D32 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        .recommendation-banner-content {
            flex: 1;
        }
        .recommendation-banner-title {
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: 0.25rem;
        }
        .recommendation-banner-text {
            font-size: 0.95rem;
            opacity: 0.9;
        }
        
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .prod-card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.25rem;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            position: relative;
        }
        .prod-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border-color: #2E7D32;
        }
        .prod-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #E8F5E9;
            color: #2E7D32;
            padding: 0.2rem 0.5rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .prod-icon {
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
        }
        .prod-title {
            font-weight: 700;
            font-size: 1.1rem;
            color: #1E293B;
            margin-bottom: 0.5rem;
            min-height: 2.2rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .prod-desc {
            font-size: 0.85rem;
            color: #64748B;
            margin-bottom: 1rem;
            min-height: 3rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .prod-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .prod-price {
            font-weight: 800;
            font-size: 1.25rem;
            color: #2E7D32;
        }
        .prod-rating {
            font-size: 0.85rem;
            color: #F59E0B;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        /* Stepper tracking styles */
        .stepper-wrapper {
            display: flex;
            justify-content: space-between;
            margin: 2rem 0;
            position: relative;
        }
        .stepper-item {
            flex: 1;
            text-align: center;
            position: relative;
            z-index: 2;
        }
        .stepper-item::before {
            position: absolute;
            content: '';
            border-bottom: 3px solid #E2E8F0;
            width: 100%;
            top: 20px;
            left: -50%;
            z-index: -1;
        }
        .stepper-item:first-child::before {
            content: none;
        }
        .stepper-item .step-counter {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #E2E8F0;
            margin: 0 auto 10px auto;
            font-weight: bold;
            color: #64748B;
            font-size: 1rem;
        }
        .stepper-item.completed .step-counter {
            background-color: #2E7D32;
            color: white;
        }
        .stepper-item.completed::before {
            border-bottom: 3px solid #2E7D32;
        }
        .stepper-item.active .step-counter {
            background-color: #2E7D32;
            color: white;
            box-shadow: 0 0 0 4px rgba(46, 125, 50, 0.2);
        }
        .stepper-item .step-name {
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748B;
        }
        .stepper-item.active .step-name {
            color: #2E7D32;
        }
        .stepper-item.completed .step-name {
            color: #1E293B;
        }
        
        /* Responsive Mobile Adjustments */
        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
            }
            .hero-container {
                padding: 1.5rem 1.25rem !important;
                margin-bottom: 1.5rem !important;
            }
            .hero-title {
                font-size: 2rem !important;
            }
            .hero-subtitle {
                font-size: 0.95rem !important;
            }
            .result-card {
                padding: 1.25rem !important;
                margin-bottom: 1rem !important;
            }
            .metric-value {
                font-size: 1.75rem !important;
            }
            
            /* Responsive Stepper Timeline */
            .stepper-wrapper {
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 1.5rem !important;
                margin: 1.5rem 0 !important;
                padding-left: 0.5rem !important;
            }
            .stepper-item {
                display: flex !important;
                align-items: center !important;
                gap: 1.25rem !important;
                text-align: left !important;
                width: 100% !important;
                position: relative !important;
            }
            .stepper-item::before {
                position: absolute !important;
                content: '' !important;
                border-left: 3px solid #E2E8F0 !important;
                border-bottom: none !important;
                width: 3px !important;
                height: 1.5rem !important;
                top: -1.5rem !important;
                left: 20px !important;
                z-index: -1 !important;
            }
            .stepper-item:first-child::before {
                content: none !important;
            }
            .stepper-item.completed::before {
                border-left: 3px solid #2E7D32 !important;
                border-bottom: none !important;
            }
            .stepper-item .step-counter {
                margin: 0 !important;
                flex-shrink: 0 !important;
            }
            .stepper-item .step-name {
                font-size: 0.9rem !important;
            }
            
            /* Compact Tab layout for mobile */
            div[data-baseweb="tab-list"] {
                gap: 8px !important;
            }
            div[data-baseweb="tab"] {
                padding: 6px 10px !important;
                font-size: 0.85rem !important;
            }
        }
        
        /* Voice Narration Player Styling */
        .voice-player-card {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: all 0.3s ease;
        }
        .voice-player-card:hover {
            box-shadow: 0 8px 24px rgba(46, 125, 50, 0.08);
            border-color: rgba(46, 125, 50, 0.3);
        }
        .voice-btn {
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .voice-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .voice-btn.play {
            background-color: #2E7D32;
            color: white;
        }
        .voice-btn.play:hover:not(:disabled) {
            background-color: #1B5E20;
            transform: translateY(-1px);
        }
        .voice-btn.pause {
            background-color: #F59E0B;
            color: white;
        }
        .voice-btn.pause:hover:not(:disabled) {
            background-color: #D97706;
            transform: translateY(-1px);
        }
        .voice-btn.stop {
            background-color: #EF4444;
            color: white;
        }
        .voice-btn.stop:hover:not(:disabled) {
            background-color: #DC2626;
            transform: translateY(-1px);
        }
        .voice-select {
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            background: white;
            font-size: 0.85rem;
            color: #1E293B;
            font-weight: 500;
            outline: none;
            cursor: pointer;
        }
        
        /* CSS Soundwave animation */
        .voice-wave {
            display: flex;
            align-items: flex-end;
            gap: 3px;
            height: 24px;
            padding: 0 4px;
        }
        .voice-bar {
            width: 3px;
            height: 4px;
            background-color: #2E7D32;
            border-radius: 2px;
            transition: height 0.2s ease;
        }
        .voice-wave.speaking .voice-bar {
            animation: pulse_bar 1s infinite alternate;
        }
        .voice-wave.speaking .bar-1 { animation-delay: 0.1s; }
        .voice-wave.speaking .bar-2 { animation-delay: 0.3s; }
        .voice-wave.speaking .bar-3 { animation-delay: 0.5s; }
        .voice-wave.speaking .bar-4 { animation-delay: 0.2s; }
        .voice-wave.speaking .bar-5 { animation-delay: 0.4s; }
        
        .voice-wave.paused .voice-bar {
            background-color: #F59E0B;
        }
        
        @keyframes pulse_bar {
            0% { height: 4px; }
            100% { height: 20px; }
        }
        
        /* Microphone Button Styling */
        .mic-btn-container {
            display: inline-flex;
            align-items: center;
            margin-left: 0.5rem;
            vertical-align: middle;
        }
        .mic-btn {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 50%;
            width: 42px;
            height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        .mic-btn:hover {
            border-color: #2E7D32;
            box-shadow: 0 6px 12px rgba(46, 125, 50, 0.12);
            transform: scale(1.05);
        }
        .mic-btn.recording {
            background: #FFEBEE;
            border-color: #EF4444;
            color: #EF4444;
            animation: mic_pulse 1.5s infinite;
        }
        
        @keyframes mic_pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_branding():
    """
    Renders the sidebar branding elements.
    """
    from src.translations import t
    
    with st.sidebar:
        logo_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png"))
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
        else:
            st.image("https://img.icons8.com/color/96/000000/sprout.png", width=80)
        st.markdown(f"<h2 style='margin-top:0;'>{t('app_title')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #64748B; font-size: 0.9rem;'>{t('app_subtitle')}</p>", unsafe_allow_html=True)
        
        # Language Selector
        langs = ["en", "hi", "mr", "es"]
        lang_labels = {"en": "English", "hi": "हिन्दी (Hindi)", "mr": "मराठी (Marathi)", "es": "Español (Spanish)"}
        selected_lang_idx = langs.index(st.session_state.get("language", "en"))
        
        lang_choice = st.selectbox(
            "🌐 Language / भाषा / Idioma",
            options=langs,
            index=selected_lang_idx,
            format_func=lambda x: lang_labels[x],
            key="language_selector"
        )
        
        if lang_choice != st.session_state.get("language", "en"):
            st.session_state.language = lang_choice
            st.rerun()
            
        st.markdown("---")
        
        st.markdown(f"### {t('supported_crops')}")
        st.markdown(f"- {t('crop_corn')}")
        st.markdown(f"- {t('crop_potato')}")
        st.markdown(f"- {t('crop_rice')}")
        st.markdown(f"- {t('crop_sugarcane')}")
        st.markdown(f"- {t('crop_wheat')}")
        
        st.markdown(f"<div style='position: fixed; bottom: 10px; font-size: 0.8rem; color: #94A3B8;'>{t('release_version')}</div>", unsafe_allow_html=True)

def render_voice_player(text_to_speak, language_code, key):
    """
    Renders a premium client-side Text-to-Speech audio guide.
    """
    import json
    from src.translations import t
    
    sanitized_key = "".join(c if c.isalnum() or c == "_" else "_" for c in key)
    text_to_speak_json = json.dumps(text_to_speak)
    
    html = f"""<div class="voice-player-card" id="voice-player-{sanitized_key}"><div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;"><div style="display: flex; align-items: center; gap: 0.75rem;"><span style="font-size: 1.5rem;">🔊</span><div><strong style="color: #1E293B; font-size: 0.95rem;">{t('voice_reader_title')}</strong><div style="font-size: 0.75rem; color: #64748B;" id="voice-status-{sanitized_key}">Ready</div></div></div><div class="voice-wave" id="voice-wave-{sanitized_key}"><span class="voice-bar bar-1"></span><span class="voice-bar bar-2"></span><span class="voice-bar bar-3"></span><span class="voice-bar bar-4"></span><span class="voice-bar bar-5"></span></div></div><hr style="margin: 0.75rem 0; border: 0; border-top: 1px solid #E2E8F0;"><div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;"><div style="display: flex; align-items: center; gap: 0.5rem;"><button class="voice-btn play" id="voice-play-{sanitized_key}" onclick="startSpeech_{sanitized_key}()">{t('voice_play')}</button><button class="voice-btn pause" id="voice-pause-{sanitized_key}" onclick="pauseSpeech_{sanitized_key}()" disabled>{t('voice_pause')}</button><button class="voice-btn stop" id="voice-stop-{sanitized_key}" onclick="stopSpeech_{sanitized_key}()" disabled>{t('voice_stop')}</button></div><div style="display: flex; align-items: center; gap: 0.5rem;"><span style="font-size: 0.8rem; color: #64748B; font-weight: 500;">{t('voice_speed')}:</span><select class="voice-select" id="voice-rate-{sanitized_key}" onchange="updateRate_{sanitized_key}()"><option value="0.8">0.8x</option><option value="1.0" selected>1.0x</option><option value="1.2">1.2x</option><option value="1.5">1.5x</option></select></div></div></div><script>(function(){{const textToSpeak={text_to_speak_json};const langCode="{language_code}";const key="{sanitized_key}";let synth=window.speechSynthesis;let utterance=null;let isPaused=false;const playBtn=document.getElementById("voice-play-"+key);const pauseBtn=document.getElementById("voice-pause-"+key);const stopBtn=document.getElementById("voice-stop-"+key);const rateSelect=document.getElementById("voice-rate-"+key);const wave=document.getElementById("voice-wave-"+key);const statusDiv=document.getElementById("voice-status-"+key);window.startSpeech_{sanitized_key}=function(){{if(isPaused){{synth.resume();isPaused=false;setSpeakingState(true);statusDiv.innerText=langCode==="hi"?"बोला जा रहा है...":(langCode==="es"?"Hablando...":"Speaking...");return;}}synth.cancel();setTimeout(function(){{utterance=new SpeechSynthesisUtterance(textToSpeak);window.activeUtterance_{sanitized_key}=utterance;const voices=synth.getVoices();let selectedVoice=null;if(langCode==="hi"){{selectedVoice=voices.find(v=>v.lang.startsWith("hi")||v.lang.includes("IN"))||null;utterance.lang="hi-IN";}}else if(langCode==="es"){{selectedVoice=voices.find(v=>v.lang.startsWith("es"))||null;utterance.lang="es-ES";}}else{{selectedVoice=voices.find(v=>v.lang.startsWith("en"))||null;utterance.lang="en-US";}}if(selectedVoice){{utterance.voice=selectedVoice;}}utterance.rate=parseFloat(rateSelect.value);utterance.onstart=function(){{setSpeakingState(true);statusDiv.innerText=langCode==="hi"?"बोला जा रहा है...":(langCode==="es"?"Hablando...":"Speaking...");}};utterance.onend=function(){{setSpeakingState(false);statusDiv.innerText=langCode==="hi"?"पूर्ण":(langCode==="es"?"Completado":"Completed");isPaused=false;}};utterance.onerror=function(e){{console.error("SpeechSynthesisUtterance error",e);setSpeakingState(false);statusDiv.innerText="Error";isPaused=false;}};synth.speak(utterance);}},100);}};window.pauseSpeech_{sanitized_key}=function(){{if(synth.speaking&&!synth.paused){{synth.pause();isPaused=true;setSpeakingState(false,true);statusDiv.innerText=langCode==="hi"?"रुका हुआ":(langCode==="es"?"Pausado":"Paused");}}}};window.stopSpeech_{sanitized_key}=function(){{synth.cancel();isPaused=false;setSpeakingState(false);statusDiv.innerText=langCode==="hi"?"रोका गया":(langCode==="es"?"Detenido":"Stopped");}};window.updateRate_{sanitized_key}=function(){{if(synth.speaking&&!isPaused){{window.startSpeech_{sanitized_key}();}}}};function setSpeakingState(speaking,pausedState=false){{if(speaking){{wave.classList.add("speaking");wave.classList.remove("paused");playBtn.disabled=true;pauseBtn.disabled=false;stopBtn.disabled=false;}}else{{wave.classList.remove("speaking");if(pausedState){{wave.classList.add("paused");playBtn.disabled=false;pauseBtn.disabled=true;stopBtn.disabled=false;}}else{{wave.classList.remove("paused");playBtn.disabled=false;pauseBtn.disabled=true;stopBtn.disabled=true;}}}}}}}})();</script>"""
    import streamlit as st
    st.markdown(html, unsafe_allow_html=True)

def render_voice_search(target_placeholder, language_code, key, use_query_param=False, query_param_name=""):
    """
    Renders a Speech-to-Text microphone search button.
    Supports either direct DOM input writing or query-parameter page reload.
    """
    import json
    from src.translations import t
    
    sanitized_key = "".join(c if c.isalnum() or c == "_" else "_" for c in key)
    target_placeholder_json = json.dumps(target_placeholder)
    
    html = f"""<div class="mic-btn-container" id="mic-container-{sanitized_key}"><button class="mic-btn" id="mic-btn-{sanitized_key}" onclick="startSpeechRecognition_{sanitized_key}()" title="{t('voice_mic_tooltip')}">🎤</button></div><script>(function(){{const key="{sanitized_key}";const targetPlaceholder={target_placeholder_json};const langCode="{language_code}";const useQuery={str(use_query_param).lower()};const queryName="{query_param_name}";const micBtn=document.getElementById("mic-btn-"+key);let recognition=null;let isRecording=false;const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SpeechRecognition){{micBtn.style.display="none";return;}}window.startSpeechRecognition_{sanitized_key}=function(){{if(isRecording){{recognition.stop();return;}}recognition=new SpeechRecognition();recognition.continuous=false;recognition.interimResults=false;if(langCode==="hi"){{recognition.lang="hi-IN";}}else if(langCode==="es"){{recognition.lang="es-ES";}}else{{recognition.lang="en-US";}}recognition.onstart=function(){{isRecording=true;micBtn.classList.add("recording");}};recognition.onend=function(){{isRecording=false;micBtn.classList.remove("recording");}};recognition.onerror=function(event){{console.error("Speech recognition error",event.error);isRecording=false;micBtn.classList.remove("recording");}};recognition.onresult=function(event){{const transcript=event.results[0][0].transcript;console.log("Speech transcript:",transcript);if(useQuery&&queryName){{const url=new URL(window.location.href);url.searchParams.set(queryName,transcript);window.location.href=url.href;}}else{{const inputs=document.querySelectorAll('input[type="text"]');let targetInput=null;for(const input of inputs){{if(input.placeholder&&input.placeholder.toLowerCase().includes(targetPlaceholder.toLowerCase())){{targetInput=input;break;}}}}if(!targetInput&&inputs.length > 0){{targetInput=inputs[0];}}if(targetInput){{const nativeInputValueSetter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,"value").set;if(nativeInputValueSetter){{nativeInputValueSetter.call(targetInput,transcript);}}else{{targetInput.value=transcript;}}targetInput.dispatchEvent(new Event('input',{{bubbles:true}}));targetInput.dispatchEvent(new Event('change',{{bubbles:true}}));targetInput.focus();setTimeout(()=>{{const enterEvent=new KeyboardEvent('keydown',{{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}});targetInput.dispatchEvent(enterEvent);}},100);}}else{{console.warn("No text input found for placeholder: ",targetPlaceholder);}}}}}};recognition.start();}};}})();</script>"""
    import streamlit as st
    st.markdown(html, unsafe_allow_html=True)


