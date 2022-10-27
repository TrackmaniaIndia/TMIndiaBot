package com.trackmaniaindia.tmibot.commands;

import net.dv8tion.jda.api.events.guild.GuildReadyEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;

import java.util.ArrayList;
import java.util.List;

public class CommandManager extends ListenerAdapter {
    /**
     * Adds commands to a guild when it is ready. Much faster
     * than adding global commands.
     *
     * {@inheritDoc}
     */
    @Override
    public void onGuildReady(GuildReadyEvent event) {
        // Does not include new guilds the bot joins
        List<CommandData> commandData = new ArrayList<>();
        commandData.add(Commands.slash("ping", "Ping Pong!"));
        event.getGuild().updateCommands().addCommands(commandData).queue();
    }
}
