import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# NEW: sector mapping
try:
    from sectors import SYMBOL_TO_SECTOR  # dict: {"ABOT": "Pharmaceuticals", ...}
except Exception as e:
    st.warning(f"Could not import sector mapping: {e}")
    SYMBOL_TO_SECTOR = {}


data_folder = os.path.join(os.getcwd(), "Settlement_Output")


# === Load data ===
@st.cache_data
def load_data(period):
    file_map = {
        "Daily": "combined_daily.csv",
        "Weekly": "aggregated_weekly.csv",
        "Monthly": "aggregated_monthly.csv"
    }
    path = os.path.join(data_folder, file_map[period])
    if not os.path.exists(path):
        st.error(f"File not found: {path}")
        return pd.DataFrame()
    df = pd.read_csv(path, thousands=",", encoding_errors="ignore")
    df.columns = df.columns.str.strip().str.replace('\u00A0', ' ', regex=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    df = df.dropna(subset=["Date"])
    return df

# Add Sector column from mapping
df["Sector"] = df["Symbol"].map(SYMBOL_TO_SECTOR).fillna("Unclassified")

# === Index Constituents ===
KSE100_STOCKS = [
    "KEL","PIBTL","BOP","PTC","PAEL","SEARL","CNERGY","SSGC","FCCL","DHPL","HUBC","NBP","PPL","MLCF","HUMNL","SNGP",
    "AIRLINK","TRG","YOUW","FFL","PSO","OGDC","AKBL","FFC","UNITY","ATRL","ILP","LUCK","SYS","DGKC","MEBL","ENGROH",
    "MARI","PSX","HBL","CPHL","KAPCO","NML","FHAM","ISL","TGL","EFERT","LOTCHEM","FABL","FATIMA","DCR","NATF","GHGL",
    "AGP","BAFL","GAL","AICL","JVDC","PIOC","HCAR","UBL","KOHC","HGFA","GHNI","MTL","APL","BAHL","MCB","POL","PABC",
    "PKGP","GLAXO","KTML","SAZEW","COLG","INIL","HALEON","CHCC","LCI","ABL","TPLRF1","SCBPL","PKGS","BWCL","SSOM",
    "PSEL","HINOON","GADT","SHFA","INDU","SRVI","ATLH","JDWS","MEHT","PAKT","BNWM","ABOT","PGLC","IBFL","HMB",
    "NESTLE","RMPL","UPFL","MUREB","THALL"
]

KMIALLSHR_STOCKS = [
    "KEL","PIBTL","TELE","PAEL","BECO","PRL","SEARL","CNERGY","FECTC","SSGC","TREET","QUICE","CEPB","POWER","FCCL",
    "HUBC","CTM","PPL","MLCF","SNGP","WASL","DCL","YOUW","TOMCL","FFL","PSO","GGGL","OGDC","GCIL","UNITY","MACFL",
    "ATRL","TPLP","BNL","SLGL","ASL","UCAPM","ITTEFAQ","ILP","LUCK","SYS","DGKC","BIPL","OBOY","FFLM","GATM","FCL",
    "MEBL","ENGROH","MUGHAL","GGL","PREMA","MARI","GWLC","CPHL","EPCL","NML","IMAGE","FHAM","ISL","TGL","EFERT",
    "FLYNG","LOTCHEM","DOL","FABL","FATIMA","IREIT","SYM","DCR","LIVEN","NATF","IDRT","GHGL","FEM","FPJM","GATI",
    "AGP","AVN","BFAGRO","GAL","JVDC","PIOC","ANL","HCAR","RPL","BGL","KML","GHNI","AGSML","IPAK","DYNO","MTL",
    "DFSM","APL","SPEL","ALNRS","OCTOPUS","SPWL","BBFL","HTL","GTYR","NETSOL","FCEPL","EMCO","SGF","FEROZ","SHCM",
    "STCL","PAKOXY","BFBIO","GLAXO","WAFI","DLL","FPRM","SGPL","ICL","JSML","BRRG","FRCL","SAZEW","TPLT","AGTL",
    "ICCI","BCL","KSBP","TRSM","ANTM","BPL","MIRKS","INIL","HALEON","SERT","CHCC","SURC","BFMOD","LCI","FECM",
    "ORM","ECOP","MACTER","SARC","OLPM","UDPL","TPLRF1","FTMM","IBLHL","PKGS","BWCL","MERIT","CPPL","KOHE","SSOM",
    "PSEL","GFIL","HINOON","GEMSPNL","BERG","CRTM","KOHTM","ZAHID","CLOV","PPP","STYLERS","MFFL","LEUL","GOC",
    "EXIDE","HINO","SHFA","ARCTM","ATBA","LPGL","BWHL","SHDT","ARPL","DAAG","REDCO","SEL","HRPL","UBDL","ASHT",
    "POML","GLPL","STJT","BIFO","MSCL","JDWS","MQTM","AHTM","BATA","SITC","SHEZ","FRSM","SASML","SMCPL","ADAMS",
    "DINT","WAHN","FZCM","BNWM","ZIL","FIBLM","ABOT","SINDM","SNAI","FML","NRSL","CCM","IBFL","OML","HAEL","SCL",
    "INKL","NESTLE","FTSM","TICL","RUPL","SZTM","AABS","KPUS","ELCM","KHYT","FIMM","CFL","RMPL","UPFL","IDSM",
    "PSYL","CLVL","GVGL","TCORP","PAKD","HPL","FANM","DADX","KCL","PIM","HAFL","SFL","TOWL","AGIL","AKGL","AWTX",
    "BTL","BUXL","GEMBCEM","GEMBLUEX","GEMMEL","GEMPAPL","GIL","JDMT","NSRM","RCML","SANSM","SHSML","STL","STML","ZTL"
]

# === Sidebar Controls ===
st.sidebar.title("📊 UIN Screener Controls")
period = st.sidebar.selectbox("Select period:", ["Daily", "Weekly", "Monthly"])
index_choice = st.sidebar.selectbox("Filter by Index:", ["ALLSHR (All Stocks)", "KSE100", "KMIALLSHR"])
threshold_uin = st.sidebar.slider("Minimum UIN % Volume", 0, 100, 60)

# Trade volume filter in millions
st.sidebar.markdown("**Minimum Trade Volume (Millions)**")
min_trade_vol_m = st.sidebar.number_input(
    label="",
    min_value=0.0, value=50.0, step=0.5,  # default 50M
    help="Rows with Trade Volume below this (in millions) will be filtered out."
)
min_trade_vol_abs = int(min_trade_vol_m * 1_000_000)

symbol_search = st.sidebar.text_input("Filter by symbol (optional):").upper()

# --- Sector filter (optional) ---
sector_choice = st.sidebar.selectbox(
    "Filter by sector (optional):",
    ["All sectors"] + sorted(SECTOR_MAP.keys())
)
if sector_choice != "All sectors":
    df = df[df["Sector"] == sector_choice]

# === Load Data ===
df = load_data(period)
if df.empty:
    st.stop()

from datetime import timedelta  # add this near your imports if not already there

# --- Date range filter (applies before other filters) ---
min_date = df["Date"].min()  # already a datetime.date
max_date = df["Date"].max()  # already a datetime.date

# default: last 30 days or entire range if fewer than 30 days
default_start = max(min_date, max_date - timedelta(days=30)) if min_date and max_date else None
default_range = (default_start, max_date) if default_start else None

date_start, date_end = st.sidebar.date_input(
    "Date range",
    value=default_range,
    min_value=min_date,
    max_value=max_date,
)

# Handle Streamlit returning single date instead of a tuple
if isinstance(date_start, tuple):
    date_start, date_end = date_start

# Apply filter
if date_start and date_end:
    df = df[(df["Date"] >= date_start) & (df["Date"] <= date_end)].copy()


if "UIN % Volume" not in df.columns:
    if "UIN Percentage Volume" in df.columns:
        df["UIN % Volume"] = df["UIN Percentage Volume"]
    elif "UIN Percentage Volume " in df.columns:
        df["UIN % Volume"] = df["UIN Percentage Volume "]
    else:
        st.warning("UIN % Volume column not found.")
        st.stop()

# === Apply Index Filter ===
if index_choice == "KSE100":
    df = df[df["Symbol"].isin(KSE100_STOCKS)]
elif index_choice == "KMIALLSHR":
    df = df[df["Symbol"].isin(KMIALLSHR_STOCKS)]

# === Apply Threshold Filters ===
filtered = df[
    (df["UIN % Volume"] >= threshold_uin) &
    (df["Trade Volume"] >= min_trade_vol_abs)
].copy()

if symbol_search:
    filtered = filtered[filtered["Symbol"].str.contains(symbol_search, case=False)].copy()

# Display trade volume in millions
filtered["Trade Volume (M)"] = (filtered["Trade Volume"] / 1_000_000).round(2)


# === Main Display ===
st.title("📈 PSX UIN Participation Screener")
st.caption(
    f"{period} data | Index: {index_choice} | UIN ≥ {threshold_uin}% | "
    f"Trade Volume ≥ {min_trade_vol_m:.2f}M | Dates: {date_start} → {date_end}"
)

# === Filtered Table (sorted newest → oldest) ===
st.dataframe(
    filtered.sort_values("Date", ascending=False)[
        ["Symbol", "Date", "UIN % Volume", "Trade Volume (M)"]
    ],
    hide_index=True
)


# === 1️⃣ Automatic Top 5 Chart ===
if not filtered.empty:
    st.subheader("📊 Top 5 Symbols by UIN % Volume")
    top5 = (
        filtered.groupby("Symbol")["UIN % Volume"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index
    )
    df_top = df[df["Symbol"].isin(top5)]
    fig_auto = px.line(
        df_top,
        x="Date", y="UIN % Volume", color="Symbol",
        title="Top 5 UIN % Volume Trends",
        markers=True
    )
    fig_auto.update_layout(yaxis_title="UIN % Volume (%)")
    st.plotly_chart(fig_auto, use_container_width=True)
else:
    st.info("No data available for Top 5 chart.")

# === 2️⃣ Manual Comparison Chart ===
st.subheader("📉 UIN % & Trade Volume Trends (Manual Selection)")

all_symbols = sorted(df["Symbol"].unique().tolist())
selected_symbols = st.multiselect(
    "Select symbols to visualize (max 5):",
    all_symbols,
    default=all_symbols[:5],
    max_selections=5,
)

if selected_symbols:
    df_sel = df[df["Symbol"].isin(selected_symbols)]
    fig = go.Figure()

    for s in selected_symbols:
        d = df_sel[df_sel["Symbol"] == s]
        fig.add_trace(
            go.Scatter(x=d["Date"], y=d["UIN % Volume"],
                       mode="lines+markers", name=f"{s} UIN %",
                       yaxis="y1")
        )
        fig.add_trace(
            go.Bar(x=d["Date"], y=d["Trade Volume"] / 1_000_000,
                   name=f"{s} Trade Vol", yaxis="y2", opacity=0.5)
        )

    fig.update_layout(
        title="UIN % Volume vs Trade Volume",
        yaxis=dict(title="UIN % Volume (%)", side="left"),
        yaxis2=dict(title="Trade Volume", overlaying="y", side="right", showgrid=False),
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Select symbols from the dropdown to plot.")

# === 3️⃣ UIN % Heatmap ===
st.subheader("🔥 UIN % Heatmap by Symbol")

pivot = df.pivot_table(index="Symbol", columns="Date", values="UIN % Volume", aggfunc="mean")

fig2 = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale="Viridis",
    labels=dict(color="UIN % Volume"),
)
fig2.update_layout(height=800, xaxis_title="Date", yaxis_title="Symbol")
st.plotly_chart(fig2, use_container_width=True)


st.subheader("📊 Sector summary (in current filters)")

if df.empty:
    st.info("No rows after filters.")
else:
    sec = (
        df.groupby("Sector", as_index=False)
          .agg({"UIN % Volume":"mean", "Trade Volume":"sum"})
    )
    sec["Trade Volume (M)"] = sec["Trade Volume"] / 1_000_000
    sec = sec.sort_values(["Trade Volume"], ascending=False)

    st.dataframe(
        sec[["Sector","UIN % Volume","Trade Volume (M)"]],
        hide_index=True
    )

    import plotly.express as px
    fig = px.bar(
        sec,
        x="Sector", y="Trade Volume (M)",
        hover_data={"UIN % Volume":":.2f"},
        title="Total Trade Volume by Sector (M)",
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)
