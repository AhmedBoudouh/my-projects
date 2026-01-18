<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    String lang = (String) session.getAttribute("lang");
    if (lang == null) lang = "en";
    java.util.ResourceBundle bundle = java.util.ResourceBundle.getBundle("messages", new java.util.Locale(lang));
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title><%= bundle.getString("reset.title") %></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="<%= request.getContextPath() %>/css/styles.css">
</head>
<body>

<nav class="navbar">
    <div class="nav-container">
        <a href="<%= request.getContextPath() %>/home.jsp" class="nav-logo">SignApp</a>
        <div class="nav-links">
            <a href="<%= request.getContextPath() %>/jsp/signin.jsp"><%= bundle.getString("signin") %></a>
            <a href="<%= request.getContextPath() %>/jsp/signup.jsp" class="button-outline"><%= bundle.getString("signup") %></a>
            <a href="<%= request.getContextPath() %>/change-lang?lang=en" class="<%= "en".equals(lang) ? "active-lang" : "" %>">EN</a>
            <a href="<%= request.getContextPath() %>/change-lang?lang=fr" class="<%= "fr".equals(lang) ? "active-lang" : "" %>">FR</a>
        </div>
    </div>
</nav>

<div class="container">
    <h2><%= bundle.getString("reset.title") %></h2>

    <% if (request.getParameter("error") != null) { %>
        <p class="error"><%= request.getParameter("error") %></p>
    <% } %>

    <form action="<%= request.getContextPath() %>/reset-password" method="post">
        <input type="hidden" name="token" value="<%= request.getParameter("token") %>">

        <label for="newPassword"><%= bundle.getString("reset.new") %>:</label>
        <div class="password-wrapper">
            <input type="password" id="newPassword" name="newPassword" required>
            <img src="../images/visibilityOff.png" id="toggleNew" alt="toggle password">
        </div>

        <div class="strength-container">
            <span class="strength-label"><%= bundle.getString("strength.label") %></span>
            <div class="strength-bar"><div id="strengthLevel" class="strength-level"></div></div>
        </div>

        <label for="confirmPassword"><%= bundle.getString("reset.confirm") %>:</label>
        <div class="password-wrapper">
            <input type="password" id="confirmPassword" name="confirmPassword" required>
            <img src="../images/visibilityOff.png" id="toggleConfirm" alt="toggle password">
        </div>
        <p id="matchMessage" class="error" style="display:none;"></p>

        <input type="submit" value="<%= bundle.getString("reset.submit") %>">
    </form>

    <p><a href="<%= request.getContextPath() %>/jsp/signin.jsp"><%= bundle.getString("forgot.back") %></a></p>
</div>

<script>
    function toggleVisibility(inputId, iconId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(iconId);
        icon.addEventListener("click", () => {
            const type = input.type === "password" ? "text" : "password";
            input.type = type;
            icon.src = type === "password" ? "../images/visibilityOff.png" : "../images/visibilityOn.png";
        });
    }

    toggleVisibility("newPassword", "toggleNew");
    toggleVisibility("confirmPassword", "toggleConfirm");

    const passwordField = document.getElementById("newPassword");
    const confirmField = document.getElementById("confirmPassword");
    const strengthBar = document.getElementById("strengthLevel");
    const matchMessage = document.getElementById("matchMessage");
    const form = document.querySelector("form");

    passwordField.addEventListener("input", () => {
        const val = passwordField.value;
        let width = 0;
        if (val.length >= 8 && /[A-Z]/.test(val) && /[0-9]/.test(val) && /[\W]/.test(val)) width = 100;
        else if (val.length >= 6 && /[A-Z0-9]/.test(val)) width = 60;
        else if (val.length > 0) width = 30;
        strengthBar.style.width = width + "%";
    });

    form.addEventListener("submit", function (e) {
        if (passwordField.value !== confirmField.value) {
            e.preventDefault();
            matchMessage.textContent = "<%= bundle.getString("reset.nomatch") %>";
            matchMessage.style.display = "block";
        } else {
            matchMessage.style.display = "none";
        }
    });
</script>

</body>
</html>
