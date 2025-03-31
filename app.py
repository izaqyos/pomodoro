import streamlit as st
import time
from datetime import timedelta, datetime, date
import os
import base64
from io import BytesIO
from PIL import Image
from utils import get_sound_html, create_directories
from data_manager import PomodoroDataManager
from stats_page import show_stats_page

# Set page configuration
st.set_page_config(
    page_title="Pomodoro Timer",
    page_icon="⏰",
    layout="centered",
)

# Initialize data manager
data_manager = PomodoroDataManager()

# Load CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("style.css")
except FileNotFoundError:
    # Fallback to inline CSS if file not found
    st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #FF6347;
            text-align: center;
            margin-bottom: 1rem;
        }
        .timer-display {
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
            margin: 2rem 0;
        }
        .session-info {
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .completed-tasks {
            color: #4CAF50;
            text-decoration: line-through;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }
        .stButton button {
            min-width: 100px;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to get image as base64 for beep sound
def get_base64_audio_html(audio_path):
    """Generate base64 encoded html audio tag"""
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        html = f"""
            <audio autoplay>
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
        """
        return html

# Initialize session state
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
    st.session_state.work_duration = 25
    st.session_state.short_break_duration = 5
    st.session_state.long_break_duration = 15
    st.session_state.pomodoro_count = 0
    st.session_state.current_mode = "Work"
    st.session_state.remaining_time = st.session_state.work_duration * 60
    st.session_state.start_time = None
    st.session_state.tasks = []
    st.session_state.completed_tasks = []
    st.session_state.show_stats = False
    st.session_state.show_add_task = False
    st.session_state.task_statuses = ["Open", "In Progress", "Done", "Blocked"]

# Ensure directories exist
create_directories()

# Choose which page to display
if st.session_state.show_stats:
    show_stats_page()
else:
    # App title
    st.markdown('<div class="main-title">Pomodoro Timer</div>', unsafe_allow_html=True)
    
    # Display current date
    current_date = date.today().strftime("%A, %B %d, %Y")
    st.markdown(f'<div class="date-display">📅 {current_date}</div>', unsafe_allow_html=True)
    
    # Add real-time clock display with seconds - initialize with current server time
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Custom JavaScript for all time-related displays - more reliable implementation
    st.markdown(f"""
    <div class="clock-display" id="clock">{current_time}</div>
    <script>
        // Initialize or get the global timers object to avoid duplicate intervals
        window.pomodoroTimers = window.pomodoroTimers || {{}};
        
        // Clear any existing clock interval
        if (window.pomodoroTimers.clockIntervalId) {{
            clearInterval(window.pomodoroTimers.clockIntervalId);
            window.pomodoroTimers.clockIntervalId = null;
        }}
        
        // Function to update the clock
        function updateClock() {{
            console.log("Updating clock");
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            
            const clockElement = document.getElementById('clock');
            if (clockElement) {{
                clockElement.textContent = `${{hours}}:${{minutes}}:${{seconds}}`;
                console.log("Clock updated:", `${{hours}}:${{minutes}}:${{seconds}}`);
            }}
        }}
        
        // Start the clock immediately and set interval
        console.log("Starting clock");
        updateClock();
        window.pomodoroTimers.clockIntervalId = setInterval(updateClock, 1000);
        console.log("Clock started with interval ID:", window.pomodoroTimers.clockIntervalId);
    </script>
    """, unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Timer durations
        col1, col2 = st.columns(2)
        with col1:
            new_work_duration = st.number_input("Work Duration (min)", min_value=1, max_value=60, value=st.session_state.work_duration)
        with col2:
            new_short_break = st.number_input("Short Break (min)", min_value=1, max_value=30, value=st.session_state.short_break_duration)
        
        new_long_break = st.number_input("Long Break (min)", min_value=1, max_value=60, value=st.session_state.long_break_duration)
        
        # Apply settings if changed
        if (new_work_duration != st.session_state.work_duration or 
            new_short_break != st.session_state.short_break_duration or 
            new_long_break != st.session_state.long_break_duration):
            
            st.session_state.work_duration = new_work_duration
            st.session_state.short_break_duration = new_short_break
            st.session_state.long_break_duration = new_long_break
            
            # Reset timer if settings changed
            if not st.session_state.timer_running:
                if st.session_state.current_mode == "Work":
                    st.session_state.remaining_time = st.session_state.work_duration * 60
                elif st.session_state.current_mode == "Short Break":
                    st.session_state.remaining_time = st.session_state.short_break_duration * 60
                else:  # Long Break
                    st.session_state.remaining_time = st.session_state.long_break_duration * 60
        
        # Task management
        st.header("📝 Task Management")
        if st.button("Add New Task"):
            st.session_state.show_add_task = True
            st.experimental_rerun()
        
        # Statistics toggle
        st.header("📊 Statistics")
        if st.button("View Statistics"):
            st.session_state.show_stats = True
            st.experimental_rerun()

    # Task addition form
    if st.session_state.show_add_task:
        st.subheader("Add New Task")
        with st.form("add_task_form"):
            new_task = st.text_input("Task Description")
            col1, col2 = st.columns(2)
            with col1:
                task_status = st.selectbox("Status", st.session_state.task_statuses)
            with col2:
                due_date = st.date_input("Due Date", min_value=date.today())
            
            submit = st.form_submit_button("Add Task")
            if submit and new_task:
                # Create a task dictionary with all information
                task = {
                    "description": new_task,
                    "status": task_status,
                    "due_date": due_date.isoformat(),
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.tasks.append(task)
                st.session_state.show_add_task = False
                st.experimental_rerun()
        
        if st.button("Cancel"):
            st.session_state.show_add_task = False
            st.experimental_rerun()

    # Main container for the timer
    mode_class = "work-mode" if st.session_state.current_mode == "Work" else "break-mode"
    mode_emoji = "🍅" if st.session_state.current_mode == "Work" else "☕"

    st.markdown(f'<div class="{mode_class}">', unsafe_allow_html=True)

    # Display current mode
    st.markdown(f'<div class="session-info">{mode_emoji} {st.session_state.current_mode} Session</div>', unsafe_allow_html=True)

    # Calculate initial timer value in HH:MM:SS format
    hours, remainder = divmod(st.session_state.remaining_time, 3600)
    mins, secs = divmod(remainder, 60)
    timer_text = f"{hours:02d}:{mins:02d}:{secs:02d}"
    
    # Create a div with ID for JavaScript to update
    timer_id = "pomodoro-timer"
    
    # Display timer with JavaScript for real-time updates - improved implementation
    st.markdown(f"""
    <div class="timer-display" id="{timer_id}">{timer_text}</div>
    <script>
        // Initialize or update timer variables - use the same global object
        window.pomodoroTimers = window.pomodoroTimers || {{}};
        window.pomodoroTimers.remainingSeconds = {st.session_state.remaining_time};
        window.pomodoroTimers.timerRunning = {str(st.session_state.timer_running).lower()};
        
        // Clear any existing timer interval
        if (window.pomodoroTimers.timerIntervalId) {{
            clearInterval(window.pomodoroTimers.timerIntervalId);
            window.pomodoroTimers.timerIntervalId = null;
            console.log("Cleared previous timer interval");
        }}
        
        // Function to update the timer display
        function updateTimerDisplay() {{
            if (!window.pomodoroTimers.timerRunning) return;
            
            if (window.pomodoroTimers.remainingSeconds > 0) {{
                window.pomodoroTimers.remainingSeconds -= 1;
                
                // Calculate hours, minutes, seconds
                const hours = Math.floor(window.pomodoroTimers.remainingSeconds / 3600);
                const remainder = window.pomodoroTimers.remainingSeconds % 3600;
                const minutes = Math.floor(remainder / 60);
                const seconds = remainder % 60;
                
                // Format with leading zeros
                const displayHours = String(hours).padStart(2, '0');
                const displayMinutes = String(minutes).padStart(2, '0');
                const displaySeconds = String(seconds).padStart(2, '0');
                
                // Update display
                const timerElement = document.getElementById("{timer_id}");
                if (timerElement) {{
                    timerElement.textContent = `${{displayHours}}:${{displayMinutes}}:${{displaySeconds}}`;
                    console.log("Timer updated:", `${{displayHours}}:${{displayMinutes}}:${{displaySeconds}}`);
                }}
                
                // If timer reaches zero, notify server
                if (window.pomodoroTimers.remainingSeconds === 0) {{
                    window.parent.postMessage({{type: 'timer_ended'}}, '*');
                    setTimeout(function() {{ window.location.reload(); }}, 500);
                }}
            }}
        }}
        
        // Start timer if it should be running
        if (window.pomodoroTimers.timerRunning) {{
            window.pomodoroTimers.timerIntervalId = setInterval(updateTimerDisplay, 1000);
            console.log("Pomodoro timer started with " + window.pomodoroTimers.remainingSeconds + 
                        " seconds remaining, interval ID:", window.pomodoroTimers.timerIntervalId);
        }}
    </script>
    """, unsafe_allow_html=True)

    # Progress bar
    total_seconds = 0
    if st.session_state.current_mode == "Work":
        total_seconds = st.session_state.work_duration * 60
    elif st.session_state.current_mode == "Short Break":
        total_seconds = st.session_state.short_break_duration * 60
    else:  # Long Break
        total_seconds = st.session_state.long_break_duration * 60

    progress = 1.0 - (st.session_state.remaining_time / total_seconds) if total_seconds > 0 else 0
    st.progress(progress)

    # Display pomodoro count
    st.markdown(f"<div class='session-info'>Completed Pomodoros: {st.session_state.pomodoro_count}</div>", unsafe_allow_html=True)
    
    # Add debug info to verify timer status
    if st.session_state.timer_running:
        debug_status = "Running"
    else:
        debug_status = "Paused"
    st.markdown(f"<div class='debug-info'>Timer Status: {debug_status} • Remaining Time: {st.session_state.remaining_time}s</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close the mode container

    # Timer control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        button_id = "start_stop_button"
        start_stop_text = "▶️ Start" if not st.session_state.timer_running else "⏸️ Pause"
        start_stop_button = st.button(start_stop_text, key=button_id)
        
    with col2:
        reset_button = st.button("🔄 Reset")
        
    with col3:
        skip_button = st.button("⏭️ Skip")

    # Add JavaScript to enable immediate response to button clicks
    st.markdown(f"""
    <script>
        // Function to update UI when timer state changes
        window.updateTimerUI = function(isRunning) {{
            window.pomodoroTimers.timerRunning = isRunning;
            
            if (isRunning && !window.pomodoroTimers.timerIntervalId) {{
                window.pomodoroTimers.timerIntervalId = setInterval(updateTimerDisplay, 1000);
                console.log("Timer started via UI update, new interval ID:", window.pomodoroTimers.timerIntervalId);
            }} else if (!isRunning && window.pomodoroTimers.timerIntervalId) {{
                clearInterval(window.pomodoroTimers.timerIntervalId);
                window.pomodoroTimers.timerIntervalId = null;
                console.log("Timer paused via UI update");
            }}
        }};
        
        // Add click handlers to timer control buttons
        document.addEventListener('DOMContentLoaded', function() {{
            // Wait a short time for all elements to be available
            setTimeout(function() {{
                // Find and attach click handlers to all timer control buttons
                document.querySelectorAll('button').forEach(function(button) {{
                    const buttonText = button.innerText.toLowerCase();
                    
                    // Already attached event listeners
                    if (button.hasAttribute('data-timer-button')) return;
                    
                    if (buttonText.includes('start') || buttonText.includes('pause')) {{
                        button.setAttribute('data-timer-button', 'start-pause');
                        button.addEventListener('click', function() {{
                            console.log("Start/Pause button clicked");
                            window.updateTimerUI(!window.pomodoroTimers.timerRunning);
                        }});
                    }}
                }});
            }}, 500);
        }});
    </script>
    """, unsafe_allow_html=True)

    # Handle button clicks
    if start_stop_button:
        st.session_state.timer_running = not st.session_state.timer_running
        if st.session_state.timer_running:
            st.session_state.start_time = time.time()
        # Force reload to update JavaScript timer state
        st.experimental_rerun()

    if reset_button:
        st.session_state.timer_running = False
        if st.session_state.current_mode == "Work":
            st.session_state.remaining_time = st.session_state.work_duration * 60
        elif st.session_state.current_mode == "Short Break":
            st.session_state.remaining_time = st.session_state.short_break_duration * 60
        else:  # Long Break
            st.session_state.remaining_time = st.session_state.long_break_duration * 60
        # Force reload to update JavaScript timer state
        st.experimental_rerun()

    if skip_button:
        st.session_state.timer_running = False
        
        # Switch modes
        if st.session_state.current_mode == "Work":
            st.session_state.pomodoro_count += 1
            # Save completed pomodoro to stats
            data_manager.save_pomodoro_completed()
            
            if st.session_state.pomodoro_count % 4 == 0:
                st.session_state.current_mode = "Long Break"
                st.session_state.remaining_time = st.session_state.long_break_duration * 60
            else:
                st.session_state.current_mode = "Short Break"
                st.session_state.remaining_time = st.session_state.short_break_duration * 60
        else:  # If in a break
            st.session_state.current_mode = "Work"
            st.session_state.remaining_time = st.session_state.work_duration * 60
        
        st.experimental_rerun()

    # Task lists
    st.markdown("---")
    st.subheader("📋 Task Management")

    # Display tasks with status and due date
    task_container = st.container()
    with task_container:
        # Filter controls
        col1, col2 = st.columns(2)
        with col1:
            filter_status = st.multiselect("Filter by Status", 
                                        options=st.session_state.task_statuses, 
                                        default=st.session_state.task_statuses)
        with col2:
            filter_date = st.radio("Filter by Due Date", 
                                   ["All", "Today", "This Week", "Overdue"], 
                                   horizontal=True)
        
        # Function to check if a task should be displayed based on filters
        def should_display_task(task):
            # Status filter
            if task["status"] not in filter_status:
                return False
            
            # Date filter
            task_due_date = date.fromisoformat(task["due_date"])
            today = date.today()
            
            if filter_date == "Today" and task_due_date != today:
                return False
            elif filter_date == "This Week":
                # Check if the due date is within the next 7 days
                week_from_now = today + timedelta(days=7)
                if not (today <= task_due_date <= week_from_now):
                    return False
            elif filter_date == "Overdue":
                if task_due_date >= today:
                    return False
            
            return True
        
        # Pending tasks
        st.subheader("Pending Tasks")
        if not st.session_state.tasks:
            st.info("No pending tasks. Add a task using the sidebar.")
        else:
            # Filter tasks
            filtered_tasks = [task for task in st.session_state.tasks if should_display_task(task)]
            
            if not filtered_tasks:
                st.info("No tasks match your filter criteria.")
            
            # Sort tasks by due date
            filtered_tasks.sort(key=lambda x: date.fromisoformat(x["due_date"]))
            
            for idx, task in enumerate(filtered_tasks):
                with st.container():
                    st.markdown(f'<div class="task-card status-{task["status"].lower().replace(" ", "-")}">', unsafe_allow_html=True)
                    
                    # Task details row
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{idx+1}. {task['description']}**")
                    
                    with col2:
                        due_date = date.fromisoformat(task["due_date"])
                        due_text = due_date.strftime("%b %d")
                        
                        # Highlight overdue tasks
                        if due_date < date.today():
                            st.markdown(f"<span class='overdue-date'>🚨 {due_text}</span>", unsafe_allow_html=True)
                        else:
                            st.write(f"📅 {due_text}")
                    
                    with col3:
                        # Display task status with appropriate styling
                        status_colors = {
                            "Open": "🔵", 
                            "In Progress": "🟠", 
                            "Done": "🟢", 
                            "Blocked": "🔴"
                        }
                        status_emoji = status_colors.get(task["status"], "⚪️")
                        st.write(f"{status_emoji} {task['status']}")
                    
                    with col4:
                        # Action buttons
                        action_col1, action_col2 = st.columns(2)
                        with action_col1:
                            # Update status button
                            if st.button("✏️", key=f"edit_{idx}"):
                                # Show status update form for this task
                                task["_editing"] = True
                                st.experimental_rerun()
                        
                        with action_col2:
                            # Complete/Done button
                            if st.button("✓", key=f"done_{idx}"):
                                # If already done, move to completed tasks
                                if task["status"] == "Done":
                                    st.session_state.completed_tasks.append(task)
                                    st.session_state.tasks.remove(task)
                                    # Save completed task to stats
                                    data_manager.save_task_completed(task["description"])
                                # Otherwise, mark as done
                                else:
                                    task["status"] = "Done"
                                st.experimental_rerun()
                    
                    # Status update form if editing
                    if task.get("_editing", False):
                        new_status = st.selectbox(
                            "Update Status",
                            st.session_state.task_statuses,
                            index=st.session_state.task_statuses.index(task["status"]),
                            key=f"status_{idx}"
                        )
                        new_due_date = st.date_input(
                            "Update Due Date",
                            date.fromisoformat(task["due_date"]),
                            key=f"due_date_{idx}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Save", key=f"save_{idx}"):
                                task["status"] = new_status
                                task["due_date"] = new_due_date.isoformat()
                                task.pop("_editing", None)
                                st.experimental_rerun()
                        with col2:
                            if st.button("Cancel", key=f"cancel_{idx}"):
                                task.pop("_editing", None)
                                st.experimental_rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

        # Add "Add Task" button at the bottom of the list
        if st.button("➕ Add New Task", key="add_task_bottom"):
            st.session_state.show_add_task = True
            st.experimental_rerun()

        # Completed tasks
        st.subheader("Completed Tasks")
        if not st.session_state.completed_tasks:
            st.info("No completed tasks yet.")
        else:
            for idx, task in enumerate(st.session_state.completed_tasks):
                description = task["description"] if isinstance(task, dict) else task
                st.markdown(f'<div class="completed-tasks task-card">✅ {idx+1}. {description}</div>', unsafe_allow_html=True)

    # Update timer
    if st.session_state.timer_running:
        # For server-side timer updates
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.remaining_time = max(0, st.session_state.remaining_time - int(elapsed_time))
        st.session_state.start_time = time.time()
        
        # If timer ends
        if st.session_state.remaining_time <= 0:
            st.session_state.timer_running = False
            
            # Play notification sound using our utility function
            st.markdown(get_sound_html(), unsafe_allow_html=True)
            st.balloons()
            
            # Switch modes
            if st.session_state.current_mode == "Work":
                st.session_state.pomodoro_count += 1
                # Save completed pomodoro to stats
                data_manager.save_pomodoro_completed()
                
                if st.session_state.pomodoro_count % 4 == 0:
                    st.session_state.current_mode = "Long Break"
                    st.session_state.remaining_time = st.session_state.long_break_duration * 60
                else:
                    st.session_state.current_mode = "Short Break"
                    st.session_state.remaining_time = st.session_state.short_break_duration * 60
            else:  # If in a break
                st.session_state.current_mode = "Work"
                st.session_state.remaining_time = st.session_state.work_duration * 60
            
            # Force page reload to reset timer
            st.experimental_rerun()
        
        # Add JavaScript to listen for timer completion
        st.markdown("""
        <script>
            // Listen for timer completion
            window.addEventListener('message', function(e) {
                // Check if the message is about the timer ending
                if (e.data && e.data.type === 'timer_ended') {
                    // Reload the page to trigger server-side timer end processing
                    window.location.reload();
                }
            });
        </script>
        """, unsafe_allow_html=True)

    # Add explanatory text at the bottom
    st.markdown("""
    ---
    ### How to Use the Pomodoro Timer

    1. **Work Session (Pomodoro)**: Focus on a task for the work duration (default 25 minutes)
    2. **Short Break**: Take a short break (default 5 minutes)
    3. **After 4 Work Sessions**: Take a longer break (default 15 minutes)

    Use the task list to keep track of what you're working on!
    """)

    # Footer
    st.markdown(
        '<div class="footer">Pomodoro Timer App • Made with ❤️ using Streamlit</div>',
        unsafe_allow_html=True
    ) 