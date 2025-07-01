# Stop and uninstall the existing service
sudo ./svc.sh stop
sudo ./svc.sh uninstall

# Remove current runner config
./config.sh remove --token <PASTE_NEW_TOKEN_HERE>
./config.sh --url https://github.com/zilvertonz/GBS_DAE_Devops_Automation --token <PASTE_NEW_TOKEN_HERE>
sudo ./svc.sh install
sudo systemctl start actions.runner.zilvertonz-GBS_DAE_Devops_Automation.hdclappxd135.service
sudo systemctl enable actions.runner.zilvertonz-GBS_DAE_Devops_Automation.hdclappxd135.service
