package com.auth.service;

import com.auth.model.UserDAO;

public class UserService {
    private final UserDAO userDAO = UserDAO.getInstance();

    public boolean authenticateUser(String email, String password) {
        return userDAO.userExists(email)
                && userDAO.isUserVerified(email)
                && userDAO.verifyPassword(email, password);
    }

    public String getUsername(String email) {
        return userDAO.getUsernameByEmail(email);
    }

    public boolean resetPassword(String email, String newPassword) {
        return userDAO.updatePassword(email, newPassword);
    }

    public boolean createUser(String username, String email, String password) {
        return userDAO.addUser(username, email, password);
    }
}
