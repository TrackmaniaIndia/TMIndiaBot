#!/bin/bash
cd ..

echo "creating logs"
mkdir -pv logs

echo "creating logs/commands.log"
touch logs/commands.log

echo "creating bot/resources/temp"
mkdir -pv bot/resources/temp

echo "creating config.yaml"
touch config.yaml

echo "creating bot/utils/node"
mkdir -pv bot/utils/node

echo "creating bot/resources/temp"
mkdir -pv bot/resources/temp

echo "creating times_run.txt"
echo 0 > bot/resources/times_run.txt

echo "creating guild_data folder"
mkdir -pv bot/resources/guild_data

echo "cloning TrackmaniaLeaderboard"
git clone git@github.com:NottCurious/TrackmaniaLeaderboards.git bot/resources/leaderboard
