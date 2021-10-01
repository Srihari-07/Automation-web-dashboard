async function downloadsOrganizer(){

	const response = await fetch("/api/downloads_Organizer/run", { method: "POST" });
    const data = await response.json();

    const container = document.getElementById("output");
        	container.innerHTML = '';

        	const statusEl = document.createElement('h3');
    		statusEl.innerText = `Status: ${data.status}`;
    		container.appendChild(statusEl);

    		const messageEl = document.createElement('p');
    		messageEl.innerText = data.message;
    		container.appendChild(messageEl);

    		if(response.status === 404){
    			return;
    		}
    		
    		const detailsList = document.createElement('ul');

    		for (const [key, value] of Object.entries(data.result)) {
      			const li = document.createElement('li');
      			li.innerText = `${key}: ${value}`;
      			detailsList.appendChild(li);
    		}
    		
    		container.appendChild(detailsList);
}

document.getElementById('scriptBtn').addEventListener('click', downloadsOrganizer);