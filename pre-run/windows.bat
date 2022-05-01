@echo off

echo creating logs
mkdir logs

echo creating logs/commands.log
touch logs/commands.log

echo creating bot/resources/temp
mkdir bot\resources\temp

echo creating config.yaml
touch config.yaml

echo creating bot/utils/node
mkdir bot\utils\node

echo creating bot/resources/temp
mkdir bot\resources\temp

echo creating times_run.txt
echo 0 > bot/resources/times_run.txt

echo creating guild_data folder
mkdir -p bot/resources/guild_data

echo cloning TrackmaniaLeaderboards
git clone https://github.com/NottCurious/TrackmaniaLeaderboards.git bot/resources/leaderboard
