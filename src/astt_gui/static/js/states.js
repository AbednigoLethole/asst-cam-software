//////////////////////Mode states///////////////////////////////
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
        var modeButton = document.getElementById("modeState");

        modeButton.style.backgroundColor = modeColor;
        modeButton.innerText = newMode;
    });
}
///////////////////////Stow pin State //////////////////////////

function StowPinState(stowState) {
    var stateColor = "";
    var stowStateAndColour = {
        "Unknown": "#212529",
        "StowPinEngaged": "#dc3545",
        "StowPinReleased": "#198754"
    };
    if (stowState in stowStateAndColour) {
        stateColor = stowStateAndColour[stowState];
    }

    document.addEventListener("DOMContentLoaded", function() {
        var stateButton = document.getElementById("funcState");

        stateButton.style.backgroundColor = stateColor;
        stateButton.innerText = stowState;
    });
}

/////////////////////Function State //////////////////////////////

function funcState(funcState) {
    var stateColor = "";
    var funcStateAndColour = {
        "Unknown": "#212529",
        "Braked": "#dc3545",
        "Moving": "#198754"
    };
    if (funcState in funcStateAndColour) {
        stateColor = funcStateAndColour[funcState];
    }

    document.addEventListener("DOMContentLoaded", function() {
        var stateButton = document.getElementById("funcState");

        stateButton.style.backgroundColor = stateColor;
        stateButton.innerText = funcState;
    });
}

StowPinState("StowPinReleased")
modeChanged("Idle")
funcState("Braked")

