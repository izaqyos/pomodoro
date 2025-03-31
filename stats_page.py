import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, date, timedelta
from data_manager import PomodoroDataManager

def show_stats_page():
    """Show the statistics page"""
    
    st.markdown('<div class="main-title">Pomodoro Statistics</div>', unsafe_allow_html=True)
    
    # Display current date
    current_date = date.today().strftime("%A, %B %d, %Y")
    st.markdown(f'<div class="date-display">📅 {current_date}</div>', unsafe_allow_html=True)
    
    # Initialize data manager
    data_manager = PomodoroDataManager()
    
    # Load daily stats
    daily_stats = data_manager.load_daily_stats()
    weekly_summary = data_manager.get_weekly_summary()
    task_stats = data_manager.get_tasks_stats()
    
    # Daily stats section
    st.markdown("## Today's Progress")
    
    # Create columns for today's stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pomodoros Completed", daily_stats["pomodoros_completed"])
    
    with col2:
        completed_tasks = daily_stats.get("completed_tasks", [])
        st.metric("Tasks Completed", len(completed_tasks))
    
    with col3:
        last_completed = daily_stats.get("last_completed")
        if last_completed:
            last_time = datetime.fromisoformat(last_completed).strftime("%H:%M:%S")
            st.metric("Last Pomodoro", last_time)
        else:
            st.metric("Last Pomodoro", "None")
    
    # Weekly stats section
    st.markdown("## Weekly Overview")
    
    if weekly_summary["total_pomodoros"] > 0:
        # Create a DataFrame for the chart
        dates = []
        counts = []
        
        # Get the last 7 days
        today = date.today()
        for i in range(6, -1, -1):  # 6 days ago to today
            day = today - timedelta(days=i)
            day_iso = day.isoformat()
            count = weekly_summary["daily_counts"].get(day_iso, 0)
            dates.append(day.strftime("%a"))  # Abbreviated day name
            counts.append(count)
        
        # Create DataFrame
        data = pd.DataFrame({
            "Day": dates,
            "Pomodoros": counts
        })
        
        # Create chart
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X("Day", sort=None),  # Don't sort to keep chronological order
            y="Pomodoros",
            color=alt.condition(
                alt.datum.Pomodoros > 0,
                alt.value("#FF6347"),  # Tomato color for days with pomodoros
                alt.value("#DDDDDD")   # Gray for days without pomodoros
            ),
            tooltip=["Day", "Pomodoros"]
        ).properties(
            title="Pomodoros Completed This Week"
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Summary statistics
        st.markdown("### Weekly Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Pomodoros", weekly_summary["total_pomodoros"])
        
        with col2:
            st.metric("Days Active", weekly_summary["days_active"])
        
        with col3:
            daily_avg = weekly_summary["total_pomodoros"] / max(1, weekly_summary["days_active"])
            st.metric("Daily Average", f"{daily_avg:.1f}")
        
        # Most productive day
        if weekly_summary["daily_counts"]:
            most_productive_day = max(weekly_summary["daily_counts"].items(), key=lambda x: x[1])
            day_name = datetime.fromisoformat(most_productive_day[0]).strftime("%A")
            st.success(f"🏆 Your most productive day was **{day_name}** with **{most_productive_day[1]}** pomodoros!")
    else:
        st.info("No pomodoros completed this week yet. Complete your first one to start tracking!")
    
    # Task statistics section
    st.markdown("## Task Statistics")
    
    # Create a task status distribution chart if we have task data
    if weekly_summary["task_counts"]["total"] > 0:
        # Create data for the chart
        status_data = []
        for status, count in weekly_summary["task_counts"]["by_status"].items():
            if count > 0:
                status_data.append({"Status": status, "Count": count})
        
        # If we have status data, create a chart
        if status_data:
            status_df = pd.DataFrame(status_data)
            
            # Create pie chart for task status distribution
            status_chart = alt.Chart(status_df).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(
                    field="Status", 
                    type="nominal",
                    scale=alt.Scale(
                        domain=["Open", "In Progress", "Done", "Blocked"],
                        range=["#2196F3", "#FF9800", "#4CAF50", "#F44336"]
                    )
                ),
                tooltip=["Status", "Count"]
            ).properties(
                title="Task Status Distribution",
                width=300,
                height=300
            )
            
            st.altair_chart(status_chart, use_container_width=True)
            
            # Show task status count metrics
            st.markdown("### Task Status Breakdown")
            status_cols = st.columns(4)
            
            status_colors = {
                "Open": "🔵", 
                "In Progress": "🟠", 
                "Done": "🟢", 
                "Blocked": "🔴"
            }
            
            for i, (status, count) in enumerate(weekly_summary["task_counts"]["by_status"].items()):
                with status_cols[i % 4]:
                    emoji = status_colors.get(status, "⚪️")
                    st.metric(f"{emoji} {status}", count)
        
        # Add a total tasks metric 
        st.metric("Total Tasks", weekly_summary["task_counts"]["total"])
    else:
        st.info("No tasks completed this week yet. Complete some tasks to see statistics!")
    
    # Task completion section
    st.markdown("## Recent Task Completions")
    
    completed_tasks = daily_stats.get("completed_tasks", [])
    if completed_tasks:
        for i, task in enumerate(completed_tasks):
            if isinstance(task, dict):
                description = task.get("description", task.get("text", "Unknown Task"))
                completed_time = datetime.fromisoformat(task["completed_at"]).strftime("%H:%M:%S")
                status = task.get("status", "Done")
                
                # Get status emoji
                status_colors = {
                    "Open": "🔵", 
                    "In Progress": "🟠", 
                    "Done": "🟢", 
                    "Blocked": "🔴"
                }
                emoji = status_colors.get(status, "⚪️")
                
                st.markdown(f"**{i+1}.** {description} {emoji} - *completed at {completed_time}*")
            else:
                # Handle legacy format tasks that are just strings
                st.markdown(f"**{i+1}.** {task} - *completed today*")
    else:
        st.info("No tasks completed today yet. Complete a task to see it here!")
    
    # Navigation back to main app
    if st.button("⬅️ Back to Timer"):
        st.session_state.show_stats = False
        st.experimental_rerun() 