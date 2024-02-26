document.getElementById('send-message').addEventListener('click', function() {
    append_user_input(),
    scroll_to_bottom();
});

////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////

function append_user_input() {
    //get the

    // Get the user input value
    const user_input = document.getElementById('user_input').value;

    // Get the div with the id messages-div
    const div = document.getElementById('messages-div');

    // Create a div element with the class "user_message_div"
    const user_message_div = document.createElement('div');
    user_message_div.className = 'user_message_div new-card';

    // Create a div element with the class "about-user"
    const about_user = document.createElement('div');
    about_user.className = 'about-user';

    // Create a div element with the class "devider"
    const devider = document.createElement('div');
    devider.className = 'devider-user';

    // Create an h1 element with the text "{{userusername}}"
    const h1 = document.createElement('h1');
    h1.textContent = '{{userusername}}';

    // Append the devider and h1 to the about_user div
    about_user.appendChild(devider);
    about_user.appendChild(h1);

    // Create a div element with the class "user-message"
    const user_message = document.createElement('div');
    user_message.className = 'user-message';

    // Create a p element
    const p = document.createElement('p');
    p.innerHTML = user_input;

    // Append the p to the user_message div
    user_message.appendChild(p);

    // Append the about_user and user_message to the user_message_div
    user_message_div.appendChild(about_user);
    user_message_div.appendChild(user_message);

    // Append the user_message_div to the div with the id "messages-div"
    div.appendChild(user_message_div);

    if (div.appendChild(user_message_div)) {
        scroll_to_bottom(),
        //call the sendData function
        sendData(user_input);
    }

    //call the removeClass function
    style_user_message_div();
}
//////////////////////////////////////////////////////////////////

function style_user_message_div() {
    // Get the user_message_div element
    const user_message_div = document.querySelector(".user_message_div new-card");

    if (user_message_div) {
        //add a style to the user_message_div
        user_message_div.style.display = "none";
        //set the display to block after 5 seconds
        setTimeout(() => {
            user_message_div.style.display = "block";
        }, 5000);

        //call the removeClassUser function
        remove_class_user();
    }
}

//////////////////////////////////////////////////////////////////

function remove_class_user() {
    setTimeout(() => {
        const ai_response = document.querySelector('.user_message_div');
        ai_response.classList.remove('new-card');
        //add a new class to the ai-response div
        ai_response.classList.add('old-card');
        //call the sendData function
        sendData(document.getElementById('user_input').value);
    }, 5000);
}

///////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////

function append_ai_message(data) {
    setTimeout(() => {

    // Get the div with the id messages-div
    const div = document.getElementById('messages-div');

    // Create a div element with the class "ai-response"
    const ai_response = document.createElement('div');
    ai_response.className = 'ai-response new-card';

    // Create a div element with the class "about-ai"
    const about_ai = document.createElement('div');
    about_ai.className = 'about-ai';

    // Create an h1 element with the text "WRENCH"
    const h1 = document.createElement('h1');
    h1.textContent = 'WRENCH';

    // Create a div element with the class "devider"
    const devider = document.createElement('div');
    devider.className = 'devider';

    // Append the h1 and deviderDiv to the aboutAIDiv
    about_ai.appendChild(h1);
    about_ai.appendChild(devider);

    // Create a div element with the class "ai-message"
    const ai_message = document.createElement('div');
    ai_message.className = 'ai-message';

    // Create a p element with the innerHTML set to the data
    const p = document.createElement('p');
    p.innerHTML = data;

    // Append the p to the aiMessageDiv
    ai_message.appendChild(p);

    // Append the aboutAIDiv and aiMessageDiv to the message-div
    ai_response.appendChild(about_ai);
    ai_response.appendChild(ai_message);

    // Append the aiResponseDiv to the div with the id "ai-response"
    div.appendChild(ai_response);

    //call the removeClass function
    if (div.appendChild(ai_response)) {
        //call scroll_to_bottom function
        scroll_to_bottom(),
        remove_class();
    }
    }, 3000);
}

//////////////////////////////////////////////////////////////////

function remove_class() {
    setTimeout(() => {
        const ai_response = document.querySelector('.ai-response');
        ai_response.classList.remove('new-card');
        ai_response.classList.add('old-card');
    }, 5000);
}
//////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////

function scroll_to_bottom() {
    // Get the div with the id "messages-div"
    const div = document.getElementById('messages-div');
    // Scroll to the bottom of the div smoothly
    div.scrollTop = div.scrollHeight;
}
//////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////

function sendData(user_input) {
    const keywords = user_input;
    const url = `/chatbot/get-keywords/${keywords}`;

    if (user_input == '') {
        alert('Please enter a message');
        return; // Exit the function if user input is empty
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            append_ai_message(data.response);
            console.log(data.response);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

//////////////////////////////////////////////////////////////////