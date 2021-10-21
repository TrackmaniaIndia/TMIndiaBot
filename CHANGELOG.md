### CHANGELOG

<small>v1.0-b1.0</small>

<small><small>19th October, 2021</small></small>

* v1.0 Rewrite Begins
* Make main bot and important files
* Make Generic Cog
* Make on_ready listener


<small>v1.0-b1.1</small>

<small><small>20th October, 2021</small></small>

* Make first slash command (ping)
* Change Requirements.txt to now use the master branch of py-cord
    * Py-cord master branch now has slash commands and will be the nightly build


<small>v1.0-b1.2</small>

<small><small>21st October, 2021</small></small>

* Prefix Command
* Each COG will now have both slash and normal command, indicated by _slash for *slash cogs*
* using `ctx.reply(mention_author=False)` instead of `ctx.send`
