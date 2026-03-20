"""
Extract PCA coordinates from the 3K RGP PLINK2 PCA output and write
public-safe derived artifacts to data/derived/pca_coordinates/.

Source files (from d:\local\3krgp\analysis\pca\):
  pca.eigenvec  — columns: sample_id, PC1..PC10
  pca.eigenval  — one eigenvalue per line

Output:
  data/derived/pca_coordinates/eigenvalues.json
  data/derived/pca_coordinates/pca_centroids.json   (per study group, anonymised)
  data/derived/pca_coordinates/pca_samples.tsv      (anonymised sample IDs)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RICE_3K = Path(r"d:\local\3krgp")
PCA_DIR = RICE_3K / "analysis" / "pca"
OUT_DIR = REPO_ROOT / "data" / "derived" / "pca_coordinates"

# Map study prefixes to anonymised group labels
STUDY_GROUPS = {
    "IRIS_313-8": "indica",
    "IRIS_313-9": "indica",
    "IRIS_313-10": "temperate_japonica",
    "IRIS_313-11": "temperate_japonica",
    "IRIS_313-7": "tropical_japonica",
    "IRIS_313-6": "aus",
    "IRIS_313-5": "aromatic",
}


def assign_group(sample_id: str) -> str:
    for prefix, label in STUDY_GROUPS.items():
        if sample_id.startswith(prefix):
            return label
    return "other"


def anonymise_id(sample_id: str, idx: int, group: str) -> str:
    """Replace real sample ID with group_NNN."""
    return f"{group}_{idx:04d}"


def load_eigenvec(path: Path) -> tuple[list[str], list[list[float]]]:
    """Parse PLINK-style eigenvec: first col = FID, second = IID, rest = PCs."""
    sample_ids, coords = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        # PCAngsd eigenvec: sample_id  PC1 PC2 ... PCN
        # PLINK eigenvec:   FID IID PC1 ... PCN
        if len(parts) >= 3 and not parts[0].lstrip("-").replace(".", "").isdigit():
            # Looks like sample ID is first col (PCAngsd format)
            sample_ids.append(parts[0])
            coords.append([float(x) for x in parts[1:]])
    return sample_ids, coords


def load_eigenval(path: Path) -> list[float]:
    vals = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            vals.append(float(line))
    return vals


def variance_explained(eigenvalues: list[float]) -> list[float]:
    total = sum(eigenvalues)
    return [round(v / total * 100, 3) for v in eigenvalues]


def compute_centroids(
    anon_ids: list[str],
    groups: list[str],
    coords: list[list[float]],
    n_pcs: int = 5,
) -> dict[str, dict]:
    from collections import defaultdict

    grouped: dict[str, list[list[float]]] = defaultdict(list)
    for g, c in zip(groups, coords):
        grouped[g].append(c[:n_pcs])

    centroids = {}
    for g, vecs in grouped.items():
        n = len(vecs)
        means = [round(sum(v[i] for v in vecs) / n, 6) for i in range(n_pcs)]
        centroids[g] = {"n": n, "pc_means": means}
    return centroids


def main() -> None:
    eigenvec_path = PCA_DIR / "pca.eigenvec"
    eigenval_path = PCA_DIR / "pca.eigenval"

    if not eigenvec_path.exists():
        print(f"ERROR: eigenvec not found at {eigenvec_path}", file=sys.stderr)
        print("Run this script from a machine with glNexus outputs mounted.", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading eigenvec...", end=" ", flush=True)
    sample_ids, coords = load_eigenvec(eigenvec_path)
    print(f"{len(sample_ids)} samples, {len(coords[0])} PCs")

    eigenvalues = load_eigenval(eigenval_path) if eigenval_path.exists() else []
    var_exp = variance_explained(eigenvalues) if eigenvalues else []

    # Anonymise sample IDs
    groups = [assign_group(s) for s in sample_ids]
    group_counters: dict[str, int] = {}
    anon_ids = []
    for s, g in zip(sample_ids, groups):
        group_counters[g] = group_counters.get(g, 0) + 1
        anon_ids.append(anonymise_id(s, group_counters[g], g))

    # Write eigenvalues
    eval_out = {
        "n_pcs": len(eigenvalues),
        "eigenvalues": eigenvalues,
        "variance_explained_pct": var_exp,
        "cumulative_var_pct": [round(sum(var_exp[:i+1]), 3) for i in range(len(var_exp))],
    }
    (OUT_DIR / "eigenvalues.json").write_text(json.dumps(eval_out, indent=2))
    print(f"Written eigenvalues.json  (PC1={var_exp[0] if var_exp else '?'}%)")

    # Write anonymised sample coordinates (PC1-5 only)
    n_pcs_out = min(5, len(coords[0]) if coords else 0)
    tsv_lines = ["sample_id\tgroup\t" + "\t".join(f"PC{i+1}" for i in range(n_pcs_out))]
    for aid, g, c in zip(anon_ids, groups, coords):
        row = [aid, g] + [f"{v:.6f}" for v in c[:n_pcs_out]]
        tsv_lines.append("\t".join(row))
    (OUT_DIR / "pca_samples.tsv").write_text("\n".join(tsv_lines) + "\n", encoding="utf-8")
    print(f"Written pca_samples.tsv  ({len(anon_ids)} samples, PC1-{n_pcs_out})")

    # Write per-group centroids
    centroids = compute_centroids(anon_ids, groups, coords)
    (OUT_DIR / "pca_centroids.json").write_text(json.dumps(centroids, indent=2))
    print(f"Written pca_centroids.json  ({len(centroids)} groups)")


if __name__ == "__main__":
    main()
