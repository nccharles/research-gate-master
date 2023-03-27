  
#!/bin/bash

# Author: Sylvie
# Copyright: Copyright 2023, AUCA Research Gate

# Add current directory to the pythonpath variable. This will fix import errors on some systems.
# Systems for which this will work:
# - Mac OS, Linux
# The error fixed is "ModuleNotFoundError: No module found with name 'src'" that shows up 
# when attempting to run code from the ur research gate directory".

print_to_user() {
  echo $1
}

append_to_bashrc() {
  echo  $1 >> ~/.bashrc
}

# Check if system has .bashrc file.
FILE=~/.bashrc
if ! test -f "$FILE"; then
    print_to_user "This setup is incompatible with your system."
    exit
fi

# Check if the changes were not made in the past. Avoid duplicate exports. 
if grep -q "^export PYTHONPATH=:$PWD$" ~/.bashrc ; then
print_to_user "Path already set."
print_to_user "Setup completed."
  exit 
fi

bold=$(tput bold)
normal=$(tput sgr0)
green='\e[0;32m'

# append the export command to the .bashrc file
append_to_bashrc "# UR Research Gate"
append_to_bashrc "export PYTHONPATH=$PYTHONPATH:$PWD"
append_to_bashrc "export PATH=$PATH:$PWD"
print_to_user "-> $PYTHONPATH added to PYTHONPATH"
print_to_user "-> $PATH now includes current directory"
print_to_user "Setup completed!"

# Final message to the user 
print_to_user "${green} Setup has been configured.${normal}, but "
print_to_user "You need to run ${bold}source ~/.bashrc${normal} for changes to take effect or reboot the system."

