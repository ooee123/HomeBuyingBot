This is my Raspberry Pi service that listens to Redfin URL entities, and does some data gathering.

homeBuyingBot.service is the .service file used for systemctl. Copy into /lib/systemd/system/

Then use

`sudo systemctl start homeBuyingBot.service`
`sudo systemctl restart homeBuyingBot.service`
`sudo systemctl stop homeBuyingBot.service`
`sudo systemctl enable homeBuyingBot.service`
`sudo systemctl disable homeBuyingBot.service`
`sudo systemctl status --lines=100 homeBuyingBot.service`
