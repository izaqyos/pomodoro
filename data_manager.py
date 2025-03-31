import os
import json
from datetime import datetime, date, timedelta

class PomodoroDataManager:
    """Manages data persistence for the Pomodoro application"""
    
    def __init__(self, data_dir="data"):
        """Initialize the data manager with the data directory path"""
        self.data_dir = data_dir
        self.ensure_data_dir_exists()
        
    def ensure_data_dir_exists(self):
        """Ensure that the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_stats_filepath(self):
        """Get the filepath for storing stats for the current day"""
        today = date.today().isoformat()
        return os.path.join(self.data_dir, f"stats_{today}.json")
    
    def save_pomodoro_completed(self):
        """Record a completed pomodoro"""
        filepath = self.get_stats_filepath()
        stats = self.load_daily_stats()
        
        # Update stats
        stats["pomodoros_completed"] += 1
        stats["last_completed"] = datetime.now().isoformat()
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(stats, f)
        
        return stats
    
    def load_daily_stats(self):
        """Load the daily stats"""
        filepath = self.get_stats_filepath()
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # If file is corrupted or not found, return default stats
                pass
        
        # Default stats
        return {
            "date": date.today().isoformat(),
            "pomodoros_completed": 0,
            "last_completed": None
        }
    
    def save_task_completed(self, task_description, task_data=None):
        """Record a completed task"""
        filepath = self.get_stats_filepath()
        stats = self.load_daily_stats()
        
        # Initialize tasks list if it doesn't exist
        if "completed_tasks" not in stats:
            stats["completed_tasks"] = []
        
        # Add task to completed tasks
        if task_data is None:
            # For backward compatibility with old format
            task_data = {
                "description": task_description,
                "completed_at": datetime.now().isoformat()
            }
        elif isinstance(task_data, str):
            # Handle case where task_data is just the text
            task_data = {
                "description": task_data,
                "completed_at": datetime.now().isoformat()
            }
        elif isinstance(task_data, dict) and "description" not in task_data:
            # If task_data is a dict but missing description
            task_data["description"] = task_description
        
        # Ensure completed_at is present
        if "completed_at" not in task_data:
            task_data["completed_at"] = datetime.now().isoformat()
            
        stats["completed_tasks"].append(task_data)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(stats, f)
        
        return stats
    
    def get_tasks_stats(self):
        """Get statistics about completed tasks, grouped by status"""
        filepath = self.get_stats_filepath()
        stats = self.load_daily_stats()
        
        # Default task stats
        task_stats = {
            "total_completed": 0,
            "by_status": {
                "Open": 0,
                "In Progress": 0,
                "Done": 0,
                "Blocked": 0
            }
        }
        
        # Count completed tasks
        if "completed_tasks" in stats:
            task_stats["total_completed"] = len(stats["completed_tasks"])
            
            # Count by status if available
            for task in stats["completed_tasks"]:
                if isinstance(task, dict) and "status" in task:
                    status = task["status"]
                    if status in task_stats["by_status"]:
                        task_stats["by_status"][status] += 1
                    else:
                        task_stats["by_status"][status] = 1
                else:
                    # For old format tasks without status, count as "Done"
                    task_stats["by_status"]["Done"] += 1
        
        return task_stats
    
    def get_weekly_summary(self):
        """Get a summary of the pomodoros completed in the last 7 days"""
        today = date.today()
        summary = {
            "total_pomodoros": 0,
            "days_active": 0,
            "daily_counts": {},
            "task_counts": {
                "total": 0,
                "by_status": {
                    "Open": 0,
                    "In Progress": 0,
                    "Done": 0,
                    "Blocked": 0
                }
            }
        }
        
        # Check the last 7 days
        for i in range(7):
            day = today - timedelta(days=i)
            day_iso = day.isoformat()
            day_file = os.path.join(self.data_dir, f"stats_{day_iso}.json")
            
            if os.path.exists(day_file):
                try:
                    with open(day_file, 'r') as f:
                        day_stats = json.load(f)
                        day_count = day_stats.get("pomodoros_completed", 0)
                        
                        if day_count > 0:
                            summary["days_active"] += 1
                            summary["total_pomodoros"] += day_count
                            summary["daily_counts"][day_iso] = day_count
                        
                        # Count task statistics
                        if "completed_tasks" in day_stats:
                            tasks = day_stats["completed_tasks"]
                            summary["task_counts"]["total"] += len(tasks)
                            
                            for task in tasks:
                                if isinstance(task, dict) and "status" in task:
                                    status = task["status"]
                                    if status in summary["task_counts"]["by_status"]:
                                        summary["task_counts"]["by_status"][status] += 1
                                    else:
                                        summary["task_counts"]["by_status"][status] = 1
                                else:
                                    # For old format tasks without status, count as "Done"
                                    summary["task_counts"]["by_status"]["Done"] += 1
                except:
                    # Skip if there's an error reading the file
                    pass
        
        return summary 