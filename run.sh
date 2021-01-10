#!/bin/bash
killall -q acm-bot
nohup ./acm-bot > bot.log 2>&1 &
