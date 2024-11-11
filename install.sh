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
    local result="${1:-1}" ok="${2:-OK}" fail="${3:-FAILURE}"

    if [ "$result" -eq 0 ]; then echo "$ok"; else exitMsg "$fail"; fi
}

exitMsg()
{
    echo "${1:-Unknown Error!}"
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
else
    git pull
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
    sudo apt -qq -y install python3-full python3-pip pipx pythonpy
    echoResult $?
fi
####################################################################
# INSTALL PYTHON MODULES
####################################################################
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
# setuptools
echo "Installing setuptools"
yes | pip install setuptools
echoResult $?
# systemd-python
echo "Installing systemd-python"
yes | pip install systemd-python
echoResult $?
# wheel
echo "Installing wheel"
yes | pip install wheel
echoResult $?
# yaspin
echo "Installing yaspin"
yes | pip install yaspin
echoResult $?
####################################################################
# INSTALL DOTFILES_PY
####################################################################
cd "$HOME/.local/dotfiles-py" || exitMsg "Couldn't change to directory '$HOME/.local/dotfiles-py'"
pip install -e .
echoResult $?
