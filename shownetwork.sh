#!/bin/bash
timeout_secs=4
SETCOLOR="python rgbled.py"
RED="1,0,0"
GREEN="0,1,0"
endTime=$(( $(date +%s) + timeout_secs )) # Calculate end time.
rc=255
while [ $(date +%s) -lt $endTime ]; do  # Loop until interval has elapsed.
  sleep 1
  ping -c 1 www.github.com 2>&1
  rc=$?
  if [[ $rc -eq 0 ]]; then
    break
  fi
done
if [[ $rc -eq 0 ]]; then
  $SETCOLOR $GREEN
else
  $SETCOLOR $RED
fi
