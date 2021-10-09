const scriptBtn = document.getElementById("scriptBtn");
const outputWindow = document.getElementById("output");
const taskStatus = document.getElementById("taskStatus");

// Frontend POLLING
async function checkStatus(taskID){
    taskStatus.classList.add("taskStatus"); // Panel to show the Task Status.

    const response = await fetch(`/api/downloads_Organizer/status/${taskID}`, { method: "GET" });
    const data = await response.json();

    taskStatus.innerText = data.status;

    if(!response.ok){  // If the response code is between 400 to 500
        outputWindow.innerHTML = data.error;
        return;
    }
    else if(data.status === "running"){
        setTimeout(() => checkStatus(taskID), 1000);
    }
    else if(data.status === "failed"){
        outputWindow.innerHTML = "";

        const statusEl = document.createElement("h2");
        statusEl.innerText = data.status;
        outputWindow.appendChild(statusEl);

        const messageEl = document.createElement("h3");
        messageEl.innerText = data.error;
        outputWindow.appendChild(messageEl);

    }
    else if(data.status === "completed"){
        // SUCCESS UI
        outputWindow.innerHTML = "";

        const statusEl = document.createElement("h2");
        statusEl.innerText = data.status;
        outputWindow.appendChild(statusEl);

        const messageEl = document.createElement("h3");
        messageEl.innerText = "Folder Organized Successfully";
        outputWindow.appendChild(messageEl);

        const detailsList = document.createElement("ul");
        detailsList.classList.add("textStyles");

        for (const [key, value] of Object.entries(data.result)) {
            const li = document.createElement("li");
            li.innerText = `${key}: ${value}`;
            detailsList.appendChild(li);
        }

        outputWindow.appendChild(detailsList);
    }
}

// Main Function for running the Script
async function downloadsOrganizer() {
    // RUNNING STATE
    scriptBtn.disabled = true;
    scriptBtn.innerText = "Running...";
    outputWindow.classList.add("outputStyle");
    outputWindow.innerHTML = "Please wait...";

    try {
        const response = await fetch("/api/downloads_Organizer/start", { method: "POST" });
        const data = await response.json();

        checkStatus(data.task_id);

    } catch (error) {
        // NETWORK / SERVER ERROR
        outputWindow.innerText = "Something went wrong";
    }

    // BACK TO IDLE
    scriptBtn.disabled = false;
    scriptBtn.innerText = "Run Again";
}

scriptBtn.addEventListener("click", downloadsOrganizer);


