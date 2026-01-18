package com.auth.controller;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import org.mindrot.jbcrypt.BCrypt;
import com.auth.model.UserDAO;
import com.auth.util.PasswordValidator;

@WebServlet("/reset-password")
public class ResetPasswordServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String token = request.getParameter("token");

        UserDAO userDAO = UserDAO.getInstance();

        String email = userDAO.getEmailByResetToken(token);
        if (email == null || !userDAO.isResetTokenValid(token)) {
            response.sendRedirect(request.getContextPath() + "/jsp/reset-password.jsp?error=Invalid or expired token");
            return;
        }

        HttpSession session = request.getSession();
        session.setAttribute("resetToken", token);

        response.sendRedirect(request.getContextPath() + "/jsp/reset-password.jsp?token=" + token);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String token = request.getParameter("token");
        String newPassword = request.getParameter("newPassword");
        String confirmPassword = request.getParameter("confirmPassword");

        if (!newPassword.equals(confirmPassword)) {
            response.sendRedirect(request.getContextPath() + "/jsp/reset-password.jsp?error=Passwords do not match");
            return;
        }

        UserDAO userDAO = UserDAO.getInstance();

        String email = userDAO.getEmailByResetToken(token);
        if (email == null || !userDAO.isResetTokenValid(token)) {
            response.sendRedirect(request.getContextPath() + "/jsp/reset-password.jsp?error=Invalid or expired token");
            return;
        }
        if (!PasswordValidator.isValid(newPassword)) {
            response.sendRedirect("jsp/reset-password.jsp?error=Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and optionally a special character.");
            return;
        }

        String hashedPassword = BCrypt.hashpw(newPassword, BCrypt.gensalt());

        if (userDAO.updatePassword(email, hashedPassword)) {
            response.sendRedirect(request.getContextPath() + "/jsp/signin.jsp?message=Password updated successfully");
        } else {
            response.sendRedirect(request.getContextPath() + "/jsp/reset-password.jsp?error=An error occurred. Please try again.");
        }
    }
}