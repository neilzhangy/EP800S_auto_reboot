# EP800S_auto_reboot
##Reboot your optical modem HG-EP800-S

###Add this shell command to your cron job on your router or NAS
cd /root;echo `date` >> ./logs;/usr/local/bin/python2.7 ./reboot_router.py >> ./logs;echo "--------------------" >> ./logs
