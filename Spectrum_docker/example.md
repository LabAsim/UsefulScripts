**For the design**

- fixed effects represent *themselves*
- random effects represent a *population*

**Within the model**

* fixed effects *explain* variation
* random effects *organize* unexplained variation

Random effects are effects that common sense says will explain
variation, but you *don’t want to have to know them* in order to be
able to apply the model.


**REML vs. ML** 
[$\href{https://exeter-data-analytics.github.io/StatModelling/mixed-effects-models.html}{1}$]
[$\href{https://github.com/thierryo/my_blog}{2}$]

To fit these models we use an approach called maximum likelihood (ML). ML is a very general technique with desirable asymptotic properties. However, ML estimators can be biased, particularly for small sample sizes. In mixed models an alternative approach, known as restricted maximum likelihood (REML), can be used, which produces better estimates of the model coefficients, particularly for small sample sizes. However, the REML likelihood function is different to the ML likelihood function, and only makes sense for mixed models (since it’s designed to estimate the variance components).

We may have to switch between these two approaches depending on what we want to do. In general, if you want to compare nested models that only differ in the random effects, then you can use either REML or ML. However, if you want to compare models that differ in their fixed effects, then for balanced, nested designs we can usually derive suitable tests based on REML fits. For unbalanced or non-nested designs you will need to use ML. Hence, if we are performing variable selection or model simplification, then we may have to *switch to ML when comparing models, but then refit the model using REML in order to produce estimates of the coefficients.*

**Include a variable as fixed and random effect** [$\href{https://stats.stackexchange.com/questions/263194/does-it-make-sense-to-include-a-factor-as-both-fixed-and-random-factor-in-a-line}{1}$] [$\href{https://stats.stackexchange.com/questions/79360/mixed-effects-model-with-nesting}{2}$]

You can include a variable as a fixed effect and allow it to vary within a group  

$Y \sim indepvar + (indepvar \vert group)$

