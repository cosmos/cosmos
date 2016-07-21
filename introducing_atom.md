One of the great tragedies of cryptocurrencies has been their failure to interoperate with existing systems, and even with eachother.
It is as if each currency, on its own blockchain and with its own community, were too sovereign for its own good.
This is made most apparent when you attempt to buy your first Bitcoin: you discover that it is remarkably 
difficult to buy the new internet money over the internet, at least without divulging considerable amounts of personal information and 
allowing weeks for it to be verified by third parties (exchanges) you hardly know and have been warned not to trust with too much of your money.	

While mechanisms like atomic swaps between chains can help link communities,
they suffer from a need for mature liquidity markets on each side.
The altcoin ecosystem is an alchemical soup of enthusiasts experimenting in various ways in new cryptocurrency design,
but each altcoin stands alone, siloed by the sovereignty of its own blockchain, 
many needlessly wasting electricty through convoluted Proof-of-Work (PoW) designs.

Ethereum sought to address the problem, somewhat indirectly, by inventing a new platform for computation, 
allowing arbitrary financial systems to be written against a common virtual machine using a common development environment.
Presuming all new cryptocurrencies launch on Ethereum, they will all have some capacity for interoperability.
Ethereum is a wonderful idea, but the design decisions, while motivated by important considerations
(like the need for a simple specification and guaranteed determinism), neglect a great many more 
(like the difficulty of designing a secure general purpose programming environment),
and lends Ethereum it's own sovereignty problem, which is that it excludes users who want access to the platform
but want alternatives to the current state transition machine.

Of course, Ethereum doesn't address the problem of turning fiat currency into ether,
short of having banks and major government bodies issue their currency on Ethereum.
And while many such institutions are investigating the Ethereum blockchain,
there are both scalability and governance concerns that will restrict its full scale adoption,
and hence impede integration with existing systems and currencies.

So clearly, what we need is something more general than Ethereum, 
preferably something that can easily integrate existing codebases and the states of existing blockchains,
but also something that can interface in a sane manner with the currencies issued by nation states.
In otherwords, something with extreme flexibility that does not compromise security.

Enter Atom. Atom is a network and a framework for interoperability between blockchains.
It consits of a web of "hubs" and "zones", where each "zone" is effectively an independent blockchain
with an arbitrary cryptocurrency design (be it like Bitcoin, Ethereum, ZeroCash, CryptoNote, your local banking institution, etc.), 
and each "hub" is a multi-asset cryptocurrency that facilitates interoperability between some set of zones.

Hubs and zones use the Tendermint Proof-of-Stake (PoS) algorithm, 
and the TMSP interface to host applications written in any programming language,
allowing enormous flexibility in application design,
while inheritting the security features of a Tendermint-powered blockchain.

Zones communicate with one another through a hub, 
primarily in the form of assymetric transfer of some set of tokens from one zone to another.
Effectively, a hub is a blockchain with many sidechains, 
but using PoS instead of PoW leads to a dramatic reduction in overhead without sacrificing security.
The trick is that each zone acts as a light client for the hub, and the hub acts as a light client for all its zones.
This is efficient, because Tendermint permits very efficient light client proofs, so long as the validator set is known,
which can be achieved by ensuring the light client synchronizes with validator set changes at least as often as they are permitted to occur.

Many people have rallied against the use of Proof-of-Stake, claiming it is impossible to secure.
Simultaneously, they acknowledge that it is nearly trivial to secure many PoS chains
using a single, secure PoW chain. It is my own position that the correct number of PoW chains is one,
and the correct number of PoS chains is in the thousands or millions, on par with the number of currencies, rewards systems, and various 
other token-based systems in the world.
Atom reflects this position in that it makes no distinction between hubs - there is no "top" hub and the most popular or
successful one is a matter of adoption by zones. Furthermore, there is no fundamental distinction between zones and hubs,
such that any zone with sufficient functionality can become a hub.
While we will release one particular hub in order to get things started (the aptly named Adam hub),
there is nothing stopping this hub from becoming obsolete as other hubs, even the likes of Bitcoin or Ethereum themselves,
come to compete with it, and potentially replace it.

Atom thus introduces a new kind of market dynamic that formalizes the power struggle between the
various cryptocurrency offerings, demolishing the barriers to interoperability and enabling
competition between hubs to contribute to the economic security of each hub itself - 
validators who misbehave will be abandoned for better behaving ones.
The result is a heterogeneous network, adapting for each community and each locale according to its needs,
and yet retaining a backbone of interoperability that keeps 
barriers to entry low while holding stewards of the system accountable and quality of service high.

Whether as testing grounds for new cryptocurrency designs, or an upgrade to existing ones, 
as a means for decentralized exchange, or a platform for scalable smart contracts,
Atom's potential is that of every existing cryptocurrency and more. 
The only question is, what will you build on Atom?

