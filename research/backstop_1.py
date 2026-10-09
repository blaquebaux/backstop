#!/usr/bin/python3
# =============================================================================
# backstop_1.py — the LIABILITY-DRIVEN book capstone (pension / insurer mandate).
#
# You owe long-dated liabilities; the job is to BACKSTOP them — generate surplus above the liability
# while keeping the FUNDED RATIO from lurching. Assemble the family's liability ingredients:
#   LDI hedge   (binnacle)  → long duration to track the liability
#   spread carry(bedrock)   → credit for surplus return (a compensated risk, so pair with a tail)
#   growth leg              → PLAIN equity, not the endowment replica (banyan's finding)
#   convex tail (contextual_rescue) → long-vol so the surplus survives the spread blowout
# Judged on FUNDED-RATIO terms (surplus vol, funded-ratio drawdown vs a long-duration liability) AND
# absolute terms. Benchmarks: a naive 60/40, pure-LDI (all long bonds), and the liability itself.
# Alpaca SIP daily, total-return; liability proxy = TLT.
# =============================================================================
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from _backstop_common import panel, rets

LIAB = "TLT"

def metrics(r, months):
    r=np.asarray(r,float); c=np.cumprod(1+r); dd=(c/np.maximum.accumulate(c)-1).min()
    sh=r.mean()/r.std()*math.sqrt(252) if r.std()>0 else float("nan"); z=(r-r.mean())/r.std()
    cagr=c[-1]**(252/len(r))-1
    mo={}
    for m,x in zip(months,r): mo[m]=mo.get(m,1.0)*(1+x)
    return dict(sh=sh,cagr=cagr,dd=float(dd),skew=float(np.mean(z**3)),worst=min(v-1 for v in mo.values()))

def funded(asset, liab):
    s=asset-liab; fr=np.cumprod((1+asset)/(1+liab))
    return dict(svol=s.std()*math.sqrt(252), smean=s.mean()*252, fr_dd=float((fr/np.maximum.accumulate(fr)-1).min()), fr_end=fr[-1])

def main():
    syms=["SPY","LQD","TLT","IEF","GLD","VIXM","BIL"]
    P,dates=panel(syms); R={s:rets(P[s]) for s in P}
    L=min(len(R[s]) for s in R); months=[d[:7] for d in dates[1:]][-L:]; r={s:R[s][-L:] for s in R}
    liab=r[LIAB]
    # BACKSTOP: growth + credit carry + LDI hedge + gold + convex tail
    W={"SPY":0.30,"LQD":0.25,"TLT":0.25,"GLD":0.10,"VIXM":0.10}
    bs=sum(W[s]*r[s] for s in W)
    print("="*96); print("BACKSTOP — the liability-driven book capstone (pension / insurer mandate)"); print("="*96)
    print(f"  window {dates[-L]}..{dates[-1]}  ({L/252:.1f}y)   book: "+", ".join(f"{s} {int(W[s]*100)}" for s in W)+"   liability = TLT")

    books={"BACKSTOP":bs, "naive 60/40 (SPY/IEF)":0.6*r["SPY"]+0.4*r["IEF"],
           "pure LDI (all TLT)":r["TLT"], "return-seeking (SPY)":r["SPY"]}
    print(f"\n  ABSOLUTE  {'book':24}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'worstMo':>9}{'skew':>7}")
    for k,v in books.items():
        m=metrics(v,months); print(f"            {k:24}{m['sh']:>+8.2f}{m['cagr']*100:>+7.1f}%{m['dd']*100:>+7.0f}%{m['worst']*100:>+8.1f}%{m['skew']:>+7.2f}")

    print(f"\n  FUNDED-RATIO (vs TLT liability)  {'book':24}{'surplus ret':>12}{'surplus vol':>12}{'FR maxDD':>10}")
    for k,v in books.items():
        f=funded(v,liab); print(f"                                   {k:24}{f['smean']*100:>+11.1f}%{f['svol']*100:>+11.1f}%{f['fr_dd']*100:>+9.0f}%")

    print("\n  CRISIS MONTHS (book return)")
    tests=[("2020-03","COVID"),("2022-09","rate shock"),("2025-04","tariffs")]
    print(f"    {'book':24}"+"".join(f"{lbl:>12}" for _,lbl in tests))
    for k in ("BACKSTOP","naive 60/40 (SPY/IEF)","pure LDI (all TLT)"):
        v=books[k]; row=""
        for mm,_ in tests:
            idx=[i for i,m in enumerate(months) if m==mm]; row+=f"{(np.prod([1+v[i] for i in idx])-1)*100 if idx else float('nan'):>+11.1f}%"
        print(f"    {k:24}{row}")

    print("\n  READ: a liability-driven book earns SURPLUS over the liability with CONTROLLED funded-ratio")
    print("  risk. If BACKSTOP beats the liability (positive surplus) at a smaller funded-ratio drawdown than")
    print("  a naive 60/40 — with the convex tail flipping the crisis months green — it does the job: fund the")
    print("  obligations without betting the funded ratio on rates. The growth leg is plain equity (banyan");
    print("  showed the endowment replica is dominated). backstop_2 = real liability cashflows + after-tax.")

if __name__ == "__main__":
    main()
