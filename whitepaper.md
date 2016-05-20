# Segments (These need to be reorganized)

A Tendermint blockchain can be thought of as a virtual distributed computer.
If the voting power of the validators were equal, then there is no "center" among the validators.
So, if you take down say any 2 validators in a 7-validator network, the blockchain would continue to function.


However, except in special circiumstances, the validators are not be the only actors of a Tendermint blockchain.
There are also non-validating nodes, non-active validator-toke-holders, and various end-users to consider.

There have been several proposed solutions to this "economic decentralization" problem.
* Casper
* BitShares delegated stake
* Stellar

(Analysis of each)

# The GnuClear model of decentralized scalability

Here we describe a novel model of decentralization and scalability.
GnuClear is a network of many blockchains powered by Tendermint via BCGI.
While existing proposals aim to create a "single blockchain" with total global transaction ordering,
GnuClear permits many blockchains to run concurrently with one another via a sharding mechanism.
At the basis, a global hub blockchain manages many independent blockchain shards, allowing interoperability across them in the form of packet communication.
This mechanism is called inter-blockchain communication, or IBC for short.
The hub keeps an account of multiple registered tokens across the shards, and preserves the global invariance of the total amount of each token across the shards.
These tokens can be moved from one shard to another in a special IBC packet called a "coin packet".
The blockchain shards can themselves be hubs to form a multi-level hierarchical network,
but for the sake of clarity we will only describe the simple configuration with one central hub and many shards.

(Diagram of hub and shards)

Since the GnuClear hub acts as a central ledger of tokens for the whole system, the security of the hub is of paramount importance.
While each shard may be a Tendermint blockchain that is secured by as few as 4 (or even less if BFT consensus is not needed), the hub
must be secured by a globally decentralized set of validators that can withstand the most severe attack scenarios, such as a continental
network partition or a nation-state sponsored attack.

(Link to section on economics)

# GnuClear Inter-blockchain Communication (IBC)

Now we look at how these independent sovereign blockchains (the hub and shards) communicate with each other.
Say that there are two blockchains, `Shard1` and `Hub`, and we wish for `Shard1` to produce a packet for `Hub` to act upon.
There are two types of transactions that compose the IBC protocol.
There is the `IBCBlockCommit` transaction, and the `IBCPacketProof` transaction.

(Figure of Shard1 -&gt; Hub IBC message sequence)

## IBCBlockCommit transaction

The `IBCBlockCommit` transaction is used to update the known recent block-hash of one blockchain on another blockchain.
In the example above, in order to update the known recent block-hash of `Shard1` on `Hub`, an `IBCBlockCommit` transaction
must be posted on `Hub` with the most recent block-hash of `Shard1`.

An `IBCBlockCommit` transaction is composed of:
- `ChainID string`: The ID of the blockchain, in our case "Shard"
- `BlockHash []byte`: The block hash bytes, the Merkle root which includes the app-hash
- `BlockPartsHeader PartSetHeader`: The block part-set header bytes, only needed to verify vote signatures
- `BlockHeight int`: The height of the commit
- `BlockRound int`: The round of the commit
- `Commit []Vote`: The +2/3 Tendermint `Precommit` votes that comprise a blockc commit
- `ValidatorsHash []byte`: A Merkle-tree root hash of the new validator set
- `ValidatorsHashProof SimpleProof`: A SimpleTree Merkle-proof for proving the `ValidatorsHash` against the `BlockHash`
- `AppHash []byte`: A IAVLTree Merkle-tree root hash of the application state
- `AppHashProof SimpleProof`: A SimpleTree Merkle-proof for proving the `AppHash` against the `BlockHash`

An `IBCPacketProof` transaction is composed of:
- `ChainID string`: The source blockchain ID, in our case "Shard"
- `BlockHeight int`: The blockchain height in which the following packet is included (Merkle-ized) in the block hash
- `Packet IBCPacket`: A packet of data
- `PacketProof IAVLProof`: A IAVLTree Merkle-proof for proving the packet's hash against the corresponding `AppHash`

An `IBCPacket` is composed of:
- `Number int`: A unique number for all packets, in our case from `Shard1` to `Hub`
- `Status enum`: Can be of value `Pending`, `AckSent`, `AckReceived`, `NoAckWanted`, or `Timeout`
