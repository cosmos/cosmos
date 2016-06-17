# Gnuclear
**A New Architecture for Scalable Blockchain Decentralization**

Jae Kwon jae@tendermint.com<br/>
Ethan Buchman ethan@tendermint.com

For discussions, check out the [gnuclear forum](http://forum.tendermint.com/c/gnuclear)
and also see the [issues](https://github.com/gnuclear/gnuclear-whitepaper/issues)

_NOTE: If you can read this on GitHub, then we're still actively developing this
document.  Please check regularly for updates!._

## Table of Contents ###########################################################

  * [Introduction](#introduction)
  * [Tendermint](#tendermint)
    * [Consensus](#consensus)
    * [Light Clients](#light-clients)
    * [Preventing Long Range Attacks](#preventing-long-range-attacks)
    * [Overcoming Forks and Censorship
    Attacks](#overcoming-forks-and-censorship-attacks)
    * [TMSP](#tmsp)
  * [The Gnuclear Reactor and Shards](#the-gnuclear-reactor-and-shards)
    * [The Gnuclear Reactor](#the-gnuclear-reactor)
    * [Gnuclear Shards](#gnuclear-shards)
  * [Inter-blockchain Communication (IBC)](#inter-blockchain-communication-ibc)
    * [IBC Packet Delivery
    Acknowledgement](#ibc-packet-delivery-acknowledgement)
  * [Transactions](#transactions)
    * [Transaction Types](#transaction-types)
      * [SendTx](#sendtx)
      * [BondTx](#bondtx)
      * [UnbondTx](#unbondtx)
      * [SlashTx](#slashtx)
      * [BurnQuarkTx](#burnquarktx)
      * [NewProposalTx](#newproposaltx)
      * [VoteTx](#votetx)
      * [IBCBlockCommitTx](#ibcblockcommittx)
      * [IBCPacketTx](#ibcpackettx)
    * [Transaction Gas and Fees](#transaction-gas-and-fees)
  * [Use Cases](#use-cases)
    * [Pegging to Other Cryptocurrencies](#pegging-to-other-cryptocurrencies)
    * [Ethereum Scaling](#ethereum-scaling)
    * [Multi-Application Integration](#multi-application-integration)
    * [Network Partition Mitigation](#network-partition-mitigation)
    * [Federated Name Resolution System](#federated-name-resolution-system)
  * [Issuance and Incentives](#issuance-and-incentives)
    * [The Quark Token](#the-quark-token)
    * [Limitations on the Number of
    Validators](#limitations-on-the-number-of-validators)
    * [Becoming a Validator After Genesis
    Day](#becoming-a-validator-after-genesis-day)
    * [Penalties for Validators](#penalties-for-validators)
    * [Transaction Fees](#transaction-fees)
  * [Governance](#governance)
    * [Parameter Change Proposal](#parameter-change-proposal)
    * [Text Proposal](#text-proposal)
  * [Roadmap](#roadmap)
  * [Related Work](#related-work)
    * [Consensus Systems](#consensus-systems)
      * [Classic Byzantine Fault Tolerance](#classic-byzantine-fault-tolerance)
      * [BitShares delegated stake](#bitshares-delegated-stake)
      * [Stellar](#stellar)
      * [BitcoinNG](#bitcoinng)
      * [Casper](#casper)
    * [Sharded Scaling](#sharded-scaling)
      * [Interledger Protocol](#interledger-protocol)
      * [Sidechains](#sidechains)
      * [Ethereum Scalability Efforts](#ethereum-scalability-efforts)
    * [General Scaling](#general-scaling)
      * [Lightning Network](#lightning-network)
      * [Segregated Witness](#segregated-witness)
  * [Appendix](#appendix)
    * [Gas Fees for Transactions](#gas-fees-for-transactions)
    * [TMSP specification](#tmsp-specification)
    * [Merkle tree &amp; proof
    specification](#merkle-tree--proof-specification)
  * [Acknowledgements](#acknowledgements)
  * [Citations](#citations)

## Introduction ################################################################

The combined success of the open-source ecosystem, of decentralized
file-sharing, and of public cryptocurrencies, has inspired an understanding that
decentralized internet protocols can be used to radically improve socio-economic
infrastructure.  We have seen specialized blockchain applications like Bitcoin
[\[1\]][1] (a cryptocurrency), Zerocash [\[2\]][2] (a cryptocurrency for
privacy), and generalized smart contract platforms such as Ethereum [\[3\]][3],
with countless distributed applications for the EVM such as Augur (a prediction
market) and TheDAO [\[4\]][4] (an investment club).

To date, however, these blockchains have suffered from a number of drawbacks,
including their gross energy inefficiency, poor or limited performance, and
immature governance mechanisms.  A number of proposals have been made to scale
Bitcoin's transaction throughput such as Segregated-Witness [\[5\]][5] and
BitcoinNG [\[6\]][6], but these are vertical scaling solutions that remain
limited by the capacity of a single physical machine, lest we sacrifice the
property of complete auditability.  The Lightning Network [\[7\]][7] can help
scale Bitcoin transaction volume by leaving some transactions off the ledger
completely and is well suited for micropayments and privacy preserving payment
rails, but may not be suitable for more generalized scaling needs.

An ideal solution would be one that allows multiple parallel blockchains to
interoperate while retaining their security properties, but this has proven
difficult, if not impossible, with proof-of-work. Merged-mining, for instance,
allows the work done to secure a parent chain to be re-used on a child chain,
but transactions still must be validated, in order, by each node, and a
merge-mined blockchain is vulnerable to attack if a majority of the hashing
power on the parent is not actively merge-mining the child.  An academic review
of [alternative blockchain network
architectures](http://vukolic.com/iNetSec_2015.pdf) is provided for additional
context, and we provide more summaries of some proposals and their drawbacks in
[Related Work](#related-work).

Here we present Gnuclear, a novel blockchain network architecture that addresses
all of these problems.  Gnuclear is a network of many independent blockchains,
called shards, that are connected by a central blockchain, called the reactor.
The reactor and shards are powered by Tendermint Core [\[8\]][8], which provides
a high-performance, consistent, secure
[PBFT-like](http://tendermint.com/blog/tendermint-vs-pbft/) consensus engine,
where strict fork-accountability guarantees hold over the behaviour of malicious
actors.  The Gnuclear reactor is a simple multi-asset proof-of-stake
cryptocurrency with a simple governance mechanism enabling the network to adapt
and upgrade.  The reactor and shards of the Gnuclear network communicate with
each other via an inter-blockchain communication (IBC) protocol which is
formalized here.  The Gnuclear reactor utilizes IBC packets to move tokens from
one shard to another while maintaining the total amount of tokens in the
network, thus isolating each shard from the failure of others.

We believe that Gnuclear proves that Tendermint BFT consensus is well suited for
scaling public proof-of-stake blockchains, and that it can compete with
proof-of-work in speed, security, and scalability.  Above all, we hope it grows
into a platform that works for everyone interested in distributed ledger
systems.

## Tendermint ##################################################################

In this section we describe the Tendermint consensus protocol and the interface
used to build applications with it.

### Consensus

_NOTE:  +⅔ means "more than ⅔", while ⅓+ means "⅓ or more"._

A fault-tolerant consensus protocol enables a set of non-faulty processes to
eventually agree on a value proposed by at least one of them.  The problem is
made more difficult by asynchronous network conditions, wherein messages may
have arbitrarily long delays, and by Byzantine faults, wherein processes may
exhibit arbitrary, possibly malicious, behaviour.  In particular, it is well
known that deterministic consensus in asynchronous networks is impossible with
any fail-stop faults [\[9\]][9], and that consensus protocols in non-synchronous
systems can tolerate strictly fewer Byzantine faults than crash faults (⅓ of
processes, vs. ½). The former results from the inability to distinguish crash
failures from asynchronous message delay. The latter from the fact that three
processes are not enough for a safe majority vote if one of them can lie (you
need at least four).

In addition to providing optimal fault tolerance, a well designed consensus
protocol should provide additional guarantees in the event that the tolerance
capacity is exceeded and the consensus fails.  This is especially necessary in
economic systems, where Byzantine behaviour can have substantial financial
reward.  The most important such guarantee is a form of _fork-accountability_,
where the processes that caused the consensus to fail (ie.  caused clients of
the protocol to accept different values - a fork) can be identified and punished
according to the rules of the protocol, or, possibly, the legal system.  When
the legal system is unreliable, validators can be forced to make security
deposits in order to participate, and those deposits can be revoked, or slashed,
when malicious behaviour is detected [\[10\]][10].

Note this is much unlike Bitcoin, where forking is a regular occurence due to
network asynchrony and the probabilistic nature of finding partial hash
collissions.  Since in many cases, a malicious fork is indistinguishable from a
fork due to asynchrony, Bitcoin can not reliably implement fork-accountability,
other than the implicit opportunity cost paid by miners for mining an orphaned
block.

Tendermint is a partially synchronous Byzantine fault-tolerant (BFT) consensus
protocol derived from the DLS consensus algorithm [\[20\]][20]. Tendermint is
notable for its simplicity, performance, and fork-accountability.  The protocol
requires a fixed, known set of <em>N</em> validators, where the <em>i</em>th
validator is identified by its public key.  Validators attempt to come to
consensus on one block at a time, where a block is a list of transactions.
Consensus on a block proceeds in rounds. Each round has a round-leader, or
proposer, who proposes a block. The validators then vote, in stages, on whether
or not to accept the proposed block or move on to the next round.

We call the voting stages _PreVote_ and _PreCommit_. A vote can be for a
particular block or for _Nil_.  We call a collection of +⅔ PreVotes for a single
block in the same round a _Polka_, and a collection of +⅔ PreCommits for a
single block in the same round a _Commit_.  If +⅔ PreCommit for Nil in the same
round, they move to the next round.

The proposer for a round is chosen deterministically from the ordered list of
validators.  Note that strict determinism in the protocol incurs a weak
synchrony assumption as faulty leaders must be detected and skipped.  Thus,
validators wait some amount _TimeoutPropose_ before they Prevote Nil, and the
value of TimeoutPropose increases with each round.  Progression through the rest
of a round is fully asychronous, in that progress is only made once a validator
hears from +⅔ of the network.  In practice, it would take an extremely strong
adversary to indefinetely thwart the weak synchrony assumption (causing the
consensus to fail to ever commit a block), and doing so can be made even more
difficult by using randomized values of TimeoutPropose on each validator.

An additional set of constraints, or Locking Rules, ensure that the network will
eventually commit just one value. Any malicious attempt to cause more than one
value to be committed can be identified.  First, a PreCommit for a block must
come with justification, in the form of a Polka for that block. If the validator
has already PreCommit a block at round <em>R_1</em>, we say they are _locked_ on
that block, and the Polka used to justify the new PreCommit at round
<em>R_2</em> must come in a round <em>R_polka</em> where <em>R_1 &lt; R_polka
&lt;= R_2</em>.  Second, validators must Propose and/or PreVote the block they
are locked on.  Together, these conditions ensure that a validator does not
PreCommit without sufficient evidence, and that validators which have already
PreCommit cannot contribute to evidence to PreCommit something else.  This
ensures both safety and liveness of the consensus algorithm.

The full details of the protocol are described
[here](https://github.com/tendermint/tendermint/wiki/Byzantine-Consensus-Algorithm).

Tendermint’s security derives from its use of optimal Byzantine fault-tolerance
via super-majority (+⅔) voting and the locking mechanism.  Together, they ensure
that:

* ⅓+ validators must be Byzantine to cause a violation of safety, where more
  than two values are committed.  
* if ever any set of validators succeeds in violating safety, or even attempts
  to do so, they can be identified by the protocol.  This includes both voting
for conflicting blocks and broadcasting unjustified votes.

Despite its strong guarantees, Tendermint provides exceptional performance.  In
benchmarks of 64 nodes distributed across 7 datacenters on 5 continents, on
commodity cloud instances, Tendermint consensus can process thousands of
transactions per second, with commit latencies on the order of one or two
seconds.  Notably, performance of well over a thousand transactions per second
is maintained even in harsh adversarial conditions, with validators crashing or
broadcasting maliciously crafted votes. See FIGURE (TODO) for details.

### Light Clients

A major benefit of Tendermint's consensus algorithm is simplified light client
security, especially as compared to proof-of-work, and to protocols like Bitcoin
which have no global state.  Instead of syncing a chain of block headers and
verifying the proof of work, light clients, who are assumed to know all public
keys in the validator set, need only verify the +⅔ PreCommits in the latest
block.  The need to sync all block headers is eliminated as the existence of an
alternative chain (a fork) means ⅓+ of validator deposits can be slashed.  Of
course, since slashing requires that _someone_ detects the fork, it would be
prudent for light clients, or at least those that are able, to sync headers,
perhaps more slowly, on a risk adjusted basis, where the explicit cost of a fork
can be easily calculated at ⅓+ of the bonded stake.  Additionally, light clients
must stay synced with changes to the validator set, in order to avoid certain
[long range attacks](#preventing-long-range-attacks).

In a spirit similar to Ethereum, Tendermint enables applications to embed a
global Merkle root hash in each block, allowing easily verifiable state queries
for things like account balances, the value stored in a contract, or the
existence of an unspent transaction output, depending on the nature of the
application.

### Preventing Long Range Attacks

Assuming a sufficiently resilient collection of broadcast networks and a static
validator set, any fork in the blockchain can be detected and the deposits of
the offending validators slashed.  This innovation, first suggested by Vitalik
Buterin in early 2014, solves the nothing-at-stake problem of other
proof-of-stake cryptocurrencies (see [Related Work](#related-work)). However,
since validator sets must be able to change, over a long range of time the
original validators may all become unbonded, and hence would be free to create a
new chain, from the genesis block, incurring no cost as they no longer have
deposits locked up.  This attack came to be known as the Long Range Attack (LRA)
in contrast to a Short Range Attack, where validators who are currently bonded
cause a fork and are hence punishable (assuming a fork-accountable BFT algorithm
like Tendermint consensus). Long Range Attacks are often thought to be a
critical blow to proof-of-stake.

Fortunately, the LRA can be mitigated as follows.  First, for a validator to
unbond, thereby recovering their deposit and no longer earning fees to
participate in the consensus, the deposit must be made unavailable for an amount
of time known as the "unbonding period", which may be on the order of weeks or
months.  Second, for a light client to be secure, the first time it connects to
the network it must verify a recent block-hash against a trusted source, or
preferably multiple of them.  This condition is sometimes referred to as "weak
subjectivity".  Finally, to remain secure, it must sync up with the latest
validator set at least as frequently as the length of the unbonding period. This
ensures that the light client knows about changes to the validator set before a
validator has its capital unbonded and thus no longer at stake, which would
allow it to deceive the client by carrying out a long range attack by creating
new blocks beginning back at a height where it was bonded (assuming it has
control of sufficiently many of the early private keys).

Note that overcoming the LRA in this way requires a practical tweak of the
original security model of proof-of-work. In PoW, it is assumed that a light
client can sync to the current height from the trusted genesis block at any time
simply by processing the proof-of-work in every block header.  To overcome the
LRA, however, we require that a light client come online with some regularity,
and that the first time they come online they must be particularly careful to
authenticate what they hear from the network against trusted sources. Of course,
this latter requirement is similar to that of Bitcoin, where the protocol and
software must also be obtained from a trusted source.

The above method for preventing LRA is well suited for validators and full nodes
of a Tendermint-powered blockchain because these nodes are meant to remain
connected to the network.  The method is also suitable for light clients that
can be expected to sync with the network frequently.  However, for light clients
that are not expected to have frequent access to the internet or the blockchain
network, yet another solution can be used to overcome the LRA.  Non-validator
token holders can post their tokens as collateral with a very long unbonding
period (e.g. much longer than the unbonding period for validators) and serve
light clients with a secondary method of attesting to the validity of current
and past block-hashes. While these tokens do not count toward the security of
the blockchain's consensus, they nevertheless can provide strong guarantees for
light clients.  If historical block-hash querying were supported in Ethereum,
anyone could bond their tokens in a specially designed smart contract and
provide attestation services for pay, effectively creating a market for
light-client LRA security.

### Overcoming Forks and Censorship Attacks

Due to the definition of a block commit, any ⅓+ coalition of validators can halt
the blockchain by not broadcasting their votes. Such a coalition can also censor
particular transactions by rejecting blocks that include these transactions,
though this would result in a significant proportion of block proposals to be
rejected, which would slow down the rate of block commits of the blockchain,
reducing its utility and value. The malicious coalition might also broadcast
votes in a trickle so as to grind blockchain block commits to a near halt, or
engage in any combination of these attacks.  Finally, it can cause the
blockchain to fork, by double-signing or violating the locking rules.

If a global active adversary were also involved, it can partition the network in
such a way that it may appear that the wrong subset of validators were
responsible for the slowdown. This is not just a limitation of Tendermint, but
rather a limitation of all consensus protocols whose network is potentially
controlled by an active adversary.

For these types of attacks, a subset of the validators through external means
should coordinate to sign a reorg-proposal that chooses a fork (and any evidence
thereof) and the initial subset of validators with their signatures. Validators
who sign such a reorg-proposal forego its collateral on all other forks.
Clients should verify the signatures on the reorg-proposal, verify any evidence,
and make a judgement or prompt the end-user for a decision.  For example, a
phone wallet app may prompt the user with a security warning, while a
refrigerator may accept any reorg-proposal signed by +½ of the original
validators.

No non-synchronous Byzantine fault-tolerant algorithm can come to consensus when
⅓+ of validators are dishonest, yet a fork assumes that ⅓+ of validators have
already been dishonest by double-signing or lock-changing without justification.
So, signing the reorg-proposal is a coordination problem that cannot be solved
by any non-synchronous protocol (i.e. automatically, and without making
assumptions about the reliability of the underlying network).  For now, we leave
the problem of reorg-proposal coordination to human coordination via internet
media.  Validators must take care to ensure that there are no significant
network partitions, to avoid situations where two conflicting reorg-proposals
are signed.

Assuming that the external coordination medium and protocol is robust, it
follows that forks are less of a concern than censorship attacks.

In addition to forks and censorship, which require ⅓+ Byzantine validators, a
coalition of +⅔ validators may commit arbitrary, invalid state.  This is
characteristic of any (BFT) consensus system. Unlike double-signing, which
creates forks with easily verifiable evidence, detecting committment of an
invalid state requires non-validating peers to verify whole blocks, which
implies that they keep a local copy of the state and execute each transaction,
computing the state root independently for themselves.  Once detected, the only
way to handle such a failure is via social consensus on alternative media.  For
instance, in situations where Bitcoin has failed, whether forking due to
software bugs (as in March 2013), or committing invalid state due to Byzantine
behavior of miners (as in the July 2016), the well connected community of
businesses, developers, miners, and other organizations established a social
consensus as to what manual actions were required by participants to heal the
network.  Furthermore, since validators of a Tendermint blockchain may be
expected to be identifiable, commitment of an invalid state may even be
punishable by law or some external jurisprudence, if desired.

### TMSP

The Tendermint consensus algorithm is implemented in a program called Tendermint
Core.  Tendermint Core is an application-agnostic "consensus engine" that can
turn any deterministic (blackbox) application into a distributedly replicated
blockchain.  As the Apache Web Server or Nginx connects to the Wordpress
application via CGI or FastCGI, Tendermint Core connects to blockchain
applications via the Tendermint Socket Protocol (TMSP) [\[17\]][17]. Thus, TMSP
allows for blockchain applications to be programmed in any language, not just
the programming language that the consensus engine is written in.  Additionally,
TMSP makes it possible to easily swap out the consensus layer of any existing
blockchain stack.

To draw an analogy, we will draw an analogy with a well-known cryptocurrency,
Bitcoin.  Bitcoin is a cryptocurrency blockchain where each node maintains a
fully audited Unspent Transaction Output (UTXO) database. If one wanted to
create a Bitcoin-like system on top of TMSP, Tendermint Core would be
responsible for

* Sharing blocks and transactions between nodes
* Establishing a canonical/immutable order of transactions (the blockchain)

Meanwhile, the TMSP application would be responsible for

* Maintaining the UTXO database
* Validating cryptographic signatures of transactions
* Preventing transactions from spending non-existent transactions
* Allowing clients to query the UTXO database.

Tendermint is able to decompose the blockchain design by offering a very simple
API between the application process and consensus process.

TMSP consists of 3 primary message types that get delivered from the core to the
application. The application replies with corresponding response messages.

The `AppendTx` message is the work horse of the application. Each transaction in
the blockchain is delivered with this message. The application needs to validate
each transactions received with the AppendTx message against the current state,
application protocol, and the cryptographic credentials of the transaction. A
validated transaction then needs to update the application state — by binding a
value into a key values store, or by updating the UTXO database.

The `CheckTx` message is similar to AppendTx, but it’s only for validating
transactions. Tendermint Core’s mempool first checks the validity of a
transaction with CheckTx, and only relays valid transactions to its peers.
Applications may check an incrementing nonce in the transaction and return an
error upon CheckTx if the nonce is old.

The `Commit` message is used to compute a cryptographic commitment to the
current application state, to be placed into the next block header. This has
some handy properties. Inconsistencies in updating that state will now appear as
blockchain forks which catches a whole class of programming errors. This also
simplifies the development of secure lightweight clients, as Merkle-hash proofs
can be verified by checking against the block-hash, and the block-hash is signed
by a quorum of validators.

Additional TMSP messages allow the application to keep track of and change the
validator set, and for the application to receive the block information, such as
the height and the commit votes.  The full TMSP specification can be found
[here](https://github.com/tendermint/tmsp#message-types).

## The Gnuclear Reactor and Shards #############################################

Here we describe a novel model of decentralization and scalability.  Gnuclear is
a network of many blockchains powered by Tendermint via TMSP.  While existing
proposals aim to create a "single blockchain" with total global transaction
ordering, Gnuclear permits many blockchains to run concurrently with one another
via a sharding mechanism.

At the basis, a global reactor blockchain (the Gnuclear reactor) manages many
independent blockchain shards.  A constant stream of recent block commits from
shards posted on the reactor allows the reactor to keep up with the state of
each shard.  Likewise, each shard keeps up with the state of the reactor (but
shards do not keep up with each other except indirectly through the reactor).
Packets of information are then communicated from one chain to another by
posting Merkle-proofs that collide with a recent block-hash from the source.
This mechanism is called inter-blockchain communication, or IBC for short.

![Figure of reactor and shards
acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/images/hub_and_shards.png)

Any of the shards can themselves be reactors to form a multi-level hierarchical
network, but for the sake of clarity we will only describe the simple
configuration with one central reactor and many shards.

### The Gnuclear Reactor

The Gnuclear reactor is a blockchain that hosts a multi-asset cryptocurrency,
where tokens can be held by individual users or by shards themselves.  These
tokens can be moved from one shard to another in a special IBC packet called a
"coin packet".  The reactor is responsible for preserving the global invariance
of the total amount of each token across the shards. IBC coin packet
transactions must be committed by the sender, reactor and reciever blockchains.

Since the Gnuclear reactor acts as a central ledger of tokens for the whole
system, the security of the reactor is of paramount importance.  While each
shard may be a Tendermint blockchain that is secured by as few as 4 (or even
less if BFT consensus is not needed), the reactor must be secured by a globally
decentralized set of validators that can withstand the most severe attack
scenarios, such as a continental network partition or a nation-state sponsored
attack.

### Gnuclear Shards

A Gnuclear shard is an independent blockchain that exchanges IBC messages with
the Reactor.  From the Reactor's perspective, a shard is a multi-asset account
that can send and receive tokens using IBC packets. Like a cryptocurrency
account, a shard cannot transfer more tokens than it has, but can receive tokens
from others who have them. In certain cases, a shard may be granted special
priveleges to act as a "source" of some token, where, in addition to the shard's
balance in that token, it can send up to some maximum rate of additional tokens
out to other accounts or shards, thereby inflating that token's supply. Such
packets are similar to the "coin" packet, but have type "issue". Packets of type
"issue" for a particular token may originate from only one shard - that is,
there may be only one priveleged shard per token type.  On Genesis day, a select
number of priveleged shards will be created to act as pegs to other
cryptocurrencies. The creation of new priviledged shards is left to governance.

Note that a shard where +⅔ of the validators are Byzantine can commit invalid
state.  Since the very purpose of the Gnuclear reactor is to avoid verifying
every transaction on a shard, detecting such failures must be done by
independent observers of the shard, which may appeal to social media and to the
market to make their detection known (for instance, selling/shorting a token
that is being artificially inflated by a Byzantine source-shard, and writing a
blog post about the attack).  Additionally, if the validator set of the shard is
not the same as that of the reactor, and shard validators have stake bonded on
the reactor, an explicit alert mechanism may be used on the reactor to challenge
the validity of a block and to slash the deposits of offending validators.

## Inter-blockchain Communication (IBC) ########################################

Now we look at how the reactor and shards communicate with each other.  Say that
there are three blockchains, "Shard1", "Shard2", and "Reactor", and we wish for
"Shard1" to produce a packet destined for "Shard2" going through "Reactor". For
a packet to move from one blockchain to another, a proof must be posted on the
receiving chain that the sending chain knows about a packet with the appropriate
destination. For the receiving chain to check the proof, it must keep up with
the sender's block headers.  The mechanism is similar to that used by
sidechains, requiring two interacting chains to "be aware" of one another.

The IBC protocol can therefore naturally be defined using two types of
transaction: an `IBCBlockCommitTx` transaction, which allows a blockchain to
notify another of its most recent block-hash, and an `IBCPacketTx` transaction,
which allows a sender blockchain to prove to a receiver blockchain that a packet
destined for the receiver was was included in a recent state of the sender.  The
proof depends on the receiver having received a recent block-hash via an
`IBCBlockCommitTx`.

By splitting the IBC mechanics into two separate transactions `IBCBlockCommitTx`
and `IBCPacketTx`, we allow the native fee market-mechanism of the receiving
chain to determine which packets get committed (i.e. acknowledged), while
allowing for complete freedom on the sending chain as to how many outbound
packets are allowed.

![Figure of Shard1, Shard2, and Reactor IBC without
acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_without_ack.png)

<CAPTION on a figure> In the example above, in order to update the block-hash of
"Shard1" on "Reactor" (or of "Reactor" on "Shard2"), an `IBCBlockCommitTx`
transaction must be posted on "Reactor" with the block-hash of "Shard1" (or on
"Shard2" with the block-hash of "Reactor").

_See [IBCBlockCommitTx](#ibcblockcommittx) and [IBCPacketTx](#ibcpacketcommit)
for for more information on the two IBC transaction types._

### IBC Packet Delivery Acknowledgement

There are several reasons why a sender may want the acknowledgement of delivery
of a packet by the receiving chain.  For example, the sender may not know the
status of the destination chain, if it is expected to be faulty.  Or, the sender
may want to impose a timeout on the packet (with the `MaxHeight` packet field),
while any destination chain may suffer from a denial-of-service attack with a
sudden spike in the number of incoming packets.

In these cases, the sender can require delivery acknowledgement by setting the
initial packet status to `AckPending`.  Then, it is the receiving chain's
responsibility to confirm delivery by including an abbreviated`IBCPacket` in the
app Merkle hash.

![Figure of Shard1, Shard2, and Reactor IBC with
acknowledgement](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_with_ack.png)

First, an `IBCBlockCommit` and `IBCPacketTx` are posted on "Reactor" that proves
the existence of an `IBCPacket` on "Shard1".  Say that `IBCPacketTx` has the
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
    - `MaxHeight`: 350 (say "Reactor" is currently at height 300)
  - `Payload`: &lt;The bytes of a "coin" payload&gt;

Next, an `IBCBlockCommit` and `IBCPacketTx` are posted on "Shard2" that proves
the existence of an `IBCPacket` on "Reactor".  Say that `IBCPacketTx` has the
following value:

- `FromChainID`: "Reactor"
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
on "Reactor" that proves the existence of an abbreviated `IBCPacket` on
"Shard2".  Say that `IBCPacketTx` has the following value:

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

Finally, "Reactor" must update the status of the packet from `AckPending` to
`AckReceived`.  Evidence of this new finalized status should go back to
"Shard2".  Say that `IBCPacketTx` has the following value:

- `FromChainID`: "Reactor"
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
packet unless evidence to the contrary is proven on "Reactor".  In the example
above, if "Reactor" had not received an `AckSent` status from "Shard2" by block
350, it would have set the status automatically to `Timeout`.  This evidence of
a timeout can get posted back on "Shard1", and any tokens can be returned.

![Figure of Shard1, Shard2, and Reactor IBC with acknowledgement and
timeout](https://raw.githubusercontent.com/gnuclear/gnuclear-whitepaper/master/msc/ibc_with_ack_timeout.png)

## Transactions ################################################################

In the canonical implementation, transactions are streamed to the Gnuclear
reactor application via the TMSP interface.

### Transaction Types

#### SendTx

#### BondTx

#### UnbondTx

#### SlashTx

#### BurnQuarkTx

#### NewProposalTx

#### VoteTx

#### IBCBlockCommitTx

An `IBCBlockCommitTx` transaction is composed of:

- `ChainID (string)`: The ID of the blockchain
- `BlockHash ([]byte)`: The block-hash bytes, the Merkle root which includes the
  app-hash
- `BlockPartsHeader (PartSetHeader)`: The block part-set header bytes, only
  needed to verify vote signatures
- `BlockHeight (int)`: The height of the commit
- `BlockRound (int)`: The round of the commit
- `Commit ([]Vote)`: The +⅔ Tendermint `Precommit` votes that comprise a block
  commit
- `ValidatorsHash ([]byte)`: A Merkle-tree root hash of the new validator set
- `ValidatorsHashProof (SimpleProof)`: A SimpleTree Merkle-proof for proving the
  `ValidatorsHash` against the `BlockHash`
- `AppHash ([]byte)`: A IAVLTree Merkle-tree root hash of the application state
- `AppHashProof (SimpleProof)`: A SimpleTree Merkle-proof for proving the
  `AppHash` against the `BlockHash`

#### IBCPacketTx

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
- `Type (string)`: The types are application-dependent.  Gnuclear reserves the
  "coin" packet type
- `MaxHeight (int)`: If status is not `NoAckWanted` or `AckReceived` by this
  height, status becomes `Timeout`. _Optional_

An `IBCPacketTx` transaction is composed of:

- `FromChainID (string)`: The ID of the blockchain which is providing this
  packet; not necessarily the source
- `FromBlockHeight (int)`: The blockchain height in which the following packet
  is included (Merkle-ized) in the block-hash of the source chain
- `Packet (IBCPacket)`: A packet of data, whose status may be one of
  `AckPending`, `AckSent`, `AckReceived`, `NoAck`, or `Timeout`
- `PacketProof (IAVLProof)`: A IAVLTree Merkle-proof for proving the packet's
  hash against the `AppHash` of the source chain at given height

The sequence for sending a packet from "Shard1" to "Shard2" through the
"Reactor" is depicted in {Figure X}.  First, an `IBCPacketTx` proves to
"Reactor" that the packet is included in the app-state of "Shard1".  Then,
another `IBCPacketTx` proves to "Shard2" that the packet is included in the
app-state of "Reactor".  During this procedure, the `IBCPacket` fields are
identical: the `SrcChainID` is always "Shard1", and the `DstChainID` is always
"Shard2".

The `PacketProof` must have the correct Merkle-proof path, as follows:

```
IBC/<SrcChainID>/<DstChainID>/<Number>

```
TODO: CLARIFY

When "Shard1" wants to send a packet to "Shard2" through "Reactor", the
`IBCPacket` data are identical whether the packet is Merkle-ized on "Shard1",
the "Reactor", or "Shard2".  The only mutable field is `Status` for tracking
delivery, as shown below.


### Transaction Gas and Fees

## Use Cases ###################################################################

### Pegging to Other Cryptocurrencies

A priveleged shard can act as the source of a pegged token of another
cryptocurrency. A peg is in essence similar to the relationship between a
Gnuclear reactor and shard; both must keep up with the latest blocks of the
other in order to verify proofs that tokens have moved from one to the other.  A
peg-shard on the Gnuclear network keeps up with both the reactor as well as the
other cryptocurrency.  The indirection through the peg-shard allows the logic of
the reactor to remain simple by encapsulating any non-Tendermint consensus
light-client verification logic onto the shard.

For instance, a Gnuclear shard with some validator set, possibly the same as
that of the reactor, could act as an ether-peg, where the TMSP-application on
the shard (the "peg-shard") has mechanisms to exchange IBC messages with a
peg-contract on the external Ethereum blockchain (the "target").  This contract
would allow ether holders to send ether to the peg-shard by sending it to the
peg-contract on Ethereum.  Once ether is received by the peg-contract, the ether
cannot be withdrawn unless an appropriate IBC packet is received by the
peg-contract from the peg-shard. When a peg-shard receives an IBC packet proving
that ether was received in the peg-contract for a particular Ethereum account, a
corresponding account is created on the peg-shard with that balance.  Ether on
the peg-shard ("pegged-ether") can then be transferred to and from the reactor,
and later be destroyed with a transaction that sends it to a particular
withdrawal address on Ethereum; an IBC packet proving that the transaction
occured on the peg-shard can be posted to the Ethereum peg-contract to allow the
ether to be withdrawn.

Of course, the risk of such a pegging contract is a rogue validator set.  ⅓+
Byzantine validators could cause a fork, withdrawing ether from the peg-contract
on Ethereum while keeping the pegged-ether on the peg-shard. Worse, +⅔ Byzantine
validators can steal ether outright from those who sent it to the peg-contract
by deviating from the original pegging logic of the peg-shard.

It is possible to address these issues by designing the peg to be "totally
accountable".  For example, all IBC packets both from the reactor as well as
from the target might require acknowledgement by the peg-shard in such a way
that all state transitions of the peg-shard can be efficiently challenged and
verified by either the reactor or the target.  The reactor and the target (or in
the case of Ethereum, the peg-contract) should allow the peg-shard validators to
post collateral, and token transfers out of the peg-contract should be delayed
(and collateral unbonding period sufficiently long) to allow for any challenges
to be made.  We leave the design of the specification and implementation of this
system open as a future Gnuclear improvement proposal.

While the socio-political atmosphere is not quite evolved enough yet, we can
extend the mechanism to allow for shards which peg to the fiat currency of a
nation states by forming a validator set out of some combination of institutions
responsible for the nation's currency, most particularly, its banks. Of course,
extra precautions must be made to only accept currencies backed by strong legal
systems that can enforce auditability of the banks' activities by a sufficiently
large group of trusted notaries and institutions.

A result of this integration would be, for instance, the ability of anyone with
a bank account at a participating bank to move dollars from their bank account,
which is on the shard, to other accounts on the shard, or to the reactor, or to
another shard entirely.  In this regard, Gnuclear can act as a seamless conduit
between fiat currencies and cryptocurrencies.

### Ethereum Scaling

An open issue for Ethereum is how to solve the scaling problem.  Currently,
Ethereum nodes process every single transaction and also stores all the state.
[link](https://docs.google.com/presentation/d/1CjD0W4l4-CwHKUvfF5Vlps76fKLEC6pIwu1a_kC_YRQ/mobilepresent?slide=id.gd284b9333_0_28).

Since Tendermint can commit blocks much faster than Ethereum's proof-of-work,
EVM shards powered by Tendermint consensus and operating on pegged-ether can
provide higher performance to Ethereum blockchains.  Additionally, though the
Gnuclear reactor and IBC packet mechanics does not allow for arbitrary contract
logic execution per se, it can be used to co-ordinate Ethereum contracts running
on different shards, providing a foundation for generalized Ethereum scaling via
sharding.  For example, asynchronous contract calls that "send an action" and
expect a response in return could be implemented by a sequence of two IBC
packets going in opposite directions.

### Multi-Application Integration

Gnuclear shards run arbitrary application logic, defined at the beginning of the
shard's life, and potentially updated over time by governance. Such flexibility
allows Gnuclear shards to act as pegs to other cryptocurrencies, like Ethereum
or Bitcoin, but it also permits derlivatives of those blockchains, utilizing the
same codebase but a different validator set and history. This allows many
existing cryptocurrency frameworks, such as that of Ethereum, Zerocash, Bitcoin,
CryptoNote, and so on to be used with a higher performance consensus engine on a
common network, openning tremendous opportunity for interoperability across
platforms.  Furthermore, as a multi-asset blockchain, a single transaction may
contain multiple inputs and outputs, where each input can be any token type,
enabling Gnuclear to serve directly as a platform for decentralized exchange,
though orders are assumed to be matched via other platforms. Alternatively, a
shard can serve as a fault-tolerant exchange, including hosting the orderbook,
openning up new business opportunities for blockchain backed exchanges, which
may themselves trade liquidity over the Gnuclear network.

Shards can also serve as blockchain-backed versions of enterprise and government
systems, where pieces of a particular service, traditionally run by an
organization or group of organizations, are instead run as a TMSP application on
a certain shard, allowing it to inherit the security and interoperability of the
public Gnuclear network, without sacrificing control over the underlying
service.  Thus, Gnuclear may be a best of both worlds for organizations looking
to utilize blockchain technology that are wary of relinquishing control to an
unidentified set of miners.

### Network Partition Mitigation

A major problem with consistency favouring consensus algorithms like Tendermint
is thought to be that any network partition which causes there to be no single
partition with +⅔ validators will halt consensus altogether. The Gnuclear
architecture can mitigate this problem by using a global reactor with regional
autonomous shards, where +⅔ validators in a shard are based in a common
geographic region. For instance, a common paradigm may be for individual cities,
or regions, to operate a given shard for the coordination of finances and
infrastructure, enabling municipal activity to persist in the event that
otherwise remote service providers fail.  Note that this allows real geological,
political, and network-topological features to be considered in designing robust
federated fault-tolerant systems.

### Federated Name Resolution System

NameCoin was one of the first blockchains to attempt to solve the
name-resolution problem by adapting the Bitcoin blockchain.  Unfortunately there
have been several issues with this approach.

With Namecoin, we can verify that say, <em>@satoshi</em> was registered with a
particular public key at some point in the past, but we wouldn’t know whether
the public key had since been updated recently unless we download all the blocks
since the last update of that name.  This is due to the limitation of Bitcoin's
UTXO transaction Merkle-ization model where only the transactions (but not
mutable application state) is Merkle-ized into the block-hash -- which lets us
prove existence, but not the non-existence of updates.  Thus, we can't know for
certain the most recent value of a name without trusting a full node, or
incurring significant costs in bandwidth.

Even if a Merkle-ized search tree were implemented in NameCoin, its dependency
on proof-of-work makes light client verification problematic. Light clients must
download a complete copy of the headers for all blocks in the entire blockchain
(or at least all the headers since the last update to a name).  This means that
the bandwidth requirements scale linearly with the amount of time [\[21\]][21].

With Tendermint, all we need is the most recent block-hash signed by a quorum of
validators, and a Merkle proof to the current value associated with the name.
This makes it possible to have an efficient and secure light-client verification
of _the current value of_ a name.

On Gnuclear, we can take this concept and extend it further. Each
name-registration shard in Gnuclear can have an associated top-level-domain
(TLD) name such as ".com" or ".org", and each name-registration shard can have
its own governance and registration rules.

TODO: note on integration with shard discovery, see roadmap

## Issuance and Incentives #####################################################

### The Quark Token

While the Gnuclear reactor is a multi-asset system, there is a native token
called _quarks_.  Quarks are the only staking token of Gnuclear.  Quarks are a
license for the holder to vote, validate, or delegate to other validators.  Like
Ethereum's ether, quarks are also used to pay for transaction fees to mitigate
spam.  Additional quarks are issued to validators and those who delegate to
validators.

The initial distribution of quark tokens and validators on Genesis will go to
the funders of the Gnuclear crowdsale (80%), and the Gnuclear foundation (20%).
From genesis onward, 30% of the initial quark distribution will be rewarded to
active validators and delegators.

The `BurnQuarkTx` transaction can be used to recover any proportionate amount of
tokens from the reserve pool.

#### Crowdfund

16,000,000 quarks will be sold in an Ethereum-style crowdsale. The crowdsale
will last 42 days, in which the first 14 days will have the best price, and the
purchasing power will decrease linearly to 2/3 of the initial purchasing power
in the following 28 days.  The price will be determined by dividing 16,000,000
by the total effective purchasing power of all the bids.

#### Gnuclear Foundation

The Gnuclear foundation is an external entity that is hired to develop the
Gnuclear network.  Quark holders can vote to change the foundation by changing
the `GnuclearFoundationAddress` parameter.  This foundation will have 4,000,000
quarks, of which 1,200,000 are pre-vested, and the rest will vest over a period
of 4 years, all of which can be used to the full extent for voting.

#### Gnuclear Reactor Block Reward

Every block rewards all the active validators and delegators in proportion to
their bonded quarks (before commissions).  There will be roughly 6,000,000
quarks rewarded every year, forever.  The number is not exact, because the
number of blocks per year is not exact.  As with transaction fees, delegators
pay the delegated validator a commission of 10%.

#### Incentivizing Hackers

TODO: Note about automatic bounties for hackers, to incentivize hackers to
publish evidence (like capture-the-flag) that rewards some of the validator's
quarks to the hacker, and burns some as well.

### Limitations on the Number of Validators

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
Year 10: 300
...
```

### Becoming a Validator After Genesis Day

Quark holders who are not already validators can become one by signing and
submitting a `BondTx` transaction.  The amount of quarks provided as collateral
must be nonzero.  Anyone can become a validator at any time, except when the
size of the current validator set is greater than the maximum number of
validators allowed.  In that case, the transaction is only valid if the amount
of quarks is greater than the amount of effective quarks held by the smallest
validator, where effective quarks include vesting and delegated quarks.  When a
new validator replaces an existing validator in such a way, the existing
validator becomes inactive and all the quarks and delegated quarks enter the
unbonding state.  Note that, given the distribution of genesis-validators, the
33 available validator spots, and the issuance schedule, it is impossible for
any genesis-validators to become unbonded by this mechanism.

### Penalties for Validators

There must be some penalty imposed on the validators for when they intentionally
or unintentionally deviate from the sanctioned protocol. Some evidence is
immediately admissible, such as a double-sign at the same height and round, or a
violation of "prevote-the-lock" (a violation of the Tendermint consensus
protocol).  Such evidence will result in the validator losing its good standing
and its bonded gnu tokens as well its proportionate share of tokens in the
reserve pool -- collectively called its "stake" -- will get slashed.

Sometimes, validators will not be available, either due to regional network
disruptions, power failure, or other reasons.  If, at any point in the past
`ValidatorTimeoutWindow` blocks, a validator's commit vote is not included in
the blockchain more than `ValidatorTimeoutMaxAbsent` times, that validator will
become inactive, and lose `ValidatorTimeoutPenalty` (DEFAULT 1%) of its stake.

Some "malicious" behavior do not produce obviously discernable evidence on the
blockchain. In these cases, the validators can coordinate out of band to force
the timeout of these malicious validators, if there is a supermajority
consensus.

In situations where the Gnuclear reactor halts due to a ⅓+ coalition of
validators going offline, or in situations where a ⅓+ coalition of validators
censor evidence of malicious behavior from entering the blockchain, as long as
there are -½ such Byzantine validators, the reactor will recover with a
reorg-proposal.  (Link to "Forks and Censorship Attacks").

### Transaction Fees

Gnuclear validators can accept any token type or combination of types as a fee
for processing a transaction.  Each validator can subjectively set whatever
exchange rate it wants, and choose whatever transactions it wants, as long as
the `BlockGasLimit` is not exceeded.  The collected fees minus any taxes
specified below are redistributed to the holders of bonded gnu tokens,
proportionately, every `ValidatorPayoutPeriod` blocks.

Of the collected transaction fees, `ReserveTax` (DEFAULT 2%) will go toward the
reserve pool to increase the reserve pool and increase the security and value of
the GnuCler network.  Also, a `CommonsTax` (DEFAULT 3%) will go toward the
funding of common goods.  These funds will go to the `CustodianAddress` to be
distributed in accordance with whatever is decided by the governance system.

Quark holders who delegate their voting power to other validators pay 10%
commission to the delegated validator.

## Governance ##################################################################

The Gnuclear reactor blockchain is a distributed organization that requires a
well defined governance mechanism in order to coordinate various changes to the
blockchain, such as the validator set, predefined parameters of the system, as
well as software and wetware protocol upgrades.

_TODO: Remove AbsenteeismPenalty: This will go away, and we'll either create an
artificial incentive for voting, or, we'll say that only the validators and the
delegators' votes count, and specify how delegators can override the validator's
vote._

All quark holders are responsible for voting on all proposals.  Failing to vote
on a proposal in a timely manner will result in the quark holder losing
`AbsenteeismPenalty` (DEFAULT 0.5%) of its quarks at most once per
`AbsenteeismPenaltyWindow` (DEFAULT 1 week) time period.

Each proposal requires a deposit of `MinimumProposalDeposit` tokens, which may
be a combination one or more tokens include quarks.  For each proposal, the
voter may vote to take the deposit. If more than half of the voters choose to
take the deposit (e.g. because the proposal was spam), the deposit goes to the
reserve pool, except any quarks which are burned.

For each proposal, voters may vote with the following options:

* Yay
* YayWithForce
* Nay
* NayWithForce
* Abstain

A strict majority of Yay or YayWithForce votes (or Nay or NayWithForce votes) is
required for the proposal to be decided as accepted (or decided as failed), but
1/3+ can veto the majority decision by voting with force.  When a strict
majority is vetoed, everyone gets punished by losing `VetoPenaltyFeeBlocks`
(DEFAULT 1 day's worth of blocks) worth of fees (except taxes which will not be
affected), and the party that vetoed the majority decision will be additionally
punished by losing `VetoPenaltyQuarks` (DEFAULT 0.1%) of its quarks.

### Parameter Change Proposal

Any of the parameters defined here can be changed with the acceptance of a
`ParameterChangeProposal`.

### Text Proposal

All other proposals, such as a proposal to upgrade the protocol, will be
coordinated via the generic `TextProposal`.

## Roadmap #####################################################################

* Decide on genesis-validators
* Decide on crowdfund event details
* Address shard attributes and discovery
* Launch Gnuclear crowdfunding event
* Develop Gnuclear and Tendermint
* Develop EVM shards
* Develop CryptoNote(\?) shard
* Launch Gnuclear blockchain
* Develop Tendermint V2
* ...

## Related Work ################################################################

There have been many innovations in blockchain consensus and scalability in the
past couple of years.  This section provides a brief survey of a select number
of important ones.

### Consensus Systems

#### Classic Byzantine Fault Tolerance

Consensus in the presence of malicious participants is a problem dating back to
the early 80s, when Leslie Lamport coined the phrase "Byzantine fault" to refer
to arbitrary process behavior that deviates from the intended behavior, in
contrast to a "crash fault", wherein a process simply crashes.  Early solutions
were discovered for synchronous networks where there is an upper bound on
message latency, though pratical use was limited to highly controlled
environments such as airplane controllers and datacenters synchronized via
atomic clocks.  It was not until the late 90s that Practical Byzantine Fault
Tolerance (PBFT) [\[11\]][11] was introduced as an efficient partially
synchronous consensus algorithm able to tolerate up to ⅓ of processes behaving
arbitrarily.  PBFT became the standard algorithm, spawning many variations,
including most recently by IBM as part of their contribution to Hyperledger.

The main benefit of Tendermint consensus over PBFT is that Tendermint has an
improved and simplified underlying structure, some of which is a result of
embracing the blockchain paradigm.  Tendermint blocks must commit in order,
which obviates the complexity and communication overhead associated with PBFT's
view-changes.  In Gnuclear and many cryptocurrencies, there is no need to allow
for block <em>N+i</em> where <em>i >= 1</em> to commit, when block <em>N</em>
itself hasn't yet committed. If bandwidth is the reason why block <em>N</em>
hasn't committed in Gnuclear, then it doesn't help to use bandwidth sharing
votes for blocks <em>N+i</em>. If a network partition or offline nodes is the
reason why block <em>N</em> hasn't committed, then <em>N+i</em> won't commit
anyway.

In addition, the batching of transactions into blocks allows for regular
Merkle-hashing of the application state, rather than periodic digests as with
PBFT's checkpointing scheme.  This allows for faster provable transaction
commits for light-clients and faster inter-blockchain communication.

Tendermint Core also includes many optimizations and features that go above and
beyond what is specified in PBFT.  For example, the blocks proposed by
validators are split into parts, Merkle-ized, and gossipped in such a way that
improves broadcasting performance (see LibSwift [\[19\]][19] for inspiration).
Also, Tendermint Core doesn't make any assumption about point-to-point
connectivity, and functions for as long as the P2P network is weakly connected.

#### BitShares delegated stake

While not the first to deploy proof-of-stake (PoS), BitShares [\[12\]][12]
contributed considerably to research and adoption of PoS blockchains,
particularly those known as "delegated" PoS.  In BitShares, stake holders elect
"witnesses", responsible for ordering and committing transactions, and
"delegates", responsible for co-ordinating software updates and parameter
changes.  Though BitShares achieves high performance (100k tx/s, 1s latency) in
ideal conditions, it is subject to double spend attacks by malicious witnesses
which fork the blockchain without suffering an explicit economic punishment --
it suffers from the "nothing-at-stake" problem. BitShares attempts to mitigate
the problem by allowing transactions to refer to recent block-hashes.
Additionally, stakeholders can remove or replace misbehaving witnesses on a
daily basis, though this does nothing to explicitly punish a double-spend attack
that was successful.

#### Stellar

Building on an approach pioneered by Ripple, Stellar [\[13\]][13] refined a
model of Federated Byzantine Agreement wherein the processes participating in
consensus do not constitute a fixed and globally known set.  Rather, each
process node curates one or more "quorum slices" each constituting a set of
trusted processes. A "quorum" in Stellar is defined to be a set of nodes that
contain (is a superset of) at least one quorum slice for each node in the set,
such that agreement can be reached.

The security of the Stellar mechanism relies on the assumption that the
intersection of *any* two quorums is non-empty, while the availability of a node
requires at least one of its quorum slices to consist entirely of correct nodes,
creating a trade-off between using large or small quorum-slices that may be
difficult to balance without imposing significant assumptions about trust.
Ultimately, nodes must somehow choose adequate quorum slices for there to be
sufficient fault-tolerance (or any "intact nodes" at all, of which much of the
results of the paper depend on), and the only provided strategy for ensuring
such a configuration is heirarchical and similar to the Border Gateway Protocol
(BGP), used by top-tier ISPs on the internet to establish global routing tables,
and by that used by browsers to manage TLS certificates; both notorious for
their insecurity.

The criticism in the Stellar paper of the Tendermint-based proof-of-stake
systems is mitigated by the token strategy described here, wherein a new type of
token called the _quark_ is issued that represent claims to future portions of
fees and rewards. The advantage of Tendermint-based proof-of-stake, then, is its
relative simplicity, while still providing sufficient, and provable security
guarantees.

#### BitcoinNG

BitcoinNG is a proposed improvement to Bitcoin that would allow for forms of
vertical scalability, such as increasing the block size, without the negative
economic consequences typically associated with such a change, such as the
disproportionately large impact on small miners.  This improvement is achieved
by separating leader election from transaction broadcast: leaders are first
elected by proof-of-work in "micro-blocks", and then able to broadcast
transactions to be committed until a new micro-block is found. This reduces the
bandwidth requirements necessary to win the PoW race, allowing small miners to
more fairly compete, and allowing transactions to be committed more regularly by
the last miner to find a micro-block.

#### Casper

Casper [\[16\]][16] is a proposed proof-of-stake consensus algorithm for
Ethereum.  Its prime mode of operation is "consensus-by-bet".  The idea is that
by letting validators iteratively bet on which block it believes will become
committed into the blockchain based on the other bets that it's seen so far,
finality can be achieved eventually.
[link](https://blog.ethereum.org/2015/12/28/understanding-serenity-part-2-casper/).
This is an active area of research by the Casper team.  The challenge is in
constructing a betting mechanism that can be proven to be an evolutionarily
stable strategy.  The main benefit of Casper as compared to Tendermint may be in
offering "availability over consistency" -- consensus does not require a +⅔
quorum from the validators -- perhaps at the cost of commit speed or
implementation complexity.

### Sharded Scaling

#### Interledger Protocol

The Interledger protocol [\[14\]][14] is not strictly a scalability solution. It
provides an adhoc interoperation between different ledger systems through a
loosely coupled bilateral relationship network.  Like the Lightning Network, the
purpose of ILP is to facilitate payments, but it specifically focuses on
payments across disparate ledger types, and extends the atomic transaction
mechanism to include not only hash-locks, but also a quroum of notaries (called
the Atomic Transport Protocol).  The latter mechanism for enforcing atomicity in
inter-ledger transactions is similar to Tendermint's light-client SPV echanism,
so an illustration of the distinction between ILP and Gnuclear/IBC is warranted,
and provided below.

1. The notaries of a connector in ILP does not support membership changes, and
   does not allow for flexible weighting between notaries.  On the other hand,
IBC is designed specifically for blockchains, where validators can have
different weights, and where membership can change over the course of the
blockchain.

2. As in the Lightning Network, the receiver of payment in ILP must online to
   send a confirmation back to the sender.  In a token transfer over IBC, the
validator-set of the receiver's blockchain is responsible for providing
confirmation, not the receiving user.

3. The most striking difference is that ILP's connectors are not responsible or
   keeping authoritative state about payments, whereas in Gnuclear, the
validators of the Gnuclear reactor are the authority of the state of IBC token
transfers as well as the authority of the amount of tokens held by each shard
(but not the amount of tokens held by each account within a shard).  This is he
fundamental innovation that allows for secure asymmetric tranfer of tokens from
shard to shard; the analog to ILP's connector in Gnuclear is a persistent and
maximally secure blockchain ledger.

4. The inter-ledger payments in ILP need to be backed by an exchange orderbook,
   as there is no asymmetric transfer of coins from one ledger to another, only
the transfer of value or market equivalents.

#### Sidechains

Sidechains [\[15\]][15] are a proposed mechanism for scaling the Bitcoin network
via alternative blockchains that are "pegged" to the Bitcoin blockchain.
Sidechains allow bitcoins to effectively move from the Bitcoin blockchain to the
sidechain and back, and allow for experimentation in new features on the
sidechain.  The mechanism, known as a two-way peg, uses the standard Simple
Payment Verification (SPV) used by Bitcoin light clients, where proof of a
sufficiently long chain of block headers containing a particular transaction
serves as evidence for the existence of the transaction. Each chain in the peg
serves as a light client of the other, using SPV proofs to determine when coins
should be transferred across the peg and back.  Of course, since Bitcoin uses
proof-of-work, Bitcoin sidechains suffer from the many risks of proof-of-work as
a consensus mechanism, which are particularly exacerbated in a scalability
context. That said, the core mechanism of the two-way peg is in principle the
same as that employed by the Gnuclear network, though using a consensus
algorithm that scales more securely.

#### Ethereum Scalability Efforts

Ethereum is currently researching a number of different strategies to shard the
state of the Ethereum blockchain to address scalability needs. These efforts
have the goal of maintaining the abstraction layer offered by the current
Ethereum Virtual Machine across the shared state space. Research efforts are
being conducted by the Ethereum Foundation under Serenity, the Consensys
organizations and the Dfinity project. [\[18\]][18]

### General Scaling

#### Lightning Network

The Lightning Network is a proposed message relay network operating at a layer
above the Bitcoin blockchain, enabling many orders of magnitude improvement in
transaction throughput by moving the majority of transactions outside of the
consensus ledger into so-called "payment channels". This is made possible by
on-chain cryptocurrency scripts, which enables parties to enter into stateful
contracts where the state can be updated by sharing digital signatures, and
contracts can be closed by finally publishing evidence onto the blockchain, a
mechanism first popularized by cross-chain atomic swaps.  By openning payment
channels with many parties, participants in the Lightning Network can become
focal points for routing the payments of others, leading to a fully connected
payment channel network, at the cost of capital being tied up on payment
channels.

While the Lightning Network can also easily extend across multiple independent
blockchains to allow for the transfer of _value_ via an exchange market, it
cannot be used to assymetrically transfer _tokens_ from one blockchain to
another.  The main benefit of the Gnuclear network described here is to enable
such direct token transfers.  That said, we expect payment channels and the
Lightning Network to become widely adopted along with our token transfer
mechanism, for cost-saving and privacy reasons.

#### Segregated Witness

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

<hr/>

## Appendix ####################################################################

### TMSP specification

TMSP requests/responses are simple Protobuf messages.  Check out the [schema
file](https://github.com/tendermint/tmsp/blob/master/types/types.proto).

#### AppendTx
  * __Arguments__:
    * `Data ([]byte)`: The request transaction bytes
  * __Returns__:
    * `Code (uint32)`: Response code
    * `Data ([]byte)`: Result bytes, if any
    * `Log (string)`: Debug or error message
  * __Usage__:<br/>
    Append and run a transaction.  If the transaction is valid, returns
CodeType.OK

#### CheckTx
  * __Arguments__:
    * `Data ([]byte)`: The request transaction bytes
  * __Returns__:
    * `Code (uint32)`: Response code
    * `Data ([]byte)`: Result bytes, if any
    * `Log (string)`: Debug or error message
  * __Usage__:<br/>
    Validate a transaction.  This message should not mutate the state.
    Transactions are first run through CheckTx before broadcast to peers in the
mempool layer.
    You can make CheckTx semi-stateful and clear the state upon `Commit` or
`BeginBlock`,
    to allow for dependent sequences of transactions in the same block.

#### Commit
  * __Returns__:
    * `Data ([]byte)`: The Merkle root hash
    * `Log (string)`: Debug or error message
  * __Usage__:<br/>
    Return a Merkle root hash of the application state.

#### Query
  * __Arguments__:
    * `Data ([]byte)`: The query request bytes
  * __Returns__:
    * `Code (uint32)`: Response code
    * `Data ([]byte)`: The query response bytes
    * `Log (string)`: Debug or error message

#### Flush
  * __Usage__:<br/>
    Flush the response queue.  Applications that implement `types.Application`
need not implement this message -- it's handled by the project.

#### Info
  * __Returns__:
    * `Data ([]byte)`: The info bytes
  * __Usage__:<br/>
    Return information about the application state.  Application specific.

#### SetOption
  * __Arguments__:
    * `Key (string)`: Key to set
    * `Value (string)`: Value to set for key
  * __Returns__:
    * `Log (string)`: Debug or error message
  * __Usage__:<br/>
    Set application options.  E.g. Key="mode", Value="mempool" for a mempool
connection, or Key="mode", Value="consensus" for a consensus connection.
    Other options are application specific.

#### InitChain
  * __Arguments__:
    * `Validators ([]Validator)`: Initial genesis-validators
  * __Usage__:<br/>
    Called once upon genesis

#### BeginBlock
  * __Arguments__:
    * `Height (uint64)`: The block height that is starting
  * __Usage__:<br/>
    Signals the beginning of a new block. Called prior to any AppendTxs.

#### EndBlock
  * __Arguments__:
    * `Height (uint64)`: The block height that ended
  * __Returns__:
    * `Validators ([]Validator)`: Changed validators with new voting powers (0
      to remove)
  * __Usage__:<br/>
    Signals the end of a block.  Called prior to each Commit after all
transactions

### Merkle Tree & Proof Specification

There are two types of Merkle trees supported in the Tendermint/Gnuclear
ecosystem: The Simple Tree, and the IAVL+ Tree.

### Simple Tree

The Simple Tree is a Merkle tree for a static list of elements.  If the number
of items is not a power of two, some leaves will be at different levels.  Simple
Tree tries to keep both sides of the tree the same height, but the left may be
one greater.  This Merkle tree is used to Merkle-ize the transactions of a
block, and the top level elements of the application state root.

```
                *
               / \
             /     \
           /         \
         /             \
        *               *
       / \             / \
      /   \           /   \
     /     \         /     \
    *       *       *       h6
   / \     / \     / \
  h0  h1  h2  h3  h4  h5

  A SimpleTree with 7 elements
```

## IAVL+ Tree

The purpose of the IAVL+ data structure is to provide persistent storage for
key-value pairs in the application state such that a deterministic Merkle root
hash can be computed efficiently.  The tree is balanced using a variant of the
[AVL algortihm](http://en.wikipedia.org/wiki/AVL_tree), and all operations are
O(log(n)).

In an AVL tree, the heights of the two child subtrees of any node differ by at
most one.  Whenever this condition is violated upon an update, the tree is
rebalanced by creating O(log(n)) new nodes that point to unmodified nodes of the
old tree.  In the original AVL algorithm, inner nodes can also hold key-value
pairs.  The AVL+ algorithm (note the plus) modifies the AVL algorithm to keep
all values on leaf nodes, while only using branch-nodes to store keys.  This
simplifies the algorithm while keeping the merkle hash trail short.

The AVL+ Tree is analogous to Ethereum's [Patricia
tries](http://en.wikipedia.org/wiki/Radix_tree).  There are tradeoffs.  Keys do
not need to be hashed prior to insertion in IAVL+ trees, so this provides faster
ordered iteration in the key space which may benefit some applications.  The
logic is simpler to implement, requiring only two types of nodes -- inner nodes
and leaf nodes.  The Merkle proof is on average shorter, being a balanced binary
tree.  On the other hand, the Merkle root of an IAVL+ tree depends on the order
of updates.

TODO Replace with Ethereum's Patricia Trie if there is a binary variant.

#### Merkle Proof Path Expression

TODO

## Acknowledgements ############################################################

We thank our friends and peers for assistance in conceptualizing, reviewing, and
providing support for our work with Tendermint and Gnuclear.

* [Zaki Manian](https://github.com/zmanian) of
  [SkuChain](https://www.skuchain.com/) provided much help in formatting and
wording, especially under the TMSP section
* [Jehan Tremback](https://github.com/jtremback) of Althea and Dustin Byington
  for helping with initial iterations
* [Andrew Miller](http://soc1024.com/) for feedback on consensus
* Also thanks to [Bill Gleim](https://github.com/gleim) for various
  contributions.
* TODO Your name and organization here if you want.

## Citations ###################################################################

[1]: https://bitcoin.org/bitcoin.pdf
[2]: http://zerocash-project.org/paper
[3]: https://github.com/ethereum/wiki/wiki/White-Paper
[4]: https://download.slock.it/public/DAO/WhitePaper.pdf
[5]: https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
[6]: https://arxiv.org/pdf/1510.02037v2.pdf
[7]: https://lightning.network/lightning-network-paper-DRAFT-0.5.pdf
[8]: https://github.com/tendermint/tendermint/wiki
[9]: https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf
[10]: https://blog.ethereum.org/2014/01/15/slasher-a-punitive-proof-of-stake-algorithm/
[11]: http://pmg.csail.mit.edu/papers/osdi99.pdf
[12]: https://bitshares.org/technology/delegated-proof-of-stake-consensus/
[13]: https://www.stellar.org/papers/stellar-consensus-protocol.pdf
[14]: https://interledger.org/rfcs/0001-interledger-architecture/
[15]: https://blockstream.com/sidechains.pdf
[16]: https://blog.ethereum.org/2015/08/01/introducing-casper-friendly-ghost/
[17]: https://github.com/tendermint/tmsp
[18]: https://github.com/ethereum/EIPs/issues/53
[19]: http://www.ds.ewi.tudelft.nl/fileadmin/pds/papers/PerformanceAnalysisOfLibswift.pdf
[20]: http://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf
[21]: https://en.bitcoin.it/wiki/Thin_Client_Security

* [1] Bitcoin: https://bitcoin.org/bitcoin.pdf
* [2] ZeroCash: http://zerocash-project.org/paper
* [3] Ethereum: https://github.com/ethereum/wiki/wiki/White-Paper
* [4] TheDAO: https://download.slock.it/public/DAO/WhitePaper.pdf
* [5] Segregated Witness: https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
* [6] BitcoinNG: https://arxiv.org/pdf/1510.02037v2.pdf
* [7] Lightning Network: https://lightning.network/lightning-network-paper-DRAFT-0.5.pdf
* [8] Tendermint: https://github.com/tendermint/tendermint/wiki
* [9] FLP Impossibility: https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf
* [10] Slasher: https://blog.ethereum.org/2014/01/15/slasher-a-punitive-proof-of-stake-algorithm/
* [11] PBFT: http://pmg.csail.mit.edu/papers/osdi99.pdf
* [12] BitShares: https://bitshares.org/technology/delegated-proof-of-stake-consensus/
* [13] Stellar: https://www.stellar.org/papers/stellar-consensus-protocol.pdf
* [14] Interledger: https://interledger.org/rfcs/0001-interledger-architecture/
* [15] Sidechains: https://blockstream.com/sidechains.pdf
* [16] Casper: https://blog.ethereum.org/2015/08/01/introducing-casper-friendly-ghost/
* [17] TMSP: https://github.com/tendermint/tmsp
* [18] Ethereum Sharding: https://github.com/ethereum/EIPs/issues/53
* [19] LibSwift: http://www.ds.ewi.tudelft.nl/fileadmin/pds/papers/PerformanceAnalysisOfLibswift.pdf
* [20] DLS: http://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf
* [21] Thin Client Security: https://en.bitcoin.it/wiki/Thin_Client_Security

#### Unsorted links

* https://www.docdroid.net/ec7xGzs/314477721-ethereum-platform-review-opportunities-and-challenges-for-private-and-consortium-blockchains.pdf.html
