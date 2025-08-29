# Monitoring & Risk Reflection
## Reflection 

Our momentum + minimum-variance portfolio must be productionized with explicit guardrails across four layers. 
**Data:** upstream price feeds may lag (e.g., corporate actions), drift schemas, or spike nulls—corrupting month-end features and the 60-month Ledoit–Wolf window. 
**Model:** regimes can flip; 12–1 momentum may saturate (all ones), covariance can become ill-conditioned, and weight caps can bind (k·cap<1), making optimization brittle; realized transaction costs may exceed assumptions. 
**System:** batch jobs, the Flask API, or scheduler can fail (timeouts, memory/mutex leaks), yielding stale weights. 
**Business:** after-cost performance may trail SPY/EW, drawdowns can breach limits, or turnover can rise beyond ops capacity, eroding trust.

Mitigation: monitor freshness, completeness, and drift so features remain reliable; track model selection density, turnover, covariance condition number, realized volatility vs. backtest, and rolling Sharpe; instrument p95 latency, error rate, and uptime for services; compare PnL, max drawdown, and net alpha to benchmarks. When thresholds trip, alert owners and execute a safe runbook: freeze new trades, fall back to last-known-good weights or EW/60-40, quarantine inputs, rehydrate data, and restart services with audit logs. Retraining is monthly or trigger-based (feature drift or performance break). Ownership is explicit: Data Engineering owns feeds and schema contracts; MLOps owns pipelines, infra, and dashboards; Quant Research owns model code/metrics and approves parameter changes; the Product/PM owner approves rollbacks and communications. All incidents are logged with SLAs and clear handoffs so recovery is fast and auditable.

## Monitoring Plan

### 1) Failure modes 
- Data freshness lag / schema drift / increased nulls
- Feature drift (PSI) or selection saturation (all 1s)
- Covariance instability / optimizer infeasibility (k·cap < 1)
- API/system faults (5xx, timeouts, missed jobs)
- Business underperformance (net Sharpe, drawdown vs. benchmarks)

### 2) Metric & initial threshold
- Data: freshness ≤ 24h; null rate < 1%; PSI(key monthly returns/vol) < 0.20; missing ticker days < 5/mo
- Model: selection count k ∈ [1, |U|]; turnover ≤ 40%/mo; covariance cond. number < 1e7; rolling 3-mo Sharpe ≥ 0.30; infeasible rate = 0%
- System: uptime ≥ 99%; p95 API latency < 300 ms; 5xx rate < 1%; job SLA miss = 0
- Business: 3-mo max DD not worse than SPY by >5pp; net excess vs. EW ≥ −0.5%/mo; tracking error ≤ 8% (ann.)

### 3) Alerts & first runbook step
- Recipients: Data Eng (data), MLOps (system), Quant (model), PM (business)
- First step: freeze trades; swap to last-known-good weights or EW/60-40; validate inputs and rehydrate data; restart service; open incident ticket

### 4) Retraining cadence / triggers
- Cadence: monthly
- Triggers: PSI ≥ 0.20 on ≥3 key features; 2-week rolling Sharpe < 0.0; covariance cond. number ≥ 1e7; turnover > 50% for 2 consecutive months; selection saturation (all-1s) in ≥80% of last quarter

### 5) Ownership & handoffs
- Data Eng: updates data freshness/drift dashboards; MLOps: service/pipeline dashboards & pager; Quant: model dashboards, code, approvals; PM: rollback approval & comms
- Issues logged in GitHub/Notion with tags; handoffs by label (data/system/model/business) and SLA ownership.


