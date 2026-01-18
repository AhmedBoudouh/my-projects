package com.auth.controller;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.auth.model.UserDAO;

@WebServlet("/signin")
public class SigninServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String email = request.getParameter("email");
        String password = request.getParameter("password");

        UserDAO userDAO = UserDAO.getInstance();

        if (!userDAO.userExists(email)) {
            response.sendRedirect(request.getContextPath() + "/jsp/signup.jsp?error=Account does not exist. Please sign up.");
            return;
        }

        if (!userDAO.isUserVerified(email)) {
            response.sendRedirect(request.getContextPath() + "/jsp/signin.jsp?error=Please verify your email first");
            return;
        }

        if (!userDAO.verifyPassword(email, password)) {
            response.sendRedirect("jsp/signin.jsp?error=Incorrect password. Please try again.");
            return;
        }

        HttpSession session = request.getSession();
        session.setAttribute("email", email);

        String username = userDAO.getUsernameByEmail(email);
        session.setAttribute("username", username);

        userDAO.updateLastLogin(email);
        String lastLogin = userDAO.getLastLogin(email); 
        session.setAttribute("lastLogin", lastLogin); 

        String remember = request.getParameter("rememberMe");
        if ("on".equals(remember)) {
            Cookie emailCookie = new Cookie("rememberedEmail", email);
            emailCookie.setMaxAge(7 * 24 * 60 * 60);
            response.addCookie(emailCookie);
        } 
       
        response.sendRedirect("jsp/profile.jsp");
    }
}
