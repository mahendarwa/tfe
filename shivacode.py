cd ~/actions-runner
./svc.sh stop
sudo ./svc.sh uninstall

./config.sh remove --token <TOKEN>
./config.sh --url https://github.com/zilvertonz/GBS_DAE_Devops_Automation --token <TOKEN>
sudo ./svc.sh install
sudo systemctl start actions.runner.zilvertonz-GBS_DAE_Devops_Automation.hdclappxd135.service
sudo systemctl enable actions.runner.zilvertonz-GBS_DAE_Devops_Automation.hdclappxd135.service
