#!/bin/bash
cd ..

echo "creating logs"
mkdir -p logs

echo "creating logs/commands.log"
touch logs/commands.log

echo "creating bot/resources/temp"
mkdir -p bot/resources/temp

echo "creating config.yaml"
touch config.yaml

echo "creating bot/utils/node"
mkdir -p bot/utils/node

echo "cloning TMIndiaBotApi"
git clone git@github.com:TrackmaniaIndia/TMIndiaBotApi.git bot/utils/node/TMIndiaBotApi

echo "cloning TrackmaniaLeaderboard"
git clone git@github.com:NottCurious/TrackmaniaLeaderboards.git bot/resources/leaderboard