package com.trackmaniaindia.tmibot.api.player;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

public class PlayerMetaInfo {
    private String displayUrl;
    public boolean inNadeo;
    public boolean inTmgl;
    public boolean inTmioDevTeam;
    public boolean isSponsor;
    private int sponsorLevel;
    private String twitch;
    private String twitter;
    private String youtube;
    private String vanity;

    private final static Logger LOGGER = LogManager.getLogger(PlayerMetaInfo.class);

    // Constructor
    public PlayerMetaInfo() {
        LOGGER.debug("Default PlayerMetaInfo constructor called.");

        this.displayUrl = null;
        this.inNadeo = false;
        this.inTmgl = false;
        this.inTmioDevTeam = false;
        this.isSponsor = false;
        this.sponsorLevel = -1;
        this.twitch = null;
        this.twitter = null;
        this.youtube = null;
        this.vanity = null;
    } // Default Constructor

    public PlayerMetaInfo(JSONObject jsonObject) {
        LOGGER.debug("PlayerMetaInfo constructor called.");

        throw new UnsupportedOperationException("Constructor not implemented yet.");
    } // JSON Constructor

    // Other Functions

    // Getter Functions
    public String getDisplayUrl() {
        if (this.displayUrl == null) {
            return "";
        } else {
            return this.displayUrl;
        } // if-else
    } // getDisplayUrl

    public String getTwitch() {
        if (this.twitch == null) {
            return "";
        } else {
            return this.twitch;
        } // if-else
    } // getTwitch

    public String getTwitter() {
        if (this.twitter == null) {
            return "";
        } else {
            return this.twitter;
        } // if-else
    } // getTwitter

    public String getYoutube() {
        if (this.youtube == null) {
            return "";
        } else {
            return this.youtube;
        } // if-else
    } // getYoutube

    public String getVanity() {
        if (this.vanity == null) {
            return "";
        } else {
            return this.vanity;
        } // if-else
    } // getVanity

    public int getSponsorLevel() {
        return this.sponsorLevel;
    } // getSponsorLevel
} // PlayerMetaInfo