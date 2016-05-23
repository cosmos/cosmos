# GnuClear: A New Architecture for Scalable Blockchain Decentralization

The combined success of the open-source ecosystem, of decentralized file-sharing, and of public cryptocurrencies,
has inspired an understanding that decentralized internet protocols can be used to radically improve socio-economic infrastructure.
We have seen specialized blockchain applications like Bitcoin (a cryptocurrency), Namecoin (a name registry), ZCash (a cryptocurrency for privacy);
and also generalized smart contract platforms such as Ethereum, with countless distributed applications for the EVM such as Augur (a prediction market) and TheDAO (an investment club).

To date, however, all blockchains have suffered from a number of drawbacks, including their gross energy inefficiency, poor or limited performance, and immature governance mechanisms.
What is needed is an architecture for a network of parallel blockchains that can work together in concert, while maintaining certain invariances (such as the total amount of coins)
across these "shards" in a robust way.  Yet, existing blockchain consensus algorithms based on proof-of-work have proven to be difficult (if not impossible) to scale in parallel.
Existing scalability proposals such as payment channels allow for atomic cross-chain transactions, but do not allow for the transfer of coins from one chain to another.

We present GnuClear, a novel blockchain network architecture that addresses all of these problems.
The main GnuClear hub blockchain (as well as connected shards) are powered by Tendermint, which provides a high-performance, safe, secure consensus engine,
where strict accountability guarantees hold over the behaviour of malicious actors.
The GnuClear hub is a simple multi-asset proof-of-stake cryptocurrency with a simple governance mechanism enabling the network to adapt and upgrade.
The hub and shards of the GnuClear network communicate with each other via an inter-blockchain communication (IBC) protocol which is formalized here.
The GnuClear hub utilizes IBC packets to move coins from one shard to another while maintaining the total amount of coins in the network.

We hope that the GnuClear network can become inspiration for the future internet of blockchains.


## Related Work

### BitShares delegated stake
### Stellar
### Lightning Network
### BitcoinNG
### Segregated Witness
### Casper
Casper is a proposed Proof-of-Stake consensus algorithm.  Its prime mode of operation is "consensus-by-bet".
The idea is that by letting validators iteratively bet on which block it believes will become committed into the blockchain based on the other bets that it's seen so far,
finality can be achieved eventually.
[link](https://blog.ethereum.org/2015/12/28/understanding-serenity-part-2-casper/).
This is an active area of research by the Casper team.
The challenge is in constructing a betting mechanism that can be proven to be an evolutionarily stable strategy.
The main benefit of Casper as compared to Tendermint may be in offering "availability over consistency" -- consensus does not require a +2/3 quorum from the validators --
perhaps at the cost of commit speed or implementation complexity.

## Tendermint

### Consensus
### TMSP


## The GnuClear model of scalable decentralization

Here we describe a novel model of decentralization and scalability.
GnuClear is a network of many blockchains powered by Tendermint via TMSP.
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


## GnuClear Inter-blockchain Communication (IBC)

Now we look at how these independent sovereign blockchains (the hub and shards) communicate with each other.
Say that there are three blockchains, "Shard1", "Shard2", and "Hub", and we wish for "Shard1" to produce a packet destined for "Shard2" going through "Hub".
There are two types of transactions that compose the IBC protocol.
There is the `IBCBlockCommitTx` transaction, and the `IBCPacketProofTx` transaction.

![Figure of Shard1, Shard2, and Hub IBC without acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_without_ack.png)

### IBCBlockCommitTx transaction

The `IBCBlockCommitTx` transaction is used to update the known recent block-hash of one blockchain on another blockchain.
In the example above, in order to update the block-hash of "Shard1" on "Hub" (or of "Hub" on "Shard2"), an `IBCBlockCommitTx` transaction
must be posted on "Hub" with the block-hash of "Shard1" (or on "Shard2" with the block-hash of "Hub").

An `IBCBlockCommitTx` transaction is composed of:
- `ChainID (string)`: The ID of the blockchain
- `BlockHash ([]byte)`: The block hash bytes, the Merkle root which includes the app-hash
- `BlockPartsHeader (PartSetHeader)`: The block part-set header bytes, only needed to verify vote signatures
- `BlockHeight (int)`: The height of the commit
- `BlockRound (int)`: The round of the commit
- `Commit ([]Vote)`: The +2/3 Tendermint `Precommit` votes that comprise a block commit
- `ValidatorsHash ([]byte)`: A Merkle-tree root hash of the new validator set
- `ValidatorsHashProof (SimpleProof)`: A SimpleTree Merkle-proof for proving the `ValidatorsHash` against the `BlockHash`
- `AppHash ([]byte)`: A IAVLTree Merkle-tree root hash of the application state
- `AppHashProof (SimpleProof)`: A SimpleTree Merkle-proof for proving the `AppHash` against the `BlockHash`

### IBCPacketTx transaction

An `IBCPacket` is composed of:
- `Header (IBCPacketHeader)`: The packet header
- `Payload ([]byte)`: The bytes of the packet payload. _Optional_
- `PayloadHash ([]byte)`: The hash for the bytes of the packet. _Optional_

Either one of `Payload` or `PayloadHash` must be present.
The hash of an `IBCPacket` is a simple Merkle root of the two items, `Header` and `Payload`.
An `IBCPacket` without the full payload is called an _abbreviated packet_.

An `IBCPacketHeader` is composed of:
- `SrcChainID (string)`: The source blockchain ID
- `DstChainID (string)`: The destination blockchain ID
- `Number (int)`: A unique number for all packets
- `Status (enum)`: Can be one of `AckPending`, `AckSent`, `AckReceived`, `NoAck`, or `Timeout`
- `Type (string)`: The types are application-dependent.  GnuClear reserves the "coin" packet type
- `MaxHeight (int)`: If status is not `NoAckWanted` or `AckReceived` by this height, status becomes `Timeout`. _Optional_

An `IBCPacketTx` transaction is composed of:
- `FromChainID (string)`: The ID of the blockchain which is providing this packet; not necessarily the source
- `FromBlockHeight (int)`: The blockchain height in which the following packet is included (Merkle-ized) in the block hash of the source chain
- `Packet (IBCPacket)`: A packet of data, whose status may be one of `AckPending`, `AckSent`, `AckReceived`, `NoAck`, or `Timeout`
- `PacketProof (IAVLProof)`: A IAVLTree Merkle-proof for proving the packet's hash against the `AppHash` of the source chain at given height

By splitting the IBC mechanics into two separate transactions `IBCBlockCommitTx` and `IBCPacketProofTx`,
we allow the native fee market-mechanism of the receiving chain to determine which packets get committed (i.e. acknowledged),
while allowing for complete freedom on the sending chain as to how many packets outbound packets are allowed.

The sequence for sending a packet from "Shard1" to "Shard2" through the "Hub" is depicted in {Figure X}.
First, an `IBCPacketTx` proves to "Hub" that the packet is included in the app-state of "Shard1".
Then, another `IBCPacketTx` proves to "Shard2" that the packet is included in the app-state of "Hub".
During this procedure, the `IBCPacket` fields are identical: the `SrcChainID` is always "Shard1", and the `DstChainID` is always "Shard2".

The `PacketProof` must have the correct Merkle-proof path, as follows:
```
IBC/<SrcChainID>/<DstChainID>/<Number>
```

When "Shard1" wants to send a packet to "Shard2" through "Hub",
the `IBCPacket` data are identical whether the packet is Merkle-ized on "Shard1", 
The only mutable field is `Status` for tracking delivery, as shown below.

### IBC Packet Delivery Acknowledgement

There are several reasons why a sender may want the acknowledgement of delivery of a packet by the receiving chain.
For example, the sender may not know the status of the destination chain, if it is expected to be faulty.
Or, the sender may want to impose a timeout on the packet (with the `MaxHeight` packet field),
while any destination chain may suffer from a denial-of-service attack with a sudden spike in the number of incoming packets.

In these cases, the sender can require delivery acknowledgement by setting the intial packet status to `AckPending`.
Then, it is the receiving chain's responsibility to confirm delivery by including an abbreviated`IBCPacket` in the app Merkle hash.

![Figure of Shard1, Shard2, and Hub IBC with acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_with_ack.png)

First, an `IBCBlockCommit` and `IBCPacketTx` are posted on "Hub" that proves the existence of an `IBCPacket` on "Shard1".
Say that `IBCPacketTx` has the following value:
- `FromChainID`: "Shard1"
- `FromBlockHeight`: 100 (say)
- `Packet`: an `IBCPacket`:
  - `Header`: an `IBCPacketHeader`:
    - `SrcChainID`: "Shard1"
    - `DstChainID`: "Shard2"
    - `Number`: 200 (say)
    - `Status`: `AckPending`
    - `Type`: "coin"
    - `MaxHeight`: 350 (say "Hub" is currently at height 300)
  - `Payload`: &lt;The bytes of a "coin" payload&gt;

Next, an `IBCBlockCommit` and `IBCPacketTx` are posted on "Shard2" that proves the existence of an `IBCPacket` on "Hub".
Say that `IBCPacketTx` has the following value:
- `FromChainID`: "Hub"
- `FromBlockHeight`: 300
- `Packet`: an `IBCPacket`:
  - `Header`: an `IBCPacketHeader`:
    - `SrcChainID`: "Shard1"
    - `DstChainID`: "Shard2"
    - `Number`: 200
    - `Status`: `AckPending`
    - `Type`: "coin"
    - `MaxHeight`: 350
  - `Payload`: &lt;The same bytes of a "coin" payload&gt;

Next, "Shard2" must include in its app-hash an abbreviated packet that shows the new status of `AckSent`.
An `IBCBlockCommit` and `IBCPacketTx` are posted back on "Hub" that proves the eexistence of an abbreviated `IBCPacket` on "Shard2".
Say that `IBCPacketTx` has the following value:
- `FromChainID`: "Shard2"
- `FromBlockHeight`: 400 (say)
- `Packet`: an `IBCPacket`:
  - `Header`: an `IBCPacketHeader`:
    - `SrcChainID`: "Shard1"
    - `DstChainID`: "Shard2"
    - `Number`: 200
    - `Status`: `AckSent`
    - `Type`: "coin"
    - `MaxHeight`: 350
  - `PayloadHash`: &lt;The hash bytes of the same "coin" payload&gt;

Finally, "Hub" must update the status of the packet from `AckPending` to `AckReceived`.
Evidence of this new finalized status should go back to "Shard2".
Say that `IBCPacketTx` has the following value:
- `FromChainID`: "Hub"
- `FromBlockHeight`: 301
- `Packet`: an `IBCPacket`:
  - `Header`: an `IBCPacketHeader`:
    - `SrcChainID`: "Shard1"
    - `DstChainID`: "Shard2"
    - `Number`: 200
    - `Status`: `AckReceived`
    - `Type`: "coin"
    - `MaxHeight`: 350
  - `PayloadHash`: &lt;The hash bytes of the same "coin" payload&gt;

Meanwhile, "Shard1" may optimistically assume successful delivery of a "coin" packet unless evidence to the contrary is proven on "Hub".
In the example above, if "Hub" had not received an `AckSent` status from "Shard2" by block 350, it would have set the status automatically to `Timeout`.
This evidence of a timeout can get posted back on "Shard1", and any coins can be returned.

![Figure of Shard1, Shard2, and Hub IBC with acknowledgement and timeout](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_with_ack_timeout.png)


## GnuClear Shard Use Cases

### Pegging

### Network partition mitigation
A global hub with regional autonomous shards can practically mitigate problems that arise from intermittent global network partitions.

### Distributed Exchange

### Ethereum Scaling
An open issue for Ethereum is how to solve the scaling problem.  Currently, Ethereum nodes process every single transaction and also stores all the state.
[link](https://docs.google.com/presentation/d/1CjD0W4l4-CwHKUvfF5Vlps76fKLEC6pIwu1a_kC_YRQ/mobilepresent?slide=id.gd284b9333_0_28).
While the GnuClear hub and IBC packet mechanics does not allow for arbitrary contract logic execution as does Ethereum per se,
it can be used as a foundation for generalized Ethereum scaling via sharding.
For example, asynchronous contract calls that "send an action" and expect a response in return could be implemented by a sequence of two IBC packets going in opposite directions.

### Application integration
e.g. to Ethereum, ZCash, or Bitcoin

## Economics

### Transaction Fees
### Initial Distribution
### Inflation Model


## Governance

### Coin Issuance
* Proposals manage inflation by sending new money to an account or shard
* PoW, Conference, Crowd Sales

### Validator Set Changes
### Software Upgrades

## Roadmap

### Initial proposals for distribution (PoW, conferences)
### Shard discovery
### Tendermint V2

<hr/>

## Appendix

### Merkle tree & proof specification

* SimpleTree
* IAVLTree
* Expression langauge
