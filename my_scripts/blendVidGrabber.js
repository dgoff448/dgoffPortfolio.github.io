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
if (queryParams.BlendVideo) {
    const videoPath = `images/Blender Pics/${queryParams.BlendVideo}.mp4`;
    const videoElement = document.getElementById("BlendVideo");
    const sourceElement = videoElement.querySelector("source");

    sourceElement.src = videoPath;
    videoElement.load(); // Load the new video source

    if (queryParams.Scale) {
        const scale = parseFloat(queryParams.Scale);
    

        // Add event listener for loadedmetadata event
        videoElement.addEventListener('loadedmetadata', () => {
            const width = videoElement.videoWidth;
            const height = videoElement.videoHeight;

            console.log("Width: " + videoElement.videoWidth);
            console.log("Height: " + videoElement.videoHeight);

            videoElement.width = width * scale;
            videoElement.height = height * scale;

            console.log("New Width: " + width * scale);
            console.log("New Height: " + height * scale);
        });
    }
    
    sourceElement.src = videoPath;
    videoElement.load(); // Load the new video source

    document.getElementById("Title").innerHTML = queryParams.BlendVideo;

    // Fetch the content of the text file
    fetch(`descriptions/${queryParams.BlendVideo}.txt`)
    .then(response => response.text())
    .then(data => {
        document.getElementById('description').innerText = data;
    })
    .catch(error => {
        console.error('Error fetching the text file:', error);
    });



}