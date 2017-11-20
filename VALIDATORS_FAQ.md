# Validators FAQ

## General concepts

### What is a validator?

Validators are the pillars of the network. Their role is to run a full node and participate in consensus by broadcasting votes which contain cryptographic signatures signed by their private key. Validators relay themselves to commit new blocks in the blockchain and receive rewards in exchange for their work. They must also participate in governance by voting on proposals.

### What is a full node?

A full node is a program that fully validates transactions and blocks of a blockchain. It is distinct from a light node that only processes block headers and a small subset of transactions. Running a full node requires more resources than a light-node but is necessary in order to be a validator. In practice, running a full node only implies running a non-compromised and up-to-date version of the software with low network latency and without down time. 

### What is a delegator?

Delegators are Atoms holders who  cannot ordo not want to run validator operations, which involve IT admin and secure data center, themselves. Through the Cosmos UI, a user can delegate to a validator and obtain a part of its reward in exchange.

### How to become a validator?

Any participant in the network can signal that they want to become a validator by sending a “self-designation” transaction, where they must fill out the following parameters:
* Validator's name
* Validator's website
* Validator's description
* Initial commission rate
* Minimum self-bond amount
* Initial self-bond amount

After that, users can bond Atoms to this address, effectively adding stake to it. The total stake of an address is the combination of atoms bonded by users (called delegators) and atoms self-bonded by the participant who designated himself.

Out of all the addresses that signaled themselves, the 100 with the most stake are the ones who are designated as validators. If a validator’s total stake falls below the top 100 then that validator loses its validator’s privileges. Over time, the maximum number of validators will increase, according to a predefined schedule:

* **Year 0:** 100
* **Year 1:** 113
* **Year 2:** 127
* **Year 3:** 144
* **Year 4:** 163
* **Year 5:** 184
* **Year 6:** 208
* **Year 7:** 235
* **Year 8:** 265
* **Year 9:** 300
* **Year 10:** 300

### How will delegators choose their validators?

Delegators are free to choose validators according to their own subjective criteria. However, there are a number of objective criteria that can be expected to influence delegators decision when it comes to choosing their validators, namely:
* **Commission rate:** Validators with low commissions will likely be more attractive.
* **Amount of self-bonded atoms:** Number of atoms a validator self-bonded to its staking pool. A validator with higher amount of self-bonded atoms has more skin-in-the-game, making it more liable for its actions.
* **Amount of delegated atoms:** Total number of atoms delegated to a validator. A high stake shows that the community trusts this validator, but it also means that this validator is a bigger target for hackers. Indeed, hackers are incentivized to hack bigger validators as they receive a reward proportionate to the stake of the validator they can prove to have compromised. We expect validators to become less and less attractive as their amount of delegated atoms grows.
* **Track record:** Delegators will likely look at the track record of the validators they plan to delegate to. This includes seniority, past votes on proposals, historical average uptime and how often the node was compromised.

Apart from these objective criteria that will be displayed in the Tendermint wallet’s UI, there will be a possibility for validators to signal a website address to complete their resume. Validators will need to build reputation one way or another to attract delegators. For example, it would be a good practice for validators to have their setup audited by third parties. Note though that the Tendermint company will not approve or conduct any audit itself.

### Do validators need to be publicly identified?

No, they don’t. Each delegator will value each validator based on objective and subjective criteria. Validators will be able (and are recommended) to register a website address when they nominate themselves so that they can advertise their operation as they see fit. Some delegators may prefer a website that clearly displays the team running the validator and their resume, while others might prefer anonymous validators with positive track records. Most likely both identified and anonymous validators will coexist in the validator set.

### What are the directives of a validator?

Validators have two main directives:
* **Be able to constantly run a correct version of the software:** validators need to make sure that their servers are always online and their private keys are not compromised. 
* **Actively participate in governance:** validators are required to vote on every proposal.

Additionally, validators are expected to be active members of the community. They should always be up to date with the current state of the ecosystem so that they can easily adapt to any change.

### What does ‘participate in governance’ entail?

Validators and delegators on the Cosmos Hub can vote on proposals to change preset parameters of the system automatically (such as the block gas limit), coordinate upgrades, as well as vote on amendments to the human-readable constitution that govern the policies of the Cosmos Hub. The governance system allows for smooth coordination within the network. 

Validators play a special role in the governance system. Being the pillars of the system, they are required to vote on every proposal. It is especially important since delegators who do not vote will inherit the vote of their validators. If a validator does not vote on a proposal it will get a small punishment, and if it does not vote on many successive proposals, the validator will become unbonded.

### What does staking imply?

Bonded atom holders receive rewards and the right to participate in governance. In exchange, they accept to lock their funds. If they want to retrieve them, they need to wait for a *three weeks unbonding period*.

If a validator misbehaves, a certain portion of its total stake is slashed (the severity of the penalty depends on the type of fault). This means that every user that bonded atoms to this validator gets penalized in proportion of its stake. Delegators are therefore incentivized to delegate to validators that they believe will behave correctly.

### Can a validator run away with its delegator’s atom?

By delegating to a validator, a user delegates staking power. The more staking power a validator has, the more weight it has in the consensus and governance processes. However, this does not mean that the validator has custody of its delegator’s atoms. *By no means a validator can run away with its delegator’s funds*. 

Even though delegator’s funds cannot be stolen by their validators, they are still liable if their validators misbehave. In such case, each delegator’s stake will be partially slashed in proportion of the total stake of the validator.

### What is the incentive to stake?

Each member of a validator’s staking pool earns different types of rewards:
* **Block rewards:** Native tokens of applications run by validators (e.g. atoms) are inflated to produce block rewards. 
* **Transaction fees:** The Hub maintains a whitelist of token that are accepted as fee payment. These fees are part of the total reward received by validators and delegators.

These rewards are divided among validator’s staking pools according to each validator’s weight. Then, they are divided among delegators in proportion to each delegator’s stake.

### What is the incentive to run a validator ?

Validators earn additional rewards in the form of commissions on the fees that are collected. These fees can be collected not only in atoms but in any token that has been whitelisted by atom holders. 

Validators also play a major role in governance. If a delegator does not vote, it inherits the vote from its validator. This gives validators a major responsibility in the ecosystem.

### What is a commission?

Fee rewards received by a validator’s pool are split between the validator and its delegators. The part that goes to the validator is called the validator’s commission. Each validator is free to set its initial commission, but there will be rules on how to change it.

Note that validators cannot set commission on block rewards (also called inflationary rewards or provisions). This is to prevent a continuous shift in distribution from delegators to validators which would further the concentration of atoms and ultimately weaken the security of the system.

### How are the block rewards distributed?

Block rewards are socially distributed, meaning that each block reward is distributed to each validator according to their stake.

Let’s take an example where we have 10 validators with equal staking power and commission rate of 1%. Let’s also assume that the reward for a block is 1000 atoms and that each validator has 20% of self-bonded atoms. These tokens do not go directly to the proposer. Instead, they are evenly spread among validators. So now each validator’s pool has 100 atoms. These 100 atoms will be distributed according to each participant’s stake:
* Validator will get 20 atoms
* All delegators will get 80 atoms

Then, each delegator can claim its part of the 80 atoms in proportion of their stake in the validator’s staking pool.

### How are the fees distributed?

Fees are also socially distributed, but the block proposer can get a bonus on the fees of the block it proposes if it includes more than the strict minimum of required precommits.

When a validator is selected to propose the next block, it must include at least +⅔ precommits for the previous block in the form of validators signatures. However, there is an incentive to include more than ⅔ precommits in the form of a bonus. If a proposer includes all the signatures in its block, then it will get the full bonus of 5% on the fees it included in the block. The bonus ranges from 1 to 5% for ⅔ to 100% included signatures. Of course the proposer should not wait too long or other validator would timeout and move on to the next proposer. Validators thus have to find a balance between wait time to get the most signatures and risk of losing out on proposing the next block. This mechanism aims to incentivize non-empty block proposals, better networking between validators as well as mitigating censorship.


Let’s take a concrete example to illustrate the aforementioned concept. In this example, there are 10 validators with equal stake. Each of them applies a 1% commission and has 20% of self-bonded atoms. We consider a successful block collects a total of 1025.51020408 atoms in fees.

First, a 2% tax is applied.
* 2% * 1025.51020408 = 20.51020408 atoms go to the reserve pool

1005 atoms now remain. Let’s assume that the proposer included 100% of the signatures in its block. It thus obtains the full bonus of 5%.

We have to solve this simple equation to find the reward R for each validator:

`9*R + R + R*5% = 1005 ⇔ R = 1005/10.05 = 100`

* For the proposer validator
  * The pool obtains R + R*5% = 105 atoms
  * Commission = 105*80%*1% = 0.84 atoms
  * Validator reward = 100 * 20% + Commission = 21.84 atoms
  * Delegators rewards = 105 * 80% - Commission = 83.16 atoms (each delegator will be able to claim its portion of these rewards in proportion of their stake)
* For each non-proposer validator
  * The pool obtains R = 100 atoms
  * Commission = 100*80%*1% = 0.8 atoms
  * Validator reward = 100 * 20% + Commission = 20.8 atoms
  * Delegators rewards = 100 * 80% - Commission = 79.2 atoms (each delegator will be able to claim its portion of these rewards in proportion of their stake)

### What are the slashing conditions?

If a validator misbehaves, its bonded stake along with its delegator’s stake and will be slashed. The severity of the punishment depends on the type of fault. There are 3 main faults that can result in loss of funds for a validator and its delegators :

* **Double signing:** If someone reports on chain A that a validator signed two blocks at the same height on chain A and chain B, this validator will get slashed on chain A
* **Unavailability:** If a validator’s signature has not been included in the last X block, the validator will get slashed by a marginal amount proportional to X. If X is above a certain limit Y, then the validator will get unbonded
* **Non-voting:** If a validator did not vote on a proposal and once the fault is reported by a someone, his stake will be a little slashed. He will also get a penalty. Once a validator gets a penalty, no additional penalty can be submitted for a given period (3 weeks). After this period, if a second penalty is submitted, the validator gets a second light slash and gets unbonded. If, after the first penalty, no other penalty is submitted for a 3 months period, then the penalty can be cleared by sending a special transaction.

### Incentives for validator #101 to stake?

Validator candidates that do not have enough total stake to be in the validator set will have to run validator operation (or at least be ready to) without getting any revenue. 

There are solutions that are considered to mitigate this issue. For example, we could create a sub-layer of delegation. Validator candidate could delegate to existing validators while they’re trying to attract delegators, thereby generating revenue. At the same time, delegators already bonded to validators could signal their intention to switch to this validator candidate should it get enough stake to enter the validator set. When the validator candidate would get enough pledge, it would transition to a validator and all the delegator who pledged would join its staking pool.

### Do validators need to self-bond atoms?

Delegators should want their validator to have self-bonded atoms in their staking pool; that is, bonded atoms of their own. In other words, validators should have skin-in-the-game. 

In order for delegators to have some guarantee about how much skin-in-the-game their validator has, the latter must signal a minimum amount of self-bonded atoms. If a validator's self-bond goes below the limit that it predefined, this delegator and all of its delegators will unbond. 

### How to prevent concentration of stake in the hands of a few top validators?

For now we are expecting the community to behave in a smart and self-preserving way. When a mining pool in Bitcoin gets too much mining power the community usually stops contributing to that pool. We want to harness the same effect with Cosmos initially. We will put several mechanisms in place to smoothen this process as much as possible:

* **Fast switching:** We want to allow delegators to easily switch from one validator to the other, in order to reduce validator stickiness 
* **Hack bounty:** We want to incentivize the community to hack validators. There will be bounties proportionate to the size of the validator, so that a validator becomes bigger of a target as its stake grows.
* **UI warning:** Users will be warned by the wallet’s UI if they want to delegate to a validator that already has a significant amount of staking power

### Will validators of the Cosmos Hub ever be required to validate other zones in the Cosmos ecosystem?

It is highly probable that they will. If governance decides so, validators of the Cosmos hub might have to validate other zones in the Cosmos ecosystem. For example, validators of the Cosmos hub will also validate the first public Ethermint zone. Of course, they will be compensated for it in the form of block rewards and transaction fees. These rewards will be paid in the native currency of the Ethermint zone, called `photons`.


## Technical requirements 

### What are hardware requirements ?

Validators should expect to provision one or more data center locations with redundant power, networking, firewalls, HSMs and servers.
We expect a modest level of hardware specifications will be needed initially and requirements to rise as network use rises. Participating in the testnet is the best way to learn more.

### What are software requirements ?

In addition to running a cosmos node, validators are going to need to develop monitoring, alerting and management solutions.

### What are bandwidth requirements ?

The Cosmos network has the capacity for very high throughput relative to chains like Ethereum or Bitcoin.
We recommend that the data center nodes only connect to trusted full nodes in the cloud or other validators that know each other socially. This relieves the data center node from the burden of mitigating Denial of Service attacks and syncing new nodes on the network.
But if the network becomes more heavily used, multigigabyte per day data center bandwidth is very realistic.

### What does running a validator imply in terms of logistics ? 

A successful validator operation will require the efforts of multiple highly skilled individuals and continuous operational attention. This will be considerable more involved than running a bitcoin miner for instance.

### How to handle key management ?

Validators should expect to run an HSM that supports ed25519 keys. Here are the current options:
* YubiHSM 2
* Ledger Nano S
* Potential options
* Ledger BOLOS SGX enclave
* Thales nCypher support
* Tendermint SGX enclave

### What can validators expect in terms of operations ? 

Running effective operation is the key to avoiding unexpectedly unbending or being slashed. This includes being able to respond to attacks, outages etc. Maintain security and isolation in your data center etc.

### What are the maintenance requirements

Validators should expect to perform regular software updates to accommodate upgrades and bug fixes. There will inevitably be issues with the network early in its bootstrapping phase that will require substantial vigilance 

### How can validators protect themselves from denial-of-service attacks
 
DDOS attacks occur when an attacker sends a flood of internet traffic to an IP address to prevent the server at the IP address from connecting to the internet.
A DDOS attacker scan the network and learn the IP address of various validator nodes and try to disconnect them from communication with floods of traffic. 

One recommended way to mitigate these risks is for validators to carefully structure their network topology in a so-called Sentry node architecture. 
Validator nodes should only connect to full nodes they trust because they operate them themselves or are run by other validators they no socially. A Validator node will typically run in a data center. Most data center provide direct links the networks of major cloud providers. The validator can use those links to connect to sentry nodes in the cloud. 

Sentry nodes can be quickly spun up or change their ip addresses. Because the links to the sentry nodes are in private ip space, an internet based attacked cannot distrust them directly. This will ensure validator block proposals and votes always make to the rest of the network.

It is expected that good operating procedures on that part of validators will complete mitigate these threats.

### How can I join the testnet ?

The Testnet is a great environment to test your validator setup before launch.

We view testnet participation as a great way to signal to the community that you are ready and able to operate a validator. You can find all relevant information about the testnet and more here : https://cosmos.network/validators

### Is there a faucet ?

If you want to obtain coins, you can do so by using this faucet (maintained by community) : https://www.cosmosvalidators.com/
