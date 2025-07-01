cd ~/actions-runner

# Stop and uninstall old runner
sudo ./svc.sh stop
sudo ./svc.sh uninstall

# Delete the old config (skip `config.sh remove`)
rm -rf .runner
./config.sh --url https://github.com/zilvertonz/GBS_DAE_Devops_Automation --token <new_token>
sudo ./svc.sh install
sudo systemctl start actions.runner.zilvertonz-GBS_DAE_Devops_Automation.hdclappxd135.service
sudo systemctl enable actions.runner.zilvertonz-GBS_DAE_Devops_Automation.hdclappxd135.service
