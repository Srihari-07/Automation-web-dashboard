from services.job_manager import getTask,updateDB_status,updateDB_progress

from AutomationEngine.downloadsOrganizer import organize_Downloads # Actual Automation Script

# Worker function for Organizing Download's Folder
def downloadsOrganizer(task_id):
    currentTask = getTask(task_id)
    

        # Updates the Database based on the progress of the work done.
        def report_progress(percent):
            updateDB_progress(currentTask,percent)

        # --- Automation Logic here ---
        try:
            updateDB_status(currentTask, "running")

            # Automation Script
            results = organize_Downloads(
                progress_callback=report_progress
            )

            currentTask.status = "completed"
            currentTask.progress = 100
            db.session.commit()  # Save progress to SQLite
        except Exception as e:
            currentTask.status = "failed"
            db.session.commit()

        





	