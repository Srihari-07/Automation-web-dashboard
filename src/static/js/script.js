const scriptBtn = document.getElementById("scriptBtn");
const outputWindow = document.getElementById("output");
const taskStatus = document.getElementById("taskStatus");
const progressBar = document.getElementById("progress-bar");

scriptBtn.addEventListener("click", downloadsOrganizer);

// Main Function for running the Script
async function downloadsOrganizer() {
    // RUNNING STATE
    scriptBtn.disabled = true;
    progressBar.style.width = 0;
    scriptBtn.innerText = "Running...";
    outputWindow.classList.add("outputStyle");
    outputWindow.style.borderColor = "#723d0e";

    try {
        const response = await fetch("/api/downloads_Organizer/start", { method: "POST" });
        const data = await response.json();
        if(data.task_id){
            monitorTask(data.task_id , data.message);
        }
    } catch (error) {
        outputWindow.innerText = "Something went wrong";
    }
}


// Frontend POLLING
async function monitorTask(taskId,message){
    const progressContainer = document.getElementById("progress-container");
    progressContainer.classList.add("progress-container");

    outputWindow.innerHTML = message;

     // Create a timer that runs every 1.5 seconds
    const interval = setInterval(async () => {
        try {
            // 1. Fetch the latest status from your Status API
            const response = await fetch(`/api/status/${taskId}`,{ method: "GET" });
            const data = await response.json();

            // 2. Update the Progress Bar width
            progressBar.style.width = `${data.progress}%`;

            // 3. Check if we should stop the loop
            if (data.status === 'completed') {
                clearInterval(interval); // Stop asking
                outputWindow.innerHTML = "<h2> Download's Folder Organized!</h2> <h3> (Go Check it out)</h3>";
                outputWindow.style.borderColor = "#1bff00";
            }
            else if (data.status === 'failed') {
                clearInterval(interval);
                taskStatus.innerText = "Error: Task Failed";
                outputWindow.style.borderColor = "#ff0000";
            }
             // BACK TO IDLE
            scriptBtn.disabled = false;
            scriptBtn.innerText = "Run Again";

        } 
        catch (error) {
            console.error("Polling error:", error);
            clearInterval(interval);
        }
    }, 1500); 

}



