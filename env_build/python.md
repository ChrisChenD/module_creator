git update

apt update:
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

# config docker
sudo apt install docker

> 做一个镜像可以直接使用docker

https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh



export npm_pro=npm_pro
npx create-next-app@latest $npm_pro -y
cd $npm_pro 
npm run dev


# down python
sudo apt update
sudo apt install python3.9


109.244.159.137