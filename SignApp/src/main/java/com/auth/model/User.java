package com.auth.model;

import java.util.Date;

public class User {
    private String username;
    private String email;
    private String password;
    private String verificationToken;
    private boolean verified;
    private Date tokenExpiry;

    private User(Builder builder) {
        this.username = builder.username;
        this.email = builder.email;
        this.password = builder.password;
        this.verificationToken = builder.verificationToken;
        this.verified = builder.verified;
        this.tokenExpiry = builder.tokenExpiry;
    }

    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public String getPassword() { return password; }
    public String getVerificationToken() { return verificationToken; }
    public boolean isVerified() { return verified; }
    public Date getTokenExpiry() { return tokenExpiry; }

    public static class Builder {
        private String username;
        private String email;
        private String password;
        private String verificationToken;
        private boolean verified;
        private Date tokenExpiry;

        public Builder setUsername(String username) {
            this.username = username;
            return this;
        }

        public Builder setEmail(String email) {
            this.email = email;
            return this;
        }

        public Builder setPassword(String password) {
            this.password = password;
            return this;
        }

        public Builder setVerificationToken(String verificationToken) {
            this.verificationToken = verificationToken;
            return this;
        }

        public Builder setVerified(boolean verified) {
            this.verified = verified;
            return this;
        }

        public Builder setTokenExpiry(Date tokenExpiry) {
            this.tokenExpiry = tokenExpiry;
            return this;
        }

        public User build() {
            return new User(this);
        }
    }
}