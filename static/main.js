let previousBotResponse;
let previousUserAction;

function replacePreviousElement(newElement, previousElement) {
    if (previousElement) {
        previousElement.remove();
    }
    return newElement;
}

async function handleAction(action) {
    const chatBox = document.getElementById('chat-box');
    const loadingSpinner = document.getElementById('loading-spinner');
  
    // Show the loading spinner
    loadingSpinner.style.display = "block";
  
    // Add the user action to the chat box
    const userActionDiv = document.createElement("div");
    userActionDiv.innerHTML = `${action.toUpperCase()}`;
  
    previousUserAction = replacePreviousElement(userActionDiv, previousUserAction);
    chatBox.appendChild(previousUserAction);

    const payload = {
        action: action
    };

    try {
        const response = await fetch('https://ai--coach-e9e8ac9df88e.herokuapp.com/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Hide the loading spinner
        loadingSpinner.style.display = "none";
    
        // Add the bot's response to the chat box
        const botResponseDiv = document.createElement("div");
        botResponseDiv.id = 'bot-response';
        botResponseDiv.innerHTML = `AI: ${data.response}`;
  
        previousBotResponse = replacePreviousElement(botResponseDiv, previousBotResponse);
        chatBox.appendChild(previousBotResponse);
        
    } catch (e) {
        // Hide the loading spinner in case of an error
        loadingSpinner.style.display = "none";
        console.error(e);
    }
}