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