const cityInput = document.getElementById("city-input");

if (cityInput) {
    cityInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            cityInput.form.requestSubmit();
        }
    });
}