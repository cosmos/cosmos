# COSMOS
## a network of distributed ledgers

Cosmos is a project with an ambitious mission -- to create a network of
distributed ledgers that solve long-standing problems in the cryptocurrency and
blockchain space.

Cosmos is a network of independent parallel blockchains that are each powered by
classical BFT consensus algorithms like Tendermint
[1](http://github.com/tendermint/tendermint).  The first blockchain in this
network will be the Cosmos Hub.  The Cosomos Hub connects to many other
blockchains (or _zones_) via a novel inter-blockchain communication protocol.
The Cosmos Hub tracks numerous token types, and keeps record of the total
number of tokens in each connected zone.  Tokens can be transferred from one
zone to another, securely and quickly, without the need for a liquid exchange
between zones, because all inter-zone coin transfers go through the Cosmos Hub.

This architecture solves so many problems that the blockchain space faces today,
including application interoperability, scalability, and seamless upgradability.
For example, zones derived from Bitcoind, Go-Ethereum, CryptoNote, ZCash, or any
blockchain system can be plugged into the Cosmos Hub.  These zones allow Cosmos
to scale infinitely to meet global transaction demand.  And, zones are a great
fit for a distributed exchange, which will be supported as well.

Cosmos is not just a single distributed ledger, and the Cosmos Hub isn't a
walled garden or the center of its universe.  We are designing a protocol for an
open network of distributed legers that can serve as a new foundation for our
future financial systems, based on principles of cryptography, sound economics,
consensus theory, transparency, and accountability.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_zone.png" height="100"/>

A Cosmos zone is a distributed ledger, or blockchain.  Each zone can have
different transaction logic and economic/governance/security policies.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_zone_ibc.png" height="100"/>

We've developed a trick that allows zones to communicate with each other
directly.  It's based on classical BFT algorithms, like Tendermint.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_evm_sharding.png" height="240"/>

With this technique, we could make Ethereum scale by constructing a common
hub blockchain.  All inter-zone token movements would go through the hub.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_evm_upgrading.png" height="60"/>

Upgrading the EVM would be seamless, with less risk of contentious
hard-forks.  Anyone could plug in a better, upgraded smart contract system.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_dist_exchange.png" height="240"/>

We could import other blockchains and have a distributed exchange on its
own zone.  This could be strictly more secure than centralized exchanges.

<img src="https://raw.githubusercontent.com/cosmos/cosmos/master/images/ex_network.png" height="300"/>

The Cosmos hub isn't the center of the universe.  Any zone can be a hub.
