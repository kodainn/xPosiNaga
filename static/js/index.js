var ws = new WebSocket("ws://localhost:8000/posinaga");

ws.onmessage = function(event) {
    
};

function sendSearchReviewPosinaga(event) {
    const searchText = document.getElementById('search-text').value;
    const sendMessage = {
        "action": "start",
        "search_text": searchText
    };
    ws.send(JSON.stringify(sendMessage))
}