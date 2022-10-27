package com.trackmaniaindia.tmibot.api.player.matchmaking;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.util.Date;

public class PlayerMatchmakingResult {
    private int afterScore;
    public boolean leave;
    private String liveId;
    public boolean mvp;
    private String playerId;
    private Date startTime;
    public boolean win;

    private final static Logger LOGGER = LogManager.getLogger(PlayerMatchmakingResult.class);

    // Constructors
    public PlayerMatchmakingResult() {
        LOGGER.debug("Default PlayerMatchmakingResult constructor called.");

        this.afterScore = -1;
        this.leave = false;
        this.liveId = null;
        this.mvp = false;
        this.playerId = null;
        this.startTime = new Date();
        this.win = false;
    } // Default Constructor

    public PlayerMatchmakingResult(JSONObject jsonObject) {
        LOGGER.debug("PlayerMatchmakingResult constructor called.");

        throw new UnsupportedOperationException("Constructor not implemented yet.");
    }

    // Functions

    // Getter Functions
    public int getAfterScore() {
        return this.afterScore;
    } // getAfterScore

    public String getLiveId() {
        if (this.liveId == null) {
            return "";
        } else {
            return this.liveId;
        }
    } // getLiveId

    public String getPlayerId() {
        if (this.playerId == null) {
            return "";
        } else {
            return this.playerId;
        }
    } // getPlayerId

    public Date getStartTime() {
        return this.startTime;
    } // getStartTime

    public String getStartTimeString() {
        return this.startTime.toString();
    } // getStartTimeString
} // PlayerMatchmakingResult
