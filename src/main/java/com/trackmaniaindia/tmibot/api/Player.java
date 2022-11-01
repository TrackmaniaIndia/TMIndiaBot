package com.trackmaniaindia.tmibot.api;

import com.trackmaniaindia.tmibot.api.player.*;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class Player {
    private String clubTag;
    private Date firstLogin;
    private String playerId;
    private Date lastClubTagChange;
    private PlayerMetaInfo meta;
    private String name;
    private PlayerTrophies trophies;
    private List<PlayerZone> zoneList;
    private PlayerMatchmaking threes;
    private PlayerMatchmaking royal;

    // Constructors
    public Player() {
        this.clubTag = null;
        this.firstLogin = new Date();
        this.playerId = null;
        this.lastClubTagChange = new Date();
        this.meta = new PlayerMetaInfo();
        this.name = null;
        this.trophies = new PlayerTrophies();
        this.zoneList = new ArrayList<>();
        this.threes = new PlayerMatchmaking();
        this.royal = new PlayerMatchmaking();
    } // Default Constructor

    public Player(JSONObject jsonObject) {
        throw new UnsupportedOperationException("Constructor not implemented yet.");
    } // JSON Constructor

    // Other Functions
    public static String getPlayerId(String username) {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // getPlayerId

    public static Player getPlayer(String playerId) {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // getPlayer

    public static String getUsername(String playerId) {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // getUsername

    public static List<PlayerSearchResult> searchPlayer(String username) {
        throw new UnsupportedOperationException("Function not implemented yet.");
    } // searchPlayer

    // Getter Functions
    public String getClubTag() {
        return this.clubTag;
    } // getClubTag

    public Date getFirstLogin() {
        return this.firstLogin;
    } // getFirstLogin

    public String getPlayerId() {
        return this.playerId;
    } // getPlayerId

    public Date getLastClubTagChange() {
        return this.lastClubTagChange;
    } // getLastClubTagChange

    public PlayerMetaInfo getMeta() {
        return this.meta;
    } // getMeta

    public String getName() {
        return this.name;
    } // getName

    public PlayerTrophies getTrophies() {
        return this.trophies;
    } // getTrophies

    public List<PlayerZone> getZoneList() {
        return this.zoneList;
    } // getZoneList

    public PlayerMatchmaking getThrees() {
        return this.threes;
    } // getThrees

    public PlayerMatchmaking getRoyal() {
        return this.royal;
    } // getRoyal
}
