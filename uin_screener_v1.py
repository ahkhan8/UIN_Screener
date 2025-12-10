# uin_screener_v1.py
import os
from datetime import timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="PSX UIN Participation Screener", layout="wide")

# ─── Paths ──────────────────────────────────────────────────────────────────────
DATA_FOLDER = os.path.join(os.getcwd(), "Settlement_Output")

# ─── Index constituents ─────────────────────────────────────────────────────────
KSE100_STOCKS = [
    "KEL","PIBTL","BOP","PTC","PAEL","SEARL","CNERGY","SSGC","FCCL","DHPL","HUBC","NBP","PPL",
    "MLCF","HUMNL","SNGP","AIRLINK","TRG","YOUW","FFL","PSO","OGDC","AKBL","FFC","UNITY","ATRL",
    "ILP","LUCK","SYS","DGKC","MEBL","ENGROH","MARI","PSX","HBL","CPHL","KAPCO","NML","FHAM","ISL",
    "TGL","EFERT","LOTCHEM","FABL","FATIMA","DCR","NATF","GHGL","AGP","BAFL","GAL","AICL","JVDC",
    "PIOC","HCAR","UBL","KOHC","HGFA","GHNI","MTL","APL","BAHL","MCB","POL","PABC","PKGP","GLAXO",
    "KTML","SAZEW","COLG","INIL","HALEON","CHCC","LCI","ABL","TPLRF1","SCBPL","PKGS","BWCL","SSOM",
    "PSEL","HINOON","GADT","SHFA","INDU","SRVI","ATLH","JDWS","MEHT","PAKT","BNWM","ABOT","PGLC",
    "IBFL","HMB","NESTLE","RMPL","UPFL","MUREB","THALL"
]
KMIALLSHR_STOCKS = [
    "KEL","PIBTL","TELE","PAEL","BECO","PRL","SEARL","CNERGY","FECTC","SSGC","TREET","QUICE","CEPB",
    "POWER","FCCL","HUBC","CTM","PPL","MLCF","SNGP","WASL","DCL","YOUW","TOMCL","FFL","PSO","GGGL",
    "OGDC","GCIL","UNITY","MACFL","ATRL","TPLP","BNL","SLGL","ASL","UCAPM","ITTEFAQ","ILP","LUCK",
    "SYS","DGKC","BIPL","OBOY","FFLM","GATM","FCL","MEBL","ENGROH","MUGHAL","GGL","PREMA","MARI",
    "GWLC","CPHL","EPCL","NML","IMAGE","FHAM","ISL","TGL","EFERT","FLYNG","LOTCHEM","DOL","FABL",
    "FATIMA","IREIT","SYM","DCR","LIVEN","NATF","IDRT","GHGL","FEM","FPJM","GATI","AGP","AVN",
    "BFAGRO","GAL","JVDC","PIOC","ANL","HCAR","RPL","BGL","KML","GHNI","AGSML","IPAK","DYNO","MTL",
    "DFSM","APL","SPEL","ALNRS","OCTOPUS","SPWL","BBFL","HTL","GTYR","NETSOL","FCEPL","EMCO","SGF",
    "FEROZ","SHCM","STCL","PAKOXY","BFBIO","GLAXO","WAFI","DLL","FPRM","SGPL","ICL","JSML","BRRG",
    "FRCL","SAZEW","TPLT","AGTL","ICCI","BCL","KSBP","TRSM","ANTM","BPL","MIRKS","INIL","HALEON",
    "SERT","CHCC","SURC","BFMOD","LCI","FECM","ORM","ECOP","MACTER","SARC","OLPM","UDPL","TPLRF1",
    "FTMM","IBLHL","PKGS","BWCL","MERIT","CPPL","KOHE","SSOM","PSEL","GFIL","HINOON","GEMSPNL",
    "BERG","CRTM","KOHTM","ZAHID","CLOV","PPP","STYLERS","MFFL","LEUL","GOC","EXIDE","HINO","SHFA",
    "ARCTM","ATBA","LPGL","BWHL","SHDT","ARPL","DAAG","REDCO","SEL","HRPL","UBDL","ASHT","POML",
    "GLPL","STJT","BIFO","MSCL","JDWS","MQTM","AHTM","BATA","SITC","SHEZ","FRSM","SASML","SMCPL",
    "ADAMS","DINT","WAHN","FZCM","BNWM","ZIL","FIBLM","ABOT","SINDM","SNAI","FML","NRSL","CCM",
    "IBFL","OML","HAEL","SCL","INKL","NESTLE","FTSM","TICL","RUPL","SZTM","AABS","KPUS","ELCM",
    "KHYT","FIMM","CFL","RMPL","UPFL","IDSM","PSYL","CLVL","GVGL","TCORP","PAKD","HPL","FANM",
    "DADX","KCL","PIM","HAFL","SFL","TOWL","AGIL","AKGL","AWTX","BTL","BUXL","GEMBCEM","GEMBLUEX",
    "GEMMEL","GEMPAPL","GIL","JDMT","NSRM","RCML","SANSM","SHSML","STL","STML","ZTL"
]

# ─── Helpers ────────────────────────────────────────────────────────────────────
ALT_DATE = ["Date", "DATE"]
ALT_SYMBOL = ["Symbol", "SYMBOL", "Company Symbol"]
ALT_UINPCT = ["UIN % Volume", "UIN% Volume", "UIN %Volume",
              "UIN Percentage Volume", "UIN Percentage Volume "]
ALT_TRADVOL = ["Trade Volume", "Trade Volume ", "Traded Volume", "Volume Traded"]

def _first_present(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None

def _standardize_schema(df: pd.DataFrame) -> pd.DataFrame:
    # strip and normalize NBSPs
    df.columns = df.columns.str.strip().str.replace("\u00A0", " ", regex=True)

    # Map alternates to canonical
    colmap = {}
    present = set(df.columns)

    d = _first_present(present, ALT_DATE)
    s = _first_present(present, ALT_SYMBOL)
    u = _first_present(present, ALT_UINPCT)
    tv = _first_present(present, ALT_TRADVOL)

    if d and d != "Date": colmap[d] = "Date"
    if s and s != "Symbol": colmap[s] = "Symbol"
    if u and u != "UIN % Volume": colmap[u] = "UIN % Volume"
    if tv and tv != "Trade Volume": colmap[tv] = "Trade Volume"

    if colmap:
        df = df.rename(columns=colmap)

    # Required columns
    must_have = {"Date", "Symbol"}
    missing = must_have - set(df.columns)
    if missing:
        st.error(f"Missing required columns: {', '.join(sorted(missing))}. Found: {list(df.columns)}")
        return pd.DataFrame()

    # Parse Date -> datetime.date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    df = df.dropna(subset=["Date"])

    # Optional numeric coercions
    if "UIN % Volume" in df.columns:
        df["UIN % Volume"] = pd.to_numeric(df["UIN % Volume"], errors="coerce")
    if "Trade Volume" in df.columns:
        df["Trade Volume"] = pd.to_numeric(df["Trade Volume"], errors="coerce")

    # Normalize Symbol
    df["Symbol"] = df["Symbol"].astype(str).str.strip().str.upper()
    return df

# ─── Data loader ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(period: str) -> pd.DataFrame:
    file_map = {
        "Daily": "combined_daily.csv",
        "Weekly": "aggregated_weekly.csv",
        "Monthly": "aggregated_monthly.csv",
    }
    path = os.path.join(DATA_FOLDER, file_map[period])
    if not os.path.exists(path):
        st.error(f"File not found: {path}")
        return pd.DataFrame()

    df = pd.read_csv(path, thousands=",", encoding_errors="ignore")
    df = _standardize_schema(df)
    return df

# NEW: helper to build KMIALLSHR ≥ 70% summary based on last 2 periods
def build_kmiallshr_70_summary(uin_threshold: float = 70.0) -> pd.DataFrame:
    """
    For each KMIALLSHR symbol and each period (Daily/Weekly/Monthly),
    mark it if the last TWO observations in that dataset have
    UIN % Volume >= uin_threshold.
    """
    period_syms: dict[str, set] = {}

    for per in ["Daily", "Weekly", "Monthly"]:
        dfp = load_data(per)
        if dfp.empty or "UIN % Volume" not in dfp.columns:
            period_syms[per] = set()
            continue

        # only KMIALLSHR symbols, drop NaNs
        dfp = dfp[dfp["Symbol"].isin(KMIALLSHR_STOCKS)].copy()
        dfp = dfp.dropna(subset=["UIN % Volume"])
        if dfp.empty:
            period_syms[per] = set()
            continue

        ok_syms = set()

        # check last 2 observations for each symbol
        for sym, g in dfp.groupby("Symbol"):
            g = g.sort_values("Date")
            if len(g) < 2:
                continue  # need at least 2 points
            last2 = g.tail(2)
            if (last2["UIN % Volume"] >= uin_threshold).all():
                ok_syms.add(sym)

        period_syms[per] = ok_syms

    # union of all symbols that satisfy any timeframe
    all_symbols = sorted(set().union(*period_syms.values()))
    if not all_symbols:
        return pd.DataFrame()

    rows = []
    for sym in all_symbols:
        rows.append({
            "Symbol": sym,
            "Daily ≥ 70% (last 2 days)": "✅" if sym in period_syms.get("Daily", set()) else "",
            "Weekly ≥ 70% (last 2 weeks)": "✅" if sym in period_syms.get("Weekly", set()) else "",
            "Monthly ≥ 70% (last 2 months)": "✅" if sym in period_syms.get("Monthly", set()) else "",
        })

    return pd.DataFrame(rows)

def compute_kmiallshr_signal_lists():
    """
    Returns three lists of KMIALLSHR symbols:

    - daily_list: UIN % Volume ≥ 80 for the last 3 *daily* observations
    - weekly_list: UIN % Volume ≥ 65 for the last *weekly* observation
    - monthly_list: UIN % Volume ≥ 60 for the last *monthly* observation
    """
    daily_list = []
    weekly_list = []
    monthly_list = []

    # ----- Daily: ≥ 80 for last 3 observations -----
    df_day = load_data("Daily")
    if not df_day.empty and "UIN % Volume" in df_day.columns:
        df_day = df_day[df_day["Symbol"].isin(KMIALLSHR_STOCKS)].copy()
        df_day = df_day.dropna(subset=["UIN % Volume"])
        for sym, g in df_day.groupby("Symbol"):
            g = g.sort_values("Date")
            if len(g) < 3:
                continue
            last3 = g.tail(3)
            if (last3["UIN % Volume"] >= 80).all():
                daily_list.append(sym)
        daily_list = sorted(daily_list)

    # ----- Weekly: ≥ 65 for last week -----
    df_week = load_data("Weekly")
    if not df_week.empty and "UIN % Volume" in df_week.columns:
        df_week = df_week[df_week["Symbol"].isin(KMIALLSHR_STOCKS)].copy()
        df_week = df_week.dropna(subset=["UIN % Volume"])
        if not df_week.empty:
            last_week_date = df_week["Date"].max()
            last_week = df_week[df_week["Date"] == last_week_date]
            weekly_list = sorted(
                last_week.loc[last_week["UIN % Volume"] >= 65, "Symbol"]
                .unique()
                .tolist()
            )

    # ----- Monthly: ≥ 60 for last month -----
    df_month = load_data("Monthly")
    if not df_month.empty and "UIN % Volume" in df_month.columns:
        df_month = df_month[df_month["Symbol"].isin(KMIALLSHR_STOCKS)].copy()
        df_month = df_month.dropna(subset=["UIN % Volume"])
        if not df_month.empty:
            last_month_date = df_month["Date"].max()
            last_month = df_month[df_month["Date"] == last_month_date]
            monthly_list = sorted(
                last_month.loc[last_month["UIN % Volume"] >= 60, "Symbol"]
                .unique()
                .tolist()
            )

    return daily_list, weekly_list, monthly_list

# ─── Sidebar controls ───────────────────────────────────────────────────────────
st.sidebar.title("📊 UIN Screener Controls")
period = st.sidebar.selectbox("Select period:", ["Daily", "Weekly", "Monthly"])
index_choice = st.sidebar.selectbox("Filter by Index:", ["ALLSHR (All Stocks)", "KSE100", "KMIALLSHR"])
threshold_uin = st.sidebar.slider("Minimum UIN % Volume", 0, 100, 60)

st.sidebar.markdown("**Minimum Trade Volume (Millions)**")
min_trade_vol_m = st.sidebar.number_input(
    label="",
    min_value=0.0, value=50.0, step=0.5,
    help="Rows with Trade Volume below this (in millions) will be filtered out."
)
min_trade_vol_abs = int(min_trade_vol_m * 1_000_000)

symbol_search = st.sidebar.text_input("Filter by symbol (optional):").strip().upper()

# ─── Load dataframe NOW (prevents NameError) ────────────────────────────────────
df = load_data(period)
if df.empty:
    st.warning("No data available after loading. Check your CSVs under Settlement_Output.")
    st.stop()

# ─── Date range filter ──────────────────────────────────────────────────────────
min_date = df["Date"].min()
max_date = df["Date"].max()
default_start = max(min_date, max_date - timedelta(days=30))
date_range = st.sidebar.date_input(
    "Date range",
    value=(default_start, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple):
    date_start, date_end = date_range
else:
    date_start = date_end = date_range

df = df[(df["Date"] >= date_start) & (df["Date"] <= date_end)].copy()
if df.empty:
    st.warning("No rows within the selected date range.")
    st.stop()

# ─── Ensure needed analysis columns ─────────────────────────────────────────────
needed = {"UIN % Volume", "Trade Volume"}
missing_needed = [c for c in needed if c not in df.columns]
if missing_needed:
    st.error(f"Missing columns for analysis: {', '.join(missing_needed)}")
    st.stop()

# ─── Index filter ───────────────────────────────────────────────────────────────
if index_choice == "KSE100":
    df = df[df["Symbol"].isin(KSE100_STOCKS)]
elif index_choice == "KMIALLSHR":
    df = df[df["Symbol"].isin(KMIALLSHR_STOCKS)]
if df.empty:
    st.info("No symbols left after index filter.")
    st.stop()

# ─── Threshold + symbol filter ──────────────────────────────────────────────────
filtered = df[
    (df["UIN % Volume"] >= threshold_uin) &
    (df["Trade Volume"] >= min_trade_vol_abs)
].copy()

if symbol_search:
    filtered = filtered[filtered["Symbol"].str.contains(symbol_search, case=False, na=False)].copy()

filtered["Trade Volume (M)"] = (filtered["Trade Volume"] / 1_000_000).round(2)

# ─── Header ────────────────────────────────────────────────────────────────────
st.title("📈 PSX UIN Participation Screener")
st.caption(
    f"{period} data | Index: {index_choice} | UIN ≥ {threshold_uin}% | "
    f"Trade Volume ≥ {min_trade_vol_m:.2f}M | Dates: {date_start} → {date_end}"
)

# ─── KMIALLSHR high-UIN shortlists (interactive) ───────────────────────────────
st.subheader("🎯 KMIALLSHR High-UIN Shortlists")

daily_list, weekly_list, monthly_list = compute_kmiallshr_signal_lists()

# Load full daily data once for detail view
df_daily_full = load_data("Daily")
df_daily_full = df_daily_full[
    df_daily_full["Symbol"].isin(KMIALLSHR_STOCKS)
].copy()
df_daily_full = df_daily_full.sort_values("Date")

tabs = st.tabs([
    "Daily (≥ 80%, last 3 daily obs)",
    "Weekly (≥ 65%, last week)",
    "Monthly (≥ 60%, last month)",
])

# ---- Daily tab ----
with tabs[0]:
    st.caption("KMIALLSHR stocks where UIN % Volume ≥ 80 for each of the last 3 daily observations.")
    if daily_list:
        st.dataframe(
            pd.DataFrame({"Symbol": daily_list}),
            hide_index=True,
            use_container_width=True,
            height=200,  # makes it scrollable
        )
        daily_symbol = st.selectbox(
            "Click / select a ticker to see last 3 daily rows:",
            daily_list,
            key="daily_symbol_select",
        )
        if daily_symbol:
            df_sym = df_daily_full[df_daily_full["Symbol"] == daily_symbol].tail(3)
            st.markdown(f"**Last 3 daily rows for `{daily_symbol}`**")
            st.dataframe(
                df_sym[["Date", "Symbol", "UIN % Volume", "Trade Volume"]],
                hide_index=True,
                use_container_width=True,
            )
    else:
        st.caption("No KMIALLSHR symbols meet this daily condition.")

# ---- Weekly tab ----
with tabs[1]:
    st.caption("KMIALLSHR stocks where UIN % Volume ≥ 65 in the last weekly observation.")
    if weekly_list:
        st.dataframe(
            pd.DataFrame({"Symbol": weekly_list}),
            hide_index=True,
            use_container_width=True,
            height=200,
        )
        weekly_symbol = st.selectbox(
            "Click / select a ticker to see last 3 daily rows:",
            weekly_list,
            key="weekly_symbol_select",
        )
        if weekly_symbol:
            df_sym = df_daily_full[df_daily_full["Symbol"] == weekly_symbol].tail(3)
            st.markdown(f"**Last 3 daily rows for `{weekly_symbol}`**")
            st.dataframe(
                df_sym[["Date", "Symbol", "UIN % Volume", "Trade Volume"]],
                hide_index=True,
                use_container_width=True,
            )
    else:
        st.caption("No KMIALLSHR symbols meet this weekly condition.")

# ---- Monthly tab ----
with tabs[2]:
    st.caption("KMIALLSHR stocks where UIN % Volume ≥ 60 in the last monthly observation.")
    if monthly_list:
        st.dataframe(
            pd.DataFrame({"Symbol": monthly_list}),
            hide_index=True,
            use_container_width=True,
            height=200,
        )
        monthly_symbol = st.selectbox(
            "Click / select a ticker to see last 3 daily rows:",
            monthly_list,
            key="monthly_symbol_select",
        )
        if monthly_symbol:
            df_sym = df_daily_full[df_daily_full["Symbol"] == monthly_symbol].tail(3)
            st.markdown(f"**Last 3 daily rows for `{monthly_symbol}`**")
            st.dataframe(
                df_sym[["Date", "Symbol", "UIN % Volume", "Trade Volume"]],
                hide_index=True,
                use_container_width=True,
            )
    else:
        st.caption("No KMIALLSHR symbols meet this monthly condition.")


# ─── 1) Automatic Top 5 chart ──────────────────────────────────────────────────
if not filtered.empty:
    st.subheader("📊 Top 5 Symbols by mean UIN % Volume")
    top5 = (
        filtered.groupby("Symbol", as_index=False)["UIN % Volume"].mean()
        .sort_values("UIN % Volume", ascending=False)
        .head(5)["Symbol"]
        .tolist()
    )
    df_top = df[df["Symbol"].isin(top5)].sort_values("Date")
    if not df_top.empty:
        fig_auto = px.line(
            df_top, x="Date", y="UIN % Volume", color="Symbol",
            title="Top 5 UIN % Volume Trends", markers=True
        )
        fig_auto.update_layout(yaxis_title="UIN % Volume (%)")
        st.plotly_chart(fig_auto, use_container_width=True)
    else:
        st.info("No data available for Top 5 chart after current filters.")
else:
    st.info("No rows meet the UIN/Volume thresholds for the Top 5 chart.")

# ─── 2) Manual comparison chart ────────────────────────────────────────────────
st.subheader("📉 UIN % and Trade Volume Trends (Manual Selection)")
all_symbols = sorted(df["Symbol"].unique().tolist())
default_pick = all_symbols[:5] if len(all_symbols) >= 5 else all_symbols
selected_symbols = st.multiselect(
    "Select symbols to visualize (max 5):",
    all_symbols,
    default=default_pick,
    max_selections=5,
)

if selected_symbols:
    df_sel = df[df["Symbol"].isin(selected_symbols)].sort_values("Date")
    fig = go.Figure()
    for s in selected_symbols:
        d = df_sel[df_sel["Symbol"] == s]
        fig.add_trace(go.Scatter(x=d["Date"], y=d["UIN % Volume"],
                                 mode="lines+markers", name=f"{s} UIN %", yaxis="y1"))
        fig.add_trace(go.Bar(x=d["Date"], y=d["Trade Volume"] / 1_000_000,
                             name=f"{s} Trade Vol (M)", yaxis="y2", opacity=0.5))
    fig.update_layout(
        title="UIN % Volume vs Trade Volume",
        yaxis=dict(title="UIN % Volume (%)", side="left"),
        yaxis2=dict(title="Trade Volume (Millions)", overlaying="y", side="right", showgrid=False),
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Select symbols from the dropdown to plot.")

# ─── 3) Heatmap ────────────────────────────────────────────────────────────────
st.subheader("🔥 UIN % Heatmap by Symbol")
pivot = (
    df.pivot_table(index="Symbol", columns="Date", values="UIN % Volume", aggfunc="mean")
    .sort_index()
)
pivot = pivot.reindex(sorted(pivot.columns), axis=1)  # sort dates
fig2 = px.imshow(
    pivot.astype(float),
    aspect="auto",
    color_continuous_scale="Viridis",
    labels=dict(color="UIN % Volume"),
)
# dynamic height: 18px/row capped between 400–1000
heat_h = int(min(max(18 * max(1, len(pivot)), 400), 1000))
fig2.update_layout(height=heat_h, xaxis_title="Date", yaxis_title="Symbol")
st.plotly_chart(fig2, use_container_width=True)

# ─── Download filtered ─────────────────────────────────────────────────────────
st.download_button(
    "⬇️ Download filtered rows (CSV)",
    data=filtered.sort_values(["Date", "Symbol"]).to_csv(index=False),
    file_name=f"filtered_{period}_{date_start}_to_{date_end}.csv",
    mime="text/csv",
)
