package com.trackmaniaindia.tmibot.listeners;

import net.dv8tion.jda.api.events.session.ReadyEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class OnReady extends ListenerAdapter {

    private final static Logger LOGGER = LogManager.getLogger(OnReady.class);

    /**
     * Listener for when the bot is finally ready.
     * @param event The event itself.
     */
    @Override
    public void onReady(ReadyEvent event) {
        LOGGER.info("TMIndiaBot is now ready!");
        super.onReady(event);
    }
}
