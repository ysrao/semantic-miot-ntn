"""Stage 2: NTN access and channel simulation (paper Sec. VII.B).

Maps each admitted report into access attempts, transmission time, repetitions,
success/failure and delay under a common LEO contact trace:

  * Bent-pipe store-and-forward: reports generated between passes wait for the
    next contact window.
  * Slotted random access within a pass: a report picks a random slot; the
    attempt succeeds iff no background report chose the same slot.
    Per-attempt success p = exp(-G) with offered slot load G (slotted ALOHA,
    Poisson arrivals). Retries inflate G; a fixed-point iteration accounts
    for the retry load (up to ``max_attempts``, then defer to next pass).
  * Both independent (Poisson) and geographically correlated burst arrivals.

The population sweep finds the largest M with
Pr(delivery delay <= D) >= deadline_success_target, i.e. supported devices
per beam from access constraints rather than linear payload extrapolation.
"""
import numpy as np

SEC_PER_DAY = 86400.0


def pass_starts(ntn):
    """Start times (s) of the contact windows within one day."""
    ppd = ntn["passes_per_day"]
    spacing = SEC_PER_DAY / ppd
    return np.arange(ppd) * spacing, ntn["pass_duration_s"]


def _fixed_point_G(G0, max_attempts, iters=50):
    """Solve G = G0 * E[attempts | G] for the retry-inflated slot load.

    E[attempts] is the truncated geometric sum_{k<max_att} (1-p)^k, which is
    numerically stable for p -> 0 (unlike (1-(1-p)^m)/p, which underflows).
    """
    G = G0
    for _ in range(iters):
        p = float(np.exp(-G))
        E_att = float(sum((1.0 - p) ** k for k in range(max_attempts)))
        G_new = G0 * E_att
        if abs(G_new - G) < 1e-9 * max(1.0, G):
            G = G_new
            break
        G = G_new
    return G


def simulate_reports(rng, n_reports, G, ntn, t_msg_mean, deadline_s, burst=False):
    """Monte-Carlo delivery of n_reports under slot load G.

    Returns dict with per-report delays and summary statistics.
    """
    starts, dur = pass_starts(ntn)
    spacing = SEC_PER_DAY / ntn["passes_per_day"]
    max_att = ntn["max_attempts"]
    backoff = ntn["backoff_s"]
    p = float(np.exp(-G))
    slot_s = ntn["T_RA_s"] + t_msg_mean
    n_slots = max(1, int(dur / slot_s))
    T_tx = t_msg_mean - ntn["T_RA_s"]

    delays = np.zeros(n_reports)
    attempts = np.zeros(n_reports)
    ok = np.zeros(n_reports, dtype=bool)
    for r in range(n_reports):
        t_gen = rng.random() * SEC_PER_DAY
        # next pass start >= t_gen (store-and-forward wait)
        k = int(np.ceil(t_gen / spacing - 1e-9)) % ntn["passes_per_day"]
        t = starts[k]
        if t < t_gen:
            t = t_gen  # inside a pass already (edge case)
        delivered = False
        total_att = 0
        while not delivered:
            # attempts within this pass (fresh attempt budget each pass)
            t_att = max(t, t_gen)
            att = 0
            while att < max_att:
                total_att += 1
                if rng.random() < p:
                    t_del = t_att + ntn["T_RA_s"] + T_tx
                    delivered = True
                    break
                att += 1
                t_att += backoff + rng.random() * backoff
                if t_att > t + dur:  # ran out of pass -> defer
                    break
            if delivered:
                break
            # defer to next pass
            k = (k + 1) % ntn["passes_per_day"]
            t = t + spacing
            if t - t_gen > 3 * SEC_PER_DAY:  # give up after 3 days
                break
        delays[r] = (t_del - t_gen) if delivered else np.inf
        attempts[r] = total_att
        ok[r] = delivered
    finite = np.isfinite(delays)
    dsucc = np.mean((delays <= deadline_s) & finite)
    return {
        "delay_s": delays, "attempts": attempts, "delivered": ok,
        "p_attempt": p, "G": G, "n_slots": n_slots,
        "mean_attempts": float(attempts.mean()),
        "mean_delay_s": float(delays[finite].mean()) if finite.any() else float("inf"),
        "deadline_success": float(dsucc),
        "deliver_fail": float(1 - finite.mean()),
    }


def evaluate_mode(rng, M, reports_per_day_per_dev, t_msg_mean, ntn, deadline_s,
                  burst_extra_per_pass=0.0, n_mc=None):
    """Evaluate one (population, mode) point.

    burst_extra_per_pass: additional correlated reports landing in one pass
    (geographically correlated burst stress test).
    """
    n_mc = n_mc or ntn["n_mc_reports"]
    ppd = ntn["passes_per_day"]
    dur = ntn["pass_duration_s"]
    slot_s = ntn["T_RA_s"] + t_msg_mean
    n_slots = max(1, int(dur / slot_s))
    R_pass = M * reports_per_day_per_dev / ppd + burst_extra_per_pass
    G0 = R_pass / n_slots
    G = _fixed_point_G(G0, ntn["max_attempts"])
    res = simulate_reports(rng, n_mc, G, ntn, t_msg_mean, deadline_s)
    res["M"] = M
    res["G0"] = G0
    res["R_pass"] = R_pass
    res["burst"] = burst_extra_per_pass > 0
    return res


def supported_devices(rng, reports_per_day_per_dev, t_msg_mean, ntn, deadline_s,
                      burst_extra_frac=0.0):
    """Sweep the population grid; return supported M and the full sweep table."""
    rows = []
    for M in ntn["pop_grid"]:
        burst_extra = burst_extra_frac * M  # correlated cluster reports in one pass
        r = evaluate_mode(rng, M, reports_per_day_per_dev, t_msg_mean, ntn,
                          deadline_s, burst_extra_per_pass=burst_extra)
        rows.append(r)
    target = ntn["deadline_success_target"]
    ok_M = [r["M"] for r in rows if r["deadline_success"] >= target]
    return (max(ok_M) if ok_M else 0), rows
