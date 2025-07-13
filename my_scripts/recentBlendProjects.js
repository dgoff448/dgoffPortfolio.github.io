fetch('BlendProjects.txt')
  .then(response => response.text())
  .then(data => {
    const lines = data.trim().split(/\r?\n/).slice(0, 3);

    //output lines to console for debugging
    console.log("Recent Blender Projects:", lines);

    lines.forEach((line, index) => {
      const [nameRaw, formatRaw] = line.split(',');
      if (!nameRaw || !formatRaw) return;

      const name = nameRaw.trim();
      const format = formatRaw.trim();
      const num = index + 1;

      // Image and title elements by ID
      const imageEl = document.getElementById(`RecentBlenderProject${num}`);
      const titleEl = document.getElementById(`RecentTitle${num}`);

      // Parent <a> tag to update the href (image is inside it)
      const anchorEl = imageEl.closest('a');

      // Update image src
      imageEl.src = `images/Blender Pics/${name} Thumbnail.png`;

      // Update title text
      titleEl.textContent = format === "Vid" ? `${name} (Animation)` : name;

      // Update href based on file type
      if (format === "Vid") {
        anchorEl.href = `BlenderSubpageVideo.html?BlendVideo=${name}&Scale=.3`;
      } else {
        anchorEl.href = `BlenderSubpage.html?BlendImage=${name}`;
      }
    });
  })
  .catch(error => {
    console.error("Error reading recentBlenderProjects.txt:", error);
  });