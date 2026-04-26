function predict() {

    let fileInput = document.getElementById("file");

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        if (data.error) {
            document.getElementById("result").innerHTML = data.error;
            return;
        }

        document.getElementById("result").innerHTML =
            "🚨 " + data.result + " (" + data.confidence + "%)";

        let signal = data.signal;

        new Chart(document.getElementById("chart"), {
            type: 'line',
            data: {
                labels: signal.map((_, i) => i),
                datasets: [{
                    label: "EEG Signal",
                    data: signal,
                    borderColor: "blue",
                    fill: false
                }]
            }
        });

    });
}