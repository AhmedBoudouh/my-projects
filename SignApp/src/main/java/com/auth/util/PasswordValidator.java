package com.auth.util;

public class PasswordValidator {

 
    public static boolean isValid(String password) {
        if (password == null || password.isEmpty()) {
            return false;
        }

        return isLengthValid(password) &&
               hasUppercase(password) &&
               hasLowercase(password) &&
               hasDigit(password) &&
               hasSpecialCharacter(password); 
    }

    private static boolean isLengthValid(String password) {
        return password.length() >= 8;
    }

    private static boolean hasUppercase(String password) {
        return password.matches(".*[A-Z].*");
    }

private static boolean hasLowercase(String password) {
        return password.matches(".*[a-z].*");
    }
    private static boolean hasDigit(String password) {
        return password.matches(".*\\d.*");
    }

    private static boolean hasSpecialCharacter(String password) {
        return password.matches(".*[@#$%^&+=!].*");
    }
}