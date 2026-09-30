#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MRI Gradient Viewer
© Jason Rock 2026

Streamlit version
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="MRI Gradient Viewer",
    layout="centered"
)

st.title("MRI Gradient Viewer")

st.markdown("""
**Interactive visualization of MRI gradient fields**
 
**Notes:**
- The magnetic field values shown on the colour bar are relative.
- Colours represent field strength.
- Arrows represent the direction and magnitude of the magnetic field.
- When B0 is disabled, arrow lengths are scaled for visibility. B0 will always be stronger than any gradient field.
""")


# ---------------------------------------------------------
# PARAMETERS
# ---------------------------------------------------------

B0 = 8.0

MAX_GRADIENT = 0.7

# Slightly smaller grid for faster updates
x = np.linspace(-5, 5, 11)
z = np.linspace(-5, 5, 11)

X, Z = np.meshgrid(x, z)

# Display-only scaling factor
ARROW_SCALE_WITH_B0 = 1
ARROW_SCALE_NO_B0 = 3.0


# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------

st.sidebar.header("Controls")

Gx = st.sidebar.slider(
    "Gx",
    min_value=-MAX_GRADIENT,
    max_value=MAX_GRADIENT,
    value=0.0,
    step=0.1
)

Gz = st.sidebar.slider(
    "Gz",
    min_value=-MAX_GRADIENT,
    max_value=MAX_GRADIENT,
    value=0.0,
    step=0.1
)

show_B0 = st.sidebar.checkbox(
    "Show B0",
    value=True
)


# ---------------------------------------------------------
# FIELD CALCULATION
# ---------------------------------------------------------

def compute_field(Gx, Gz, show_B0=True):

    B = (B0 if show_B0 else 0.0) + Gx * X + Gz * Z

    U = np.zeros_like(B)
    V = B

    return U, V


# ---------------------------------------------------------
# COLOUR LIMITS
# ---------------------------------------------------------

max_x = np.max(np.abs(X))
max_z = np.max(np.abs(Z))

gradient_limit = (
    MAX_GRADIENT * max_x
    + MAX_GRADIENT * max_z
)

global_min_B0 = B0 - gradient_limit
global_max_B0 = B0 + gradient_limit

global_min_noB0 = -gradient_limit
global_max_noB0 = gradient_limit


# ---------------------------------------------------------
# CALCULATE FIELD
# ---------------------------------------------------------

U, V = compute_field(
    Gx,
    Gz,
    show_B0
)

# ---------------------------------------------------------
# DISPLAY SCALING
# (affects arrow size only, not colours)
# ---------------------------------------------------------

if show_B0:
    display_V = V * ARROW_SCALE_WITH_B0
else:
    display_V = V * ARROW_SCALE_NO_B0


# ---------------------------------------------------------
# PLOT
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(4.5, 4.5))

q = ax.quiver(
    X,
    Z,
    U,
    display_V,
    V.flatten(),
    pivot="mid",
    cmap="rainbow",
    scale=170,
    width=0.006
)

if show_B0:

    q.set_clim(
        global_min_B0,
        global_max_B0
    )

else:

    q.set_clim(
        global_min_noB0,
        global_max_noB0
    )

cbar = fig.colorbar(
    q,
    ax=ax
)

if show_B0:

    cbar.set_ticks(
        [global_min_B0, B0, global_max_B0]
    )

else:

    cbar.set_ticks(
        [global_min_noB0, 0, global_max_noB0]
    )

cbar.set_label(
    "Relative Magnetic Field Strength"
)

ax.set_title(
    "MRI Gradient Field (x-z plane)"
)

ax.set_xlabel(
    "x position"
)

ax.set_ylabel(
    "z position"
)

ax.set_aspect(
    "equal"
)

fig.text(
    0.01,
    0.01,
    "MRI Gradient Viewer\n© Jason Rock 2026",
    ha="left",
    va="bottom",
    fontsize=8,
    color="dimgray",
    bbox=dict(
        facecolor="white",
        edgecolor="lightgray",
        alpha=0.8,
        pad=3
    )
)

plt.tight_layout()

st.pyplot(
    fig,
    clear_figure=True,
    use_container_width=False
)


# ---------------------------------------------------------
# INFORMATION PANEL
# ---------------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.write(
    f"Current Gx = {Gx:.1f} mT/m"
)

st.sidebar.write(
    f"Current Gz = {Gz:.1f} mT/m"
)

st.sidebar.write(
    f"Maximum gradient = ±{MAX_GRADIENT:.1f} mT/m"
)

st.markdown("---")
st.markdown("**MRI Gradient Viewer**  \nJason Rock")