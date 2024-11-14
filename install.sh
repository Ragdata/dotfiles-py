#!/usr/bin/env bash
# shellcheck disable=SC1091
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
TERM_ESC=$'\033'
TERM_CSI="${TERM_ESC}["
RESET=$(printf -- '%s0m' "$TERM_CSI")
RED=$(printf -- '%s31m' "$TERM_CSI")
GOLD=$(printf -- '%s33m' "$TERM_CSI")
####################################################################
# FUNCTIONS
####################################################################
echoResult()
{
    local result="${1:-1}" ok="${2:-OK}" fail="${3:-FAILURE}"

    if [ "$result" -eq 0 ]; then echo -e "${GOLD}$ok${RESET}"; else exitMsg "$fail"; fi
}

exitMsg()
{
    echo -e "${RED}${1:-Unknown Error!}${RESET}"
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
    echo -e "${GOLD}Enabling passwordless sudo${RESET}"
    sudo sh -c "echo \"$USER ALL=(ALL) NOPASSWD:ALL\" > /etc/sudoers.d/$USER"
fi
####################################################################
# UPDATE & UPGRADE
####################################################################
echo -e "${GOLD}Install Package Management Tools${RESET}"
sudo apt -y install software-properties-common
echo -e "${GOLD}Add Python PPA${RESET}"
sudo add-apt-repository ppa:deadsnakes/ppa
echo -e "${GOLD}Updating package registry${RESET}"
sudo apt -y update
echo -e "${GOLD}Upgrading system files${RESET}"
sudo apt -y full-upgrade
####################################################################
# CREATE DIRECTORIES
####################################################################
[ ! -d "$HOME/.backup" ] && mkdir -p "$HOME/.backup"
[ ! -d "$HOME/.dotfiles" ] && mkdir -p "$HOME/.dotfiles"
[ ! -d "$HOME/.local" ] && mkdir -p "$HOME/.local"
[ ! -d "$HOME/.venv" ] && mkdir -p "$HOME/.venv"
####################################################################
# INSTALL GIT
####################################################################
if ! di::checkPkg "git-lfs"; then
    echo -e "${GOLD}Installing git${RESET}"
    sudo apt -qq -y install git git-lfs
    echoResult $?
fi
####################################################################
# CLONE REPO
####################################################################
if [ ! -d "$HOME/.local/dotfiles-py" ]; then
    echo -e "${GOLD}Cloning Repository${RESET}"
    git clone https://github.com/Ragdata/dotfiles-py.git "$HOME/.local/dotfiles-py"
    echoResult $?
else
    git pull
fi
####################################################################
# CREATE XDG DIRECTORIES
####################################################################
echo -e "${GOLD}Creating XDG Directories${RESET}"
sudo install -v -b -m 0644 -C -D -t "/etc/xdg" "$HOME/.local/dotfiles-py/src/etc/xdg/user-dirs.defaults" \
    || exitMsg "Failed to install user-dirs.defaults"
xdg-user-dirs-update
echoResult $?
####################################################################
# INSTALL PYTHON
####################################################################
if ! di::checkPkg "pythonpy"; then
    echo -e "${GOLD}Installing / Updating Python3${RESET}"
    sudo apt -y install update-manager python3-full python3-pip pipx python3-update-manager
    echoResult $?
fi
####################################################################
# LAUNCH VIRTUAL ENVIRONMENT
####################################################################
echo -e "${GOLD}Launching virtual environment${RESET}"
python3 -m venv --system-site-packages "$HOME/.venv/dot"
source "$HOME/.venv/dot/bin/activate"
####################################################################
# CONFIGURE PIPX
####################################################################
pipx ensurepath
#sudo pipx ensurepath --global
#pipx completions
####################################################################
# INSTALL PYTHON PACKAGES
####################################################################
echo -e "${GOLD}Installing Python Packages${RESET}"
pip install GitPython PyGithub dynaconf gitdb setuptools systemd-python wheel yaspin
echoResult $?
####################################################################
# INSTALL DOTFILES_PY
####################################################################
echo -e "${GOLD}Installing dotfiles-py${RESET}"
cd "$HOME/.local/dotfiles-py" || exitMsg "Couldn't change to directory '$HOME/.local/dotfiles-py'"
pip install -e .
cd - || exitMsg "Couldn't return to previous directory"
echoResult $?
