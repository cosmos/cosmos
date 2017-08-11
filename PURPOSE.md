We believe in the power of public blockchains to provide a public good,
powered by a collection of self-motivated actors governed by the rules of a
shared consensus ledger, in an environment of competition and freedom of choice.
We have learned important lessons from the successes and failures of prior
cryptocurrencies,  and have been creating innovations of our own that will
unleash a new era of speed, security, scalability, and usability.

Cosmos is a culmination of these lessons and innovations, designed to be
extended to incorporate even future innovations, to create a distributed ledger
platform suitable for generations to come.

One of the great tragedies of cryptocurrencies has been their failure to
interoperate with existing systems, and even with each other.  It is as if each
virtual currency, on its own blockchain and with its own community, were too
sovereign for its own good.  This is made most apparent when you attempt to buy
your first Bitcoin: you discover that it is remarkably difficult to buy the new
internet money over the internet, at least without divulging considerable
amounts of personal information and allowing weeks for it to be verified by
third parties (exchanges) you hardly know and have been warned not to trust with
too much of your money.	

While mechanisms like [atomic
swaps](https://en.bitcoin.it/wiki/Atomic_cross-chain_trading) between chains can
help link communities, they suffer from a need for mature liquidity markets and
active participants on each side (or suffer long timeouts).  The [alt-coin
ecosystem](https://coinmarketcap.com/) is an alchemical soup of enthusiasts
experimenting in various ways in new cryptocurrency design, but each alt-coin
stands alone, siloed by the lack of a general inter-blockchain communication
system, many needlessly wasting electricty through convoluted Proof-of-Work
(PoW) designs.

[Ethereum](https://ethereum.org/) sought to address the problem, somewhat
indirectly, by inventing a new platform for computation, allowing arbitrary
financial systems to be written against a common virtual machine using a common
development environment.  Presuming all new cryptocurrencies launch on Ethereum,
they will all have some capacity for interoperability.  Ethereum is a wonderful
idea, but the design decisions, while motivated by important considerations
(like the need for a simple specification and guaranteed determinism), neglect a
great many more (like the difficulty of designing a secure general purpose
programming environment), and lends Ethereum its own sovereignty problem, which
is that it excludes users who want access to the platform but want alternatives
to the current state transition machine.

Of course, Ethereum doesn't address the problem of turning fiat currency into
ether, either, short of having banks and major government bodies issue their
currency on Ethereum.  And while
[many](http://www.coindesk.com/south-africa-diy-ethereum-blockchain-tests/)
[such](http://www.coindesk.com/south-africa-diy-ethereum-blockchain-tests/)
[institutions](http://www.coindesk.com/fidor-ethereum-core-banking/) are
investigating the Ethereum blockchain, there are both scalability and governance
concerns that will restrict its full scale adoption, and hence impede
integration with existing systems and currencies.

Each existing cryptocurrency supports some cultural ideal.  Bitcoin is decidedly
libertarian, with a slight anarchist leaning which is ultimately betrayed by the
economics of Proof-of-Work.  Ethereum is less a political statement and more an
avant garde academic excercise in distributed systems, computer science, and
contract theory.  Dogecoin is a testament to the capacity for Humans to bond
over the absurd, a phenomenon more commonly known as "being social".  Steem
offers a more structured version of being social, with a basis in content
production and curation.  And so on. But there are many more idealogical
currencies to create, many more virtual machine designs to try, each affording a
unique experiment in the intersection between governance, culture, and
economics.  Would it not be a tragedy for all these experiments to be so rigidly
siloed from one another by great chasms of incompatibility?

Clearly, what we need is something more general than Ethereum - a sort of meta-Ethereum; 
something that can integrate existing codebases and the states of existing blockchains;
something that can interface in a sane manner with the currencies issued by nation states; 
something that formalizes the relationship between cryptocurrencies and connects them without compromising their independence;
something with extreme flexibility that does not compromise security.

Enter Cosmos. Cosmos is a network and a framework for interoperability between
blockchains.  It consists of a web of "hubs" and "zones", where each "zone" is
effectively an independent blockchain with an arbitrary cryptocurrency design
(be it like Bitcoin, Ethereum, ZeroCash, CryptoNote, your local banking
institution, etc.), and each "hub" is a multi-asset cryptocurrency that
facilitates interoperability between some set of zones.

Hubs and zones are powered by the [Tendermint](http://tendermint.com/)
[Proof-of-Stake (PoS) consensus
algorithm](https://github.com/tendermint/tendermint/wiki/Byzantine-Consensus-Algorithm),
using the [TMSP
interface](http://tendermint.com/blog/tendermint-socket-protocol/) to host
applications written in any programming language.  TMSP permits enormous
flexibility in application design, and enables the application to inherit the
security features of a Tendermint-powered blockchain.

Zones communicate with one another through a hub, primarily in the form of
assymetric transfer of some set of tokens from one zone to another.
Effectively, a hub is a blockchain with many
[sidechains](https://blockstream.com/sidechains.pdf), but using PoS instead of
PoW leads to a dramatic reduction in overhead without sacrificing security.  The
trick is that each zone acts as a light client for the hub, and the hub acts as
a light client for all its zones.  [Tendermint makes this
efficient](https://github.com/tendermint/tendermint/wiki/Light-Client-Protocol)
with compact light client proofs that are secure so long as the validator set is
known, which can be achieved by ensuring the light client [synchronizes with
validator set changes at least as often as they are permitted to
occur](https://blog.ethereum.org/2014/11/25/proof-stake-learned-love-weak-subjectivity/).

Many people have [rallied against the use of
Proof-of-Stake](https://download.wpsoftware.net/bitcoin/pos.pdf), claiming it is
impossible to secure.  Simultaneously, they acknowledge that it is nearly
trivial to secure many PoS chains using a single, secure PoW chain.  It is [my
own position](https://twitter.com/buchmanster/status/738550345597648896) that
the correct number of PoW chains is one, and the correct number of PoS chains is
in the thousands or millions, on par with the number of currencies, rewards
systems, and various other token-based systems in the world.

Cosmos reflects this position in that it makes no distinction between hubs - there
is no "top" hub, and the most popular or successful hub is a matter of adoption
by zones.  Furthermore, there is no fundamental distinction between zones and
hubs, such that any zone with sufficient functionality can become a hub.  While
we will release one particular hub in order to get things started (the aptly
named Adam hub), there is nothing stopping this hub from becoming obsolete as
other hubs, even the likes of Bitcoin or Ethereum themselves, come to compete
with it, and potentially replace it.

Cosmos thus introduces a new kind of market dynamic that formalizes the power
struggle between the various cryptocurrency offerings, demolishing the barriers
to interoperability and enabling competition between hubs to contribute to the
economic security of each hub itself - validators who misbehave will be
abandoned for better behaving ones.  The result is a heterogeneous network,
adapting for each community and each locale according to its needs, and yet
retaining a backbone of interoperability that keeps barriers to entry low while
holding stewards of the system accountable and quality of service high.

Whether as testing grounds for new cryptocurrency designs, or an upgrade to
existing ones, as a means for decentralized exchange, or a platform for scalable
smart contracts, Cosmos's potential is that of every existing cryptocurrency and
more in synergy.  The only question is, what will you build on Cosmos?
