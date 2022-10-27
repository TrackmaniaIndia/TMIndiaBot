package com.trackmaniaindia.tmibot.api.player;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class PlayerSearchResult {
    private String clubTag;
    private String name;
    private String playerId;
    private List<PlayerZone> zones;
    private PlayerMatchmaking threes;
    private PlayerMatchmaking royal;

    private final static Logger LOGGER = LogManager.getLogger(PlayerSearchResult.class);

    // Constructor
    public PlayerSearchResult() {
        LOGGER.debug("Default PlayerSearchResult constructor called.");

        this.clubTag = null;
        this.name = null;
        this.playerId = null;
        this.zones = new ArrayList<>();
        this.threes = new PlayerMatchmaking();
        this.royal = new PlayerMatchmaking();
    } // Default Constructor

    public PlayerSearchResult(JSONObject jsonObject) {
        LOGGER.debug("PlayerSearchResult constructor called.");

        throw new UnsupportedOperationException("Constructor not implemented.");
    }

    // Other Functions

    // Getter Functions
    public String getClubTag() {
        if (this.clubTag == null) {
            return null;
        } else {
            return this.clubTag;
        } // if-else
    } // getClubTag

    public String getName() {
        return this.name;
    } // getName

    public String getPlayerId() {
        return this.playerId;
    } // getPlayerId

    public List<PlayerZone> getZones() {
        return this.zones;
    } // getZones

    public PlayerMatchmaking getThrees() {
        return this.threes;
    } // getThrees

    public PlayerMatchmaking getRoyal() {
        return this.royal;
    } // getRoyal
} // PlayerSearchResult