Atom Crowdfund Plan
-------------------

DATE: July 22nd, 2016<br/>
NOTE: The details in this plan override what is currently in the whitepaper.

* The Atom Foundation will be a Canadian entity.  Its mission is to create,
  maintain, and further develop, the Atom Ecosystem.

* There will be a Crowdfunding campaign to sell tokens called "atoms" that give
  the holder limited license to use the Atom Ecosystem.  The proceeds of the
Crowdfunding campaign will go to the Atom Foundation to develop the Essential
Atom Software and Services.

* Upon completion of the Crowdfund, all the atom holders, including the Atom
  Foundation, play the Delegation Game in a special purpose Ethereum smart
contract (which holds no Ether).  The top 100 validators after delegation will
be chosen as validators on Genesis.

* Everyone's atoms will vest over a period of two years after Genesis.  Unvested
  atoms cannot be transferred.  Everyone must actively vote during the first two
years of vesting.

* On Genesis, the distribution of atoms will be split between:
  * the Early Funders (5%)
  * the Atom Foundation (20%)
  * the Crowdfund Funders (75%)

* The Atom Foundation can receive more atoms from Atom Governance if it passes a
  proposal with an attached award.

* In addition, 25% of the total number of atoms on Genesis (a constant
  predetermined amount), will be inflated by the Atom Hub Block Reward every
year, to be distributed in proportion to the bonded atom holders.

## Definitions

**Atom Foundation**: The Atom Foundation is a designated legal entity that is
responsible for overseeing the crowdfunding and genesis of the Atom Hub.  After
Genesis, the Atom Foundation takes on a managerial role of managing any excess
funds from the crowdfund, education and PR, and oversees the long term
sustainability of the Atom Ecosystem.

**Atom Ecosystem**: Includes the Atom Hub, other zones that we might officially
support, client software, etc.  All code in the Atom Ecosystem will be Apache2.0

**Atom Hub**: An Atom hub is itself a blockchain, or zone, that connects to many
other zones.  The hub facilitates token movement between zones.  The Atom Hub is
the first hub, and the first zone.  It is also written as "Adam".  There may be
more hubs in the future.

**Atom Hub Block Reward**: The blockchain will reward the Validators and
Delegators in proportion to their bonded atoms, and afterwards account for any
commissions that delegators pay to delegate validators.  The reward will consist
of two categories -- transaction fees, and inflationary atoms.  The transction
fees will be any fee collected by a validator.  In addition, there will be
inflationary atoms at a constant amount of 25% x 20M atoms, or 5M atoms per year.
Atom holders who do not put their atoms at stake by being a validator or
delegating to a validator will not receive any of the Atom Hub Block Rewards.

**Crowdfund**: An atom token crowdfund event that happens during a period of 42
days.  There will be a website where those who wish to purchase atoms can sign
up The crowdfund proceeds will be used to complete the Essential Atom Software
and Services, starting with the release of TendermintCore. 

**Delegator**: An atom holder who put their atoms at stake by delegating its
validating power and voting power to a validator.  They are still responsible
for voting on proposals during the vesting period, but if they don't vote they
will be penalized, but they will inherit the vote of the delegated validator.

**Early Funders**: The Early Funders are qualified investors who purchase 5% of
the Genesis atoms prior to the crowdfund. The proceeds from the early funding
will go toward legal and PR fees, and also help pay salary for the Atom
Foundation until the crowdfunding is complete.

**Validator**: Validators are full nodes of an Atom zone that have the
responsibility of committing blocks in that zone.  The Atom Hub will start with
100 validator spots. Due to the limited number of validator spots, not everyone
who has atoms can be a validator.  Instead, everyone else can bond atoms and
delegate their consensus voting power to any of the 100 validators.  Before
Genesis, the Atom Crowdfund funders will play the Delegation Game to determine
the top 100 bonded delegates who will become the genesis validators.

### Essential Atom Software and Services

**TendermintCore**
  * _Alpha_
    * fix existing issues
    * mempool optimization
    * peer exchange handler
    * validator set changes
    * fork detection and handling
  * _Beta_
    * tendermint consensus v2

**Atom Hub**
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
    * Atom network explorer client

**Other**
  * hardware wallet _with sufficient funding, sold separately_
  * Ethereum peg _with sufficient funding_
  * Bitcoin peg _with partner, if possible_

## Funding

Funds will be raised by the Atom Foundation in 2 phases.

### Phase 0: the Prefund

During the Prefund, 5% of future Genesis atoms will be sold to qualified
investors with a cap and/or discount.  The proceeds from the Early Investors
will be used to prepare for and execute the crowdfund, as well as to pay for
legal expenses.

### Phase 1: the Crowdfund

During the Crowdfund, 75% of future Genesis atoms will be sold to sophisticated
members of the public who wish to support or participate in this project.
The crowdfund will happen over a period of 42 days as the Ethereum crowdfund,
and be capped an amount to be determined later.

The crowdfund will be capped at $12M equivalent of bitcoins after the first 24
hours of the crowfund.  After 24 hours since the beginning of the crowdfund,
when the total amount raised exceeds $12M given the price of bitcoin at 9am PDT
the morning of, the crowdfund will immediately stop.

### Funding Milestones

* If the crowdfund does not meet the minimum $3M -- 95+% of funds returned
* If the crowdfund exceeds $3M -- Essential Atom Software
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
1. EoCF + 7 months: alpha release candidate of Atom Hub for security audit
1. EoCF + 9 months: alpha release of Atom Hub
1. EoCF + 10 months: launch Atom Hub alpha
1. EoCF + 12 months: begin sale of open-source hardware wallet (if funding
   milestone reached)
1. EoCF + 13 months: beta release candidate of Alpha Hub for security audit
1. EoCF + 15 months: launch Atom Hub beta
1. EoCF + 15 months+: Continuous development, timeline set by Foundation

* Timeline for Bitcoin peg support depends on partnership
* Timeline for Ethereum peg support set after alpha release of Atom Hub
