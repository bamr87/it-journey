#!/bin/bash
echo "Hello Mac! let's suit up"
read -p 'Enter something here: ' parm1
if [[ $parm1 = "bash" ]]; then
  echo 'You Selected : $parm1'
  myVar=$parm1
  echo "$myVar is parameter 1"
fi
