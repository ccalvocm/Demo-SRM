git clone --depth=1 https://www.github.com/ccalvocm/Demo-SRM.git /home/srm/Demo-SRM
echo "clonado"
chgrp -R 1000 /home/srm/Demo-SRM/
chmod 770 -R /home/srm/Demo-SRM
echo "cambio de usuario"
cd /home/srm/Demo-SRM
sudo -u srm python interfaz.py