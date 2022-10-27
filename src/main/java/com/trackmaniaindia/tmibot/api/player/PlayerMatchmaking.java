package com.trackmaniaindia.tmibot.api.player;

import com.trackmaniaindia.tmibot.api.player.matchmaking.MatchmakingLeaderboardPlayer;
import com.trackmaniaindia.tmibot.api.player.matchmaking.PlayerMatchmakingResult;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.util.List;

public class PlayerMatchmaking {
    private String matchmakingType;
    private int typeId;
    private int progression;
    private int rank;
    private int score;
    private int division;
    private String divisionStr;
    private int minPoints;
    private int maxPoints;
    private String playerId;

    private final static Logger LOGGER = LogManager.getLogger(PlayerMatchmaking.class);

    // Constructors
    public PlayerMatchmaking() {
        LOGGER.debug("Default PlayerMatchmaking constructor called.");

        this.matchmakingType = null;
        this.typeId = -1;
        this.progression = -1;
        this.rank = -1;
        this.score = -1;
        this.division = -1;
        this.divisionStr = null;
        this.minPoints = -1;
        this.maxPoints = -1;
        this.playerId = null;
    } // Default Constructor

    public PlayerMatchmaking(JSONObject jsonObject) {
        LOGGER.debug("PlayerMatchmaking constructor called.");

        throw new UnsupportedOperationException("Constructor not implemented.");
    } // Constructor

    // Other functions
    public List<PlayerMatchmakingResult> history(int page) {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // history

    public List<PlayerMatchmakingResult> history() {
        return this.history(0);
    } // history

    public static List<MatchmakingLeaderboardPlayer> topMatchmaking(int page, boolean royal) {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // topMatchmaking

    public static List<MatchmakingLeaderboardPlayer> topMatchmaking(int page) {
        return PlayerMatchmaking.topMatchmaking(page, false);
    } // topMatchmaking

    public static List<MatchmakingLeaderboardPlayer> topMatchmaking() {
        return PlayerMatchmaking.topMatchmaking(0, false);
    }

    // Getter Functions
}
