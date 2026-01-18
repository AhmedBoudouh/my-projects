package com.auth.controller;

import java.io.IOException;
import java.sql.Date;
import java.util.UUID;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.auth.model.UserDAO;
import com.sendgrid.Content;
import com.sendgrid.Email;
import com.sendgrid.Mail;
import com.sendgrid.Method;
import com.sendgrid.Request;
import com.sendgrid.Response;
import com.sendgrid.SendGrid;

@WebServlet("/forgot-password")
public class ForgotPasswordServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String email = request.getParameter("email");

        UserDAO userDAO = UserDAO.getInstance();
        if (!userDAO.userExists(email)) {
            response.sendRedirect(request.getContextPath() + "/jsp/forgot-password.jsp?error=Email not registered");
            return;
        }

        String resetToken = UUID.randomUUID().toString();
        Date expiry = new Date(System.currentTimeMillis() + 24 * 60 * 60 * 1000);

        if (!userDAO.saveResetToken(email, resetToken, expiry)) {
            response.sendRedirect(request.getContextPath() + "/jsp/forgot-password.jsp?error=An error occurred. Please try again.");
            return;
        }

        sendResetEmailAsync(email, resetToken, request);


        response.sendRedirect(request.getContextPath() + "/jsp/forgot-password.jsp?message=Reset link sent to your email");
    }
    private void sendResetEmailAsync(String email, String token, HttpServletRequest request) {
        Runnable emailTask = () -> {
            try {
                sendResetEmail(email, token, request);
            } catch (Exception e) {
                e.printStackTrace();
            }
        };

        Thread emailThread = new Thread(emailTask);
        emailThread.start();  
    }


    private void sendResetEmail(String email, String token, HttpServletRequest request) {
        String baseUrl = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort();
        String resetLink = baseUrl + "/SignApp/reset-password?token=" + token;

        Email from = new Email("cdrbiskra@gmail.com");
        String subject = "Password Reset";
        Email to = new Email(email);
        Content content = new Content("text/plain", "Please reset your password by clicking this link: " + resetLink);

        Mail mail = new Mail(from, subject, to, content);

        SendGrid sg = new SendGrid("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");
        Request apiRequest = new Request();
        try {
            apiRequest.setMethod(Method.POST);
            apiRequest.setEndpoint("mail/send");
            apiRequest.setBody(mail.build());
            Response apiResponse = sg.api(apiRequest);

            System.out.println("Password reset email sent successfully to: " + email);
            System.out.println("SendGrid Status Code: " + apiResponse.getStatusCode());
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Failed to send password reset email to: " + email);
        }
        
    }
}