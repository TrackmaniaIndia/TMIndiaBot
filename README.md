# TMIndiaBot

Discord bot for the [TM India Discord Server](https://discord.gg/aztYuhWxgU "TM India Discord invite")

##### *v1.6*

**New Features**

1. Website (kinda) for command list (/commandlist)
2. COTD Data (/cotddetails)
3. Suggestions (/suggest)
4. Current Day TOTD (/totd)
5. Link to Testing Server (/testingserver)
6. **Bot Invite Link (/invitelink)**

**Bug Fixes (Major)**

1. Broken player details matchmaking rank is now fixed

**Bug Fixes (Minor)**

1. Updated Command Descriptions
2. New Embed Colours
3. Changed a few links to URL buttons

### Command List

Command List can be found [here](https://gist.github.com/NottCurious/f9b618bbfd8aa133d0de2655b94bfca6)

#### Developers

NottCurious

* [Github](https://github.com/NottCurious)
* Discord: NottCurious#4351
* Main Bot Dev

Artifex

* [Github](https://github.com/Artifexdevstuff)
* Discord: Dmart bag#9718
* Bot Dev

Calcium the Penguin

* Discord: Calcium The Bored Penguin#2006
* Contributor

#### Special Thanks

Thank you to Trackmania.io Developer Miss and node-Trackmania.io Developer Greep for their NPM Package!

##### Update (26th October, 2021)

* We now do not need to run a seperate command terminal just for the api.
* The bot will no longer work unless you have access to the private api repo. Please contact the developers if you want
  access to clone it
* If you have access, please clone the repo into util/node/

##### Update (12th December, 2021)

* The API is now Open Source, you can find
  it [here](https://github.com/artifexdevstuff/TMIndiaBotApi "TMIndiaBotApi Github Link")
* API bugs out when a new COTD is released (roughly 11:30pm IST), a fix is being worked on by tmio devs
* You can also opt to clone the API seperately and run it from there, the bot has a confirmation prompt for running the
  api

##### Update (16th December, 2021)

* Above bug has been fixed
* Leaderboards will be moved into their own public repository
  found [here](https://github.com/NottCurious/TrackmaniaLeaderboards)
    * If you have access, clone into `./data` and rename the folder to `leaderboard`