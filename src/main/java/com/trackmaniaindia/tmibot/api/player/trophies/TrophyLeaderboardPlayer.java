package com.trackmaniaindia.tmibot.api.player.trophies;

import com.trackmaniaindia.tmibot.api.Player;
import com.trackmaniaindia.tmibot.api.player.PlayerZone;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class TrophyLeaderboardPlayer {
    private String playerName;
    private String clubTag;
    private String playerId;
    private int rank;
    private String score;
    private List<PlayerZone> zones;

    private final static Logger LOGGER = LogManager.getLogger(TrophyLeaderboardPlayer.class);

    // Constructors
    public TrophyLeaderboardPlayer() {
        this.playerName = null;
        this.clubTag = null;
        this.playerId = null;
        this.rank = -1;
        this.score = null;
        this.zones = new ArrayList<>();
    } // Default Constructor

    public TrophyLeaderboardPlayer(JSONObject jsonObject) {
        throw new UnsupportedOperationException("Constructor not implemented yet.");
    } // json Constructor

    // Other Functions
    public Player getPlayer() {
        return Player.getPlayer(this.playerId);
    }

    // Getter Functions
    public String getPlayerName() {
        return this.playerName;
    } // getPlayerName

    public String getClubTag() {
        return this.clubTag;
    } // getClubTag

    public String getPlayerId() {
        return this.playerId;
    } // getPlayerId

    public int getRank() {
        return this.rank;
    } // getRank

    public String getScore() {
        return this.score;
    } // getScore

    public List<PlayerZone> getZones() {
        return this.zones;
    } // getZones
}
