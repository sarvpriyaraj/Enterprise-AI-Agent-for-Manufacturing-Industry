import base64  # Encodes binary images to text strings for HTML injection.
from pathlib import Path  # Handles directory paths cleanly across operating systems.
import streamlit as st  # The main framework powering the web UI dashboard.

try:  # Attempts to isolate the backend import safely.
    from orchestrator_4_comments_ship import run_ducati_agent  # Pulls the main self-healing Graph-RAG agent function.
    backend_error = None  # Resets the error tracker if connection succeeds.
except Exception as e:  # Captures crashes if the backend engine fails.
    backend_error = str(e)  # Saves the error details to display to the user.

st.set_page_config(  # Configures global browser window settings for the app.
    page_title="Ducati AI Agent Assistant",  # Sets the text appearing on the browser tab title.
    page_icon="🏍️",  # Adds a motorcycle emoji as the browser tab favicon.
    layout="wide"  # Expands the dashboard canvas across the full screen width.
)  # Closes the page configuration function block.

LOGO_PATH = "ducati_logo.png"  # Defines the local image file name for the brand logo.
AGENT_LOGO_PATH = "AI_Agent_Logo.png"  # Defines the file name for the assistant avatar logo.
BIKE_PATH = "ducati_panigale.png"  # Defines the file name for the background hero image.

@st.cache_data  # Optimizes performance so images only load once instead of every frame.
def load_image_base64(path: str):  # Creates a function to transform local files into browser-safe strings.
    p = Path(path)  # Wraps the raw string path into a robust path object.
    if not p.exists():  # Verifies if the image asset actually exists on disk.
        return None  # Properly returns nothing if a file is missing.
    return base64.b64encode(p.read_bytes()).decode()  # Reads the image bits and converts them to text string data.

logo_b64 = load_image_base64(LOGO_PATH)  # Caches and loads the corporate header logo string.
agent_b64 = load_image_base64(AGENT_LOGO_PATH)  # Caches and loads the system avatar asset string.
bike_b64 = load_image_base64(BIKE_PATH)  # Caches and loads the motorcycle landing asset string.

st.markdown("""
    <style>
    :root {
        --ducati-red: #CC0000;
        --ducati-red-dark: #A30000;
        --ducati-grey: #555555;
    }

    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }

    .full-bleed {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
    }

    .ducati-topbar {
        background-color: var(--ducati-red);
        color: white;
        padding: 12px 60px;
        display: flex;
        align-items: center;
        gap: 12px;
        height: 58px;
        overflow: visible;
    }
    .ducati-topbar .shield {
        font-size: 28px;
        line-height: 1;
    }
    .ducati-topbar .brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 2px;
    }
    .ducati-topbar .logo-img {
        height: 84px;
        width: auto;
        display: block;
        margin: -13px 0;
    }
    .tiny-spacer { height: 10px; }

    .ducati-hero-title {
        text-align: left;
        color: var(--ducati-red);
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 18px 0 0 0;
    }
    .ducati-agent-label {
        text-align: left;
        color: #111111;
        font-size: 22px;
        font-weight: 800;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }
    .ducati-agent-tagline {
        text-align: left;
        color: var(--ducati-red);
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .chat-panel {
        border: 1px solid #EAEAEA;
        border-radius: 12px;
        padding: 20px;
        background-color: #FAFAFA;
        min-height: 420px;
        max-height: 550px;
        overflow-y: auto;
    }

    .chat-bubble-user {
        background-color: #F2F2F2;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 14px;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    .chat-bubble-agent {
        background-color: #FFFFFF;
        border: 1.5px solid var(--ducati-red);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 18px;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    .avatar-user {
        background-color: #2F6FED;
        color: white;
        border-radius: 50%;
        width: 30px; height: 30px;
        min-width: 30px;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px;
    }
    
    .avatar-agent {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 50%;
        width: 30px; height: 30px;
        min-width: 30px;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
    }
    .avatar-agent img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .bubble-label { font-weight: 700; font-size: 14px; margin-bottom: 2px; }
    .bubble-text { font-size: 14.5px; color: #222222; }

    .typing-dots span {
        display: inline-block;
        width: 6px; height: 6px;
        margin-right: 3px;
        background-color: var(--ducati-red);
        border-radius: 50%;
        opacity: 0.4;
    }

    .cat-card {
        border: 1.5px solid var(--ducati-red);
        border-radius: 12px;
        text-align: center;
        padding: 14px 8px;
        margin-bottom: 12px;
        height: 152px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: box-shadow 0.15s ease;
    }
    .cat-card:hover { box-shadow: 0 4px 14px rgba(204,0,0,0.2); }
    .cat-icon { font-size: 34px; color: var(--ducati-red); margin-bottom: 8px; }
    .cat-label { font-size: 13.5px; font-weight: 700; color: #111111; line-height: 1.2; }
    .cat-rail-heading {
        color: var(--ducati-red);
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .chat-panel-media {
        position: relative;
        border: 1px solid #EAEAEA;
        border-radius: 12px;
        background-color: #FAFAFA;
        min-height: 388px;
        max-height: 388px;
        padding: 0px !important; 
        overflow: hidden;
        box-sizing: border-box;
    }
    
    .chat-panel-media img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important; 
        display: block;
    }
    
    .chat-panel-media .media-caption {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.6); 
        color: #FFFFFF !important;
        padding: 10px;
        font-size: 13.5px;
        text-align: center;
    }
    
    .hero-agent-img {
        max-height: 130px;
        width: auto;
    }
    </style>
""", unsafe_allow_html=True)  # Injects all corporate branding CSS layouts directly into the screen render engine.

logo_html = (  # Begins a conditional statement string builder block for the header image.
    f'<img class="logo-img" src="data:image/png;base64,{logo_b64}" />'  # Generates the corporate shield layout if data exists.
    if logo_b64 else  # Evaluates the fallback check.
    '<div class="shield">🛡️</div>'  # Standard emoji fallback text if image is missing.
)  # Ends the conditional variable binding assignment.

st.markdown(f"""
    <div class="full-bleed">
        <div class="ducati-topbar">
            {logo_html}
            <div class="brand">DUCATI</div>
        </div>
    </div>
""", unsafe_allow_html=True)  # Renders the absolute full-width red top navigation dashboard bar.

if backend_error:  # Checks if the graph database initialization crashed.
    st.error(f"⚠️ **Backend Initialization Failure:** Could not connect to Neo4j database instance. Details: `{backend_error}`. Please check if your Neo4j Desktop database is currently running.")  # Renders a visible error banner flag on the web UI.
if not logo_b64:  # Validates file availability flag.
    st.warning(f"Missing layout element: **{LOGO_PATH}**")  # Shows notification warning message for missing assets.
if not agent_b64:  # Validates file availability flag.
    st.warning(f"Missing layout element: **{AGENT_LOGO_PATH}**")  # Shows notification warning message for missing assets.
if not bike_b64:  # Validates file availability flag.
    st.warning(f"Missing layout element: **{BIKE_PATH}**")  # Shows notification warning message for missing assets.

st.markdown('<div class="tiny-spacer"></div>', unsafe_allow_html=True)  # Spawns a small visual vertical break buffer.

icons_col, agent_col = st.columns([1, 2.2], gap="large")  # Divides layout into department tiles column and a chat container column.

categories = [  # Declares data dictionary layout for functional factory departments.
    ("⚙️", "Design & Engineering"),  # Functional operational block entry.
    ("🏭", "Manufacturing (MES)"),  # Functional operational block entry.
    ("🔗", "SCM & Procurement"),  # Functional operational block entry.
    ("📈", "Sales & Marketing"),  # Functional operational block entry.
    ("🚚", "Logistics & Delivery"),  # Functional operational block entry.
    ("🛠️", "Service & After Sales"),  # Functional operational block entry.
]  # Ends structural operational metadata array.

with icons_col:  # Focuses rendering operations onto the left grid section panel.
    st.markdown('<div class="cat-rail-heading">Explore Department Operations</div>', unsafe_allow_html=True)  # Prints left panel subtitle.
    sub_a, sub_b = st.columns(2, gap="small")  # Creates a 2-column inner nested grid layout for buttons.
    for i, (icon, label) in enumerate(categories):  # Loops through each operational department layout index.
        target = sub_a if i % 2 == 0 else sub_b  # Switches across layout items evenly between column A and column B.
        with target:  # Switches targeting context to active nested grid slot.
            st.markdown(f"""
                <div class="cat-card">
                    <div class="cat-icon">{icon}</div>
                    <div class="cat-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)  # Prints custom interactive department card template onto the UI.

with agent_col:  # Switches targeting focus onto the right panel area window.
    hero_a, hero_b = st.columns([1, 3], gap="medium")  # Splits main profile zone into profile picture vs titles.
    with hero_a:  # Targets layout block focus for the portrait window.
        if agent_b64:  # Checks if avatar profile image text string exists.
            st.markdown(  # Spawns a custom HTML compiler block.
                f'<img class="hero-agent-img" src="data:image/png;base64,{agent_b64}" />',  # injects encoded image directly into custom CSS profile shape.
                unsafe_allow_html=True  # Bypasses string sanitation engines to process graphic components.
            )  # Closes markdown element statement.
        else:  # Fallback tracker check trigger.
            st.markdown("<div style='text-align:left; font-size:64px; line-height:1;'>🤖</div>", unsafe_allow_html=True)  # Emits raw emoji placeholder if portrait file fails.
            
    with hero_b:  # Targets layout block focus for title data block.
        st.markdown('<p class="ducati-hero-title" style="font-size:32px; margin:0;">DUCATI</p>', unsafe_allow_html=True)  # Outputs bold main brand card title tag.
        st.markdown('<p class="ducati-agent-label" style="font-size:17px; margin-top:2px;">AI AGENT ASSISTANT</p>', unsafe_allow_html=True)  # Outputs assistant role sub-classification header.
        st.markdown('<p class="ducati-agent-tagline" style="margin-bottom:0;">Your Intelligent Companion for Ducati Operations</p>', unsafe_allow_html=True)  # Outputs lower description tagline message.

    st.markdown('<div class="tiny-spacer"></div>', unsafe_allow_html=True)  # Adds clean separation spacing above viewport windows.

    if "history" not in st.session_state:  # Looks for persistent conversational storage dictionary markers.
        st.session_state.history = []  # Instantiates empty array thread if starting up a fresh window state.

    if not st.session_state.history:  # Condition triggered if user has not entered questions yet.
        if bike_b64:  # Verifies background graphic asset verification flag.
            st.markdown(  # Spawns structural graphic landing block layout container.
                f"""
                <div class="chat-panel-media">
                    <img src="data:image/png;base64,{bike_b64}" />
                    <div class="media-caption">Your conversation with the Ducati AI Agent will appear here.</div>
                </div>
                """,
                unsafe_allow_html=True  # Renders large background cover image asset layout module cleanly.
            )  # Concludes welcome layout block wrapper instance.
        else:  # Fallback block layout tracker.
            st.markdown(  # Prints clean gray visual empty structural box template.
                '<div class="chat-panel"><div class="chat-panel-empty">'  # Formats raw text centering alignment properties.
                'Your conversation with the Ducati AI Agent will appear here.'  # Message indicating chat window status.
                '</div></div>',  # Shuts inner layout division containers down.
                unsafe_allow_html=True  # Grants compilation authorization clear space.
            )  # Concludes template fallback render.
    else:  # Triggers instead if conversational history contains turns.
        agent_avatar_html = f'<img src="data:image/png;base64,{agent_b64}" />' if agent_b64 else '🤖'  # pre-compiles active avatar asset parameters.
        
        with st.container():  # Declares an isolated screen rendering context canvas frame.
            st.markdown('<div class="chat-panel">', unsafe_allow_html=True)  # Opens the structural panel division background wrapper.
            for turn in st.session_state.history:  # Begins iteration walk loop through logged system dialogue turns.
                if turn["role"] == "user":  # Validates if log line matches message data sent from user.
                    st.markdown(f"""
                        <div class="chat-bubble-user">
                            <div class="avatar-user">👤</div>
                            <div>
                                <div class="bubble-label">User:</div>
                                <div class="bubble-text">{turn['text']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)  # Prints custom gray layout user bubble containing message string text.
                else:  # Executes if row entry matches AI agent reply footprint instead.
                    st.markdown(f"""
                        <div class="chat-bubble-agent">
                            <div class="avatar-agent">{agent_avatar_html}</div>
                            <div>
                                <div class="bubble-label">Ducati AI Agent:</div>
                                <div class="bubble-text">{turn['text']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)  # Prints custom red border layout agent bubble containing structural text query answer.
            st.markdown('</div>', unsafe_allow_html=True)  # Closes structural scrollable conversation background container wrapper panel.

    for turn in st.session_state.history:  # Loops history records again explicitly to display technical debugging trees.
        if turn["role"] == "agent" and turn.get("cypher"):  # Isolates generated Cypher queries matching actual database communications.
            with st.expander("🛠️ View Final Executed Cypher Query"):  # Generates drop-down button interface framework module widget.
                st.code(turn["cypher"], language="cypher")  # Highlights structural query text formatting strings with syntax highlighting.

# ---------------------------------------------------------
# 7. CHAT INPUT + AGENT EXECUTION LOOP
# ---------------------------------------------------------
user_query = st.chat_input("Ask anything about Ducati – Design, Engineering, Manufacturing, SCM, Sales and Logistics...")  # Locks a chat bar text line tracker component onto viewport base.

if user_query:  # Code block triggers only when user presses submit key enter action.
    if backend_error:  # Blocks query execution if connection checks are bad.
        st.error("Cannot process input question: The backend database engine connection remains unavailable.")  # Alerts screen console area tracker status.
    else:  # Normal target execution processing roadmap path block.
        st.session_state.history.append({"role": "user", "text": user_query, "cypher": None})  # Inserts human prompt text into log array dataset immediately.
        agent_avatar_html = f'<img src="data:image/png;base64,{agent_b64}" />' if agent_b64 else '🤖'  # Resolves operational status profile logo details.

        placeholder = st.empty()  # Reserves a dynamic mutable layout coordinate handle on screen workspace area.
        placeholder.markdown(f"""
            <div class="chat-bubble-agent">
                <div class="avatar-agent">{agent_avatar_html}</div>
                <div>
                    <div class="bubble-label">Ducati AI Agent:</div>
                    <div class="bubble-text">AI Agent is thinking<span class="typing-dots"><span></span><span></span><span></span></span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)  # Displays animated glowing loading component template inside the designated viewport coordinate.

        try:  # Wraps processing execution stream context inside defense tracking block.
            result = run_ducati_agent(user_query)  # Hands user prompt to backend graph processing framework, waits for completion response.
            ai_response = result["final_answer"]  # Stores natural language response text inside variable container.
            generated_cypher = result.get("cypher_query")  # Gathers compiled cypher database logging string details.
        except Exception as e:  # Error breakout block routing tracking handler.
            ai_response = f"An execution error stopped the pipeline tracking flow: {str(e)}"  # Forwards exception message directly to terminal display variables.
            generated_cypher = None  # Resets logging parameters to prevent code view module generation crashes.

        placeholder.empty()  # Destroys and clears active visible glowing loading animation element away completely.
        st.session_state.history.append({"role": "agent", "text": ai_response, "cypher": generated_cypher})  # appends complete AI response structures into persistent turn database logs.
        st.rerun()  # Forces instant screen frame refresh update cycle to reflect recent messages.