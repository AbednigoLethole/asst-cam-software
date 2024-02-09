//////////////////////Mode states///////////////////////////////
function modeChanged(newMode) {
    var modeColor = "";
    var modeAndColour = {
        "UNKNOWN": "#212529",
        "IDLE": "#dc3545",
        "STOW": "#ffc107",
        "POINT": "#198754"
    };
    if (newMode in modeAndColour) {
        modeColor = modeAndColour[newMode];
    }
    var modeButton = document.getElementById("modeState");

    modeButton.style.backgroundColor = modeColor;
    modeButton.innerText = newMode;

}
///////////////////////Stow pin State //////////////////////////

function stowPinStateChanged(stowState) {

    var stowStateColor = "";
    var stowStateName = "";
    var disengagedEnums = [
        "NOT_ENGAGED_NOT_RELEASED_NOT_STOW_WINDOW",
        "NOT_ENGAGED_NOT_RELEASED_STOW_WINDOW",
        "NOT_ENGAGED_RELEASED_NOT_STOW_WINDOW",
        "NOT_ENGAGED_RELEASED_STOW_WINDOW",
    ];

    var engagedEnums = [
        "ENGAGED_NOT_RELEASED_NOT_STOW_WINDOW",
        "ENGAGED_NOT_RELEASED_STOW_WINDOW", 
        "ENGAGED_RELEASED_NOT_STOW_WINDOW",
        "ENGAGED_RELEASED_STOW_WINDOW",
    ];

    disengagedEnums.forEach((disengagedEnum) => {
        if (disengagedEnum == stowState) {
            stowStateColor = "#198754";
            stowStateName = "DISENGAGED";
        }
    });

    engagedEnums.forEach((engagedEnum) => {
        if (engagedEnum == stowState) {
            stowStateColor = "#dc3545";
            stowStateName = "ENGAGED";
        }
    });
    
    if (stowState == "UNKNOWN"){
        stowStateColor = "#212529";
        stowStateName = stowState;
    }
    console.log("stow state: " + stowStateName);
    var stateButton = document.getElementById("stowState");
    stateButton.style.backgroundColor = stowStateColor;
    stateButton.innerText = stowStateName;

}

/////////////////////Function State //////////////////////////////

function funcStateChanged(funcState) {
    var stateColor = "";
    var funcStateAndColour = {
        "UNKNOWN": "#212529",
        "BRAKED": "#dc3545",
        "MOVING": "#198754"
    };
    if (funcState in funcStateAndColour) {
        stateColor = funcStateAndColour[funcState];
    }

    console.log("gets there")
    var stateButton = document.getElementById("funcState");

    stateButton.style.backgroundColor = stateColor;
    stateButton.innerText = funcState;
 
}
var socket = io.connect();
socket.on("updateStateMode", function (msg) {
    console.log("Received mode & state Data :: " + msg.mode + " :: " + msg.funcState + " :: " + msg.stowPinState);

    modeChanged(msg.mode);
    funcStateChanged(msg.funcState);
    stowPinStateChanged(msg.stowPinState)
 
  });
