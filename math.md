**Binomial** 
* $$P(X=x) = \begin{pmatrix}
   n \\
   r
\end{pmatrix} θ^{r} (1-θ)^{n-r}$$

Hypothesis testing

* This means that the p-value is the probability of a false positive event. In
other words, the p-value is the probability that we reject the null
hypothesis when it is true!
This is the reason that, if the p value is less than the alpha level, we reject
the null hypothesis.

Confidence intervals
* Another concept is the “confidence interval”. A 95% confidence interval
contains the true value for θ 95% of the time.

The three classical principles of experimental design are applicable to
clinical trials as well:
* Local control
	* This is to reduce variability by blocking or stratification by site in
multi-center trials
* Replication
	* Replication of experimental units is used to estimate variability. As
obvious as it seems by today’s standards, it has been slowly accepted
by physicians.
* Randomization
	* Randomization is a universally accepted method to reduce bias in
clinical trials

**Therapeutic drug development trials are classified into four phases.**
* Phase I
	* These are dose-finding studies
* Phase II
	* These look for evidence of activity, efficacy and safety at a fixed dose(determined by Phase I studies)
	* Cancer Phase IIa trials, that are small scale feasibility studies using intermediate endpoints (e.g., precursor lesions or biomarkers)
	* Cancer  Phase IIb trials are randomized comparative studies using intermediate endpoints
* Phase III
	* In these trials, new treatments, with evidence of safety and efficacy,
are compared with alternatives, no therapy or placebo.
	* These prevention studies employ comparative designs like Phase IIb
trials and use definitive endpoints (e.g., cancer incidence)
	* Comparative studies employ a concurrent comparison group (internal
control) and are designed to provide precise estimates of treatment
difference. CTE trials correspond to the Phase III part of the original
classification.
	

* Phase IV
	* Phase IV studies occur after regulatory approval to look for
uncommon side effects
	* Cancer: These are defined population studies
* Phase V (Cancer)
	* Phase V are demonstration and implementation trials

**Hypothesis testing** [$$\href{https://en.wikipedia.org/wiki/Type_I_and_type_II_errors}{1}$$]

$$\def \arraystretch{1.5}
   \begin{array}{c:c:c}
    & H_0\text{ is True} & H_a\text{ is True} \\ \hline
   Reject-H_0 & \text{Type I error (False Positive, Probability=α)} & \text{No error (True Positive, Probability=1-β )}\\ \hdashline
   Reject-H_a \text{ (Not reject }H_0) & \text{No error (True Negative, Probability=1-α)} & \text{Type II error (False Negative, Probability=β)} \\ \hline
\end{array}$$

While the Type-I error is easier to control as it is based on a single factor
(the significance of the test), there are three factors that influence the
Type II error
* The critical value for the rejection of the null hypothesis
* The variability of the estimator under the alternative
* The distance between the centers of the null and the alternative
hypothesis

Investigators have control of the former and the second factors (through
manipulation of the sample size). However, the magnitude of the
alternative hypothesis (distance from the null) is out of investigator
control.

Usually studies employ equal treatment allocation. This is done because,
equal allocation is the most efficient (in terms of variability, power and
sample size) design. However, there are many situation that unequal
treatment allocation is needed:
* Maximize the number of subjects assigned to the new treatment
* Treatments may differ in cost.
It is mentioned in the textbook (Section 11.7.2) that a treatment
allocation ratio r : 1 where r = $$\sqrt{C}$$
 (the square root of the relative
cost C) the total cost of study is minimized. For example, if one
treatment is 10 times more expensive an allocation ratio of 3:1 will
minimize cost.
* Variability in treatment response is unequal between the treatments.
In this case, an allocation ratio r = n1
n2 = 1/σ1
1/σ2 equal to the ratio of
the inverse of the two standard deviations will maximize the power of
the statistical test.

**Phase 1**

* optimal biological dose of a drug (OBD)
* All dose finding studies are conducted with increasing doses until a
predefined clinical outcome is observed.

The basic design found in most oncology studies, but also in many other contexts
of cytotoxic medications, proceeds as follows: Once an a priori determine
schedule of progressive dose escalation, the following steps are performed:
* Assign three (3) patients to the lowest dose
* If no one experiences the response event of interest (usually a serious
toxicity or death) proceed to the next higher dose and expose three more
patients to that higher dose
* Continue increasing the dose until one or more patients has the event then
proceed as follows:
	* If only one patient has the event then expose three more patients at
the same dose. If two or more out of the six patients have the event of
interest then the dose is reduced
* Any dose where two or more toxicities happen is reduced

There are various optimality criteria for the OBD.
* The minimum effective dose (MED)
	* For example, in an analgesic, this the optimal dose that completely relieves
mild to moderate pain in 90% of recipients
* Maximum non-toxic dose (MND)
	* The optimal dose oof an antibiotic may be the dose that causes major side
effects in less than 5% of recipients
* Maximum tolerated dose (MTD)
	* In cytotoxic drugs, traditionally the maximum dose that can be tolerated has
been thought optimal, such as the dose that yields serious or life-threatening
toxicity in no more than 30% of the recipients.
* Most likely to succeed dose (MLS)
	* This is the dose that suppresses 99% of the molecular target activity in at
least 90% of patients.

* **Operating characteristics(OC)**
	* The OC of a study is the probability of stopping before the
$$i$$th dose
	* To compute the OC of a design, consider the binomial probability of
observing k responses out of n subjects as b(k; n, p)
* **Unconditional probability** $$Q_i$$ 
	* the conditional probability of passing the $$i$$th dose
	* For 3up-3down design: $$Q_i = \prod_{k=1}^i{b(0;3,p_k) + b(1;3,p_k)*b(0;3,p_k)}$$, with $$p_k$$ the probability of adverse event at each dose level (i.e $$p_1 = 0.1, p_2=0.2,etc$$). For other designs, 4up-4down, it's the same formula, just replace 3 with the desired number 

**Power calculations**

$$z_{a/2} = - z_{1-a/2}$$

* Survival analysis
	* This functions calculates the **events**. You don't care about the total sample size
	* For HR: $$n = \frac{4*θ^2}{(logHR)^2}$$
	*	$$θ = Ζ_{1 - α/2} - Ζ_β = Ζ_{1 - α/2} + Ζ_{1-β}$$
	* i.e. for 30% reduction => HR = 0.7
* For means or proportions
	* Suppose that $$σ$$ is the same in both arms
	* If logistic and proportions: 

	$$ n = \frac{2*σ^2*θ^2}{δ^2}$$

	* if logistic, sd => $$σ = \frac{p}{1-p}$$
	* $$δ = p_2 - p_1$$, p is the proportion of each group
	* $$δ = μ_2 - μ_1$$, μ is the mean in each group
* If H0 => p_c = p_a = (p_c+p_a) /2 = p
 
	$$n = \frac{(Ζ_{1 - α/2} * \sqrt{2*p*(1-p)} + Z_β * \sqrt{p_1c * (1-p_c) + p_a(1-p_a)})^2}{δ^2}$$

* total_study_time = min_follow_up_time + R (accrual time)
* For 10% dropout, we recalculate the desired events:
	We have already calculated N (events) for a given α & β. So if this number is the 90% of the final sample size $$X = \frac{N}{0.9}$$
 
$$\def \arraystretch{1.5}
   \begin{array}{c:c} \hline
    \text{0.9 (90\%)} & N_{events}\\ \hdashline
   1 (100\%) & X_{target} \\ \hline
\end{array}$$

* Information time for i time: $$ I_i = \dfrac{n_{i}}{n_{events\_ in\_ the\_ end\_of\_study}}$$

**Strata for sex**
* Produce blocks for 100 males and 100 females to randomly assign 2 treatments
* In the end, male could be 90 and females 50. However, treatment allocation within sex stratum would be random, due to block randomazition!
* Random block size (2 to 8) to sufficiently αποκρυψω το allocation.


