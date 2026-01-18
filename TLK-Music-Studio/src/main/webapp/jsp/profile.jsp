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
    <title><%= bundle.getString("profile.title") %></title>
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

<div class="container profile-card">
    <h2><%= bundle.getString("profile.welcome") %> <%= session.getAttribute("username") %>!</h2>
    <p><%= bundle.getString("profile.loggedin") %></p>
    <a href="<%= request.getContextPath() %>/signout" class="button"><%= bundle.getString("signout") %></a>
</div>

<p class="last-login"><%= bundle.getString("profile.lastlogin") %> <%= session.getAttribute("lastLogin") %></p>

</body>
</html>
