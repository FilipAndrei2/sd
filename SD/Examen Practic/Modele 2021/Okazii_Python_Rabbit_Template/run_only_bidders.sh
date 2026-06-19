#!/bin/bash

for index in [1 .. 20]
do
  exec python3 Bidder.py &
done