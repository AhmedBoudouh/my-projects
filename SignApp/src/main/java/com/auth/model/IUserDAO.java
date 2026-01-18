package com.auth.model;

public interface IUserDAO {
    boolean userExists(String email);
    boolean isUserVerified(String email);
    boolean verifyPassword(String email, String password);
    boolean updatePassword(String email, String newPassword);
    String getUsernameByEmail(String email);
}
