package com.trackmaniaindia.tmibot.api.player.matchmaking;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

public class MatchmakingLeaderboardPlayer {
    private String playerName;
    private String playerTag;
    private String playerId;
    private int rank;
    private int score;
    private int progression;

    private final static Logger LOGGER = LogManager.getLogger(MatchmakingLeaderboardPlayer.class);

    // Constructor

    /**
     * Default Constructor
     */
    public MatchmakingLeaderboardPlayer() {
        LOGGER.debug("Default MatchmakingLeaderboardPlayer constructor called.");

        this.playerName = null;
        this.playerTag = null;
        this.playerId = null;
        this.rank = -1;
        this.score = -1;
        this.progression = -1;
    } // Default Constructor

    /**
     * Constructor that uses a json object and parses it by itself.
     * @param jsonData The json data from the api.
     */
    public MatchmakingLeaderboardPlayer(JSONObject jsonData) {
        LOGGER.debug("MatchmakingLeaderboardPlayer constructor called.");

        throw new UnsupportedOperationException("Constructor not implemented yet.");
    } // MatchmakingLeaderboardPlayer

    // Other Functions

    // Getter Functions
    public String getPlayerName() {
        return this.playerName;
    } // getPlayerName

    public String getPlayerTag() {
        return this.playerTag;
    } // getPlayerTag

    public String getPlayerId() {
        return this.playerId;
    } // getPlayerId

    public int getRank() {
        return this.rank;
    } // getRank

    public int getScore() {
        return this.score;
    } // getScore

    public int getProgression() {
        return this.progression;
    } // getProgression
} // MatchmakingLeaderboardPlayer
