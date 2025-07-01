sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start actions.runner.zilvertonz-GBS_DAE_Python_ETL.hdclappxd135.service
sudo systemctl enable actions.runner.zilvertonz-GBS_DAE_Python_ETL.hdclappxd135.service
sudo systemctl status actions.runner.zilvertonz-GBS_DAE_Python_ETL.hdclappxd135.service
journalctl -u actions.runner.zilvertonz-GBS_DAE_Python_ETL.hdclappxd135.service -f
