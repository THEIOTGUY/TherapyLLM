// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyC4kkMJH-rtAPOQ-rNnMWqbkQ4o-FngNts",
    authDomain: "large-languge-model.firebaseapp.com",
    databaseURL: "https://large-languge-model-default-rtdb.firebaseio.com",
    projectId: "large-languge-model",
    storageBucket: "large-languge-model.appspot.com",
    messagingSenderId: "1049616362097",
    appId: "1:1049616362097:web:28f348d76a019fc0b709d0"
  };
firebase.initializeApp(firebaseConfig);

// Get a reference to the database service and storage
const database = firebase.database();
const storage = firebase.storage();

// Get references to HTML elements
const messageList = document.getElementById('message-list');
const messageInput = document.getElementById('message-input');

// Function to send a message to Firebase
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message !== '') {
        const messageList = document.getElementById('message-list');

        // Append the new message to the message list
        const newMessage = document.createElement('li');
        newMessage.textContent = message;
        messageList.appendChild(newMessage);

        // Scroll down to show the new message
        messageList.scrollTop = messageList.scrollHeight;

        // Clear the input field
        messageInput.value = '';

        // Update the Firebase "input" value
        database.ref('input').set(message);
    }
}
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
        event.preventDefault(); // Prevent the default Enter key behavior (e.g., newline in the textarea)
    }
}
// Function to display messages
function displayMessage(snapshot, messageType) {
    const message = snapshot.val();
    const listItem = document.createElement('li');
    listItem.textContent = `${messageType}: ${message}`;
    messageList.appendChild(listItem);
}

// Listen for changes in the "input" node
database.ref('input').on('value', (snapshot) => {
    displayMessage(snapshot, 'Input');
});

// Listen for changes in the "output" node
database.ref('output').on('value', (snapshot) => {
    displayMessage(snapshot, 'Output');
});

// Function to delete messages and update Firebase value "DELETE" with random string
function deleteMessages() {
    // Clear existing messages from the webpage
    messageList.innerHTML = '';

    // Generate a random string
    const randomString = generateRandomString();

    // Update Firebase value "DELETE" with the random string
    database.ref('DELETE').set(randomString);
}


// Function to generate a random string
function generateRandomString() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const length = 10;
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Function to download a PDF from Firebase Storage (force download)
function downloadPdf() {
    // Replace 'your-pdf-file.pdf' with the actual path to your PDF file in Firebase Storage
    const pdfRef = storage.ref('example_report_with_heading.pdf');

    pdfRef.getDownloadURL()
        .then((url) => {
            // Create a hidden link element
            const link = document.createElement('a');
            link.href = url;
            link.target = '_blank';
            link.download = 'example_report_with_heading.pdf'; // Specify the desired file name

            // Append the link to the body
            document.body.appendChild(link);

            // Trigger a click on the link to initiate the download
            link.click();

            // Remove the link from the DOM after a short delay
            setTimeout(() => {
                document.body.removeChild(link);
            }, 100);

        })
        .catch((error) => {
            console.error('Error downloading PDF:', error);
        });
}

