<%@ page contentType="text/html;charset=UTF-8" %>
<%
    String lang = (String) session.getAttribute("lang");
    if (lang == null) lang = "en";
    java.util.ResourceBundle bundle = java.util.ResourceBundle.getBundle("messages", new java.util.Locale(lang));
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title><%= bundle.getString("home.title") %></title>
    <link rel="stylesheet" href="css/styles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<!-- Navigation -->
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


<div class="container" style="text-align: center;">
    <h2><%= bundle.getString("home.welcome") %></h2>
    <p style="margin-bottom: 20px;"><%= bundle.getString("home.tagline") %></p>

    <div>
        <a href="jsp/signin.jsp" class="btn-home"><%= bundle.getString("signin") %></a>
        <a href="jsp/signup.jsp" class="btn-home" style="margin-left: 10px;"><%= bundle.getString("signup") %></a>
    </div>
  <p style="font-size: 13px; color: #888;">
    <%= bundle.getString("home.developedby") %>
</p>
    
    <p style="margin-top: 20px; font-size: 13px; color: #666;">
        &copy; 2025 SignApp. <%= bundle.getString("home.copyright") %>
    </p>
  
</div>

</body>
</html>

