(function() {
    const modal = document.getElementById("sponsor-spotlight-modal-footer");
    const closeButton = document.querySelector('button[aria-label="Close Sponsor Spotlight"]');
    const sponsorName = document.getElementById("sponsor-name-footer");

    const report = {
        modalState: "hidden",
        buttonState: "not-clicked",
        sponsorNameState: "not-set",
        styles: {},
    };

    // 1. Checking Modal visibility (opacity and pointer-events)
    const modalOpacity = window.getComputedStyle(modal).opacity;
    const modalPointerEvents = window.getComputedStyle(modal).pointerEvents;

    if (modalOpacity === "1" && modalPointerEvents === "auto") {
        report.modalState = "visible";
    } else {
        report.modalState = "hidden";
    }

    // 2. Checking if Sponsor name is being updated correctly
    if (sponsorName.textContent !== "[Sponsor Name]") {
        report.sponsorNameState = "set";
    } else {
        report.sponsorNameState = "not-set";
    }

    // 3. Verifying Button functionality (click event)
    closeButton.addEventListener("click", function() {
        report.buttonState = "clicked";
    });

    // 4. Checking for CSS overriding issues (Visibility, Animations, and Transitions)
    const modalStyles = {
        opacity: modalOpacity,
        pointerEvents: modalPointerEvents,
        display: window.getComputedStyle(modal).display,
        animation: window.getComputedStyle(modal).animation,
        transition: window.getComputedStyle(modal).transition,
    };

    report.styles = modalStyles;

    // Output audit result
    console.log("Modal Audit Report:");
    console.log("Modal Visibility: " + report.modalState);
    console.log("Sponsor Name Set: " + report.sponsorNameState);
    console.log("Button Clicked: " + report.buttonState);
    console.log("CSS Styles: ", report.styles);
})();
