#!/usr/bin/env python3
"""
helix-cad-gates / render_views.py — STEP -> one PNG sheet with 6 orthographic views + 1 isometric.

Feeds (a) the CEO Spatial Blindness gate of helix-cad-bridge Step 5 and (b) the intent judge
(helix-cad-judge). Views are labelled with the model axes so a mirror / axis swap is visible.
Pure local: build123d tessellation + matplotlib painter's algorithm (no OpenGL, no network).

Usage: python render_views.py --step model.step --out model_views.png [--title "P1 Chốt"]
Exit: 0 written · 3 IO error.
"""
import argparse
import os
import sys

import numpy as np

VIEWS = [  # (label, view direction = where the camera looks, up vector)
    ("Front (−Y→+Y) · X→ Z↑", (0, 1, 0), (0, 0, 1)),
    ("Back (+Y→−Y)", (0, -1, 0), (0, 0, 1)),
    ("Left (−X→+X)", (1, 0, 0), (0, 0, 1)),
    ("Right (+X→−X)", (-1, 0, 0), (0, 0, 1)),
    ("Top (+Z→−Z) · X→ Y↑", (0, 0, -1), (0, 1, 0)),
    ("Bottom (−Z→+Z)", (0, 0, 1), (0, 1, 0)),
    ("Iso", (-1, 1, -1), (0, 0, 1)),
]


def _basis(d, up):
    d = np.asarray(d, float); d /= np.linalg.norm(d)
    up = np.asarray(up, float)
    right = np.cross(d, up); right /= np.linalg.norm(right)
    true_up = np.cross(right, d)
    return d, right, true_up


def render(step, out, title=None, tol=0.2):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    from build123d import import_step
    shape = import_step(step)
    verts, tris = shape.tessellate(tol, 0.3)
    V = np.array([[v.X, v.Y, v.Z] for v in verts])
    T = np.array(tris)
    tri = V[T]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    nn = np.linalg.norm(n, axis=1, keepdims=True); nn[nn == 0] = 1; n = n / nn
    fig, axes = plt.subplots(2, 4, figsize=(20, 10), dpi=110)
    for ax, (label, d, up) in zip(axes.flat, VIEWS):
        d, r, u = _basis(d, up)
        pts2 = np.stack([tri @ r, tri @ u], axis=-1)
        depth = (tri @ d).mean(axis=1)
        facing = (n @ d) < 0  # back-face culling: long tessellation triangles defeat pure depth sorting
        order = [i for i in np.argsort(-depth) if facing[i]]  # far first, front-facing only
        shade = np.clip(-(n @ d), 0, 1)
        cols = [(0.35 + 0.6 * s,) * 3 for s in shade[order]]
        ax.add_collection(PolyCollection(pts2[order], facecolors=cols, edgecolors=(0, 0, 0, 0.15), linewidths=0.2))
        ax.autoscale(); ax.set_aspect("equal"); ax.set_title(label, fontsize=10)
        ax.tick_params(labelsize=7)
    bb = shape.bounding_box()
    axes.flat[-1].axis("off")
    axes.flat[-1].text(0.02, 0.6, f"{title or os.path.basename(step)}\nbbox X×Y×Z = "
                       f"{bb.size.X:.2f} × {bb.size.Y:.2f} × {bb.size.Z:.2f} mm\nvolume = {shape.volume:,.0f} mm³",
                       fontsize=12, va="top")
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render 6 orthographic views + iso of a STEP to one PNG.")
    ap.add_argument("--step", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title")
    a = ap.parse_args(argv)
    if not os.path.exists(a.step):
        print(f"[IO-ERROR] no STEP: {a.step}", file=sys.stderr)
        return 3
    print(render(a.step, a.out, a.title))
    return 0


if __name__ == "__main__":
    sys.exit(main())
