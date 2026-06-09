# Write-up: Synthetic Survey Response Generator (LangChain Version)

## My Approach and Why I Chose It

When I first looked at this problem, the obvious solution was to just dump the entire survey into an LLM and ask it to generate 200 responses in one go. But that approach has a real problem — the responses end up feeling disconnected from each other. Someone might rate their satisfaction 1 out of 5 and then write a glowing open-text answer, or give a 0 for likelihood to recommend despite saying everything was perfect. That is not how real people respond.

So instead I built a pipeline around the idea of personas. Before generating anything, the system picks a type of customer — someone who is happy and loyal, a frustrated buyer who got a late delivery, a neutral shopper who was just okay with the experience, and so on. Five archetypes in total, each appearing in realistic proportions across the 200 responses.

Once a persona is chosen, the numeric answers like satisfaction rating and NPS are sampled from probability distributions specific to that persona. A frustrated customer is far more likely to give a 1 or 2 on satisfaction, and their NPS is locked into a range that makes sense for that score — so you will never see someone rate satisfaction 1 out of 5 and then give a 9 out of 10 NPS. That kind of contradiction is caught before it ever reaches the output.

The LLM only comes into play for the open-text question. By the time it is called, it already knows the satisfaction score, NPS, product category, and whether delivery was on time. All of that context flows through a structured LangChain prompt template, so the generated feedback is grounded in the actual numbers and never contradicts what the respondent already said numerically.

## Why LangChain Specifically

I built a pipeline using LangChain instead of calling the Groq API directly. The core idea is that LangChain's pipe operator chains the prompt, the LLM, and the output parser into a single readable line:

```
chain = prompt | llm | parser
```

This has a few concrete benefits. First, the prompt is managed through a named-variable PromptTemplate, so there is no string formatting scattered across the code — every variable like satisfaction, nps, category, delivery, and sentiment is declared upfront and plugged in cleanly at call time. Second, the StrOutputParser handles stripping the raw LLM response to plain text automatically, so there is no manual parsing needed. Third, the chain is built once at module load and reused for every call, which is more efficient than constructing a new client object per response.

The underlying LLM is still Groq's free tier running llama-3.1-8b-instant, giving 14,400 requests per day at no cost. A small sleep between calls keeps token usage within the per-minute budget without any issues.

## How I Would Measure Whether the Outputs Are Any Good

The most direct check is coherence between Q1 and Q2. If you compute the Pearson correlation between satisfaction and NPS across all 200 responses, a realistic dataset should land somewhere around 0.7 to 0.85. Too low and the scores feel random; too high and they look artificially perfect.

Beyond that, running a simple sentiment classifier like VADER on the open-text answers and checking whether negative sentiment lines up with low satisfaction scores is a good sanity check. If someone wrote an angry comment but rated satisfaction 5, something is wrong.

It is also worth checking the distribution of satisfaction scores against real e-commerce benchmarks, where the average tends to sit around 3.8 out of 5. If the synthetic data skews too heavily toward extremes or looks perfectly uniform, it is a sign the persona weights need adjustment.

A specific check this version makes easy is delivery coherence — every response where Q4 is No should have an open-text answer that mentions delivery or timing. That is straightforward to verify programmatically and it is a direct measure of whether the prompt template is doing its job.

Finally, reading a random sample of 20 responses by hand is honestly the most reliable test. If they feel like things a real person might write in a quick post-purchase survey, the system is working.

## One Thing I Would Do Differently With More Time

The persona weights and score distributions are currently hand-tuned based on intuition — things like "frustrated customers give a 1 or 2 about 75% of the time." That works well enough, but it is essentially a guess.

With more time I would fit a simple mixture model on even a small set of real survey responses, maybe 30 to 50 rows. That would give empirically grounded distributions instead of manually chosen ones, and it would automatically pick up correlations that are hard to anticipate — like whether Electronics buyers tend to rate delivery satisfaction differently from Clothing buyers, or how strongly category choice predicts NPS. The pipeline would stay the same, but the numbers driving it would be rooted in reality rather than estimates.

On the LangChain side, one natural extension would be adding LangSmith tracing, which is free at low usage levels. Every chain invocation would be logged automatically with the inputs, outputs, and latency, making it much easier to spot patterns in where the LLM is drifting away from the intended tone without having to read every CSV row manually.
