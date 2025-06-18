document.addEventListener("DOMContentLoaded", function() {
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const loginButton = document.getElementById("btn");

    usernameInput.addEventListener("input", toggleLoginButton);
    passwordInput.addEventListener("input", toggleLoginButton);

    function toggleLoginButton() {
        if (usernameInput.value.trim() !== "" && passwordInput.value.trim() !== "") {
            loginButton.removeAttribute("disabled");
        } else {
            loginButton.setAttribute("disabled", "disabled");
        }
    }

    // Add event listener to form submit
    document.getElementById("loginForm").addEventListener("submit", function(event) {
        // Prevent default form submission
        event.preventDefault();
        
        // Check if username and password are valid
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        if (username === "nancy" && password === "nancy123") {
            // Redirect to the desired page
            window.location.href = "http://127.0.0.1:5500/admin%20dashboard/navbar.html#";
        } else {
            // Handle invalid credentials
            alert("Invalid username or password!");
        }
    });
});
