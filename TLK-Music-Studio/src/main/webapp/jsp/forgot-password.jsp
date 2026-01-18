<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    String lang = (String) session.getAttribute("lang");
    if (lang == null) lang = "en"; // default language
    java.util.ResourceBundle bundle = java.util.ResourceBundle.getBundle("messages", new java.util.Locale(lang));
%>
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= bundle.getString("forgot.title") %></title>
    <link rel="stylesheet" href="../css/styles.css">
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
        <h2><%= bundle.getString("forgot.title") %></h2>

        <% if (request.getParameter("error") != null) { %>
            <p class="error"><%= request.getParameter("error") %></p>
        <% } %>
        <% if (request.getParameter("message") != null) { %>
            <p class="success"><%= request.getParameter("message") %></p>
        <% } %>

        <form action="../forgot-password" method="post">
            <label for="email"><%= bundle.getString("email") %>:</label>
            <input type="email" id="email" name="email" required>

            <input type="submit" value="<%= bundle.getString("forgot.sendlink") %>">
        </form>

        <p><a href="<%= request.getContextPath() %>/jsp/signin.jsp"><%= bundle.getString("forgot.back") %></a></p>
    </div>
</body>
</html>
