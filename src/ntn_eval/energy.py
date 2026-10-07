"""Device energy model, paper eq (5).

E_x = E_sense + E_AI,x + E_access,x + E_tx,x + E_retx,x + E_idle

All quantities are per device over the observation interval. Parameter values
are MODELED (plausible NB-IoT-class numbers), not hardware measurements; the
break-even analysis reports them as a sensitivity range per Sec. VII.D.
"""
import numpy as np


def tx_time_s(H, L, K, R):
    """Payload transmission time (without access), from eq (2)."""
    return K * 8.0 * (H + L) / R


def device_energy(n_obs, reports, ai_mJ, energy_cfg, ntn_cfg,
                  mean_attempts=1.0):
    """Return the eq (5) energy breakdown in Joules for one device."""
    E = energy_cfg
    ntn = ntn_cfg
    T_obs_s = float(n_obs)  # placeholder replaced below
    e_sense = n_obs * E["E_sense_mJ"] / 1000.0
    e_ai = n_obs * ai_mJ / 1000.0
    N = len(reports)
    e_access = N * E["E_access_mJ"] / 1000.0            # first attempts
    e_retx = N * E["E_access_mJ"] / 1000.0 * (mean_attempts - 1.0)  # retries
    t_tx = np.array([tx_time_s(h, l, ntn["K_rep"], ntn["rate_bps"])
                     for h, l in zip(reports["H"], reports["L_app"])])
    e_tx = float(t_tx.sum()) * E["P_tx_W"]
    return {
        "E_sense_J": e_sense, "E_AI_J": e_ai, "E_access_J": e_access,
        "E_tx_J": e_tx, "E_retx_J": max(0.0, e_retx),
        "E_idle_J": None,  # filled by total_energy (needs T_obs)
        "N_reports": N, "n_obs": n_obs,
    }


def total_energy(breakdown, T_obs_s, energy_cfg):
    """Add idle energy and the total."""
    b = dict(breakdown)
    b["E_idle_J"] = energy_cfg["P_sleep_uW"] * 1e-6 * T_obs_s
    b["E_total_J"] = (b["E_sense_J"] + b["E_AI_J"] + b["E_access_J"]
                      + b["E_tx_J"] + b["E_retx_J"] + b["E_idle_J"])
    return b


def net_saving(E_sem_J, E_raw_J):
    """Net energy saving S_E = 1 - E_sem / E_raw."""
    return 1.0 - E_sem_J / E_raw_J


def breakeven_ai_mJ(E_raw_J, E_sem_noAI_J, n_obs):
    """AI energy per inference (mJ) at which S_E = 0.

    E_sem_noAI_J excludes the AI term; solving
    E_sem_noAI + n_obs * ai = E_raw.
    """
    headroom_J = E_raw_J - E_sem_noAI_J
    if headroom_J <= 0:
        return 0.0
    return headroom_J / n_obs * 1000.0
