function modeChanged(newMode) {
    var modeColor = "";
    var modeAndColour = {
        "Unknown": "#212529",
        "Idle": "#dc3545",
        "Stow": "#ffc107",
        "Point": "#198754"
    };
    if (newMode in modeAndColour) {
        modeColor = modeAndColour[newMode];
    }

    document.addEventListener("DOMContentLoaded", function() {
        var modeButton = document.getElementById("Modes state");

        modeButton.style.backgroundColor = modeColor;
        modeButton.innerText = newMode;
    });
}

