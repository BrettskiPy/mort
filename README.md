# Mort

### Description
Mort is an open source game (eventually an MMORPG) that uses the Python Arcade engine and FastAPI. This game is designed to be 
as <ins>brutal</ins> as possible with key concepts such as risky item upgrades and full loot PVP. The player should 
**at all times** feel they are balancing <ins>risk</ins> vs <ins>reward</ins>. The game will always be 100% 
free with the eventual possibility for donations to support server costs and efforts. 

### PVM and PVP
#### Portal System
Players have the choice of 4 instanced PVM portal groupings. Every portal grouping (after the first) will have an increased
chance of a PVP encounter and increased PVM loot chances. When a player selects a portal their soul will attempt to travel to the 
PVM instance location specified by the portal name. During travel, a player's soul can be intercepted by "Soul Interceptors". 
If your soul is intercepted by an Interceptor, there will be a chance your soul will be protected via a "Soul Protector"
(if enabled). This will allow another player of a similar level to fight in your place for you! This option can be turned off and is 
<ins>not</ins> guaranteed to work.

![](ideas/portal_pvp.png)
![](ideas/portal_grouping.png)

#### Soul Interceptors
* Evil players seeking to steal the souls of portal travelers.  
* Successfull PVP kill will reward the Interceptor with the loot of the soul traveler or Protector and the chance of obtaining 
"Cursed Souls".
#### Soul Protectors
* Lawful players seeking to protect the souls of portal travelers.  
* Successfull PVP kill will reward the Protector with the loot of the Interceptor and the chance of obtaining "Blessed Souls"

### Upgrading
![](ideas/upgrade_mock.png)
### OTHER TOPICS 
TODO

### Technical Components 
#### Front end
* Python Arcade https://api.arcade.academy/en/latest/
#### Back end
* FastAPI https://fastapi.tiangolo.com/

### Contributing
Everyone who contributes is **a humble volunteer** and all assets are open source and can be found mostly from 
https://opengameart.org/. I'm thankful for meaningful and thoughtful contributions regardless of skill. I (BrettskiPy) will do my 
best to keep the project moving in the general creative direction I envision but, I'm absolutely open to fresh ideas. 
