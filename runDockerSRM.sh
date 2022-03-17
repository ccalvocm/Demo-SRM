git clone --depth=1 https://www.github.com/ccalvocm/Demo-SRM.git /home/srm/Demo-SRM
echo "clonado"
chgrp -R 1000 /home/srm/Demo-SRM/
chmod 770 -R /home/srm/Demo-SRM
cd /home/srm/Demo-SRM
conda run -n ciren2 python /home/srm/Demo-SRM/interfaz.py
#echo "cambio de usuario"
#
#sudo -u srm python interfaz.py