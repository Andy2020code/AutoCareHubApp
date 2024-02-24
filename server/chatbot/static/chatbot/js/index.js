var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/chat/');


function UserInput() {
    const inputElement = document.querySelector('.user-input-box');
    if (inputElement) {
        //get the value of the input
        const inputValue = inputElement.value;

        //clear the input box
        inputElement.value = "";

        //define html content to be appended
        const user_html_content = `
            <div class="user-message-information">
                <div class="user-information">
                    <h1>{{user.username}}</h1>
                </div>
                <div class="user-message">
                    <p>${inputValue}</p>
                </div>
            </div>
        `;

        //prepare to append the html content to the chat box
        //get the chat box
        const messagesDiv = document.querySelector('.messages-div');
        //append the html content to the chat box and replace username with the actual username
        messagesDiv.innerHTML += user_html_content.replace(/{{user.username}}/g, "usermane");
        //return the input value
        return inputValue;
    }else{
        console.error("Input element not found")
        return "";
    }
}

function processUserInput() {
    // Call the UserInput function to retrieve the inputValue
    const inputValue = UserInput();

    //use the value from UserInput as keyword to fetch response

  
    // Log the inputValue to the console

}

//add an event listener to the button to trigger the processUserInput function
const button = document.getElementById('send-btn');
button.addEventListener('click', function() {
  processUserInput();
});

//----------------------END OF USER INPUT PROCESS----------------------// 

//----------------------START OF AI INPUT PROCESS----------------------// 



//function to handle ai input submission
function Ai_input(responseData) {
    //check if user input is empy
    if(responseData) {
        
        //get the chat box
        const messagesDiv = document.querySelector('.messages-div');

        if (responseData) {
            
            //if there is a response, append it to the chat box
            const ai_html_content = `
                <div class="ai-message-layout latest">
                    <div class="ai-information">
                        <h1>AI</h1>
                    </div>
                    <div class="ai-content">
                        <p>${responseData}</p>
                    </div>
                </div>
            `;

            //append ai message to the chat box
            messagesDiv.insertAdjacentHTML('beforeend', ai_html_content);

            //remove the latest class from the previous latest ai message
            Remove_Latest_Class();

            //scroll to the bottom of the chat box
            setTimeout(scrollToBottom(), 1000);

        }

    }else{
        console.error("User input not found");
    }
}

function Remove_Latest_Class() {
    const latest_ai_message = document.querySelector('.ai-message-layout.latest');
    if (latest_ai_message) {
        setTimeout(function() {
            latest_ai_message.classList.remove('latest');

            //put another class as 'old' message
            latest_ai_message.classList.add('old');
        }, 5000);  
    }
}

//----------------------END OF AI INPUT PROCESS----------------------//

//----------------------START OF CHATBOX SCROLLING----------------------//
function scrollToBottom() {
    const messagesDiv = document.querySelector('.messages-div');
    const lastMessage = messagesDiv.lastElementChild;
    lastMessage.scrollIntoView({ behavior: "smooth" });
}
//----------------------END OF CHATBOX SCROLLING----------------------//

//----------------------START OF FETCH / GET RESPONSE----------------------//

function fetchData() {
    // Make a POST request to the endpoint
    fetch('/chatbot/get-response/', {
        method: 'GET',
    })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
        // Handle the response data
        if (data.response) {
            print('data received:', data.response);
            Ai_input(data.response);
        }
        console.log('Response:', data.response);
        // Do something with the data, e.g., update the UI
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// Call the fetchData function to make the request
fetchData();


//----------------------END OF FETCH / GET RESPONSE----------------------//

//----------------------START SEND WITH ENTER KEYBOARD KEY----------------------//

// Get the input field element
const inputElement = document.querySelector('.user-input-box');

// Add an event listener to the input field for the keydown event
inputElement.addEventListener('keydown', function(event) {
    // Check if the Enter key was pressed
    if (event.keyCode === 13) {
        // Prevent the default behavior of the Enter key (e.g., submitting a form)
        event.preventDefault();

        // Simulate a click on the button
        button.click();
    }
});