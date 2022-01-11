# Anti-SpammeR

Sometimes in discord server, some person spams in  all the channel. Here is a simple bot to prevent this kind of attack .
   
This bot only mute the spammer and inform the server ower about this.  

## How it works

This bot has a list of valid links, a list of spam links and it will be maintain an unverified link list. 

- If a user send a link which is neither spam nor valid links, then this link will be sent to the admin to validate the link. The link will be listed as an unverified link.  

- If any member of the server send any link form the spam link list, he/she will be muted. And will be given a role `spammer`.   
- A member of the server will have 5 chance to send any unverified links. That means if he/she send can send unverified link, 5 times. After that he will be muted. 