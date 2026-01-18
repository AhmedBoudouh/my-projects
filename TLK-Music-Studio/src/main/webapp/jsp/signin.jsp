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
    <title><%= bundle.getString("signin.title") %></title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/css/styles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <h2><%= bundle.getString("signin.title") %></h2>

    <% if (request.getParameter("error") != null) { %>
        <p class="error"><%= request.getParameter("error") %></p>
    <% } %>

    <%
        String rememberedEmail = "";
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("rememberedEmail".equals(cookie.getName())) {
                    rememberedEmail = cookie.getValue();
                    break;
                }
            }
        }
    %>

    <form action="<%= request.getContextPath() %>/signin" method="post">
        <label for="email"><%= bundle.getString("email") %>:</label>
        <input type="email" id="email" name="email" value="<%= rememberedEmail %>" required>

        <label for="password"><%= bundle.getString("password") %>:</label>
        <div class="password-wrapper">
            <input type="password" id="password" name="password" required>
            <img src="<%= request.getContextPath() %>/images/visibilityOff.png" id="togglePassword" alt="Toggle visibility">
        </div>

        <label>
            <input type="checkbox" name="rememberMe"> <%= bundle.getString("remember") %>
        </label>

        <input type="submit" value="<%= bundle.getString("signin") %>">
    </form>

    <p><%= bundle.getString("signin.noaccount") %> <a href="<%= request.getContextPath() %>/jsp/signup.jsp"><%= bundle.getString("signup.here") %></a></p>
    <p><%= bundle.getString("signin.forgot") %> <a href="<%= request.getContextPath() %>/jsp/forgot-password.jsp"><%= bundle.getString("recover") %></a></p>
</div>

<script>
    const togglePassword = document.getElementById("togglePassword");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", () => {
        const isPassword = passwordField.getAttribute("type") === "password";
        passwordField.setAttribute("type", isPassword ? "text" : "password");
        togglePassword.src = isPassword
            ? "<%= request.getContextPath() %>/images/visibilityOn.png"
            : "<%= request.getContextPath() %>/images/visibilityOff.png";
    });
</script>

</body>
</html>
