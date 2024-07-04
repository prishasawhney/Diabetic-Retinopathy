const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const meterBar = document.getElementById("meter-bar");
const responsePlaceholder = document.getElementById("response");
const errorPlaceholder = document.getElementById("error");

inputFile.addEventListener("change", uploadImage);

function uploadImage(){
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;
}

dropArea.addEventListener("dragover", function(e){
    e.preventDefault();
});
dropArea.addEventListener("drop", function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    uploadImage();
});

document.getElementById("image-upload-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("file", inputFile.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:5000/results", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }

        const data = await response.json();
        const diseaseStage = data.disease_stage;

        // Update meter-bar based on disease stage
        updateMeterBar(diseaseStage);

        // Display disease stage response
        responsePlaceholder.textContent = diseaseStage;
        errorPlaceholder.textContent = "";
    } catch (error) {
        console.error("Error:", error);
        responsePlaceholder.textContent = "NA";
        errorPlaceholder.textContent = "Error occurred while fetching Data. Please provide an image as input. Acceptable formats are .jpg, .jpeg, .png"
    }
});

function updateMeterBar(diseaseStage) {
    let widthPercent = 0;
    let barColor = "#e0e0e0";
    switch (diseaseStage) {
      case "Negative":
        widthPercent = 100;
        barColor = "#00BF11";
        break;
      case "Mild":
        widthPercent = 75;
        barColor = "#8ED203";
        break;
      case "Moderate":
        widthPercent = 50;
        barColor = "#FECE00";
        break;
      case "Severe":
        widthPercent = 25;
        barColor = "#FE9903";
        break;
      case "Proliferated":
        widthPercent = 10;
        barColor = "#FF3300";
        break;
      default:
        widthPercent = 0;
        barColor = "#e0e0e0";
        break;
    }
    meterBar.style.width = `${widthPercent}%`;
    meterBar.style.backgroundColor = `${barColor}`
}

