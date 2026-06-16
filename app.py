import streamlit as st
import datetime
import time
from zoneinfo import ZoneInfo

# Timezone Configuration (IST)
IST = ZoneInfo("Asia/Kolkata")

# Page Configuration
st.set_page_config(
    page_title="DevOps Weekly Timetable",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 1. DATA STRUCTURE
# ---------------------------------------------------------
# Define the templates and duplicate programmatically for Mon-Fri
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TASKS_TEMPLATE = [
    {"time": "05:00 AM - 08:00 AM", "task": "Wake up, Kid's Morning Routine (Cooking, Packing) & Dishes"},
    {"time": "08:15 AM - 09:30 AM", "task": "Workout & Bath 🏋️‍♀️"},
    {"time": "09:45 AM - 12:45 PM", "task": "Focus Session 1: Analytical & Core Studies 💻"},
    {"time": "12:45 PM - 02:00 PM", "task": "Cook Lunch (Manage Laundry rotation if needed)"},
    {"time": "02:00 PM - 03:30 PM", "task": "Focus Session 2: Python Coding & Laptop Work 🐍"},
    {"time": "03:30 PM - 05:00 PM", "task": "Active Daughter Time 👩‍👦"},
    {"time": "05:00 PM - 05:30 PM", "task": "House Maintenance (Sweep daily / Mop alternate days)"},
    {"time": "06:00 PM - 08:30 PM", "task": "Family Time & Evening Kid Routine"}
]

WEEKLY_SCHEDULE = {day: TASKS_TEMPLATE for day in DAYS_OF_WEEK}

# ---------------------------------------------------------
# 2. STATE PERSISTENCE INITIALIZATION
# ---------------------------------------------------------
for day, tasks in WEEKLY_SCHEDULE.items():
    for index in range(len(tasks)):
        state_key = f"task_{day}_{index}"
        if state_key not in st.session_state:
            st.session_state[state_key] = False

# Helper functions for calculations
def get_active_task_index(tasks):
    """Returns the index of the task that is active right now, or -1 if none."""
    now_time = datetime.datetime.now(IST).time()
    for idx, item in enumerate(tasks):
        try:
            parts = item["time"].split("-")
            if len(parts) == 2:
                start_str = parts[0].strip()
                end_str = parts[1].strip()
                start_time = datetime.datetime.strptime(start_str, "%I:%M %p").time()
                end_time = datetime.datetime.strptime(end_str, "%I:%M %p").time()
                
                # Check range (assume no cross-midnight for schedule)
                if start_time <= end_time:
                    if start_time <= now_time <= end_time:
                        return idx
                else: # cross-midnight just in case
                    if now_time >= start_time or now_time <= end_time:
                        return idx
        except Exception:
            pass
    return -1

def get_time_remaining(time_str):
    """Calculates minutes left in the current active task slot."""
    try:
        parts = time_str.split("-")
        if len(parts) == 2:
            end_str = parts[1].strip()
            now = datetime.datetime.now(IST)
            end_time = datetime.datetime.strptime(end_str, "%I:%M %p").time()
            end_dt = datetime.datetime.combine(now.date(), end_time, tzinfo=IST)
            
            if end_dt < now:
                # Handle edge case where clock just passed the time
                return 0
            
            diff = end_dt - now
            return int(diff.total_seconds() / 60)
    except Exception:
        pass
    return None

# ---------------------------------------------------------
# 3. STYLING (ADVANCED DEVELOPER ENVIRONMENT STYLE)
# ---------------------------------------------------------
st.markdown("""
<style>
/* Import JetBrains Mono and Inter */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

/* Main font structure */
.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Inter', -apple-system, sans-serif;
}

/* Header styled as a compiler console output */
.dev-header {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 1.25rem;
    margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
    position: relative;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.dev-header::before {
    content: "● ● ●";
    color: #8b949e;
    position: absolute;
    top: 10px;
    left: 15px;
    font-size: 8px;
    letter-spacing: 2px;
}

.dev-title {
    color: #58a6ff;
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 0px;
}

.dev-status {
    color: #7ee787;
    font-size: 0.85rem;
    margin-top: 8px;
    line-height: 1.4;
}

.dev-time {
    color: #ff7b72;
    font-weight: 600;
}

/* Tabs customization */
.stTabs [data-baseweb="tab-list"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px;
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    color: #8b949e;
    background-color: transparent;
    padding: 8px 16px;
    border-radius: 4px;
    border: none !important;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #c9d1d9;
    background-color: #21262d;
}

.stTabs [aria-selected="true"] {
    background-color: #1f6feb !important;
    color: #ffffff !important;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(31, 111, 235, 0.4);
}

/* Time badge styling */
.time-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: #58a6ff;
    background-color: #161b22;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #30363d;
}

.time-badge-active {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: #56d364;
    background-color: #0f2e1b;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #2ea043;
    animation: blinker 2s linear infinite;
}

@keyframes blinker {
    50% { opacity: 0.75; }
}

/* Custom visual improvements to Streamlit widgets */
.stCheckbox > label {
    margin-bottom: 0px !important;
}

/* Progress bar alignment */
.stProgress > div > div {
    background-color: #21262d !important;
}

.stProgress > div > div > div > div {
    background-color: #56d364 !important;
}

/* Sidebar styling improvements */
[data-testid="stSidebar"] {
    background-color: #0d1117;
    border-right: 1px solid #30363d;
}

.sidebar-header {
    font-family: 'JetBrains Mono', monospace;
    color: #c9d1d9;
    border-bottom: 1px solid #30363d;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

.stat-item {
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 10px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. SIDEBAR - CONTROL PANEL & SYSTEM STATE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">### 🛠️ SYSTEM CONTROL</div>', unsafe_allow_html=True)
    
    # Calculate Overall Weekly Progress
    total_weekly_tasks = sum(len(tasks) for tasks in WEEKLY_SCHEDULE.values())
    completed_weekly_tasks = sum(
        st.session_state[f"task_{day}_{idx}"]
        for day in WEEKLY_SCHEDULE
        for idx in range(len(WEEKLY_SCHEDULE[day]))
    )
    weekly_percent = int((completed_weekly_tasks / total_weekly_tasks) * 100) if total_weekly_tasks > 0 else 0
    
    st.markdown(f"**Weekly Compliance Rate:**")
    st.progress(weekly_percent / 100.0)
    st.markdown(f"<div class='stat-item'>📊 Completed: {completed_weekly_tasks}/{total_weekly_tasks} ({weekly_percent}%)</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**System Environment:**")
    st.markdown(f"<div class='stat-item'>🐍 Python: 3.11.15</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-item'>⚡ Streamlit: {st.__version__}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-item'>📆 Today: {datetime.datetime.now(IST).strftime('%A')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-item'>🕒 Current Time (IST): {datetime.datetime.now(IST).strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Global Actions:**")
    if st.button("🧹 Clear All Week", use_container_width=True, type="secondary"):
        for day in WEEKLY_SCHEDULE:
            for idx in range(len(WEEKLY_SCHEDULE[day])):
                st.session_state[f"task_{day}_{idx}"] = False
        st.success("All checkboxes reset!")
        time.sleep(0.5)
        st.rerun()

# ---------------------------------------------------------
# 5. MAIN HEADER
# ---------------------------------------------------------
now = datetime.datetime.now(IST)
curr_day = now.strftime("%A")
curr_time_str = now.strftime("%I:%M %p")

# Show console styled header
active_task_status = "No current active task"
if curr_day in WEEKLY_SCHEDULE:
    active_idx = get_active_task_index(WEEKLY_SCHEDULE[curr_day])
    if active_idx != -1:
        active_task_status = f"Executing: {WEEKLY_SCHEDULE[curr_day][active_idx]['task']}"

st.markdown(f"""
<div class="dev-header">
    <div class="dev-title">$ run weekly_routine.sh</div>
    <div class="dev-status">
        [SYSTEM STATUS] COMPILING ROUTINE FOR THE WEEK...<br>
        [CURRENT TIME] <span class="dev-time">{curr_day}, {curr_time_str}</span><br>
        [ACTIVE THREAD] <span style="color: #a78bfa;">{active_task_status}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. TAB ARCHITECTURE
# ---------------------------------------------------------
# Calculate status emojis for the tabs programmatically
tab_titles = []
for day in DAYS_OF_WEEK:
    completed = sum(st.session_state[f"task_{day}_{idx}"] for idx in range(len(WEEKLY_SCHEDULE[day])))
    total = len(WEEKLY_SCHEDULE[day])
    pct = int((completed / total) * 100) if total > 0 else 0
    
    if pct == 100:
        tab_titles.append(f"{day} ✅")
    elif pct > 0:
        tab_titles.append(f"{day} ({pct}%)")
    else:
        tab_titles.append(f"{day} 💤")

# Create tabs
tabs = st.tabs(tab_titles)

for i, day in enumerate(DAYS_OF_WEEK):
    tasks = WEEKLY_SCHEDULE[day]
    active_idx = get_active_task_index(tasks) if day == curr_day else -1
    
    with tabs[i]:
        st.markdown(f"### {day}'s Timetable")
        
        # Display Tasks
        for idx, item in enumerate(tasks):
            is_active = (idx == active_idx)
            state_key = f"task_{day}_{idx}"
            
            # Using st.container with custom styled layouts
            with st.container(border=True):
                col_check, col_details = st.columns([1, 19])
                
                with col_check:
                    # Persist checkbox via key
                    checked = st.checkbox("", key=state_key, label_visibility="collapsed")
                
                with col_details:
                    time_str = item["time"]
                    task_text = item["task"]
                    
                    # Style formatting
                    if is_active:
                        mins_left = get_time_remaining(time_str)
                        time_badge = f"<span class='time-badge-active'>🕒 {time_str} • ACTIVE NOW"
                        if mins_left is not None and mins_left > 0:
                            time_badge += f" ({mins_left}m left)"
                        time_badge += "</span>"
                    else:
                        time_badge = f"<span class='time-badge'>🕒 {time_str}</span>"
                    
                    if checked:
                        task_desc = f"<span style='text-decoration: line-through; color: #8b949e; font-style: italic;'>{task_text}</span>"
                    elif is_active:
                        task_desc = f"<span style='color: #ff7b72; font-weight: 700;'>{task_text} ⚡</span>"
                    else:
                        task_desc = f"<span style='color: #c9d1d9; font-weight: 600;'>{task_text}</span>"
                    
                    st.markdown(f"{time_badge} &nbsp;&nbsp;&nbsp; {task_desc}", unsafe_allow_html=True)
        
        # ---------------------------------------------------------
        # PROGRESS BAR & TAB ACTIONS
        # ---------------------------------------------------------
        completed_count = sum(st.session_state[f"task_{day}_{idx}"] for idx in range(len(tasks)))
        total_count = len(tasks)
        percent = completed_count / total_count if total_count > 0 else 0.0
        
        st.markdown("---")
        col_bar, col_button = st.columns([15, 5])
        
        with col_bar:
            st.markdown(f"**{day} Progress:** {completed_count}/{total_count} tasks completed ({int(percent * 100)}%)")
            st.progress(percent)
            
        with col_button:
            # Add reset button for current day
            if st.button(f"Reset {day} 🧹", key=f"reset_{day}", use_container_width=True):
                for idx in range(len(tasks)):
                    st.session_state[f"task_{day}_{idx}"] = False
                st.success(f"{day} reset!")
                time.sleep(0.5)
                st.rerun()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #8b949e; border-top: 1px solid #30363d; padding-top: 1.5rem; margin-bottom: 2rem;">
    <span>⚡ COMPRESSED MEMORY TIMETABLE // SECURE_PORT:8501 // STATUS: ONLINE 🟢</span>
</div>
""", unsafe_allow_html=True)
