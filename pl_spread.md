### Chapter 1. Luck vs Skill

In this chapter we explore the relationship between luck and skill. By taking the null hypothesis that our poker is purely a game of luck, and no skill, we simulate how these games may have taken place if the results were completely random. 
$$
H_0:\ \text{every player}~i~\text{has the same chance of any given result in a game}
$$

From this point forwards we are assuming that a player only adds to their buy-in if they are in a weak position. Under $H_0$, adding to your buy-in is an outcome of play and we will assume each player has an equal chance of adding to their buy-in if they find themselves in a weak position.

Let there be $G\in\mathbb{N}$ games. The set $S$ is the set of all players in the database.

Game $g$ has a set of players $S_g$ where $n_g$ is the number of players in game $g$ such that $n_g = |S_g|$.

For some player $i\in S_g$, we have that their profit-loss (PL) in game $g$ is denoted by $x_{g,i}$ and defined by:

$$
x_{g,i}=\text{Cash-out}_{g,i} - \text{Buy-in}_{g,i}
$$

Player $i$'s total PL will be the sum of all their PL's across all games. Let $T_i$ be the sum of all player $i$'s results across all games they played. We write:

$$
T_i = \sum_{g:\, i \in S_g} x_{g,i}
$$
 
Where $g:\, i \in S_g$ is the condition that we sum all of $i$'s games in which they play and ignore the games they do not. A full view of the data at this point can be seen below. Mathemticallly, this can be read as 'sum over all $g$ such that player $i$ is in the set $S_g$'.


#### Simulating a luck-only world


Under $H_0$, any way of handing out a game's results among its players is equally likely. So in each game we apply a random permutation of the results $\pi_g$ of the players:

$$x^*_{g,i} = x_{g,\pi_g(i)}$$

$\pi_g(i)$ just represents a shuffled expression of how $i$ initially performed in game $g$.

Each of the $n_g!$ permutations has probability $\frac{1}{n_g!}$, and the games are shuffled independently. One simulated version of the spreadsheet is one permutation chosen for every game, and its simulated totals are:

$$T^*_i = \sum_{g:\, i \in S_g} x^*_{g,i}$$

There are $\prod_{g} n_g!$ possible versions so we draw $N = 10{,}000$ at random, and each draw is one alternative history under $H_0$ based purely on luck. Note the following on how the shuffle works:
- Each game $g$ stays zero-sum
- The size of each game $n_g$ does not change
- The players in each game $g$ do not change.

Each simulation reshuffles who got which result within every game, so the results are the same but the winners are random. Repeating this 100,000 times shows how much spread luck alone produces.

Recall our null hypothesis. Under $H_0$, how spread out would the players' final profits be? Assuming that there is no skill involved. And is our real spread big enough to justify that there is some level of skill?

Recall our formula for player $i$'s total profit:

$$
T_i = \sum_{g:\, i \in S_g} x_{g,i}
$$

Our spread can be calculated by finding an estimation for the standard deviation, $\sigma_T$. 

Note, every game is zero-sum, so $\sum_i T_i = 0$ and recall that the total number of unique players in our database is $n = |S|$, where $S$ is the set of all players. This leads us to calculate a mean profit of $0$. See below. 

$$
\bar{T}=\frac{1}{n}\sum_{i=1}^{n} T_i=\frac{1}{n}(T_1+T_2+...+T_n)=0
$$

Now consider the formula for the standard deviation of all players profits, $\sigma_T$.

$$
\sigma_T = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\left(T_i - \bar{T}\right)^2}
$$

Which, with $\bar T=0$, becomes: 

$$
\sigma_T=\sqrt{\frac{1}{n}\sum_{1=n}^{n}T_i^{2}}
$$

A larger $\sigma_T$ means that the final/current results of each player are further apart, a large spread. The opposite holds true also.

Every alternative history $k = 1, \dots, N$ is a complete shuffled version of the original dataset, so it has its own totals $T^*_{k,i}$ and its own spread:

$$
\sigma^*_k = \sqrt{\frac{1}{n}\sum_{i=1}^{n} \left(T^*_{k,i}\right)^2}
$$

Taken together, the values $\sigma^*_1, \dots, \sigma^*_N$ show what spread luck alone produces, including how much it varies from one history to the next.

The graphs below show the spread of every single alternative history and how the spread of the real results compares. 

**Calculating the p-value**

We calculate a value which determines what proportion of total alternative histories produced a scenario spread, some $\sigma^*_k$, at least as extreme as our real spread, $\sigma_T$. We call this, the p-value. The p-value can be calculated as follows:

$$
p=\frac{\text{number of shuffled histories at least as spread out as reality}+1}{\text{number of shuffled histories}+1}
$$

We add one so our formula includes the real dataset and not just the shuffled histories. We can write this formula in a more formal fashion in the following suit:

$$
p = \frac{1 + \#\{k : \sigma^*_k \geq \sigma_T\}}{N + 1}
$$

Where $\#$ just means 'number of' and $\{k : \sigma^*_k \geq \sigma_T\}$ is the set of all shuffled histories $k$ such that its spread, $\sigma^*_k$ is greater than that of the spread of the real history. 

A small $p$ implies that luck alone rarely spreads players apart to this extreme, only this proportion of alternative histories produced under $H_0$ actually created an equivalent situation. 

A large $p$ implies that the real spread can easily be produced by luck.