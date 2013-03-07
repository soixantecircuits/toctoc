#!/usr/bin/env bash
TOCTOC_PATH="/usr/share/toctoc"
TOCTOC_LOG_PATH="/var/log/toctoc"

toctoc_install() {
  # TODO: install python libs: twitter, GPIO
  mkdir $TOCTOC_PATH
  cp toctoc/toctoc.py $TOCTOC_PATH
  cp toctoc/ding.mp3 $TOCTOC_PATH
	echo "Copied the toctoc.py script to $TOCTOC_PATH"
  mkdir $TOCTOC_LOG_PATH
  touch /var/log/toctoc/toctoc.log
  cp toctoc/toctoc /etc/init.d/
  apt-get install chkconfig
  chkconfig toctoc on
	echo "Copied the toctoc daemon script to /etc/init.d/"
  autosshdaemon_install
}

cuicui_install() {
  mkdir $TOCTOC_PATH
  cp cuicui/cuicui.py $TOCTOC_PATH
	echo "Copied the cuicui.py script to $TOCTOC_PATH"
  mkdir $TOCTOC_LOG_PATH
  touch /var/log/toctoc/cuicui.log
  cp cuicui/cuicui /etc/init.d/
  apt-get install chkconfig
  chkconfig cuicui on
	echo "Copied the cuicui daemon script to /etc/init.d/"
  autosshdaemon_install
}

autosshdaemon_install() {
  # TODO: check if a autossh_tunnel is already there
  # TODO: ask for port
  # TODO: ssh-copy-id 
  # TODO: install ssh
  # TODO: install chkconfig
  apt-get install autossh
  cp remotecontrol/autossh_tunnel /etc/init.d/
  chkconfig autossh_tunnel on
	echo "Copied the autossh_tunnel daemon scripts to /etc/init.d/"
}


case "$1" in
  project)
	echo "Installing the toctoc project"
	cuicui_install
  toctoc_install
	echo "."
	;;
  toctoc)
	echo "Installing the toctoc scripts"
	toctoc_install
	echo "."
	;;
  cuicui)
	echo "Installing the cuicui scripts"
  cuicui_install
	echo "."
	;;
  *)
	echo "Usage: ./install.sh {project|toctoc|cuicui}" >&2
	exit 3
	;;
esac

exit 0
