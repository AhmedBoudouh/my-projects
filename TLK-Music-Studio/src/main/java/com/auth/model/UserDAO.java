package com.auth.model;

import java.sql.*;
import java.util.Date;
import java.util.UUID;
import org.mindrot.jbcrypt.BCrypt;

public class UserDAO implements IUserDAO {
    private static UserDAO instance; 

    private String jdbcURL = "jdbc:mysql://localhost:3306/signapp_db";
    private String jdbcUsername = "root";
    private String jdbcPassword = "0522";
   private UserDAO() {}
 public static synchronized UserDAO getInstance() {
        if (instance == null) {
            instance = new UserDAO();
        }
        return instance;
    }

    protected Connection getConnection() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            return DriverManager.getConnection(jdbcURL, jdbcUsername, jdbcPassword);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public boolean addUser(String username, String email, String password) {
     
        User user = UserFactory.createUser(username, email, password);

        String sql = "INSERT INTO users (username, email, password, verification_token, verified, token_expiry) VALUES (?, ?, ?, ?, ?, ?)";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, user.getUsername());
            stmt.setString(2, user.getEmail());
            stmt.setString(3, user.getPassword()); 
            stmt.setString(4, user.getVerificationToken());
            stmt.setBoolean(5, user.isVerified());
            stmt.setTimestamp(6, new Timestamp(user.getTokenExpiry().getTime()));
            return stmt.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
    public boolean verifyUser(String token) {
        String sql = "UPDATE users SET verified = true WHERE verification_token = ? AND token_expiry > ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, token);
            stmt.setTimestamp(2, new Timestamp(new Date().getTime()));
            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean isUserVerified(String email) {
        String sql = "SELECT verified FROM users WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            return rs.next() && rs.getBoolean("verified");
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public String getVerificationTokenByEmail(String email) {
        String sql = "SELECT verification_token FROM users WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            return rs.next() ? rs.getString("verification_token") : null;
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public boolean userExists(String email) {
        String sql = "SELECT COUNT(*) FROM users WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            return rs.next() && rs.getInt(1) > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean verifyPassword(String email, String inputPassword) {
        String sql = "SELECT password FROM users WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                String storedHashedPassword = rs.getString("password");
                return BCrypt.checkpw(inputPassword, storedHashedPassword);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }
    public boolean saveResetToken(String email, String resetToken, Date expiry) {
        String sql = "UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, resetToken);
            stmt.setTimestamp(2, new Timestamp(expiry.getTime()));
            stmt.setString(3, email);
            return stmt.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
    
    public String getEmailByResetToken(String token) {
        String sql = "SELECT email FROM users WHERE reset_token = ? AND reset_token_expiry > ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, token);
            stmt.setTimestamp(2, new Timestamp(new Date().getTime()));
            ResultSet rs = stmt.executeQuery();
            return rs.next() ? rs.getString("email") : null;
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }
    public boolean isResetTokenValid(String token) {
        String sql = "SELECT COUNT(*) FROM users WHERE reset_token = ? AND reset_token_expiry > ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, token);
            stmt.setTimestamp(2, new Timestamp(new Date().getTime()));
            ResultSet rs = stmt.executeQuery();
            return rs.next() && rs.getInt(1) > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
    public boolean updatePassword(String email, String newPassword) {
        String sql = "UPDATE users SET password = ?, reset_token = NULL, reset_token_expiry = NULL WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, newPassword);
            stmt.setString(2, email);
            return stmt.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public String getUsernameByEmail(String email) {
        String sql = "SELECT username FROM users WHERE email = ?";
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();
            return rs.next() ? rs.getString("username") : null;
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }
        public void updateLastLogin(String email) {
            String sql = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE email = ?";
            try (Connection conn = getConnection();
                 PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, email);
                stmt.executeUpdate();
            } catch (SQLException e) {
                e.printStackTrace();
            }
      

    }
        public String getLastLogin(String email) {
            String sql = "SELECT last_login FROM users WHERE email = ?";
            try (Connection conn = getConnection();
                 PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, email);
                ResultSet rs = stmt.executeQuery();
                if (rs.next()) {
                    Timestamp ts = rs.getTimestamp("last_login");
                    return ts != null ? ts.toString() : "No previous login";
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
            return "Unavailable";
        }

}