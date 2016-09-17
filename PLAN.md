Cosmos Crowdfund Plan
---------------------

DATE: July 22nd, 2016<br/>
LAST UPDATED: Aug 12th, 2016<br/>
NOTE: The details in this plan override what is currently in the whitepaper.

* Cosmos Foundation will be a non-profit Canadian entity.  Its mission is to
  create, maintain, and further develop, the Cosmos Ecosystem.

* There will be a Crowdfunding campaign to sell tokens, called "atoms", that
  give the holder limited license to use the Cosmos Hub.  The proceeds of the
Crowdfunding campaign will go to Cosmos Foundation to develop the Essential Cosmos
Software and Services.

* There will be 20,000,000 atoms on Genesis day. On Genesis day, the
  distribution of atoms will be split between:
  * Pre-funders (5%)
  * Cosmos Foundation (20%)
  * Crowdfund Funders (75%)

* Upon completion of the Crowdfund, all the atom holders, including Cosmos Foundation,
  play the Delegation Game in a special purpose Ethereum smart contract (which
holds no Ether).  The top 100 validators after delegation will be chosen as
validators on Genesis.

* Everyone's atoms will vest over a period of two years after Genesis.  Unvested
  atoms cannot be transferred until vested.  Unvested atoms will vest over time,
at a rate of 1/(24x365x2) of the account's atoms, every hour.

* Every validator must participate in governance, or else become inactivated and
  eventually unbonded.  Delegators who delegate atoms to such validators will
also likewise get their delegated atoms inactivated and eventually unbonded.

* Anyone may receive more atoms by passing a proposal with an attached award.
  Such reward atoms will be purely inflationary.

* 1/3 of the total number of atoms will be distributed back to the bonded atom
  holders for having a stake in consensus.  This a tax (disincentive) for not
putting atoms at stake, and not participating in governance during the first two
years after Genesis.

## Definitions

**Cosmos Ecosystem**: Includes the Cosmos Network and other software and
services, including validator and client software.

**Cosmos Foundation**: Cosmos Foundation is a non-profit legal entity that manages the
Crowdfund and Genesis of the Cosmos Hub.  Besides the initial development of the
Essential Cosmos Software and Services, Cosmos Foundation has no further obligations
with regards to the Cosmos Ecosystem, Cosmos Hub, or derivatives
(forks) of the Cosmos Hub, but instead is a general participant in the network.

**Cosmos Hub**: An Cosmos hub is itself a blockchain, or zone, that connects to
many other zones.  The hub facilitates token movement between zones.  The Cosmos
Hub will be the first hub, and the first zone.

**Cosmos Hub Block Reward**: The blockchain will reward the Validators and
Delegators in proportion to their bonded atoms, and afterwards account for any
commissions that delegators pay to delegate validators.  The reward will consist
of two categories -- transaction fees, and inflationary atoms.  The transction
fees will be any fee collected by a validator.  In addition, there will be
inflationary atoms at a rate of 1/3 of the total number of atoms per year.
Cosmos holders who do not put their atoms at stake by being a validator or
delegating to a validator will not receive any of the Cosmos Hub Block Rewards.

**Cosmos Network**: Includes the Cosmos Hub and all connected zones.

**Crowdfund**: An atom token crowdfund event that happens during a period of 42
days.  There will be a website where those who wish to purchase atoms can sign
up The crowdfund proceeds will be used to complete the Essential Cosmos Software
and Services, starting with the release of TendermintCore. 

**Delegator**: An atom holder who puts their atoms at stake by delegating its
validating power and voting power to a validator.  They are still responsible
for voting on proposals during the vesting period.  If they don't vote they
will be penalized, but they will inherit the vote of the delegated validator.

**Early Funders**: The Early Funders are qualified investors who purchase 5% of
the Genesis atoms prior to the crowdfund.  The majority of the proceeds from the
early funding will go toward legal and PR fees, and also help pay salary for
Cosmos Foundation until the crowdfunding is complete.

**Validator**: Validators are full nodes of a Cosmos zone that have the
responsibility of committing blocks in that zone.  The Cosmos Hub will start
with 100 validator spots.  Due to the limited number of validator spots, not
everyone who has atoms can be a validator.  Instead, everyone else can bond
atoms and delegate their consensus voting power to any of the 100 validators.
Before Genesis, the Cosmos Crowdfund funders will play the Delegation Game to
determine the top 100 bonded delegates who will become the genesis validators.

### Essential Cosmos Software and Services

**TendermintCore**
  * _Alpha_
    * fix existing issues
    * mempool optimization
    * peer exchange handler
    * validator set changes
    * fork detection and handling
  * _Beta_
    * tendermint consensus v2

**Cosmos Hub**
  * _Alpha_
    * multiasset accounts
    * atom staking with delegation
    * governance
    * basic wallet client
  * _Beta_
    * zone support
      * exchange zone
      * ethereum zone
      * import crypto distributions
    * Cosmos network explorer client

**Other**
  * hardware wallet integration _with sufficient funding_
  * Ethereum peg _with sufficient funding_
  * Bitcoin peg _with partner, if possible_

## Funding

Funds will be raised by Cosmos Foundation in 2 phases.

### Phase 0: the Prefund

During the Prefund, 5% of future Genesis atoms will be sold to qualified
investors with a cap and/or discount.  The proceeds from the Early Investors
will be used to prepare for and execute the crowdfund, as well as to pay for
legal expenses.

### Phase 1: the Crowdfund

During the Crowdfund, 75% of future Genesis atoms will be sold to sophisticated
members of the public who wish to support or participate in this project.
The crowdfund will happen over a period of 42 days as the Ethereum crowdfund.

The crowdfund will be capped at $9M equivalent of bitcoins after the first 24
hours of the crowfund.  After 24 hours since the beginning of the crowdfund,
when the total amount raised exceeds $9M given the price of bitcoin at 9am PDT
the morning of, the crowdfund will immediately stop.

### Funding Milestones

* If the crowdfund does not meet the minimum $3M -- 95+% of funds returned
* If the crowdfund exceeds $3M -- Essential Cosmos Software
* If the crowdfund exceeds $5M -- Ethereum peg
* If the crowdfund exceeds $7M -- Open-source hardware wallet (sold separately)

Timeline
--------

1. Prefund for 5% of Genesis atoms
1. Canadian non-profit is created
1. Begin Crowdfund
1. End of Crowdfund after 42 days or cap reache (EoCF)
1. EoCF + 2 months: alpha release candidate of TendermintCore for security audit
1. EoCF + 4 months: alpha release of TendermintCore
1. EoCF + 7 months: alpha release candidate of Cosmos Hub for security audit
1. EoCF + 9 months: alpha release of Cosmos Hub
1. EoCF + 10 months: launch Cosmos Hub alpha
1. EoCF + 12 months: begin sale of open-source hardware wallet (if funding
   milestone reached)
1. EoCF + 13 months: beta release candidate of Alpha Hub for security audit
1. EoCF + 15 months: launch Cosmos Hub beta
1. EoCF + 15 months+: Continuous development, timeline set by Cosmos Foundation

* Timeline for Bitcoin peg support depends on partnership
* Timeline for Ethereum peg support set after alpha release of Cosmos Hub
