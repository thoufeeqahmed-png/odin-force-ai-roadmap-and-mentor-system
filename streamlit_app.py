"""
ODIN FORCE — Streamlit AI Roadmap & Mentor System
Supreme Asgardian Learning Companion powered by Allfather Odin, Thor, Loki & ODIN FORCE Companion.
"""

import streamlit as st
import os
import json
import base64
from pathlib import Path

# Set Page Config
st.set_page_config(
    page_title="ODIN FORCE — AI Roadmap & Mentor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "static" / "images"

# Load AI Service
try:
    from roadmap.ai_service import TAJuniorAIService
except Exception:
    # Standalone Fallback for Cloud Hosting if roadmap package is not in sys.path
    import sys
    sys.path.append(str(BASE_DIR))
    from roadmap.ai_service import TAJuniorAIService


def get_image_base64(file_path):
    """Encodes an image to base64 for embedding directly in HTML."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""


# Load Images
img_odin = get_image_base64(IMG_DIR / "mentor_odin.jpg")
img_thor = get_image_base64(IMG_DIR / "mentor_thor.jpg")
img_loki = get_image_base64(IMG_DIR / "mentor_loki.jpg")
img_odinforce = get_image_base64(IMG_DIR / "mentor_odinforce.jpg")
img_logo = get_image_base64(IMG_DIR / "ta_junior.svg")

# Custom Dark Asgardian Styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    .stApp {{
        background: radial-gradient(circle at 50% 0%, #151d33 0%, #080d1a 60%, #03060f 100%);
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }}
    
    .asgard-title {{
        font-family: 'Cinzel', serif;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        background: linear-gradient(135deg, #fef08a 0%, #f59e0b 50%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }}
    
    .asgard-subtitle {{
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 24px;
    }}
    
    .mentor-card {{
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }}
    
    .mentor-card:hover {{
        transform: translateY(-3px);
        border-color: rgba(245, 158, 11, 0.4);
    }}
    
    .odin-card {{ border-top: 3px solid #f59e0b; }}
    .thor-card {{ border-top: 3px solid #38bdf8; }}
    .loki-card {{ border-top: 3px solid #10b981; }}
    .ta-card {{ border-top: 3px solid #a855f7; }}
    
    .mentor-header-row {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 10px;
    }}
    
    .mentor-portrait-thumb {{
        width: 68px;
        height: 68px;
        border-radius: 10px;
        object-fit: cover;
        object-position: center top;
        border: 2px solid rgba(245, 158, 11, 0.5);
    }}
    
    .thor-thumb {{ border-color: #38bdf8; }}
    .loki-thumb {{ border-color: #10b981; }}
    .ta-thumb {{ border-color: #a855f7; }}
    
    .stage-card {{
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .stage-badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
        margin-bottom: 8px;
    }}
    
    .why-box {{
        background: rgba(56, 189, 248, 0.08);
        border-left: 3px solid #38bdf8;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        font-size: 0.92rem;
        color: #e0f2fe;
    }}
    
    .practice-box {{
        background: rgba(16, 185, 129, 0.08);
        border-left: 3px solid #10b981;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        font-size: 0.92rem;
        color: #d1fae5;
    }}
    
    .project-box {{
        background: rgba(168, 85, 247, 0.08);
        border-left: 3px solid #a855f7;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        font-size: 0.92rem;
        color: #f3e8ff;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #0b0f19 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5) !important;
    }}
    
    .footer-text {{
        text-align: center;
        color: rgba(148, 163, 184, 0.6);
        font-size: 0.82rem;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "saved_roadmaps" not in st.session_state:
    st.session_state.saved_roadmaps = []

if "active_roadmap" not in st.session_state:
    # Seed a default high quality AI roadmap
    default_ai = TAJuniorAIService.generate_roadmap(
        domain="Artificial Intelligence",
        current_level="Beginner",
        goal="Become an AI Engineer & Deploy LLMs",
        available_time="2 hours per day",
        duration="6 months",
        existing_skills="Python basics",
        user_name="Learner",
        mentor="odin"
    )
    # Initialize task completion states
    tasks_state = {}
    for s_idx, stage in enumerate(default_ai.get("stages", [])):
        for t_idx, task in enumerate(stage.get("tasks", [])):
            key = f"task_{s_idx}_{t_idx}"
            tasks_state[key] = (s_idx == 0 and t_idx == 0)
    
    default_ai["tasks_state"] = tasks_state
    default_ai["domain"] = "Artificial Intelligence"
    default_ai["current_level"] = "Beginner"
    default_ai["goal"] = "Become an AI Engineer & Deploy LLMs"
    default_ai["available_time"] = "2 hours per day"
    default_ai["duration"] = "6 months"
    default_ai["mentor"] = "odin"
    st.session_state.active_roadmap = default_ai
    st.session_state.saved_roadmaps.append(default_ai)


# Sidebar Branding & Navigation
with st.sidebar:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <img src="data:image/svg+xml;base64,{img_logo}" width="42" height="42" style="border-radius: 8px;">
        <div>
            <h2 style="margin: 0; font-family: 'Cinzel', serif; font-size: 1.4rem; color: #f59e0b;">ODIN FORCE</h2>
            <span style="font-size: 0.75rem; color: #94a3b8;">⚡ Supreme AI Roadmap & Mentor</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "Explore Asgardian Realms",
        [
            "🌌 Home & Asgardian Council",
            "⚔️ Forge New Roadmap",
            "🗺️ Active Roadmap & Stages",
            "⚡ Thor's Daily Action Plan",
            "🏆 Valhalla Progress Dashboard",
            "👑 Consult the Council (Q&A)",
            "📜 Saved Roadmap Library",
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Active Roadmap quick info
    if st.session_state.active_roadmap:
        r = st.session_state.active_roadmap
        st.markdown(f"**Active Realm:** `{r.get('domain', 'Custom')}`")
        st.markdown(f"**Goal:** *{r.get('goal', '')}*")
        st.markdown(f"**Guide:** {r.get('mentor', 'odin').upper()}")
        
        # Calculate progress
        tasks_state = r.get("tasks_state", {})
        total_t = len(tasks_state)
        done_t = sum(1 for v in tasks_state.values() if v)
        pct = int((done_t / total_t * 100)) if total_t > 0 else 0
        st.progress(pct / 100.0)
        st.caption(f"⚡ {pct}% Conquered ({done_t}/{total_t} Tasks)")


# -----------------------------------------------------------------------------
# 1. HOME & ASGARDIAN COUNCIL
# -----------------------------------------------------------------------------
if menu == "🌌 Home & Asgardian Council":
    st.markdown('<div class="asgard-title">ODIN FORCE — AI ROADMAP & MENTOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="asgard-subtitle">Turn any learning or career ambition into a crystal-clear, step-by-step master plan with Odin, Thor, Loki, and ODIN FORCE Companion.</div>', unsafe_allow_html=True)
    
    st.subheader("👑 The Asgardian Council of Learning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="mentor-card odin-card">
            <div class="mentor-header-row">
                <img src="data:image/jpeg;base64,{img_odin}" class="mentor-portrait-thumb">
                <div>
                    <h3 style="margin: 0; color: #f59e0b; font-family: 'Cinzel', serif;">👁️ ALLFATHER ODIN</h3>
                    <span style="font-size: 0.85rem; color: #94a3b8;">Strategic Vision & Long-term Mastery</span>
                </div>
            </div>
            <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 8px;">
                Sees the entire learning journey from high throne Hlidskjalf. Shapes foundational mastery, deep core concepts, and career trajectories.
            </p>
            <em style="font-size: 0.8rem; color: #fef08a;">"Sacrifice haste for depth. The master sees the whole battlefield."</em>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="mentor-card loki-card">
            <div class="mentor-header-row">
                <img src="data:image/jpeg;base64,{img_loki}" class="mentor-portrait-thumb loki-thumb">
                <div>
                    <h3 style="margin: 0; color: #10b981; font-family: 'Cinzel', serif;">🐍 LOKI THE TRICKSTER</h3>
                    <span style="font-size: 0.85rem; color: #94a3b8;">80/20 Creative Hacks & Shortcuts</span>
                </div>
            </div>
            <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 8px;">
                Finds high-leverage leverage points, clever debugging tricks, and out-of-the-box hacks to learn concepts 3x faster.
            </p>
            <em style="font-size: 0.8rem; color: #a7f3d0;">"Why march the heavy road when there is an open secret door?"</em>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="mentor-card thor-card">
            <div class="mentor-header-row">
                <img src="data:image/jpeg;base64,{img_thor}" class="mentor-portrait-thumb thor-thumb">
                <div>
                    <h3 style="margin: 0; color: #38bdf8; font-family: 'Cinzel', serif;">⚡ THOR THE THUNDERER</h3>
                    <span style="font-size: 0.85rem; color: #94a3b8;">Relentless Daily Drills & Action</span>
                </div>
            </div>
            <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 8px;">
                Brings the raw hammer power of Mjolnir. Pushes you through daily 25-minute Pomodoro sprints and active project execution.
            </p>
            <em style="font-size: 0.8rem; color: #bae6fd;">"Strike the anvil daily! Action shatters every doubt."</em>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="mentor-card ta-card">
            <div class="mentor-header-row">
                <img src="data:image/jpeg;base64,{img_odinforce}" class="mentor-portrait-thumb ta-thumb">
                <div>
                    <h3 style="margin: 0; color: #a855f7; font-family: 'Cinzel', serif;">🌱 ODIN FORCE COMPANION</h3>
                    <span style="font-size: 0.85rem; color: #94a3b8;">Encouragement, Kindness & Pacing</span>
                </div>
            </div>
            <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 8px;">
                Translates divine power into friendly, zero-judgment daily steps. Celebrates every milestone and keeps you motivated.
            </p>
            <em style="font-size: 0.8rem; color: #e9d5ff;">"Take a breath. One tiny step today creates massive momentum."</em>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚡ Popular Realm Presets")
    
    pcols = st.columns(4)
    presets = [
        ("🤖 Artificial Intelligence", "Artificial Intelligence", "Beginner", "Become an AI Engineer & Deploy LLMs", "2 hours per day", "6 months", "Python basics"),
        ("💻 Web Development", "Web Development", "Complete Beginner", "Build full-stack web applications", "1 hour per day", "3 months", "None"),
        ("📷 Digital Photography", "Digital Photography", "Beginner", "Start a portrait photography studio", "1 hour per day", "3 months", "Smartphone camera"),
        ("📈 Financial Investing", "Financial Investing", "Intermediate", "Build a resilient multi-asset portfolio", "30 minutes per day", "1 year", "Basic savings"),
    ]
    
    for idx, (label, dom, lvl, gol, tm, dur, sk) in enumerate(presets):
        with pcols[idx]:
            if st.button(label, key=f"preset_btn_{idx}", use_container_width=True):
                with st.spinner(f"⚡ Forging {dom} Roadmap with ODIN FORCE..."):
                    new_rm = TAJuniorAIService.generate_roadmap(
                        domain=dom, current_level=lvl, goal=gol,
                        available_time=tm, duration=dur, existing_skills=sk,
                        user_name="Learner", mentor="auto"
                    )
                    t_state = {}
                    for s_i, stg in enumerate(new_rm.get("stages", [])):
                        for t_i, tsk in enumerate(stg.get("tasks", [])):
                            t_state[f"task_{s_i}_{t_i}"] = False
                    new_rm["tasks_state"] = t_state
                    new_rm["domain"] = dom
                    new_rm["current_level"] = lvl
                    new_rm["goal"] = gol
                    new_rm["available_time"] = tm
                    new_rm["duration"] = dur
                    new_rm["mentor"] = new_rm.get("selected_mentor", "odin")
                    st.session_state.active_roadmap = new_rm
                    st.session_state.saved_roadmaps.append(new_rm)
                    st.success(f"🎉 Generated '{dom}' Roadmap! View it in the Active Roadmap tab.")
                    st.rerun()


# -----------------------------------------------------------------------------
# 2. FORGE NEW ROADMAP
# -----------------------------------------------------------------------------
elif menu == "⚔️ Forge New Roadmap":
    st.markdown('<div class="asgard-title">⚔️ FORGE YOUR PERSONALIZED ROADMAP</div>', unsafe_allow_html=True)
    st.markdown('<div class="asgard-subtitle">State your realm and ambitions. The Council of Asgard will engineer an actionable step-by-step master plan.</div>', unsafe_allow_html=True)
    
    with st.form("forge_roadmap_form"):
        col1, col2 = st.columns(2)
        with col1:
            user_name = st.text_input("Your Name (Optional)", value="Learner", placeholder="e.g. Alex")
            domain = st.text_input("Domain / Field / Realm *", value="", placeholder="e.g. Artificial Intelligence, Digital Photography, Game Dev, Robotics...")
            current_level = st.selectbox(
                "Current Skill Level *",
                ["Complete Beginner", "Beginner", "Intermediate", "Advanced"],
                index=1
            )
            mentor_choice = st.selectbox(
                "Choose Your Personal Mentor Guide *",
                [
                    "auto - Let ODIN FORCE pick based on goal",
                    "odin - Allfather Odin (Strategic Vision & Architecture)",
                    "thor - Thor the Thunderer (Daily Drills & Relentless Action)",
                    "loki - Loki the Trickster (80/20 Creative Hacks & Shortcuts)"
                ],
                index=0
            )

        with col2:
            goal = st.text_input("Specific Goal or Milestone *", value="", placeholder="e.g. Get hired as an AI Engineer, Launch a creative agency, Build an indie game...")
            available_time = st.selectbox(
                "Available Study Time *",
                ["30 minutes per day", "1 hour per day", "2 hours per day", "4+ hours per day", "5-10 hours per week"],
                index=2
            )
            duration = st.selectbox(
                "Target Timeline *",
                ["1 month", "3 months", "6 months", "1 year"],
                index=2
            )
            existing_skills = st.text_area("Existing Skills or Background (Optional)", placeholder="e.g. Python basics, Basic math, Photoshop, None...")

        submit_btn = st.form_submit_button("⚡ Forge Roadmap with ODIN FORCE", use_container_width=True)
        
        if submit_btn:
            if not domain or not goal:
                st.error("⚠️ Please specify both your Domain and Goal!")
            else:
                m_code = mentor_choice.split(" - ")[0]
                with st.spinner("⚡ Summons sent to Asgard! Assembling stages, practice drills, and project milestones..."):
                    new_rm = TAJuniorAIService.generate_roadmap(
                        domain=domain,
                        current_level=current_level,
                        goal=goal,
                        available_time=available_time,
                        duration=duration,
                        existing_skills=existing_skills,
                        user_name=user_name,
                        mentor=m_code
                    )
                    t_state = {}
                    for s_i, stg in enumerate(new_rm.get("stages", [])):
                        for t_i, tsk in enumerate(stg.get("tasks", [])):
                            t_state[f"task_{s_i}_{t_i}"] = False
                    new_rm["tasks_state"] = t_state
                    new_rm["domain"] = domain
                    new_rm["current_level"] = current_level
                    new_rm["goal"] = goal
                    new_rm["available_time"] = available_time
                    new_rm["duration"] = duration
                    new_rm["mentor"] = new_rm.get("selected_mentor", m_code if m_code != "auto" else "odin")
                    st.session_state.active_roadmap = new_rm
                    st.session_state.saved_roadmaps.append(new_rm)
                    st.success(f"🎉 Woohoo! Your '{domain}' Roadmap is forged and active!")


# -----------------------------------------------------------------------------
# 3. ACTIVE ROADMAP & STAGES
# -----------------------------------------------------------------------------
elif menu == "🗺️ Active Roadmap & Stages":
    rm = st.session_state.active_roadmap
    if not rm:
        st.info("No active roadmap found. Please forge one first in '⚔️ Forge New Roadmap'!")
    else:
        mentor_key = rm.get("mentor", "odin")
        mentor_img_b64 = img_odin if mentor_key == "odin" else (img_thor if mentor_key == "thor" else (img_loki if mentor_key == "loki" else img_odinforce))
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; margin-bottom: 20px;">
            <div>
                <div class="asgard-title">{rm.get('domain', 'Realm')} Roadmap</div>
                <div style="font-size: 1.1rem; color: #38bdf8;">🎯 <strong>Goal:</strong> {rm.get('goal', '')}</div>
                <span style="font-size: 0.85rem; color: #94a3b8;">Level: {rm.get('current_level')} • Pace: {rm.get('available_time')} ({rm.get('duration')})</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; background: rgba(15, 23, 42, 0.8); padding: 8px 14px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);">
                <img src="data:image/jpeg;base64,{mentor_img_b64}" width="48" height="48" style="border-radius: 8px; object-fit: cover;">
                <div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">PERSONAL MENTOR</div>
                    <strong style="color: #f59e0b;">{mentor_key.upper()}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if rm.get("greeting_message"):
            st.info(f"🌱 **ODIN FORCE Message:** {rm.get('greeting_message')}")
        if rm.get("mentor_greeting"):
            st.success(f"👑 **Mentor's Greeting:** {rm.get('mentor_greeting')}")

        # Progress Calculation
        tasks_state = rm.get("tasks_state", {})
        total_t = len(tasks_state)
        done_t = sum(1 for v in tasks_state.values() if v)
        pct = int((done_t / total_t * 100)) if total_t > 0 else 0
        
        st.progress(pct / 100.0)
        st.markdown(f"**Conquest Progress: {pct}%** ({done_t} of {total_t} tasks conquered)")
        
        st.markdown("---")
        
        # Display Stages
        stages = rm.get("stages", [])
        for s_idx, stage in enumerate(stages):
            with st.expander(f"📍 {stage.get('title', f'Stage {s_idx+1}')} ({stage.get('estimated_duration', 'Weeks 1-4')})", expanded=(s_idx==0)):
                st.markdown(f"**Overview:** {stage.get('description', '')}")
                
                if stage.get("why_it_matters"):
                    st.markdown(f'<div class="why-box">💡 <strong>Why this matters:</strong> {stage.get("why_it_matters")}</div>', unsafe_allow_html=True)
                
                if stage.get("what_to_practice"):
                    st.markdown(f'<div class="practice-box">🔨 <strong>What to practice:</strong> {stage.get("what_to_practice")}</div>', unsafe_allow_html=True)
                
                if stage.get("suggested_projects"):
                    st.markdown(f'<div class="project-box">🚀 <strong>Suggested Projects:</strong><br>{stage.get("suggested_projects").replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                
                st.markdown("**Tasks & Milestones:**")
                for t_idx, task in enumerate(stage.get("tasks", [])):
                    t_key = f"task_{s_idx}_{t_idx}"
                    checked = st.checkbox(
                        f"[{task.get('type', 'topic').upper()}] {task.get('title')}: {task.get('desc', '')}",
                        value=tasks_state.get(t_key, False),
                        key=f"chk_{t_key}"
                    )
                    if checked != tasks_state.get(t_key, False):
                        tasks_state[t_key] = checked
                        rm["tasks_state"] = tasks_state
                        st.rerun()


# -----------------------------------------------------------------------------
# 4. THOR'S DAILY ACTION PLAN
# -----------------------------------------------------------------------------
elif menu == "⚡ Thor's Daily Action Plan":
    rm = st.session_state.active_roadmap
    if not rm:
        st.info("No active roadmap found. Please forge one first!")
    else:
        st.markdown('<div class="asgard-title">⚡ THOR\'S DAILY ACTION PLAN</div>', unsafe_allow_html=True)
        st.markdown('<div class="asgard-subtitle">One focused goal, Thor\'s relentless 25-minute practice sprint, and Loki\'s 80/20 cheat codes.</div>', unsafe_allow_html=True)
        
        stages = rm.get("stages", [])
        tasks_state = rm.get("tasks_state", {})
        
        # Find next incomplete task
        next_task = None
        next_stage_title = "Stage 1"
        for s_idx, stg in enumerate(stages):
            for t_idx, tsk in enumerate(stg.get("tasks", [])):
                if not tasks_state.get(f"task_{s_idx}_{t_idx}", False):
                    next_task = tsk
                    next_stage_title = stg.get("title", f"Stage {s_idx+1}")
                    break
            if next_task:
                break
        
        if not next_task and stages:
            next_task = stages[0]["tasks"][0]
            next_stage_title = stages[0]["title"]
            
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="mentor-card thor-card">
                <div class="mentor-header-row">
                    <img src="data:image/jpeg;base64,{img_thor}" class="mentor-portrait-thumb thor-thumb">
                    <div>
                        <h3 style="margin: 0; color: #38bdf8; font-family: 'Cinzel', serif;">⚡ TODAY'S FOCUS: {next_task.get('title', 'Daily Practice')}</h3>
                        <span style="font-size: 0.85rem; color: #94a3b8;">Realm: {rm.get('domain')} • {next_stage_title}</span>
                    </div>
                </div>
                <p style="font-size: 1rem; color: #f8fafc; margin: 12px 0;">
                    {next_task.get('desc', 'Deep dive into this core concept. Build a small experiment or drill.')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Thor challenge & Loki Hack
            thor_drill = TAJuniorAIService.get_thor_challenge(next_stage_title, rm.get("domain", ""))
            loki_hack = TAJuniorAIService.get_loki_hack(next_stage_title, rm.get("domain", ""))
            
            st.markdown(f'<div class="practice-box">{thor_drill}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="project-box">{loki_hack}</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown("### ⏱️ Thor's Focus Timer")
            st.caption("25 Minutes Unbroken Pomodoro Sprint")
            st.markdown("1. Turn off phone notifications\n2. Open code / workspace\n3. Execute for 25 mins\n4. Mark task completed!")
            if st.button("🔨 Start 25-Min Sprint", use_container_width=True):
                st.balloons()
                st.success("⚡ Thor's blessing received! Strike the anvil!")


# -----------------------------------------------------------------------------
# 5. VALHALLA PROGRESS DASHBOARD
# -----------------------------------------------------------------------------
elif menu == "🏆 Valhalla Progress Dashboard":
    rm = st.session_state.active_roadmap
    if not rm:
        st.info("No active roadmap found!")
    else:
        st.markdown('<div class="asgard-title">🏆 VALHALLA PROGRESS DASHBOARD</div>', unsafe_allow_html=True)
        st.markdown('<div class="asgard-subtitle">Track conquered milestones, stage velocity, and Asgardian achievements.</div>', unsafe_allow_html=True)
        
        tasks_state = rm.get("tasks_state", {})
        total_t = len(tasks_state)
        done_t = sum(1 for v in tasks_state.values() if v)
        pct = int((done_t / total_t * 100)) if total_t > 0 else 0
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Overall Conquest", f"{pct}%")
        m2.metric("Conquered Tasks", f"{done_t} / {total_t}")
        m3.metric("Stages in Realm", f"{len(rm.get('stages', []))}")
        m4.metric("Active Mentor", f"{rm.get('mentor', 'odin').upper()}")
        
        st.progress(pct / 100.0)
        
        st.markdown("---")
        st.subheader("🎖️ Asgardian Milestone Badges")
        
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            unlocked = done_t > 0
            st.markdown(f"**{'🟢 UNLOCKED' if unlocked else '🔒 LOCKED'}**\n\n🛡️ **First Strike:** Began the learning journey.")
        with b2:
            unlocked = done_t >= 3
            st.markdown(f"**{'🟢 UNLOCKED' if unlocked else '🔒 LOCKED'}**\n\n⚡ **Thunder Apprentice:** Conquered 3+ tasks.")
        with b3:
            unlocked = pct >= 50
            st.markdown(f"**{'🟢 UNLOCKED' if unlocked else '🔒 LOCKED'}**\n\n👑 **Bifrost Master:** 50% Mastery achieved.")
        with b4:
            unlocked = pct == 100
            st.markdown(f"**{'🟢 UNLOCKED' if unlocked else '🔒 LOCKED'}**\n\n🏆 **Valhalla Champion:** Completed full roadmap!")


# -----------------------------------------------------------------------------
# 6. CONSULT THE COUNCIL (Q&A)
# -----------------------------------------------------------------------------
elif menu == "👑 Consult the Council (Q&A)":
    rm = st.session_state.active_roadmap
    st.markdown('<div class="asgard-title">👑 CONSULT THE COUNCIL OF ASGARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="asgard-subtitle">Ask Odin, Thor, Loki, or ODIN FORCE Companion any question about your learning journey.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        chosen_mentor = st.selectbox(
            "Select Mentor to Consult:",
            ["Allfather Odin (Wise & Strategic)", "Thor the Thunderer (Action & Drills)", "Loki the Trickster (Creative Hacks)", "ODIN FORCE (Friendly Companion)"]
        )
        stage_context = st.text_input("Stage or Topic Context", value=rm.get("domain", "General Learning") if rm else "General Learning")
    
    with col2:
        question = st.text_area("What is your question or challenge?", placeholder="e.g. How should I practice gradient descent? or How do I stay consistent?")
        ask_btn = st.button("👁️ Consult Mentor", use_container_width=True)
    
    if ask_btn and question:
        mentor_id = "odin" if "Odin" in chosen_mentor else ("thor" if "Thor" in chosen_mentor else ("loki" if "Loki" in chosen_mentor else "ta_junior"))
        with st.spinner(f"Consulting {chosen_mentor}..."):
            if mentor_id == 'odin':
                ans = f"👁️ **Allfather Odin answers:**\n\nRegarding *'{question}'* in **{stage_context}**:\nLook beyond the immediate frustration. The challenge you face is the exact trial designed to test your strategic fortitude. Meditate upon foundational principles, consult your notes (the ravens' memory), and proceed with deliberate precision."
            elif mentor_id == 'thor':
                ans = f"⚡ **Thor answers:**\n\nRegarding *'{question}'* in **{stage_context}**:\nHaha! Don't overthink it—strike the problem! If you are stuck on '{question}', put away all distractions for 20 minutes and code/practice 5 quick variations until your hands master it. Action dispels fear!"
            elif mentor_id == 'loki':
                ans = f"🐍 **Loki answers:**\n\nRegarding *'{question}'* in **{stage_context}**:\nShh, here is the secret: you don't have to follow the boring standard path. For '{question}', look for existing open-source examples, copy the pattern, tweak one variable at a time, and see why it breaks. Reverse-engineering is the fastest cheat code!"
            else:
                ans = TAJuniorAIService.ask_ta_junior_for_stage_help(stage_context, question, rm.get("domain", "General") if rm else "General")
            
            st.markdown(f"""
            <div class="mentor-card" style="border-left: 4px solid #f59e0b; margin-top: 20px;">
                <h4>Divine Counsel Received</h4>
                <p style="white-space: pre-wrap; font-size: 1rem; color: #f8fafc;">{ans}</p>
            </div>
            """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. SAVED ROADMAP LIBRARY
# -----------------------------------------------------------------------------
elif menu == "📜 Saved Roadmap Library":
    st.markdown('<div class="asgard-title">📜 SAVED ROADMAP LIBRARY</div>', unsafe_allow_html=True)
    st.markdown('<div class="asgard-subtitle">Manage, switch, or export your forged roadmaps.</div>', unsafe_allow_html=True)
    
    if not st.session_state.saved_roadmaps:
        st.info("No saved roadmaps yet.")
    else:
        for idx, saved_rm in enumerate(st.session_state.saved_roadmaps):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"### {saved_rm.get('domain', 'Realm')}: *{saved_rm.get('goal', '')}*")
                st.caption(f"Mentor: {saved_rm.get('mentor', 'odin').upper()} • Stages: {len(saved_rm.get('stages', []))}")
            with col2:
                if st.button("Set Active", key=f"set_active_{idx}", use_container_width=True):
                    st.session_state.active_roadmap = saved_rm
                    st.success(f"Activated '{saved_rm.get('domain')}'!")
                    st.rerun()
            with col3:
                rm_json = json.dumps(saved_rm, indent=2)
                st.download_button(
                    "💾 Export JSON",
                    data=rm_json,
                    file_name=f"odin_force_{saved_rm.get('domain', 'roadmap').lower().replace(' ', '_')}.json",
                    mime="application/json",
                    key=f"dl_btn_{idx}",
                    use_container_width=True
                )
            st.markdown("---")


# Footer Identity
st.markdown("""
<div class="footer-text">
    ⚡ <strong>ODIN FORCE</strong> — AI Roadmap & Asgardian Mentor System • Powered by Modern AI & Norse Wisdom<br>
    <em>I am the AI assistant of Thoufeeq Ahmed.</em>
</div>
""", unsafe_allow_html=True)
