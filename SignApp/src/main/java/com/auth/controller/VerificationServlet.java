package com.auth.controller;

import com.auth.model.UserDAO;
import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;

@WebServlet("/verification")
public class VerificationServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("email") == null) {
            response.sendRedirect(request.getContextPath() + "/jsp/signin.jsp?error=Session expired. Please sign in again.");
            return;
        }

        String email = (String) session.getAttribute("email");
        UserDAO userDAO = UserDAO.getInstance();

        String token = userDAO.getVerificationTokenByEmail(email);
        if (token == null) {
            response.sendRedirect(request.getContextPath() + "/jsp/verify.jsp?error=No verification token found for this account");
            return;
        }

        boolean verificationResult = userDAO.verifyUser(token);
        if (verificationResult) {
            response.sendRedirect(request.getContextPath() + "/jsp/verify.jsp?success=Email verified successfully!");
        } else {
            response.sendRedirect(request.getContextPath() + "/jsp/verify.jsp?error=Verification failed or token expired");
        }
    }
}