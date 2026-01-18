package com.auth.controller;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import com.auth.model.User;
import com.auth.model.UserDAO;
import com.auth.model.UserFactory;
import java.util.Properties;
import javax.mail.*;
import javax.mail.internet.*;
import com.sendgrid.*;
import java.io.IOException;
import com.auth.util.PasswordValidator;

@WebServlet("/signup")
public class SignupServlet extends HttpServlet {
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		String username = request.getParameter("username");
		String email = request.getParameter("email");
		String password = request.getParameter("password");


		if (username == null || username.isEmpty()) {
			response.sendRedirect("jsp/signup.jsp?error=Username is required");
			return;
		}
		if (email == null || email.isEmpty()) {
			response.sendRedirect("jsp/signup.jsp?error=Email is required");
			return;
		}
		if (password == null || password.isEmpty()) {
			response.sendRedirect("jsp/signup.jsp?error=Password is required");
			return;
		}
		if (!PasswordValidator.isValid(password)) {
            response.sendRedirect("jsp/signup.jsp?error=Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and optionally a special character.");
            return;
        }

		UserDAO userDAO = UserDAO.getInstance();
		if (userDAO.userExists(email)) {
			response.sendRedirect("jsp/signup.jsp?error=Email already registered");
			return;
		}

		if (userDAO.addUser(username, email, password)) {

			HttpSession session = request.getSession();
			session.setAttribute("email", email);


			String verificationToken = userDAO.getVerificationTokenByEmail(email);
			sendVerificationEmail(email, verificationToken, request);

			response.sendRedirect("jsp/signin.jsp?message=Registration successful! Check your email for verification.");
		} else {
			response.sendRedirect("jsp/signup.jsp?error=An error occurred during registration");
		}
	}

	private void sendVerificationEmail(String email, String token, HttpServletRequest request) {
		String baseUrl = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort();
		String verificationLink = baseUrl + "/SignApp/verification";

		Email from = new Email("cdrbiskra@gmail.com");
		String subject = "Email Verification";
		Email to = new Email(email);
		Content content = new Content("text/plain", "Please verify your account by clicking this link: " + verificationLink);

		Mail mail = new Mail(from, subject, to, content);

		SendGrid sg = new SendGrid("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");
		Request apiRequest = new Request();
		try {
			apiRequest.setMethod(Method.POST);
			apiRequest.setEndpoint("mail/send");
			apiRequest.setBody(mail.build());
			Response apiResponse = sg.api(apiRequest);

			System.out.println("Verification email sent successfully to: " + email);
			System.out.println("SendGrid Status Code: " + apiResponse.getStatusCode());
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("Failed to send verification email to: " + email);
		}
		
	}
}