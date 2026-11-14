## Dataset and question

**Dataset.** I used Jeff Sackmann's ATP match data from Tennis Abstract (CC BY-NC-SA 4.0), accessed through an archive on GitHub. It covers tour-level men's matches from 2015 to 2024. The files hold 27,672 matches. I used the same cleaning as in Assignment 2, removing matches on other surfaces (72, mostly carpet), unfinished matches identified from the score text (905), matches with missing ace counts (856) and matches where both players hit the same number of aces (2,116). That leaves 23,723 matches. Both visualizations use exactly these matches and the same four numbers: the share of matches won by the player who hit more aces, for ace gaps of 1 to 2, 3 to 5, 6 to 9 and 10 or more. This builds on my Assignment 2 chart, stripped down to one view.

**Question.** Do aces win matches? More precisely: how often does the player who hits more aces in a match also win it, and does that change with the size of the ace gap?

**Which is which.** Visualization B is the ethical one. Visualization A is the deceptive one.

## Visualization B (ethical)

My goal for B was that a tennis fan who does not know the statistics could read it correctly without help.

- **Zero baseline, bar length.** Win rate is a quantity, and position and length on a shared scale are the most accurately read channels in the Cleveland and McGill ranking. The bars start at 0%, following the lecture rule that bars almost always include zero, so length is proportional to value and the lie factor is 1.
- **A 50% reference line.** A win rate only means something compared with chance, so a dashed "coin flip" line marks 50%.
- **Sample sizes on every row.** The reader can see that each group is thousands of matches.
- **Plain language.** A fan who has never watched tennis can follow it: the subtitle defines an ace ("a serve the opponent never touches") and the quantity in words ("the player who hit more aces"), and the groups are labelled "extra aces hit."
- **Transparent transformations and source.** The footnote gives the 23,723 of 27,672 matches, lists every exclusion, and names the source.
- **Bias and limits.** The note says this shows association, not cause: stronger servers both hit more aces and win more. The subtitle says these are men's tour-level matches, because the data leaves out women's tennis and lower-level events, so the pattern may not hold for other players. Aggregating to the match level treats every server alike, and binning hides variation within each group.
- **One color.** The groups are ordered, not categories, so there is no reason to add hue.
- **The title is the question,** with no spin.

## Visualization A (deceptive)

A uses the same data and the same chart type. Every number and label is true. The intended impression is that aces almost decide matches and that each step up in ace gap is a huge jump. The real picture is a 15-point rise from 56.8% to 72.3%.

1. **The axis starts at 50%, not 0%.** The tick labels are honest (50% to 75%), but the bars start at 50%, so their length shows win rate above 50%, not win rate. The 1 to 2 bar is 6.8 units long and the 10+ bar is 22.3, so the top bar looks about 3.3 times the bottom one. In the data the ratio is 1.27. The effect shown in the graphic is about 8 times the effect in the data (a lie factor of about 8). It looks principled because 50% is the coin-flip point, but it also quietly rules out the possibility that the higher-ace player wins less than half the time (from lecture: axis limits set the counterfactual space). *Detection:* read the first tick, and ask whether the bars start at zero.
2. **A color ramp from light to dark green.** The color repeats the same variable as the bar length, so the picture says "stronger" twice. *Detection:* notice that color carries no new information.
3. **A skewed title and a relative-change callout.** "Hit more, win more" frames aces as the cause. "27% more likely to win" is true (72.3 divided by 56.8 is 1.27), but a relative change inflates a 15-point gap and invites a causal reading about an individual player. The line "More aces, more wins, on every court" is also true (I checked each surface in my Assignment 2 data), but it says nothing about how big the effect is. *Detection:* compute the absolute difference, and ask whether the title claims more than the data shows.
4. **Omissions.** A shows no sample sizes, no exclusions, no association-not-cause caution and no coin-flip line. The source is cited but the transformations are not. *Detection:* ask how many matches there are, who was excluded, and whether stronger servers explain both aces and wins.

## Connection to lecture and the readings

From the nested model in lecture, the cut axis (choice 1) is a Data to Design failure, because the encoding no longer matches the data. The title and callout (choice 3) aim at a Human to Interpretation failure, where correlation gets read as cause. The omissions (choice 4) hide the World to Data decisions, like the sample and the exclusions. I also used lecture's zero-baseline rule and Tufte's lie factor (effect shown divided by effect in the data) to measure choice 1.

From the readings, I used the taxonomy from "I Came Across a Junk" (Lan and Liu) to name the choices. The truncated axis is listed under inaccuracy in the misinformation category, and the distorted bar lengths it produces are data-visual disproportion, the most common flaw in their study of real charts. Leaving out sample sizes is a failure to show uncertainty, which the taxonomy lists under incompatibility. The Perils of Chart Deception paper (Mahbub et al.) found that every AI model it tested was fooled by at least one of eight deceptive designs, including axis manipulation, so axis tricks like mine work even on readers who are not looking for them. In my chart, no single choice is dramatic. The deception works because several small choices point the same way.

## Reflection on difficulty

The hardest part for me was staying honest. The strongest-looking and most straightforward tricks, such as a rescaled axis with a false label or an invented comparison, are not allowed, so I had to find choices that are technically true. Cutting the axis at the coin-flip line was the most effective because it looks like a sensible design decision.
