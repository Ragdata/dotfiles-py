#!/usr/bin/env bash
####################################################################
# install.sh
####################################################################
# Ragdata's Dotfiles - Dotfile Installer
#
# File:         install.sh
# Author:       Ragdata
# Date:         10/11/2024
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2024 Redeyed Technologies
####################################################################
# PREFLIGHT
####################################################################
if [[ "${BASH_VERSION:0:1}" -lt 4 ]]; then
    echo "This script requires a minimum Bash version of 4+"
    exit 1
fi
clear
####################################################################
# VARS
####################################################################
export DOT_REPO="$HOME/.local/dotfiles-py"
export DOT_USER="$HOME/.dotfiles"
####################################################################
# FUNCTIONS
####################################################################
echoResult()
{
    local result="${1:-1}" ok="${2:-'OK'}" fail="${3:-'FAILURE'}"

    if $result; then echo "$ok"; else exitMsg "$fail"; fi
}

exitMsg()
{
    echo "${1:-'Unknown Error!'}"
    exit "${2:-1}"
}

di::checkPkg()
{
    (($# < 1)) && exitMsg "${FUNCNAME[0]} - Missing Arguments!"

    dpkg -l | grep "${1:-}" 2> /dev/null 1>&2

    return $?
}
####################################################################
# SETUP PASSWORDLESS SUDO
####################################################################
if [ ! -f "/etc/sudoers.d/$USER" ]; then
    echo "Enabling passwordless sudo"
    sudo sh -c "echo \"$USER ALL=(ALL) NOPASSWD:ALL\" > /etc/sudoers.d/$USER"
fi
####################################################################
# UPDATE & UPGRADE
####################################################################
echo "Install Package Management Tools"
sudo apt -qq -y install software-properties-common
echo "Add Python PPA"
sudo add-apt-repository ppa:deadsnakes/ppa
echo "Updating package registry"
sudo apt -qq -y update
echo "Upgrading system files"
sudo apt -y full-upgrade
####################################################################
# CREATE DIRECTORIES
####################################################################
[ ! -d "$HOME/.backup" ] && mkdir -p "$HOME/.backup"
[ ! -d "$HOME/.dotfiles" ] && mkdir -p "$HOME/.dotfiles"
[ ! -d "$HOME/.local" ] && mkdir -p "$HOME/.local"
####################################################################
# INSTALL GIT
####################################################################
if ! di::checkPkg "git-lfs"; then
    echo "Installing git"
    sudo apt -qq -y install git git-lfs
    echoResult $?
fi
####################################################################
# CLONE REPO
####################################################################
if [ ! -d "$HOME/.local/dotfiles-py" ]; then
    echo "Cloning Repository"
    git clone https://github.com/Ragdata/dotfiles-py.git "$HOME/.local/dotfiles-py"
    echoResult $?
fi
####################################################################
# CREATE XDG DIRECTORIES
####################################################################
echo "Creating XDG Directories"
sudo install -v -b -m 0644 -C -D -t "/etc/xdg" "$HOME/.local/dotfiles-py/src/etc/xdg/user-dirs.defaults" \
    || exitMsg "Failed to install user-dirs.defaults"
xdg-user-dirs-update
echoResult $?
####################################################################
# INSTALL PYTHON
####################################################################
if ! di::checkPkg "pythonpy"; then
    echo "Installing / Updating Python3"
    sudo apt -qq -y install python3 pythonpy
    echoResult $?
fi
####################################################################
# GET PIP
####################################################################
if [ -d "$HOME/downloads" ]; then
    if [ -f "$HOME/downloads/get-pip.py" ]; then rm -f "$HOME/downloads/get-pip.py"; fi
    echo "Downloading pip install script"
    curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py > "$HOME/downloads/get-pip.py"
    echoResult $?
else
    exitMsg "Directory '$HOME/downloads' not found"
fi
####################################################################
# INSTALL PYTHON MODULES
####################################################################
# pip
if [ -f "$HOME/downloads/get-pip.py" ]; then
    echo "Installing pip"
    python3 "$HOME/downloads/get-pip.py"
    echoResult $?
fi
# pipx
echo "Installing pipx"
sudo apt -qq -y install pipx
echoResult $?
# GitPython
echo "Installing GitPython"
yes | pip install GitPython
echoResult $?
# PyGithub
echo "Installing PyGithub"
yes | pip install PyGithub
echoResult $?
# dynaconf
echo "Installing dynaconf"
yes | pip install dynaconf
echoResult $?
# gitdb
echo "Installing gitdb"
yes | pip install gitdb
echoResult $?
# systemd-python
echo "Installing systemd-python"
yes | pip install systemd-python
echoResult $?
# yaspin
echo "Installing yaspin"
yes | pip install yaspin
echoResult $?
####################################################################
# MAIN
####################################################################