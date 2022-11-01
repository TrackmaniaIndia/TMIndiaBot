package com.trackmaniaindia.tmibot.api.player;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.util.List;

public class PlayerTrophies {
    private int echelon;
    private String lastChange;
    private int points;
    private int[] trophies;
    private String playerId;

    private static final Logger LOGGER = LogManager.getLogger(PlayerTrophies.class);

    // Constructors
    public PlayerTrophies() {
        this.echelon = -1;
        this.lastChange = null;
        this.points = -1;
        this.trophies = new int[0];
        this.playerId = null;
    } // Default Constructor

    public PlayerTrophies(JSONObject jsonObject) {
        throw new UnsupportedOperationException("Constructor not implemented yet.");
    } // JSON Constructor

    // Other Functions
    public JSONObject history(int page) {
        throw new UnsupportedOperationException("Function not implmemented yet.");
    } // history

    public JSONObject history() {
        return this.history(0);
    } // history

    public int getScoreInt() {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // getScoreInt

    public void setPlayerId(String playerId) {
        // Do some checks.

        this.playerId = playerId;
    }

    // Getter Functions
    public int getEchelon() {
        return this.echelon;
    } // echelon

    public String getLastChange() {
        return this.lastChange;
    } // getLastChange

    public int getPoints() {
        return this.points;
    } // getPoints

    public int[] getTrophies() {
        return this.trophies;
    } // getTrophies

    public String getPlayerId() {
        return this.playerId;
    } // getPlayerId
}
