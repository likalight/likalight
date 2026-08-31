<div align="center">

<img src="./ascii.svg" width="500" alt="ASCII portrait of Kalairaajan Thiagarajan, typing itself out row by row"/>

### Kalairaajan Thiagarajan

<samp>applied computing (fintech) · singapore institute of technology · singapore</samp>

<a href="https://linkedin.com/in/kalairaajan">linkedin</a> ·
<a href="mailto:kalairaajan@gmail.com">email</a> ·
<a href="https://github.com/likalight?tab=repositories">repositories</a>

</div>

<br/>

> I work on the operations side of software — incident automation, retrieval
> systems, and the evaluation harnesses that decide whether either of them is
> actually working.

<br/>

<img src="./hd-about.svg" width="880" alt="about"/>

Third year of a BSc (Honours) in Applied Computing (FinTech) at the Singapore<br/>
Institute of Technology, graduating August 2027. Before that, two years as an<br/>
intelligence analyst, which is where the habit of trusting measurement over<br/>
intuition comes from.

Most of what I build is unglamorous by design: a runbook that fires before the<br/>
on-call engineer wakes up, an ETL job that turns ten gigabytes of chat logs into<br/>
twelve categories worth acting on, an eval harness that blocks a release. The<br/>
interesting part is never the model. It is what happens when the model is wrong.

<br/>

<img src="./hd-now.svg" width="880" alt="now"/>

<samp>&nbsp;→&nbsp;</samp> Finishing my degree at SIT, and building in the open<br/>
<samp>&nbsp;→&nbsp;</samp> Available for a full-time internship, January to August 2027<br/>
<samp>&nbsp;→&nbsp;</samp> Currently reading about agent evaluation and failure taxonomies

<br/>

<img src="./hd-work.svg" width="880" alt="work"/>

**Systems Engineer Intern** — Visa, Operations & Infrastructure (Containers)<br/>
<samp>may 2026 – jul 2026 · kubernetes, bash, linux, python, mcp, rag</samp>

Analysed 3,500 historical Kubernetes incidents, found that 18% were recurring<br/>
failures, and wrote the Bash remediation workflows for them. Built an AI triage<br/>
agent that diagnoses each incoming incident and hands the on-call engineer a<br/>
remediation plan before they engage — 40% off time-to-resolution. Shipped<br/>
read-only `kubectl` diagnostics and auto-healing runbooks to 12 production<br/>
clusters with zero disruption to live workloads, and tuned Prometheus and<br/>
Grafana alert rules down by 25% of their false positives.

**Machine Learning Engineer Intern** — NVIDIA, SIT × NVIDIA AI Centre<br/>
<samp>may 2025 – aug 2025 · pytorch, hugging face, mlflow, graph-rag</samp>

Built a graph-RAG pipeline over public rail safety reports that surfaces prior<br/>
incidents and their mitigations, at 85% accuracy on hazard-factor detection.<br/>
Fine-tuned TranSent-X, a RoBERTa model for Singapore transport sentiment, 32%<br/>
more accurate than off-the-shelf baselines. Wrote the LLM evaluation framework —<br/>
response-quality checks, behavioural tests, a failure taxonomy — that caught the<br/>
regressions and cut pilot defect rates by 40%.

**Intelligence Research Analyst** — Digital Intelligence Service<br/>
<samp>jul 2022 – jul 2024 · python, sql, arcgis, opencv, azure</samp>

Ingestion pipelines across AIS vessel tracking, ADS-B, satellite imagery and<br/>
geotagged social media, feeding 700+ intelligence products a year. Fused those<br/>
streams into GEOINT movement-anomaly workflows, cutting manual data-fusion time<br/>
by 25% across ten cross-unit teams.

**Business Analyst Intern** — Scoot, Cabin Services<br/>
<samp>oct 2021 – jun 2022 · sql, python, tableau, power bi, sharepoint</samp>

Took the Cabin Crew Assist App from requirements through UAT to production, and<br/>
built the compliance dashboards behind a 15% improvement in monitored outcomes.

<br/>

<img src="./hd-builds.svg" width="880" alt="builds"/>

**FinSight AI** — financial intelligence platform<br/>
<samp>fastapi · next.js · postgresql · pgvector · docker · github actions</samp>

Agentic RAG over the annual filings of 20+ SGX companies. Decomposes a<br/>
multi-step question into sub-queries and answers with page-level citations.<br/>
Retrieval is full-text plus pgvector, fused by reciprocal rank and reranked by a<br/>
cross-encoder. A RAGAS pipeline in CI holds it to 87% answer faithfulness and<br/>
blocks the merge when it slips.

**Rezonate** — chatbot evaluation platform<br/>
<samp>aws (ec2, s3) · pyspark · hdfs · fastapi · grafana</samp>

An LLM-as-judge framework scoring 5,000+ patient-chatbot conversations for<br/>
response quality, hallucination rate, intent resolution and escalation need.<br/>
Distributed PySpark ETL over 10+ GB of raw logs, with anomaly detection to<br/>
surface the twelve intent categories that needed retraining.

**GlossRide** — driver payments app<br/>
<samp>react native · node.js · express · stripe</samp>

Onboarding, job allocation, invoicing and Stripe payouts, in production with 33<br/>
private-hire drivers on iOS and Android.

**Two-time hackathon runner-up**<br/>
<samp>agent forge ai · smu ai club × agnes ai</samp>

Second place at both: an insurance-claim adjudication system that turns dashcam<br/>
evidence into approve/review/reject decisions, and a rental-inspection platform<br/>
that generates evidence-backed damage reports.

<br/>

<img src="./hd-stack.svg" width="880" alt="stack"/>

<samp>languages&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python, sql, bash, typescript, javascript, java, c++</samp><br/>
<samp>ai&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pytorch, hugging face, scikit-learn, langchain, mcp, rag, llm eval</samp><br/>
<samp>web & data&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fastapi, next.js, react, node, postgresql, pgvector, pyspark</samp><br/>
<samp>infrastructure&nbsp;&nbsp;&nbsp;kubernetes, docker, aws, azure, linux, github actions</samp><br/>
<samp>observability&nbsp;&nbsp;&nbsp;&nbsp;prometheus, grafana, mlflow</samp>

<br/>

<img src="./hd-activity.svg" width="880" alt="activity"/>

<div align="center">

<img src="./stats.svg" width="434" alt="contribution totals for the last 365 days"/>
<img src="./streak.svg" width="434" alt="current and longest contribution streaks"/>

<img src="./langs.svg" width="880" alt="top languages across public repositories"/>

<img src="./year.svg" width="880" alt="a year of contributions, one character per day"/>

</div>

<br/>

<img src="./hd-how-this-page-works.svg" width="880" alt="how this page works"/>

Every graphic above is drawn inside this repository. There are no third-party<br/>
cards, no external image hosts, and no requests leaving GitHub — so there is<br/>
nothing here that can rate-limit, 503, or quietly go dark.

<samp>&nbsp;→&nbsp;</samp> `scripts/make_ascii_svg.py` — photo to self-typing portrait. rembg cut-out,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;bilateral filter, CLAHE, a darkening curve, then 13 characters of ramp.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The typing is SMIL — a clip rect per row, staggered, `fill="freeze"`.<br/>
<samp>&nbsp;→&nbsp;</samp> `scripts/generate_stats.py` — the four data cards, from the GitHub GraphQL<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;API using only the standard library. Runs nightly, commits only on change.<br/>
<samp>&nbsp;→&nbsp;</samp> `scripts/make_headings.py` — the section headings, so they can be set in a<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;typeface GitHub would otherwise strip.<br/>
<samp>&nbsp;→&nbsp;</samp> `scripts/fontkit.py` — subsets JetBrains Mono and inlines it as base64. An<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;external font URL cannot work: these load through `<img>`, and browsers<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;refuse subresource fetches for image documents.

Two details keep the nightly job honest. The contribution window is pinned to<br/>
whole UTC days, or every run would re-bucket the weeks and commit a changed<br/>
sparkline forever. And repositories are filtered to public only, so the numbers<br/>
do not depend on whose token asked.

Full write-up of the approach:<br/>
[A GitHub profile that generates itself](https://agreeable-credit-859.notion.site/A-GitHub-profile-that-generates-itself-3abedfe9a65a81e4afc9daed90cb4e7e).<br/>
Portrait pipeline adapted from the<br/>
[ASCII Portrait README Guide](https://burly-handstand-0dc.notion.site/ASCII-Portrait-README-Guide-3a3e3f86338481f0b545ec8120bbf604).<br/>
Typeface: [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono), SIL OFL 1.1.

<br/>

<img src="./hd-contact.svg" width="880" alt="contact"/>

<samp>&nbsp;→&nbsp;</samp> <a href="mailto:kalairaajan@gmail.com">kalairaajan@gmail.com</a><br/>
<samp>&nbsp;→&nbsp;</samp> <a href="https://linkedin.com/in/kalairaajan">linkedin.com/in/kalairaajan</a><br/>
<samp>&nbsp;→&nbsp;</samp> Singapore
