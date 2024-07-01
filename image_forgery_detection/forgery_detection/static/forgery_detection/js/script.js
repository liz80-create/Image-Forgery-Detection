// script.js

document.addEventListener("DOMContentLoaded", function() {
  const leftColumn = document.getElementById("leftColumn");
  const fileInput = document.getElementById("fileInput");
  const submitButton = document.getElementById("submitButton"); // New button

  let currentImage = null;

  // Handle file selection
  fileInput.addEventListener("change", function(event) {
      const file = event.target.files[0];
      if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
              // Remove the current image if it exists
              if (currentImage) {
                  leftColumn.removeChild(currentImage);
              }

              // Create a new image element
              const img = document.createElement("img");
              img.src = e.target.result;
              leftColumn.appendChild(img);
              currentImage = img;
          };
          reader.readAsDataURL(file);
      }
  });

  // Submit button click event
  submitButton.addEventListener("click", function() {
      if (currentImage) {
          // Here you can perform actions with the submitted image
          alert("Image submitted!");
          // For example, you can send the image to the server using AJAX
          // You can replace this alert with your desired functionality
      } else {
          alert("Please select an image first!");
      }
  });

  // Drag events
  leftColumn.addEventListener("dragstart", function(event) {
      event.dataTransfer.setData("text/plain", "Dragged");
  });

  // Drop events
  leftColumn.addEventListener("dragover", function(event) {
      event.preventDefault();
  });
  leftColumn.addEventListener("drop", function(event) {
      event.preventDefault();
      const data = event.dataTransfer.getData("text/plain");
      if (data === "Dragged") {
          // Do nothing, the image should stay in the left column
      } else {
          // Create a new image element from the dropped data
          const file = event.dataTransfer.files[0];
          if (file) {
              const reader = new FileReader();
              reader.onload = function(e) {
                  // Remove the current image if it exists
                  if (currentImage) {
                      leftColumn.removeChild(currentImage);
                  }

                  // Create a new image element
                  const img = document.createElement("img");
                  img.src = e.target.result;
                  leftColumn.appendChild(img);
                  currentImage = img;
              };
              reader.readAsDataURL(file);
          }
      }
  });
});