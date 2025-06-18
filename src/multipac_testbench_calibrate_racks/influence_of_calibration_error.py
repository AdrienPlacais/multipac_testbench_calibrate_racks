#!/usr/bin/env python3
"""Evaluate the influence of calibration error on measured voltage."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray


def v_coax_from_acqui(
    v_acqui: NDArray,
    a_rack: float,
    b_rack: float,
    g_probe: float,
    z_0: float = 50.0,
) -> NDArray:
    """Compute voltage in V from acquisition voltage in [0, 10V]."""
    superscript = (abs(g_probe + 3) + a_rack * v_acqui + b_rack) / 10.0
    return np.sqrt(2e-3 * z_0 * np.power(10, superscript))


def error_study(
    delta_a_rack: float,
    delta_b_rack: float,
    delta_g_probe: float = 0.0,
    a_rack: float = 10.30,
    b_rack: float = -51.74,
    g_probe: float = -77.2,
    v_acqui: NDArray | None = None,
) -> pd.DataFrame:
    """Compute error envelopes.

    Default values for ``a_rack``, ``b_rack``, ``g_probe`` are taken from E1
    120MHz settings.

    All errors ``delta_`` must be given positive.

    """
    if v_acqui is None:
        v_acqui = np.linspace(0.0, 10.0, 1001)
    x_label = "Acquisition voltage [V]"
    mini = v_coax_from_acqui(
        v_acqui,
        a_rack - delta_a_rack,
        b_rack - delta_b_rack,
        g_probe + delta_g_probe,
    )
    nominal = v_coax_from_acqui(v_acqui, a_rack, b_rack, g_probe)
    maxi = v_coax_from_acqui(
        v_acqui,
        a_rack + delta_a_rack,
        b_rack + delta_b_rack,
        g_probe - delta_g_probe,
    )
    data = pd.DataFrame(
        {
            x_label: v_acqui,
            "mini": mini,
            "nominal": nominal,
            "maxi": maxi,
        }
    )
    ax = data.plot(x=x_label, grid=True)
    ax.set_ylabel("Actual voltage [V]")
    ax.set_yscale("log")

    error = pd.DataFrame(
        {
            "Between nominal and min": 100.0
            * np.abs((nominal - mini) / nominal),
            "Between nominal and max": 100.0
            * np.abs((nominal - maxi) / nominal),
            x_label: v_acqui,
        }
    )
    ax = error.plot(x=x_label, grid=True)
    ax.set_ylabel("Relative error [%]")

    return data


if __name__ == "__main__":
    error_study(
        delta_a_rack=2e-2,
        delta_b_rack=6e-1,
        v_acqui=np.linspace(0.0, 4.0, 1001),
    )
    plt.show()
