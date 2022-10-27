package com.trackmaniaindia.tmibot;

import com.trackmaniaindia.tmibot.api.NadeoAPI;
import com.trackmaniaindia.tmibot.commands.CommandManager;
import com.trackmaniaindia.tmibot.commands.Ping;
import com.trackmaniaindia.tmibot.listeners.OnReady;
import com.trackmaniaindia.tmibot.util.Configuration;
import io.github.cdimascio.dotenv.Dotenv;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.sharding.DefaultShardManagerBuilder;
import net.dv8tion.jda.api.sharding.ShardManager;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.core.config.Configurator;

import javax.security.auth.login.LoginException;

public class TMIndiaBot {
    private final ShardManager shardManager;

    private final static Logger LOGGER = LogManager.getLogger(TMIndiaBot.class);

    /**
     * Create a ShardManager bot and build it.
     * Also adds all the EventListeners.
     * @throws LoginException If the bot fails to log in with the specified token.
     */
    public TMIndiaBot() {
        Dotenv config = Configuration.getConfig();

        //String token = config.get("TOKEN");
        String token = config.get("TESTING_TOKEN");

        LOGGER.debug("Creating the ShardManager.");
        DefaultShardManagerBuilder builder = DefaultShardManagerBuilder.createDefault(token);
        builder.enableIntents(GatewayIntent.MESSAGE_CONTENT);
        builder.setStatus(OnlineStatus.ONLINE);
        builder.setActivity(Activity.playing("TMIndia Bot in Java is Under Development!"));

        LOGGER.info("Starting Bot.");
        this.shardManager = builder.build();

        // Adding Listeners
        LOGGER.debug("Adding Listeners.");
        this.shardManager.addEventListener(new OnReady());

        // Register commands
        this.shardManager.addEventListener(new Ping());
        this.shardManager.addEventListener(new CommandManager());

    } // TMIndiaBot

    public static void main(String[] args) {
        // Setting the LogLevel
        Configurator.setLevel("", Level.DEBUG);

        LOGGER.info("Getting Nadeo Tokens before the Bot is Created.");
        try {
            NadeoAPI.updateTokens();
        } catch (Exception e) {
            e.printStackTrace();
            LOGGER.error("An Error Occurred While Getting Nadeo Tokens.");
            System.exit(-1);
        }

        TMIndiaBot bot = new TMIndiaBot();
    } // main

    /**
     * Getter function for the {@code shardManager}.
     *
     * @return the shardManager for the bot.
     */
    public ShardManager getShardManager() {
        return this.shardManager;
    } // getShardManager
} // TMIndiaBot
