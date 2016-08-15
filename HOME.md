# COSMOS
## a network of distributed ledgers

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_zone.png" height="100"/>

A Cosmos zone is a distributed ledger (blockchain).  Each zone can have
differing transaction logic and policies.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_zone_ibc.png" height="100"/>

We've developed a trick that allows zones to communicate with each other
directly.  It's based on classical BFT algorithms, like Tendermint.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_evm_sharding.png" height="240"/>

With this technique, we could make Ethereum scale by constructing a common
hub blockchain.  All inter-zone token movements go through the hub.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_evm_upgrading.png" height="60"/>

Upgrading the EVM would be seamless, with less risk of contentious
hard-forks.  Anyone could plug in a better smart contract system.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_dist_exchange.png" height="240"/>

We could import other blockchains and have a distributed exchange on its
own zone.  This could be strictly more secure than centralized exchanges.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_network.png" height="300"/>

The Cosmos hub isn't the center of the universe.  Any zone can be a hub.
