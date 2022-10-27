package com.trackmaniaindia.tmibot.api;

import com.trackmaniaindia.tmibot.util.Configuration;
import io.github.cdimascio.dotenv.Dotenv;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpRequest;
import java.net.http.HttpClient;
import java.net.http.HttpResponse;
import java.util.Base64;

/**
 * Class that allows communication to Nadeo's Trackmania
 * API by getting the access and refresh tokens.
 */
public class NadeoAPI {
    private static String accessToken;
    private static String refreshToken;

    private final static Logger LOGGER = LogManager.getLogger(NadeoAPI.class);

    /**
     * Update the access and refresh tokens.
     *
     * @return The {@code accessToken}
     */
    public static JSONObject updateTokens() throws Exception {
        String auth_url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic";

        Dotenv config = Configuration.getConfig();
        String ubisoftUsername = config.get("UBISOFT_USERNAME");
        String ubisoftPassword = config.get("UBISOFT_PASSWORD");

        LOGGER.debug("Creating the request.");
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(auth_url))
                .header("Content-Type", "application/json")
                .header("Ubi-AppId", "86263886-327a-4328-ac69-527f0d20a237")
                .header("User-Agent", config.get("USER_AGENT"))
                .header("audience", "NadeoLiveServices")
                .header("Authorization", getBasicAuthenticationHeader(ubisoftUsername, ubisoftPassword))
                .method("POST", HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = null;

        try {
            response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        } catch (IOException | InterruptedException ie) {
            ie.printStackTrace();
        }  // try-catch

        String responseBody = null;

        try {
            responseBody = response.body();
        } catch (NullPointerException npe) {
            npe.printStackTrace();
            System.exit(-1);
        } // try-catch

        JSONObject responseJsonBody = new JSONObject(responseBody);

        try {
            // Setting the value
            NadeoAPI.setAccessToken(responseJsonBody.getString("accessToken"));
            NadeoAPI.setRefreshToken(responseJsonBody.getString("refreshToken"));
        } catch (JSONException je) {
            // Change the error to something more specific later.
            throw new Exception("Invalid UBISOFT_USERNAME and UBISOFT_PASSWORD. Check the .env file. \nFrom Server: " +
                    responseJsonBody.getString("message"));
        } // try-catch

        LOGGER.debug("Updated Access and Refresh Tokens.");
        return responseJsonBody;
    } // updateTokens

    public static JSONObject refreshTokens() throws Exception {
        LOGGER.debug("Refreshing Tokens.");

        Dotenv config = Configuration.getConfig();

        String refreshUrl = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh";

        LOGGER.debug("Creating the Request.");
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(refreshUrl))
                .header("Content-Type", "application/json")
                .header("Ubi-AppId", "86263886-327a-4328-ac69-527f0d20a237")
                .header("Authorization", "nadeo_v1 t=" + NadeoAPI.getRefreshToken())
                .header("audience", "NadeoLiveServices")
                .header("User-Agent", config.get("USER_AGENT"))
                .method("POST", HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = null;

        try {
            response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        } catch (IOException | InterruptedException ie) {
            ie.printStackTrace();
        }  // try-catch-catch

        String responseBody = null;

        try {
            responseBody = response.body();
        } catch (NullPointerException npe) {
            npe.printStackTrace();
            System.exit(-1);
        } // try-catch

        JSONObject responseJsonBody = new JSONObject(responseBody);

        try {
            // Setting the value
            NadeoAPI.setAccessToken(responseJsonBody.getString("accessToken"));
            NadeoAPI.setRefreshToken(responseJsonBody.getString("refreshToken"));
        } catch (JSONException je) {
            // Change the error to something more specific later.
            throw new Exception("Invalid UBISOFT_USERNAME and UBISOFT_PASSWORD. Check the .env file. \nFrom Server: " +
                    responseJsonBody.getString("message"));
        } // try-catch

        LOGGER.debug("Updated Access and Refresh Tokens.");
        return responseJsonBody;
    } // refreshTokens

    /**
     * Change the username and password into a proper header to use
     * in the HttpRequest.
     *
     * @param username The username of the account.
     * @param password The password of the account.
     * @return the header properly formatted for the request.
     * @throws NullPointerException if {@code username} or {@code password} is {@code null}.
     * @throws IllegalArgumentException if {@code username} or {@code password} is empty.
     */
    private static String getBasicAuthenticationHeader(String username, String password) {
        // Checking null
        if (username == null || password == null) {
            throw new NullPointerException("Username or Password cannot be null.");
        } else if (username.length() == 0 || password.length() == 0) {
            throw new IllegalArgumentException("Username or Password cannot be zero.");
        } // if-else if

        String valueToEncode = username + ":" + password;

        return "Basic " + Base64.getEncoder().encodeToString(valueToEncode.getBytes());
    }

    /**
     * Getter function for {@code accessToken}.
     *
     * @return the {@code accessToken}.
     */
    public static String getAccessToken() {
        return NadeoAPI.accessToken;
    } // getAccessToken

    /**
     * Getter function for {@code refreshToken}.
     *
     * @return the {@code refreshToken}.
     */
    public static String getRefreshToken() {
        return NadeoAPI.refreshToken;
    } // getRefreshToken

    /**
     * Setter function for {@code accessToken}.
     *
     * @param newAccessToken The new {@code accessToken} to change to.
     * @throws NullPointerException if the {@code newAccessToken} is null.
     */
    protected static void setAccessToken(String newAccessToken) {
        // Checking null
        if (newAccessToken == null) {
            throw new NullPointerException("The accessToken cannot be null.");
        } // if

        NadeoAPI.accessToken = newAccessToken;
    } // setAccessToken

    /**
     * Setter function for {@code refreshToken}.
     *
     * @param newRefreshToken the new {@code refreshToken} to change to.
     * @throws NullPointerException if the {@code newRefreshToken} is null.
     */
    protected static void setRefreshToken(String newRefreshToken) {
        // Checking null
        if (newRefreshToken == null) {
            throw new NullPointerException("The refreshToken cannot be null.");
        }

        NadeoAPI.refreshToken = newRefreshToken;
    } // setRefreshToken
} // NadeoAPI
