
sudo mkdir -p /pythonPROD/python/scripts/file_movement_pattern/{dev,prod,test}


sudo rsync -av --delete --no-o --no-g --no-perms --no-xattrs /opt/versions/python/./ /pythonPROD/python/
