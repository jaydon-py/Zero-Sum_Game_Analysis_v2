### Chapter 3. Overall Rating System (OVR)

The objective of the OVR system is to create a rating that reflects a player's ability, primarily based on how they finish per game compare and the strength of their opponents.

Profit alone is not a reliable measure of poker ability, as it can be heavily influenced by luck, risk-taking and the number of games played. Instead, OVR will measure how well a player performs relative to the other players at their table, taking into account their existing ratings.

The system will reward players for winning and penalise players for losing. However, the magnitude of these adjustments will depend on the strength of their opposition and whether they performed above or below expectations.

#### The Formula

The OVR adjustment is calculated using two separate components:

1. Result points: A reward or penalty based on the player's actual finishing position.
2. Expectation points: An additional reward or penalty based on how their actual finishing position compares to their expected position.

The final rating adjustment is calculated as:

$$
\Delta OVR = R + E
$$

With, 

$$
R = B\left(\frac{n+1-2p}{n-1}\right)~~,~~E = K(e-p)
$$

Where, 
- $B$ = Base rating adjustment. (Some scalar to be chosen)
- $K$ = Expectation adjustment factor. (Some scalar to be chosen)
- $n$ = Number of players in the game.
- $p$ = Actual finishing position.
- $e$ = Expected finishing position.

Combining the two components gives our final formula:

$$
\Delta OVR =
B\left(\frac{n+1-2p}{n-1}\right)
+K(e-p)
$$

The player's new OVR is then calculated as follows:

$$
OVR_{\text{new}}=OVR_{\text{old}}+\Delta OVR
$$

### How well does our system correlate to actual profits?

The scatter plot places each player as a single point: their current OVR on the x-axis, their total profit across all sessions on the y-axis. The regression line is a straight line of best fit drawn through those points.

Pearson's coefficient, $r$, summarises how tightly the points cluster around the line. We have that $-1\leq r\leq 1$. Formally, we define $r$ as follows:

$$
r = \frac{\text{Cov}(O,P)}{\sigma_O~\sigma_P}
$$

Note, $\text{Cov}(O,P)$ is defined as the covariance between O, Current OVR, and P, total profit. We also have that $\sigma_O$,$\sigma_P$ represents the standard deviation of the current OVR and total profit respectively.