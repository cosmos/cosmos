# Proof-of-Stake Consensus Pool Considerations

One example of the trade off between speed of transactions and security is the
number of validator nodes in a Proof of Stake (PoS) system. The more nodes
within a consensus group, the more robust the system becomes against byzantine attacks
as more nodes need to be byzantine, while conversely the longer the
consensus engine will take to run. This concept leads to the conclusion that
within a system that has regard for transaction speed, the consensus engine
should optimize for the number of validators; in other words, not allow for unlimited
validators.

In PoS, all validator nodes have stake which can be
slashed if byzantine behaviour is provably observed. As such, the more coins
there are at stake, the greater the punishment for byzantine behaviour, thus (hopefully) securing the Cosmos.
Further, to incentivize a greater total number of
staked coins within the network, non-staked coins will not benefit from the
addition of new coins minted (inflated) as the staked coins are added pro-rata to the balance of
coins held as staked by validator nodes.

If a holder of COSMOS tokens (Atoms) would like to benefit from this inflation
mechanism, but does not meet the cutoff to be a validator node, then the
holder may choose to 'stake' their Atoms with another validator node (delegation).  Delegated Atoms are subject to slashing if the validator they were staked with performs any byzantine behaviour.  Delegators must accept the
risk that the validator node which they have delegated their stake to may get compromised.

As an alternative to delegating stake to a validator, there may be another way to
participate in consensus.  Several Atom holders may combine resources to create a validator
pool.  Within a validator pool, all members operate independent nodes and run a local consensus algorithm
in order to arrive at the pool's official votes (which may contain a cryptographic threshold-signature).

Validator pools necessitate new security considerations.
Assuming that the Tendermint algorithm is used as the consensus algorithms of validator pools, to comply
with byzantine fault tolerance, all pools should at bare minimum comprise of
at least 4 validator nodes.

Consider the following Tendermint instances:

 - Tendermint with 16 normal (non-pool) validator nodes with equal voting power
   - In order to compromise the safety of the system at least 1/3 of the
     validator nodes must be byzsantine, 7 nodes
 - Tendermint with 4 pool validator nodes each with a pool of 4 nodes each with
   equal voting power
   - In order to compromise the safety of the system at least 1/3 of the
     validator nodes must be byzsantine, 2 validator nodes
   - To compromise a single validator node, at least 1/3 of the pool's nodes
     must be compramised, 2 nodes
   - In total, under an optimally densely arrangement the minimum number of
     nodes for the safety of the network to be compromised is 4 nodes:
     - Pool 1: (4 non-byzantine nodes) = non-byzantine
     - Pool 2: (4 non-byzantine nodes) = non-byzantine
     - Pool 3: (2 non-byzantine nodes, 2 byzantine nodes) = byzantine
     - Pool 4: (2 non-byzantine nodes, 2 byzantine nodes) = byzantine
   - Conversely, under the most disperse arrangement the minimum number of nodes
     for the safety of the network to be compromised is 6 nodes:
     - Pool 1: (3 non-byzantine nodes, 1 byzantine nodes) = non-byzantine
     - Pool 2: (3 non-byzantine nodes, 1 byzantine nodes) = non-byzantine
     - Pool 3: (2 non-byzantine nodes, 2 byzantine nodes) = byzantine
     - Pool 4: (2 non-byzantine nodes, 2 byzantine nodes) = byzantine

As the number of pool validator nodes and pool's nodes are allowed within a
consensus system both increase, the optimally dense scenario the number or
nodes required to compromise the systems safety approaches 1/3 of the pool's
nodes of 1/3 of all pools or 1/9 of the total number of nodes (~11%). Similarly,
for the most disperse scenario the number approaches 1/3 of all nodes, with 1/3
of pools having 1/3 byzantine nodes, making the whole pool byzantine, and 2/3s
of pools having just under 1/3 byzantine nodes making them non-byzantine. 

Despite that you can view the use of pools as decreasing the safety of a
network, its worth pointing out that ultimately as the number of nodes in a
pool increases, so does the number of computers which must be compromised in
order to make a system unsafe. So in the above example if all nodes security is
of equal strength and all parties all nodes are of equal opportunity of being
compromised than 16 nodes pooled by groups of 4 is more secure than 4
non-pooled nodes (but not as secure as 16 non-pooled nodes).  The above
assumptions may of course not be true in practice as pooling resources to a
smaller number of nodes may enable those fewer number of nodes to invest in
better security practices. 

#### Further Questions
 - How are the many different forms of malicious activity affected by pooling?
 - What are the relationships between rewards for validators and their investment 
   in further security which make pooling more or less secure than non-pooled systems?
 - What protocols can a network enforce to create a more secure 
   environment for nodes who wish to pool?

