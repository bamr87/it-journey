#!/bin/bash

echo 'welcome to calc'
read -p 'first number' parm1
read -p 'second number' parm2
answer=$(parm1 + parm2)
echo $answer
