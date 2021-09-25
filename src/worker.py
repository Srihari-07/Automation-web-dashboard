from AutomationEngine.downloadsOrganizer import organize_Downloads # Actual Automation Script

# Worker function for Organizing Download's Folder
def downloadsOrganizer(app, task_id, update_status, update_progress):
    # Updates the Database based on the progress of the work done.
    def report_progress(percent):
        update_progress(app,task_id, percent)

    # --- Automation Logic here ---
    try:
        update_status(app,task_id, "running")

        # Automation Script
        results = organize_Downloads(
            progress_callback=report_progress
        )

        update_status(app,task_id, "completed")
        update_progress(app,task_id,100)
    except Exception as e:
        update_status(app,task_id, "failed")
        print("Error in worker")
        

        





	