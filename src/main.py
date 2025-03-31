import streamlit as st
from datetime import datetime, date
import time
import sys
from pathlib import Path
import plotly.graph_objects as go

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.timer import PomodoroTimer
from src.utils.notifications import NotificationManager
from src.models.task import Task

def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"

def init_session_state():
    if 'timer' not in st.session_state:
        st.session_state.timer = PomodoroTimer()
    if 'notification' not in st.session_state:
        st.session_state.notification = NotificationManager()
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    if 'needs_rerun' not in st.session_state:
        st.session_state.needs_rerun = False
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

def add_task(name, description, due_date):
    task = Task(name=name, description=description, due_date=due_date)
    st.session_state.tasks.append(task)

def delete_task(index):
    st.session_state.tasks.pop(index)

def toggle_task(index):
    st.session_state.tasks[index].completed = not st.session_state.tasks[index].completed

def create_pomodoro_cycle_diagram():
    # Create a circular diagram showing the Pomodoro cycle
    labels = ['Work', 'Short Break', 'Work', 'Short Break', 
              'Work', 'Short Break', 'Work', 'Long Break']
    
    # Colors for different segments
    colors = ['#FF6B6B', '#4ECDC4', '#FF6B6B', '#4ECDC4',
             '#FF6B6B', '#4ECDC4', '#FF6B6B', '#45B7D1']
    
    # Duration values (for relative sizing)
    values = [25, 5, 25, 5, 25, 5, 25, 15]
    
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=colors,
        textinfo='label',
        textposition='inside',
        insidetextorientation='radial'
    )])
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Pomodoro Cycle",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        annotations=[{
            'text': '2hr cycle',
            'x': 0.5,
            'y': 0.5,
            'font_size': 20,
            'showarrow': False
        }],
        showlegend=False,
        width=400,
        height=400,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Pomodoro Timer",
        page_icon="⏰",
        layout="wide"  # Changed to wide layout
    )

    init_session_state()

    # Create three columns for timer, tasks, and diagram
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        # Timer section
        st.title("🍅 Pomodoro Timer")
        
        time_placeholder = st.empty()
        with time_placeholder:
            current_time = datetime.now()
            st.write(f"📅 {current_time.strftime('%A, %B %d, %Y')}")
            st.write(f"⏰ {current_time.strftime('%I:%M:%S %p')}")

        remaining_time = st.session_state.timer.work_duration - st.session_state.timer.current_time
        time_display = format_time(remaining_time)
        
        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{time_display}</h1>", 
                    unsafe_allow_html=True)

        button_col1, button_col2 = st.columns(2)
        with button_col1:
            if st.button("Start" if not st.session_state.timer.is_running else "Pause", 
                         use_container_width=True):
                if st.session_state.timer.is_running:
                    st.session_state.timer.pause()
                else:
                    st.session_state.timer.start()
                    st.session_state.needs_rerun = True

        with button_col2:
            if st.button("Reset", use_container_width=True):
                st.session_state.timer.reset()
                st.session_state.needs_rerun = False

        progress = 1 - (remaining_time / st.session_state.timer.work_duration)
        st.progress(progress)

    with col2:
        # Tasks section
        st.title("📋 Tasks")
        
        # Add new task
        with st.expander("➕ Add New Task", expanded=False):
            task_name = st.text_input("Task Name")
            task_description = st.text_area("Description")
            task_due_date = st.date_input(
                "Due Date",
                value=date.today(),
                min_value=date.today()
            )
            
            if st.button("Add Task", use_container_width=True):
                if task_name:  # Ensure task has a name
                    add_task(task_name, task_description, task_due_date)
                    st.success("Task added successfully!")
                else:
                    st.error("Task name is required!")

        # Display tasks
        if st.session_state.tasks:
            for idx, task in enumerate(st.session_state.tasks):
                with st.container():
                    col1, col2 = st.columns([6, 1])
                    with col1:
                        checkbox = st.checkbox(
                            task.name,
                            value=task.completed,
                            key=f"task_{idx}",
                            on_change=toggle_task,
                            args=(idx,)
                        )
                    with col2:
                        if st.button("🗑️", key=f"delete_{idx}"):
                            delete_task(idx)
                            st.rerun()
                    
                    with st.expander("Details", expanded=False):
                        st.write(f"**Description:** {task.description}")
                        st.write(f"**Due Date:** {task.due_date.strftime('%Y-%m-%d')}")
                        days_left = (task.due_date - date.today()).days
                        if days_left == 0:
                            st.write("**Due: Today!**")
                        elif days_left < 0:
                            st.error(f"**Overdue by {abs(days_left)} days!**")
                        else:
                            st.write(f"**Days left:** {days_left}")
        else:
            st.info("No tasks yet. Add your first task above!")

    with col3:
        # Add explanation text
        st.markdown("""
        ### How Pomodoro Works
        1. 🎯 **Work** for 25 minutes
        2. ☕ Take a **5-minute break**
        3. 🔄 Repeat 4 times
        4. 🌟 Take a **15-minute break**
        
        *Total cycle: 2 hours*
        """)
        
        # Add the cycle diagram
        st.plotly_chart(create_pomodoro_cycle_diagram(), use_container_width=True)

    # Timer logic
    if st.session_state.timer.is_running:
        current_time = time.time()
        elapsed = current_time - st.session_state.last_update
        
        if elapsed >= 1:
            st.session_state.timer.current_time += int(elapsed)
            st.session_state.last_update = current_time

            if st.session_state.timer.current_time >= st.session_state.timer.work_duration:
                st.session_state.timer.reset()
                st.session_state.notification.send_notification(
                    'Pomodoro Complete', 
                    'Time for a break!'
                )
                st.balloons()
                st.session_state.needs_rerun = False

    # Session statistics
    with st.sidebar:
        st.header("Session Info")
        st.write("Work Duration: 25 minutes")
        st.write("Break Duration: 5 minutes")
        
        # Timer settings
        st.header("Settings")
        work_duration = st.slider(
            "Work Duration (minutes)", 
            min_value=1, 
            max_value=60, 
            value=25
        )
        st.session_state.timer.work_duration = work_duration * 60

    # Control rerun behavior
    if st.session_state.timer.is_running and st.session_state.needs_rerun:
        time.sleep(0.1)
        st.rerun()

if __name__ == "__main__":
    main() 