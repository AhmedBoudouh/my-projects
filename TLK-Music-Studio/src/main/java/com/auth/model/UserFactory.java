package com.auth.model;

import org.mindrot.jbcrypt.BCrypt;
import java.util.Date;
import java.util.UUID;

public class UserFactory {
    public static User createUser(String username, String email, String password) {
        String hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt());
        return new User.Builder()
                .setUsername(username)
                .setEmail(email)
                .setPassword(hashedPassword)
                .setVerificationToken(UUID.randomUUID().toString())
                .setVerified(false)
                .setTokenExpiry(new Date(System.currentTimeMillis() + 24 * 60 * 60 * 1000)) 
                .build();
    }
}