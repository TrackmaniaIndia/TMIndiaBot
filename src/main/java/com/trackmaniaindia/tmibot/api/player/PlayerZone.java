package com.trackmaniaindia.tmibot.api.player;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;


/**
 * Represents the zone of the player.
 * It represents all levels of the zone.
 * -> World
 * -> Country
 * -> State/Region 1
 * -> Region 2
 */
public class PlayerZone {
    private String flag;
    private String zone;
    private int rank;

    private final static Logger LOGGER = LogManager.getLogger(PlayerZone.class);

    /**
     * Default Constructor. Should never really be called.
     */
    public PlayerZone() {
        LOGGER.debug("Default PlayerZone constructor called.");

        this.flag = null;
        this.zone = null;
        this.rank = -1;
    } // Default Constructor

    /**
     * Constructor that parses JSON data into a {@code PlayerZone} object.
     * @param jsonData The JSON data from the API.
     */
    public PlayerZone(JSONObject jsonData) {
        LOGGER.debug("PlayerZone constructor called.");

        throw new UnsupportedOperationException("Constructor not Implemented Yet.");
    } // Constructor

    /**
     * Constructor for {@code PlayerZone} object.
     * @param flag The flag of the zone.
     * @param zone The name of the zone.
     * @param rank The rank of the player in the zone.
     */
    public PlayerZone(String flag, String zone, int rank) {
        LOGGER.debug("PlayerZone constructor called.");

        this.flag = flag;
        this.zone = zone;
        this.rank = rank;
    } // Constructor

    /**
     * Makes a list of {@code PlayerZone} in to a String to be used in embeds
     *
     * @param zones the zones themselves.
     * @param addPos whether to add the positions of the players in their regions.
     * @param inline whether to put the positions on their on lines.
     * @return The created string.
     */
    public static String makeString(PlayerZone[] zones, boolean addPos, boolean inline) {
        String createdString = "";

        for (int i = 0; i < zones.length; i++) {
            if (addPos) {
                createdString += zones[i].getRank() + ". ";
            } // if

            createdString += zones[i].getZone();

            if (inline && i != zones.length - 1) {
                createdString += ", ";
            } else {
                createdString += "\n";
            } // if-else
        } // for

        return createdString;
    } // makeString

    /**
     * Overloaded makeString function that calls makeString with the inline value set to
     * {@code true}.
     * @param zones The player zones.
     * @param addPos Whether to add the positions.
     * @return The created string.
     */
    public static String makeString(PlayerZone[] zones, boolean addPos) {
        return PlayerZone.makeString(zones, addPos, true);
    } // makeString

    /**
     * Overloaded makeString function that calls makeString with the addPos value
     * set to {@code false} inline value set to {@code true}.
     *
     * @param zones The player zones.
     * @return The created string.
     */
    public static String makeString(PlayerZone[] zones) {
        return PlayerZone.makeString(zones, false, true);
    } // makeString

    /**
     * Returns the flag of this specific region.
     * @return the flag of the region.
     */
    public String getFlag() {
        return this.flag;
    } // getFlag

    /**
     * The name of the zone of the specific region.
     * @return the name of the zone of the region.
     */
    public String getZone() {
        return this.zone;
    } // getZone

    /**
     * The rank of the player in this specific region.
     * @return The rank of the player in the region.
     */
    public int getRank() {
        return this.rank;
    } // getRank
} // PlayerZone
