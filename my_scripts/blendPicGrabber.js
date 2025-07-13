// Function to get query string parameters
function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const pairs = queryString.split("&");

    for (const pair of pairs) {
    const [key, value] = pair.split("=");
    if (key) {
        params[decodeURIComponent(key)] = decodeURIComponent(value || "");
    }
    }
    return params;
}

// Grab the query parameters
const queryParams = getQueryParams();
console.log(queryParams); // Logs the query parameters to the console

// Example usage: change the paragraph text if there's a "text" query parameter
if (queryParams.text) {
    document.getElementById("text").innerText = queryParams.text;
}

// Example usage: change the image source if there's an "BlendImage" query parameter
if (queryParams.BlendImage) {
    const imagePath = `images/Blender Pics/${queryParams.BlendImage}.png`;
    document.getElementById("BlendImage").src = imagePath;
    document.getElementById("Title").innerHTML = queryParams.BlendImage;
    
    
    // Fetch the content of the text file
    fetch(`descriptions/${queryParams.BlendImage}.txt`)
    .then(response => response.text())
    .then(data => {
        document.getElementById('description').innerText = data;
    })
    .catch(error => {
        console.error('Error fetching the text file:', error);
    });
}