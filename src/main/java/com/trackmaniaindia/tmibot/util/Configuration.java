package com.trackmaniaindia.tmibot.util;

import io.github.cdimascio.dotenv.Dotenv;

public class Configuration {
    public static Dotenv getConfig() {
        Dotenv config = Dotenv.configure().ignoreIfMissing().load();

        return config;
    } // getConfig
} // Configuration
