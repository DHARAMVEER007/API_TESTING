package com.example.netappmock.auth;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/security/authentication")
public class AuthController {

    @Value("${mock.auth.username}")
    private String configuredUsername;

    @Value("${mock.auth.password}")
    private String configuredPassword;

    @Value("${mock.auth.token}")
    private String token;

    @PostMapping("/cluster-tokens")
    public ResponseEntity<?> authenticate(@RequestBody AuthRequest request) {
        if (configuredUsername.equals(request.getUsername()) && configuredPassword.equals(request.getPassword())) {
            Map<String, String> response = new HashMap<>();
            response.put("token", token);
            return ResponseEntity.status(201).body(response);
        } else {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Invalid credentials");
            return ResponseEntity.status(401).body(response);
        }
    }
}
