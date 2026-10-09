# backstop

**The liability-driven book capstone — pension / insurer mandate.**

You owe long-dated liabilities; the job is to *backstop* them — earn **surplus** over the liability
while keeping the **funded ratio** from lurching. This assembles the family's liability ingredients into
one book and judges it on funded-ratio terms (surplus vol, funded-ratio drawdown vs a long-duration
liability), not raw return:

- **LDI hedge** ([`binnacle`](https://github.com/blaquebaux/binnacle)) — long duration to track the liability
- **spread carry** ([`bedrock`](https://github.com/blaquebaux/bedrock)) — credit for surplus return
- **growth leg** — *plain equity*, because [`banyan`](https://github.com/blaquebaux/banyan) showed the endowment replica is dominated
- **convex tail** ([`contextual_rescue`](https://github.com/blaquebaux/nullbar/blob/main/contextual_rescue.py)) — long-vol so the surplus survives the spread blowout

Book: SPY 30 · LQD 25 · TLT 25 · GLD 10 · VIXM 10. Liability proxy = TLT. Alpaca SIP daily.

## Verdict

**KEEPER (liability mandate).** backstop earns a positive surplus over the liability at a far smaller
funded-ratio drawdown than a naive 60/40, with positive skew and crisis convexity. It does the mandate's
actual job — fund the obligations without betting the funded ratio on rates — and it gives up absolute
return to do it, which is the right trade for a plan.

**Funded-ratio (the mandate's scorecard, vs a TLT liability):**

| book | surplus ret | surplus vol | funded-ratio maxDD |
|---|---|---|---|
| **BACKSTOP** | +5.9% | **+10.9%** | **−22%** |
| naive 60/40 | +9.7% | +17.4% | −37% |
| pure LDI (all TLT) | 0.0% | 0.0% | 0% |
| return-seeking (SPY) | +15.4% | +24.5% | −48% |

**Absolute terms:**

| book | Sharpe | CAGR | maxDD | skew |
|---|---|---|---|---|
| BACKSTOP | +0.85 | +6.0% | −21% | **+0.16** |
| naive 60/40 | +0.93 | +9.7% | −21% | −0.24 |
| SPY | +0.88 | +15.0% | −34% | −0.35 |

*2016-01 … 2026-07 (10.5y).*

- **Positive surplus at controlled funded-ratio risk.** backstop beats the liability by +5.9%/yr while
  cutting the funded-ratio drawdown to −22% (vs −37% for a naive 60/40 and −48% for all-equity). Its
  surplus *efficiency* is on par with 60/40, but its funded-ratio *drawdown* — the thing that makes a plan
  underfunded — is far shallower, and its skew is positive where 60/40's is negative.
- **Crisis convexity:** green in COVID (+3.1%) and the 2025 tariff tantrum (+1.7%), −6.0% in the 2022 rate
  shock (vs 60/40 −7.4%, pure-LDI −8.2%). The long-vol tail (the rescued null) pays when the surplus would
  otherwise crater — the lesson from `contextual_rescue`, applied to a liability book.
- **Pure LDI is flat by construction** (0% surplus, 0% funded-ratio drawdown — it *is* the liability); the
  point of backstop is to add surplus *without* reintroducing the funded-ratio swings a return-seeking book
  carries.

## `backstop_2`

Real **actuarial liability cashflows** (not a TLT proxy) with key-rate hedging, plus after-tax treatment
and realistic rebalancing/tail-layer friction — the honest plan-level build the ETF proxy only approximates.

## Reproduce

```bash
export ALPACA_KEY_ID=... ALPACA_SECRET_KEY=...
python3 research/backstop_1.py
```

## Capstone family

`backstop` (liability) joins [`bulkhead`](https://github.com/blaquebaux/bulkhead) (preservation / FO),
[`belligerent`](https://github.com/blaquebaux/belligerent) (aggressive / HF), and
[`brawl`](https://github.com/blaquebaux/brawl) (doctrine) — same keeper ingredients, different mandates.

---

*Blaque Baux — a Carter Warrens research initiative. Research only; not investment advice. The verdict
falls where the data puts it — a plan is judged by its funded ratio, not its return.*
