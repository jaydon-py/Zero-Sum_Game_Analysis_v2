### Chapter 2. Profit Distribution

Now we are going to model profit distribution within our real dataset, measuring what the most common results are across the board. 

#### 2.1. The Normal Distribution

Since poker is a zero-sum game, the sum of all profits across any session is exactly £0. It follows that we will always have $\mu=0$ across all profits over all sessions. The spread $\sigma$ reflects the variance of outcomes - a higher variance implies a higher "spread" of results.

We assume that individual session profits $X_1, X_2, \ldots, X_n$ are independent and identically distributed draws from some unknown distribution $F$, and presume that:

$$
F \approx \mathcal{N}(0, \sigma^2)
$$

So, $F$ will follow some form of normal distribution over time. $\sigma^2$ is estimated as:

$$
\hat{\sigma}^2 = \frac{1}{n-1} \sum_{i=1}^{n} X_i^2
$$

By the Law of Large Numbers, this estimator converges in probability to the true variance as the number of sessions grows:

$$
\hat{\sigma}^2 \xrightarrow{p} \sigma^2 \quad \text{as } n \to \infty
$$

Meaning the distribution should stabilise around $\mathcal{N}(0, \sigma^2)$ over time, admittedly, maybe slightly longer than I may be alive to play the game. But nonetheless, the graph is a visual test of this hypothesis.

### Formally Defining Density

Let the profits from $n$ session be modelled by our true distribution:

$$
X_1,X_2,\ldots, X_n \overset{\text{iid}}{\sim} F
$$

- Each $X_i \in \mathbb{R}$ represents each players profit/loss per session. 
- $F$ represents the true distribution of results.
- We are making the assumption that each result is independently and identically distributed.

If $F$ is continuous, then there exists a probability density function $f$ such that:

$$
F(x) = \mathbb{P}(X\leq x) = \int_{-\infty}^{x}f(t)~dt
$$

Recall, that a probability density function $f:\mathbb{R}\to\mathbb{R}$ is defined based on the following properties:

$$
f(x)\geq 0~~~\forall x\in\mathbb{R}
$$

and

$$\int_{-\infty}^{\infty}f(x)~dx=1$$

We have that $f(x)$ will return our true density. However, as we do not have the true distribution for our model we must use an estimator to approximate. We define the estimator as follows:

$$
\hat{f}(x) = \frac{1}{nh} \sum_{i=1}^{n} K\left(\frac{x - x_i}{h}\right)
$$

Where $K$ is the kernel function and $h$ is the bandwidth, controlling the smoothness of the curve. Each data point $x_i$ contributes a small Gaussian bump centred on itself.

So, essentially, density on the y-axis exists such that for an interval $[a,b]$ we have:

$$
\mathbb{P}(a<X<b) = \int_{a}^{b}\hat{f}(x)~dx
$$
and
$$
\int_{-\infty}^{\infty}\hat{f}(x)~dx=1
$$

### Interpreting Density

The y-axis represents probability density, rather than probability itself. It describes how concentrated the probability of a session's profit or loss is around a particular value on the x-axis.

A higher density at a given profit level indicates that results are more concentrated around that value. Conversely, a lower density indicates that results are less concentrated around it.

Importantly, density is not the probability of achieving an exact profit. For a continuous distribution, the probability of observing any one exact value is zero. Instead, probabilities are obtained by calculating the area under the density curve over an interval.

For example, the probability that a session results in a profit between £0 and £50 is given by:

$$
\mathbb{P}(0 < X < 50) = \int_0^{50} \hat{f}(x)\,dx
$$

The total area under the estimated density curve is equal to 1, representing the entire probability distribution:

$$
\int_{-\infty}^{\infty}\hat{f}(x)\,dx=1
$$

Therefore, the y-axis should be interpreted as a measure of how probability is distributed across different possible session outcomes, rather than as a direct measure of the likelihood of any individual result.