# ArthaSutra — Portfolio

Shivank Thakur's portfolio site: Streamlit-based, single main script
(`arthasutra_v10.py`), editorial dark/gold design, 11 projects spanning
economics, ML, and operations research.

## Repo structure required for deployment

```
your-repo/
├── arthasutra_v10.py        ← the main app
├── requirements.txt
├── .streamlit/
│   └── config.toml          ← enables static file serving (needed for images/video)
└── static/                  ← all project screenshots, photos, and demo videos
    ├── photo_b64.jpg
    ├── geo_charts_b64.jpg
    ├── grainflow_lead.png
    └── ... (see portfolio_assets.zip for the full set)
```

All four pieces above must sit together at the repo root exactly like this —
Streamlit Cloud (and `enableStaticServing`) serves everything under `static/`
at the path `app/static/<filename>`, which is what the image/video tags in
`arthasutra_v10.py` reference directly (e.g. `app/static/grainflow_lead.png`).

## Local run

```bash
pip install -r requirements.txt
streamlit run arthasutra_v10.py
```

## Deploying (Streamlit Community Cloud)

1. Push the full structure above to a GitHub repo (public or private).
2. On share.streamlit.io, point a new app at `arthasutra_v10.py`.
3. No secrets/API keys are required — the whole site runs with just
   `streamlit` and `plotly`.

## Why a `requirements.txt` this short is correct

The main script only imports `streamlit`, `streamlit.components.v1`, and
`plotly.graph_objects` as third-party packages (`datetime`, `re`, and
`random` are Python standard library — no install needed). Individual
project sub-apps linked from the site (GeoSphere India, PolicySim, GrainFlow)
are separate deployments with their own `requirements.txt` files — this one
is only for the portfolio shell itself.

## Updating content

- **Text/project data**: edit the relevant dict inside `FLAGSHIP_PROJECTS` /
  `STRONG_TECH_PROJECTS` in `arthasutra_v10.py` directly.
- **Images/video**: drop the file into `static/`, then reference it as
  `"app/static/<filename>"` in the relevant project's `images`/`videos` list.
