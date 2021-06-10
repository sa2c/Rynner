# Rynner

Rynner project is currently under heavy development. 
You should expect a bumpy ride at this point and APIs, 
interfaces and names may change without warning. 
This project is currently not production-ready.

There are a large number of open issues, in particular on Windows platforms.

# Documentation

Current documentation may be found at:
https://rynner.readthedocs.io/

# Persistent SSH connection (Linux)

## Prerequisites

SSH installed, this should be default on all Linux machines. 
That automatically provides `ssh-agent` and `ssh-add`.

## Add SSH keys to the agent as needed

Check your `~/.ssh` directory, if there is a `config` file open it with a text editor,
if no such file exists create it and repeat the step above.
Add a new line `AddKeysToAgent=yes` and save the file.

## Start `ssh-agent` automatically

### Bash users

Add the following to your `~/.profile` file:

```shell
export SSH_AUTH_SOCK=~/.ssh/ssh-agent.$HOSTNAME.sock
ssh-add -l 2>/dev/null >/dev/null
if [ $? -ge 2 ]; then
  ssh-agent -a "$SSH_AUTH_SOCK" >/dev/null
fi
export SSH_AGENT_PID=$(pgrep ssh-agent)
```

### Zsh users

Add the following to your `~/.zprofile` file:

```shell
export SSH_AUTH_SOCK=~/.ssh/ssh-agent.$HOST.sock
ssh-add -l 2>/dev/null >/dev/null
if [ $? -ge 2 ]; then
  ssh-agent -a "$SSH_AUTH_SOCK" >/dev/null
fi
export SSH_AGENT_PID=$(pgrep ssh-agent)
```

# Install
We do not provide ready-to-install packages at the moment, 
but you can use the following command to install the latest version of Rynner:
```shell
pip install git+https://github.com/sa2c/Rynner.git
```