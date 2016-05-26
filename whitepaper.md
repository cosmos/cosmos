# GnuClear: A New Architecture for Scalable Blockchain Decentralization

The combined success of the open-source ecosystem, of decentralized
file-sharing, and of public cryptocurrencies, has inspired an understanding that
decentralized internet protocols can be used to radically improve socio-economic
infrastructure.  We have seen specialized blockchain applications like Bitcoin
(a cryptocurrency), Namecoin (a name registry), ZCash (a cryptocurrency for
privacy); and also generalized smart contract platforms such as Ethereum, with
countless distributed applications for the EVM such as Augur (a prediction
market) and TheDAO (an investment club).

To date, however, all blockchains have suffered from a number of drawbacks,
including their gross energy inefficiency, poor or limited performance, and
immature governance mechanisms.  What is needed is an architecture for a network
of parallel blockchains that can work together in concert, while maintaining
certain invariances (such as the total amount of coins) across these "shards" in
a robust way.  Yet, existing blockchain consensus algorithms based on
proof-of-work have proven to be difficult (if not impossible) to scale in
parallel.  Existing scalability proposals such as payment channels allow for
atomic cross-chain transactions, but do not allow for the transfer of coins from
one chain to another.

We present GnuClear, a novel blockchain network architecture that addresses all
of these problems.  The main GnuClear hub blockchain (as well as connected
shards) are powered by Tendermint, which provides a high-performance,
consistent, secure consensus engine, where strict accountability guarantees hold
over the behaviour of malicious actors.  The GnuClear hub is a simple
multi-asset proof-of-stake cryptocurrency with a simple governance mechanism
enabling the network to adapt and upgrade.  The hub and shards of the GnuClear
network communicate with each other via an inter-blockchain communication (IBC)
protocol which is formalized here.  The GnuClear hub utilizes IBC packets to
move coins from one shard to another while maintaining the total amount of coins
in the network.

We hope that the GnuClear network can become inspiration for the future internet
of blockchains.

## Related Work ################################################################

There have been many innovations in blockchain consensus and scalability in the
past couple of years.  This section provides a brief survey of a select number
of important ones.

### Classic Byzantine Fault Tolerance

Consensus in the presence of malicious participants is a problem dating back to
the early 80s, when Leslie Lamport appropriated the phrase "Byzantine fault" to
refer to processes that might behave arbitrarily, in contrast to a "crash
fault", wherein a process simply crashes.  Early solutions were discovered for
synchronous networks, where there is an upper bound on message latency, though
they only found practical use in highly controlled environments (airplane
controllers and datacenters synchronized via atomic clock).  It was not until
the late 90s that Practical Byzantine Fault Tolerance (PBFT) was introduced as
an asynchronous consensus algorithm able to tolerate up to 1/3 of processes
behaving arbitrarily.  PBFT became the standard algorithm, spawning many
variations, including most recently by IBM as part of their contribution to
Hyperledger. PBFT's most prominent drawback is its lack of accountability - that
is, in the event that 1/3 of processes behave maliciously and cause the
consensus to fork, it may not be possible to determine who was responsible.
Additionally, it may be argued that the algorithm is, like Paxos before it,
difficult to understand and reason about; consequently, the associated software
ecosystem has been relatively undeveloped.

### BitShares delegated stake 

While not the first to deploy Proof-of-Stake (PoS), BitShares contributed
considerably to research and adoption of PoS blockchains, particularly those
known as "delegated" PoS.  In BitShares, stake holders elect "witnesses",
responsible for ordering and committing transactions, and "delegates",
responsible for co-ordinating software updates and parameter changes.  Though
BitShares achieves high performance (100k tx/s, 1s latency) in ideal conditions,
it is subject to double spend attacks by malicious witnesses which fork the
blockchain without suffering an explicit economic punishment - a problem
referred to as "nothing-at-stake".  BitShares attempts to mitigate the problem
somewhat by allowing transactions to reference block hashes. Additionally,
stakeholders can remove or replace misbehaving witnesses on a daily basis,
though this does nothing to explicitly punish a double-spend attack that was
successful.

### Stellar 

Building on an approach pioneered by Ripple, Stellar refined a model of
Federated Byzantine Agreement wherein the the processes participating in
consensus do not constitute a fixed and globally known set.  Rather, each
process curates a personal set of "quorum slices", each constituting a set of
processes it trusts. A set containing a slice from every process is known as a
quorum.  The security of the mechanism relies on the assumption that the
intersection of *any* two quorums is non-empty, while the availability of a
process requires at least one of its quorum slices to consist of entirely of
correct nodes, creating a trade-off between using large or small quorum-slices
that may be difficult to balance without imposing significant assumptions about
trust. The approach is similar to both the Border Gateway Protocol, used by
top-tier ISPs on the internet to establish global routing tables, and by that
used by browsers to manage TLS certificates - both notorious for their
insecurity.

### BigChainDB

Attempting to tilt the balance between security and performance in favor of
performance, BigChainDB is a modification of the successful RethinkDB
(a NoSQL datastore for JSON-documents with a query language),
to include additional security guarantees without sacrificing the ability to
perform over a million txs/s.  RethinkDB uses the Raft consensus algorithm, but
only to process low-frequency events, like changes to the validator set. Thus
the system is only eventually consistent, and does not provide Byzantine Fault
Tolerance.

### Lightning Network 

The lightning network is a proposed message relay network operating at a layer
above the Bitcoin blockchain, enabling many orders of magnitude improvement in
transaction throughput by moving the majority of transactions outside of the
consensus into so-called "payment channels". This is made possible by the
Bitcoin scripting language, which enables parties to enter into stateful
contracts where the state can be updated by sharing digital signatures and
contracts can be closed by publishing evidence back to the blockchain, a
mechanism first popularized by cross-chain atomic swaps.  By openning payment
channels with many parties, participants in the lightning network can become
focal points for routing the payments of others, leading to concerns about
centralization and censorship.

### BitcoinNG

BitcoinNG is a proposed improvement to Bitcoin that would allow for forms of
vertical scalability, such as increasing the block size, without the negative
economic consequences typically associated with such a change, such as the
disproportionately large impact on small miners.  This improvement is achieved
by separating leader election from transaction broadcast: leaders are first
elected by Proof-of-Work in "micro-blocks", and then able to broadcast
transactions to be committed until a new micro-block is found. This reduces the
bandwidth requirements necessary to win the PoW race, allowing small miners to
more fairly compete, and allowing transactions to be committed more regularly
by the last miner to find a micro-block.

### Segregated Witness 

Segregated Witness is a Bitcoin improvement proposal
[link](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki) that aims
to increase the per-block tranasction throughput 2X or 3X, while simultaneously
making block syncing faster for new nodes.  The brilliance of this solution is
in how it works within the limitations of Bitcoin's current protocol and allows
for a soft-fork upgrade (i.e. clients with older versions of the software will
continue to function after the upgrade).  Tendermint being a new protocol has no
design restrictions, so it has a different scaling priorities.  Primarily,
Tendermint uses a BFT round-robin algorithm based on cryptographic signatures
instead of mining, which trivially allows horizontal scaling through multiple
parallel blockchains, while regular, more frequent block commits allow for
vertical scaling as well.

### Sidechains

### Casper 

Casper is a proposed Proof-of-Stake consensus algorithm.  Its prime
mode of operation is "consensus-by-bet".  The idea is that by letting validators
iteratively bet on which block it believes will become committed into the
blockchain based on the other bets that it's seen so far, finality can be
achieved eventually.
[link](https://blog.ethereum.org/2015/12/28/understanding-serenity-part-2-casper/).
This is an active area of research by the Casper team.  The challenge is in
constructing a betting mechanism that can be proven to be an evolutionarily
stable strategy.  The main benefit of Casper as compared to Tendermint may be in
offering "availability over consistency" -- consensus does not require a +2/3
quorum from the validators -- perhaps at the cost of commit speed or
implementation complexity.

## Tendermint ##################################################################

In this section we describe the Tendermint consensus protocol and the interface
used to build applications with it.

### Consensus

A fault tolerant consensus protocol enables a set of non-faulty processes to
eventually agree on a value proposed by at least one of them.  The problem is
made more difficult by asynchronous network conditions, wherein messages may
have arbitrarily long delays, and by Byzantine faults, wherein processes may
exhibit arbitrary, possibly malicious, behaviour.  In particular, it is well
known that deterministic consensus in asynchronous networks is impossible
\cite{flp}, and that consensus protocols can tolerate strictly fewer Byzantine
faults than crash faults ($\frac{1/3}$ of processes, vs. $\frac{1/2}$). The
former results from the inability to distinguish crash failures from
asynchronous message delay. The latter from the fact that three processes are
not enough for a safe majority vote if one of them can lie (you need at least
four).

In addition to providing optimal fault tolerance, a well designed consensus
protocol should provide additional guarantees in the event that the tolerance
capacity is exceeded and the consensus fails.  This is especially necessary in
public economic systems, where Byzantine behaviour can have substantial
financial reward.  The most important such guarantee is a form of
\emph{accountability}, where the processes that caused the consensus to fail can
be identified and punished according to the rules of the protocol, or, possibly,
the legal system.  When the legal system is unreliable, validators can be forced
to make security deposits in order to participate, and those deposits can be
revoked when malicious behaviour is detected \cite{slasher}.

Tendermint is a Byzantine Fault Tolerant (BFT) consensus protocol for
asynchronous networks, notable for its simplicity, performance, and
accountability.  The protocol requires a fixed, known set of N validators, where
the ith validator is identified by its public key, V_i.  Consensus proceeds in
rounds. At each round the round-leader, or proposer, proposes a value to be
decided.  The validators then vote, in two stages, on whether or not to accept
the proposal or move to the next round. 

We call the voting stages PreVote and PreCommit. A vote can be for a particular
block or for Nil.  We call a collection of +⅔ PreVotes for a single block in the
same round a Polka, and a collection of +⅔ PreCommits for a single block in the
same round a Commit.  If +⅔ PreCommit for Nil in the same round, they move to
the next round. 

A PreCommit for a block must come with justification, in the form of a Polka for
that block, subject to a few constraints or Locking Rules, which ensure that the
network will eventually commit just one value. Any malicious attempt to cause
more than one value to be committed can be identified.

The proposer at round r is simply r mod N. Note that the strict determinism
incurs a weak synchrony assumption as faulty leaders must be detected and
skipped.  Thus, validators wait some amount TimeoutPropose before they Prevote
Nil.  Progression through the rest of the round is fully asychronous, in that
progress is only made once a validator hears from +⅔ of the network.  The full
details of the protocol are described in FIGURE.

Tendermint’s security derives simultaneously from its use of optimal Byzantine
Fault Tolerance and a locking mechanism.  The former ensures that ⅓ or more
validators must be Byzantine to cause a violation of safety, where more than two
values are committed.  The latter ensures that, if ever any set of validators
attempts, or even succeeds, in violating safety , they can be identified by the
protocol.  This includes both voting for conflicting blocks and broadcasting
unjustified votes.

TODO: Blockchain from Consensus

TODO: Light Clients.

Despite its strong guarantees, Tendermint provides exceptional performance.  In
benchmarks of 64 nodes distributed across 7 datacenters on 5 continents, on
commodity cloud instances, Tendermint consensus can process thousands of
transactions per second, with commit latencies on the order of one or two
seconds.  Notably, performance of well over a thousand transactions per second
is maintained even in harsh adversarial conditions, with validators crashing or
broadcasting maliciously crafted votes. See FIGURE for details.

### Forks and Censorship Attacks

Due to the definition of a block commit, any 1/3+ coalition of validators can
halt the blockchain by not broadcasting their votes. Such a coalition can also
censor particular transactions by rejecting blocks that include these
transactions, though this would result in a significant proportion of block
proposals to be rejected, which would slow down the rate of block commits of the
blockchain, reducing its utility and value. The malicious coalition might also
broadcast votes in a trickle so as to grind blockchain block commits to a near
halt, or engage in any combination of these attacks.

If a global active adversary were also involved, it can partition the network
in such a way that it may appear that the wrong subset of validators were
responsible for the slowdown. This is not just a limitation of Tendermint, but
rather a limitation of all consensus protocols whose network is potentially
controlled by an active adversary.

For both types of attacks, a subset of the validators through means external to
the blockchain should coordinate to sign a reorg-proposal that chooses a fork
(and any evidence thereof) and the initial subset of validators with their
signatures. Clients should verify the signatures on the reorg-proposal, verify
any evidence, and make a judgement or prompt the end-user for a decision.
For example, a phone wallet app may prompt the user with a security warning,
while a refrigerator may accept any reorg-proposal signed by +1/2 of the
original validators. If we further require that validators who sign such a
reorg-proposal forego its collateral on all other forks, light-clients can be
assured by up to 1/6 of the bonded collateral (1/6 == 2/3 - 1/2). Notice that no
Byzantine fault tolerant algorithm can come to consensus when 1/3+ of validators
are dishonest, yet a fork assumes that 1/3+ of validators have been dishonest by
double-signing or lock-changing without justification. So, signing the reorg-
proposal is a coordination problem that cannot be solved internally by any
protocol -- not even Tendermint. It must be provided externally.

Assuming that the external coordination medium and protocol is robust, it
follows that forks are less of a concern than censorship attacks.

### TMSP

* Specification
* Flexibility in language, upgradability, compatibility with
* existing stacks Tx Throughput, compare to IBM Chaincode

## The GnuClear Hub and Shards #################################################

Here we describe a novel model of decentralization and scalability.  GnuClear is
a network of many blockchains powered by Tendermint via TMSP.  While existing
proposals aim to create a "single blockchain" with total global transaction
ordering, GnuClear permits many blockchains to run concurrently with one another
via a sharding mechanism.

At the basis, a global hub blockchain manages many independent blockchain
shards.  A constant stream of recent block commits from shards posted on the hub
allows the hub to keep up with the state of each shard.  Likewise, each shard
keeps up with the state of the hub (but shards to not keep up with each other
except indirectly through the hub).  Packets of information are then
communicated from one chain to another by posting Merkle-proofs to the source's
recent block hash.  This mechanism is called inter-blockchain communication, or
IBC for short.

The GnuClear hub hosts a multi-asset cryptocurrency, where tokens can be held by
individual users or by shards themselves.  These tokens can be moved from one
shard to another in a special IBC packet called a "coin packet".  The hub is
responsible for preserving the global invariance of the total amount of each
token across the shards.

(Diagram of hub and shards)

Since the GnuClear hub acts as a central ledger of tokens for the whole system,
the security of the hub is of paramount importance.  While each shard may be a
Tendermint blockchain that is secured by as few as 4 (or even less if BFT
consensus is not needed), the hub must be secured by a globally decentralized
set of validators that can withstand the most severe attack scenarios, such as a
continental network partition or a nation-state sponsored attack.

(Link to section on economics)

The blockchain shards can themselves be hubs to form a multi-level hierarchical
network, but for the sake of clarity we will only describe the simple
configuration with one central hub and many shards.

## Inter-blockchain Communication (IBC) ########################################

Now we look at how these independent sovereign blockchains (the hub and shards)
communicate with each other.  Say that there are three blockchains, "Shard1",
"Shard2", and "Hub", and we wish for "Shard1" to produce a packet destined for
"Shard2" going through "Hub". For a packet to move from one blockchain to
another, a proof must be posted on the receiving chain that the sending chain
knows about a packet with the appropriate destination. For the receiving chain
to check the proof, it must keep up with the sender's block headers.  The
mechanism is similar to that used by sidechains, requiring two interacting
chains to "be aware" of one another.

The IBC protocol can therefore naturally be defined using two types of
transaction: an `IBCBlockCommitTx` transaction, which allows a blockchain to
notify another of its most recent block-hash, and an `IBCPacketProofTx`
transaction, which allows a sender blockchain to prove to a receiver blockchain
that a packet destined for the receiver was was included in a recent state of
the sender.  The proof depends on the receiver having received a recent
block-hash via an `IBCBlockCommitTx`.

By splitting the IBC mechanics into two separate transactions `IBCBlockCommitTx`
and `IBCPacketProofTx`, we allow the native fee market-mechanism of the
receiving chain to determine which packets get committed (i.e. acknowledged),
while allowing for complete freedom on the sending chain as to how many outbound
packets are allowed.

![Figure of Shard1, Shard2, and Hub IBC without acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_without_ack.png)

<CAPTION on a figure>
In the example above, in order to update the block-hash of "Shard1" on "Hub" (or
of "Hub" on "Shard2"), an `IBCBlockCommitTx` transaction must be posted on "Hub"
with the block-hash of "Shard1" (or on "Shard2" with the block-hash of "Hub").

### IBCBlockCommitTx transaction

An `IBCBlockCommitTx` transaction is composed of:
- `ChainID (string)`: The ID of the blockchain
- `BlockHash ([]byte)`: The block hash bytes, the Merkle root which includes the
  app-hash
- `BlockPartsHeader (PartSetHeader)`: The block part-set header bytes, only
  needed to verify vote signatures
- `BlockHeight (int)`: The height of the commit
- `BlockRound (int)`: The round of the commit
- `Commit ([]Vote)`: The +2/3 Tendermint `Precommit` votes that comprise a block
  commit
- `ValidatorsHash ([]byte)`: A Merkle-tree root hash of the new validator set
- `ValidatorsHashProof (SimpleProof)`: A SimpleTree Merkle-proof for proving the
  `ValidatorsHash` against the `BlockHash`
- `AppHash ([]byte)`: A IAVLTree Merkle-tree root hash of the application state
- `AppHashProof (SimpleProof)`: A SimpleTree Merkle-proof for proving the
  `AppHash` against the `BlockHash`

### IBCPacketTx transaction

An `IBCPacket` is composed of:
- `Header (IBCPacketHeader)`: The packet header
- `Payload ([]byte)`: The bytes of the packet payload. _Optional_
- `PayloadHash ([]byte)`: The hash for the bytes of the packet. _Optional_

Either one of `Payload` or `PayloadHash` must be present.  The hash of an
`IBCPacket` is a simple Merkle root of the two items, `Header` and `Payload`.
An `IBCPacket` without the full payload is called an _abbreviated packet_.

An `IBCPacketHeader` is composed of:
- `SrcChainID (string)`: The source blockchain ID
- `DstChainID (string)`: The destination blockchain ID
- `Number (int)`: A unique number for all packets
- `Status (enum)`: Can be one of `AckPending`, `AckSent`, `AckReceived`,
  `NoAck`, or `Timeout`
- `Type (string)`: The types are application-dependent.  GnuClear reserves the
  "coin" packet type
- `MaxHeight (int)`: If status is not `NoAckWanted` or `AckReceived` by this
  height, status becomes `Timeout`. _Optional_

An `IBCPacketTx` transaction is composed of:
- `FromChainID (string)`: The ID of the blockchain which is providing this
  packet; not necessarily the source
- `FromBlockHeight (int)`: The blockchain height in which the following packet
  is included (Merkle-ized) in the block hash of the source chain
- `Packet (IBCPacket)`: A packet of data, whose status may be one of
  `AckPending`, `AckSent`, `AckReceived`, `NoAck`, or `Timeout`
- `PacketProof (IAVLProof)`: A IAVLTree Merkle-proof for proving the packet's
  hash against the `AppHash` of the source chain at given height

The sequence for sending a packet from "Shard1" to "Shard2" through the "Hub" is
depicted in {Figure X}.  First, an `IBCPacketTx` proves to "Hub" that the packet
is included in the app-state of "Shard1".  Then, another `IBCPacketTx` proves to
"Shard2" that the packet is included in the app-state of "Hub".  During this
procedure, the `IBCPacket` fields are identical: the `SrcChainID` is always
"Shard1", and the `DstChainID` is always "Shard2".

The `PacketProof` must have the correct Merkle-proof path, as follows:
``` IBC/<SrcChainID>/<DstChainID>/<Number> ``` TODO: CLARIFY

When "Shard1" wants to send a packet to "Shard2" through "Hub", the `IBCPacket`
data are identical whether the packet is Merkle-ized on "Shard1", the "Hub", or
"Shard2".  The only mutable field is `Status` for tracking delivery, as shown
below.

### IBC Packet Delivery Acknowledgement

There are several reasons why a sender may want the acknowledgement of delivery
of a packet by the receiving chain.  For example, the sender may not know the
status of the destination chain, if it is expected to be faulty.  Or, the sender
may want to impose a timeout on the packet (with the `MaxHeight` packet field),
while any destination chain may suffer from a denial-of-service attack with a
sudden spike in the number of incoming packets.

In these cases, the sender can require delivery acknowledgement by setting the
intial packet status to `AckPending`.  Then, it is the receiving chain's
responsibility to confirm delivery by including an abbreviated`IBCPacket` in the
app Merkle hash.

![Figure of Shard1, Shard2, and Hub IBC with acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_with_ack.png)

First, an `IBCBlockCommit` and `IBCPacketTx` are posted on "Hub" that proves the
existence of an `IBCPacket` on "Shard1".  Say that `IBCPacketTx` has the
following value:
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

Next, an `IBCBlockCommit` and `IBCPacketTx` are posted on "Shard2" that proves
the existence of an `IBCPacket` on "Hub".  Say that `IBCPacketTx` has the
following value:
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

Next, "Shard2" must include in its app-hash an abbreviated packet that shows the
new status of `AckSent`.  An `IBCBlockCommit` and `IBCPacketTx` are posted back
on "Hub" that proves the existence of an abbreviated `IBCPacket` on "Shard2".
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

Finally, "Hub" must update the status of the packet from `AckPending` to
`AckReceived`.  Evidence of this new finalized status should go back to
"Shard2".  Say that `IBCPacketTx` has the following value:
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

Meanwhile, "Shard1" may optimistically assume successful delivery of a "coin"
packet unless evidence to the contrary is proven on "Hub".  In the example
above, if "Hub" had not received an `AckSent` status from "Shard2" by block 350,
it would have set the status automatically to `Timeout`.  This evidence of a
timeout can get posted back on "Shard1", and any coins can be returned.

![Figure of Shard1, Shard2, and Hub IBC with acknowledgement and timeout](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_with_ack_timeout.png)


## GnuClear Shard Use Cases ####################################################

### Pegging

### Network partition mitigation

A global hub with regional autonomous shards can practically mitigate problems
that arise from intermittent global network partitions.

### Distributed Exchange

### Ethereum Scaling

An open issue for Ethereum is how to solve the scaling problem.  Currently,
Ethereum nodes process every single transaction and also stores all the state.
[link](https://docs.google.com/presentation/d/1CjD0W4l4-CwHKUvfF5Vlps76fKLEC6pIwu1a_kC_YRQ/mobilepresent?slide=id.gd284b9333_0_28).
While the GnuClear hub and IBC packet mechanics does not allow for arbitrary
contract logic execution as does Ethereum per se, it can be used as a foundation
for generalized Ethereum scaling via sharding.  For example, asynchronous
contract calls that "send an action" and expect a response in return could be
implemented by a sequence of two IBC packets going in opposite directions.

### Application integration

e.g. to Ethereum, ZCash, or Bitcoin

## Issuance and Incentives #####################################################

### The Gnut Token

While the GnuClear hub is a multi-asset system, there is a native coin for
staking called _gnuts_.  Unlike Ethereum's ether or Bitcoin's bitcoins,
GnuClear's gnuts are meant for staking by validators.  To discourage the use of
gnuts as a store-of-wealth or means of exchange, gnuts that are not held in bond
decay with a half-life of 5 years (PARAM).  Gnut holders who do not wish to
validate, or cannot because they do not meet the bonding threshold (PARAM) can
delegate to any of the existing validators.  Gnut holders who delegate to
validators do not pay the decay penalty.

### Number of Validators

Unlike Bitcoin or other proof-of-work blockchains, a Tendermint blockchain gets
slower with more validators due to the increased communication complexity.
Fortunately, we can support enough validators to make for a robust globally
distributed blockchain with very fast blocktimes, and, as bandwidth, storage,
and parallel compute capacity increases, we will be able to support more
validators in the future.

On genesis day, the maximum number of validators will be set to 100, and this
number will increase at a rate of 13% for 10 years, and settle at 300
validators.
```
Year 0: 100
Year 1: 113
Year 2: 127
Year 3: 144
Year 4: 163
Year 5: 184
Year 6: 208
Year 7: 235
Year 8: 265
Year 9: 300
```

### Becoming a Validator

New validators can be added in a two-step process.

First, the would-be validator must post a bond-proposal and post a collateral
deposit.  The amount of gnuts posted as collateral is what determines the
validator's voting power.

Second, the rest of the validators must vote on this proposal.  If more than 1/2
of the gnu-holders vote yes, the proposal passes, and the candidate becomes a
validator at the specified block height.

Given the same amount of usage of the GnuClear network, the validators may not
have a natural inclination to allow more gnu holders to bond, because this
decreases the amount of fees earned by each validator.  Yet, the network might
become more profitable if there were more collateral at stake, as it allows for
more transaction velocity. In that case, it might be rational for validators to
allow a new gnu holder to bond, as long as it brings more stake to the table.
Thus, bond proposals can also include any number of non-gnu tokens as collateral.
These tokens join the blockchain's token reserve pool.

```
BondProposal
  BonderAddr   []byte
  Coins        // Gnuts and other coins
  StartHeight  int
```

### Penalties for Validators

There must be some penalty imposed on the validators for when they intentionally
or unintentionally deviate from the sanctioned protocol. Some evidence is
immediately admissible, such as a double-sign at the same height and round, or
a violation of "prevote-the-lock" (a violation of the Tendermint consensus
protocol).  Such evidence will result in the validator losing its good standing
and its bonded gnu tokens as well its proportionate share of tokens from the
reserve pool will get slashed.

Sometimes, validators will not be available, either due to regional network
disruptions, power failure, or other reasons.  If, at any point in the past
`ValidatorTimeoutWindow` blocks, a validator's commit vote is not included
in the blockchain more than `ValidatorTimeoutMaxAbsent` times, that
validator will become inactive, and lose 5% of its stake.  Its stake will remain
bonded for `UnbondingPeriod` blocks.

Some "malicious" behavior do not produce obviously discernable evidence on the
blockchain. In these cases, the validators can coordinate out of band to force
the timeout of a validator.

In the case of a halt of the GnuClear hub, a valid re-org (link) can be used to
inactivate any 1/3+ coalition of validators , e.g. for going offline and halting
the GnuClear hub.

### Transaction Fees

GnuClear validators can accept any token type or combination of types as a fee
for processing a transaction.  Each validator can subjectively set whatever
exchange rate it wants, and choose whatever transactions it wants, as long as
the `BlockGasLimit` is not exceeded.  The collected fees are redistributed to
the holders of bonded gnu tokens, proportionately, every `ValidatorPayoutPeriod`
blocks.

### Initial Distribution

The initial distribution of gnut coins and validators on Genesis day is ...

TODO

### Genesis Validator Vesting

Validators on genesis day will be incentivized to continue validating, by virtue
of a vesting schedule.  All of the initial bonded gnus of the validators on
genesis day will vest at a rate of 10% a year, per block.  Vesting gnuts can be
used to the full extent for voting, but disappears after unbonding.  It follows
that vesting gnuts cannot be transferred.

## Governance ##################################################################

### Coin Issuance

* Proposals manage inflation by sending new money to an account or shard
* PoW, Conference, Crowd Sales

### Validator Set Changes

### Software Upgrades

### Penalties for Absenteeism

## Roadmap #####################################################################

* Initial proposals for distribution (PoW, conferences)
* Shard discovery
* Tendermint V2
* Support fees paid for w/ other currenties

<hr/>

## Appendix ####################################################################

### Merkle tree & proof specification

* SimpleTree
* IAVLTree
* Proof Expression langauge
