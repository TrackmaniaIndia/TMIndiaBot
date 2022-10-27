package com.trackmaniaindia.tmibot.commands;

import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class Ping extends ListenerAdapter {
    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {
        String command = event.getName();

        switch (command) {
            case "ping":
                event.reply("Pong!" + event.getUser().getAsMention()).setEphemeral(true).queue();
                break;
        }
    } // onSlashCommandInteraction
} // Ping
