
### Complete Rewrite

* Will Create CHANGELOG.md and Update this TODO soon

### Create Players Class
* Get Trackmania ID with Discord ID
* Get Trackmania ID with Username
* Store Usernames to File

* Has Fields - DiscordID, Username, TrackmaniaID
* __init__(self)
* __init__(self, discordid, username, trackmaniaid)
* __init__(self, username)

### Trophies Leaderboard

Notes:

* Start at 2am everyday
* <https://trackmania.io/api/top/trophies/{page}> -> Upto 25 Pages, 5 Req / min, Approx: 5min to Update
* Store in JSON File in /data/trophies/page{page}.json


### TOTD

Notes:

* at 10:30pm Everyday (IST)
* <https://trackmania.io/api/totd/0> (take last totd, this is all totds of the month)


## COTD and Super Royale Reminders

* 10:30pm, 6:30am and 2:30pm reminders for COTD
* 11:30pm, 7:30am and 3:30pm reminders for Super Royale

## Trackmania Commands

* Player Command
* Leaderboards Command
* ViewMaps Command
