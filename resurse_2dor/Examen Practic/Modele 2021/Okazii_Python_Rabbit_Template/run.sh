#!/bin/bash

exec python3 PrepareAuction.py &
sleep 1;
exec python3 Auctioneer.py &
exec python3 MessageProcessor.py &
exec python3 BiddingProcessor.py &
sleep 1;
for index in [1 .. 100]
do
  exec python3 Bidder.py &
done