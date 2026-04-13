package com.example.netappmock.auth;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class TokenInterceptor implements HandlerInterceptor {

    @Value("${mock.auth.token}")
    private String validToken;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        String authHeader = request.getHeader("Authorization");

        // Skip token check for the authentication endpoint
        if (request.getRequestURI().contains("/api/security/authentication/cluster-tokens")) {
            return true;
        }

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String providedToken = authHeader.substring(7);
            if (validToken.equals(providedToken)) {
                return true;
            }
        }

        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.getWriter().write("{\"error\": \"Unauthorized: Invalid or missing token\"}");
        return false;
    }
}
