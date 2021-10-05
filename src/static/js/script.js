const scriptBtn = document.getElementById("scriptBtn");
const taskStatus = document.getElementById("taskStatus");

// Frontend POLLING
async function checkStatus(){

    const response = await fetch("/api/downloads_Organizer/status", { method: "POST" });
    const data = await response.json();
    taskStatus.classList.add("taskStatus");
    taskStatus.innerText = data.status;

    if(data.status === "running"){
        setTimeout(checkStatus,1000)
    }
}

// Main Function for running the Script
async function downloadsOrganizer() {
    const outputWindow = document.getElementById("output");

    // RUNNING STATE
    scriptBtn.disabled = true;
    scriptBtn.innerText = "Running...";
    outputWindow.classList.add("outputStyle");
    outputWindow.innerHTML = "Please wait...";

    try {
        const response = await fetch("/api/downloads_Organizer/start", { method: "POST" });
        checkStatus();
        const data = await response.json();

        if (!response.ok) {
            outputWindow.innerHTML = "";

            const statusEl = document.createElement("h2");
            statusEl.innerText = data.status;
            outputWindow.appendChild(statusEl);

            const errorMessage = document.createElement("h3");
            errorMessage.innerText = data.message;
            outputWindow.appendChild(errorMessage);

            scriptBtn.innerText = "Try Again";
            return;
        }

    
        // SUCCESS UI
        outputWindow.innerHTML = "";

        const statusEl = document.createElement("h2");
        statusEl.innerText = data.status;
        outputWindow.appendChild(statusEl);

        const messageEl = document.createElement("h3");
        messageEl.innerText = data.message;
        outputWindow.appendChild(messageEl);

        const detailsList = document.createElement("ul");
        detailsList.classList.add("textStyles");

        for (const [key, value] of Object.entries(data.result)) {
            const li = document.createElement("li");
            li.innerText = `${key}: ${value}`;
            detailsList.appendChild(li);
        }

        outputWindow.appendChild(detailsList);

    } catch (error) {
        // NETWORK / SERVER ERROR
        outputWindow.innerText = "Something went wrong";
    }

    // BACK TO IDLE
    scriptBtn.disabled = false;
    scriptBtn.innerText = "Run Again";
}

scriptBtn.addEventListener("click", downloadsOrganizer);
