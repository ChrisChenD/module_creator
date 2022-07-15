# apt update:
cd /etc/apt
sudo cp sources.list sources.list.bak
sudo vi sources.list
deb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse

deb http://archive.canonical.com/ubuntu focal partner
deb-src http://archive.canonical.com/ubuntu focal partner
# update apt
sudo apt update


# git update
cd ~;mkdir git;cd git
git clone https://github.com/ChrisChenD/module_creator

# install hello.vsix
open extension

# install node
curl -fsSL https://deb.nodesource.com/setup_17.x | sudo -E bash -
sudo apt-get install -y nodejs
# create next.js
export npm_pro=npm_pro
npx create-next-app@latest $npm_pro -y
#
cd $npm_pro
npm run dev
# copy pages
rm -rf pages
git clone https://github.com/ChrisChenD/pages
# tailwind
# tailwind 1 install 
npm install -D tailwindcss
npx tailwindcss init
# tailwind 2 update config.js
cp pages/env_create/*.config.js .
# tailwind 3 compile
npx tailwindcss -i ./pages/tailwind_base.css -o ./dist/output.css --watch
# install swr
npm install swr

# run
npm run dev


# Mvc_plan
# down python
sudo apt install python3.9 -y
# down conda
去官网
https://docs.conda.io/en/latest/miniconda.html
复制下载连接

export down_link='https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh'
mkdir ~/download;cd ~/download;
curl $down_link -o Miniconda3.sh
sudo chmod +x Miniconda3.sh
./Miniconda3.sh

# down python package
conda install flask pandas numpy pymysql sqlalchemy -y

# install  mysql
sudo apt install -y mysql-client mysql-server 
sudo vi mysqld.cnf
[
    skip-grant-tables
]
sudo systemctl restart mysql
mysql
    FLUSH PRIVILEGES;
    CREATE USER 'test'@'%' IDENTIFIED BY 'test';
    GRANT ALL PRIVILEGES ON * . * TO 'test'@'%';
    FLUSH PRIVILEGES;
    quit

mysql -u test -p
    test
>>>>>>>>>>>>>>>>>>




109.244.159.137
http://175.27.223.106:3000/mvc_plan/t1
http://175.27.223.106:3000/demo/canvas_demo/demo