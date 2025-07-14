import os
import pandas as pd
import seaborn as sns
import streamlit as st
import utility as util
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def load_all_ncrb_data(folder_path):
    all_data = []
    for year in range(2001, 2012):
        for region in ["STATES", "UTs"]:
            file_path = os.path.join(folder_path, f"NCRB_{year}_{region}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df["Year"] = year
                df["RegionType"] = region
                all_data.append(df)
    print(pd.concat(all_data, ignore_index=True).reset_index(drop=True))
    return pd.concat(all_data, ignore_index=True).reset_index(drop=True)

def get_total_summary_table(df):
    df["Total"] = df[[col for col in df.columns if col.startswith("vtrc")]].sum(axis=1)
    summary = df.groupby(["States", "RegionType"])["Total"].sum().reset_index()
    return summary.sort_values(by="Total", ascending=False)

def plot_interactive_rape_trend(df, state):
    vtrc_cols = [col for col in df.columns if col.startswith("vtrc")]
    df["Total Rape Count(s)"] = df[vtrc_cols].sum(axis=1)

    state_df = pd.concat([
        df[df["UTs"].str.lower() == state.lower()],
        df[df["States"].str.lower() == state.lower()]
    ], ignore_index=True)

    trend = state_df.groupby("Year")["Total Rape Count(s)"].sum().reset_index()

    fig = px.line(
        trend,
        x="Year",
        y="Total Rape Count(s)",
        title=f"📈 {state.title()} (2001–2011)",
        markers=True,
        template="plotly_white"
    )

    fig.update_traces(line=dict(color="#002b5b", width=3), marker=dict(size=8))

    fig.update_xaxes(
        tickmode='linear',
        tick0=2001,
        dtick=1,
        tickangle=0
    )

    fig.update_layout(
        height=420,
        width=750,
        title_font=dict(size=18, family="Segoe UI"),
        xaxis_title="Year",
        yaxis_title="Total Rape Count(s)",
        hovermode="x unified",
        margin=dict(t=50, b=40, l=60, r=20),
    )

    return fig

def get_total_summary_table_for_selected_state_only(df, state):
    vtrc_cols = [col for col in df.columns if col.startswith("vtrc")]
    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    df["Total Incest Rape Count(s)"] = df[virc_cols].sum(axis=1)
    df["Total Non-Incest Rape Count(s)"] = df[vorc_cols].sum(axis=1)
    df["Total Rape Count(s)"] = df[vtrc_cols].sum(axis=1)

    state_df = pd.concat([
        df[df["UTs"].str.lower() == state.lower()],
        df[df["States"].str.lower() == state.lower()]
    ], ignore_index=True)

    summary = state_df.groupby(["Year"])[
        ["Total Incest Rape Count(s)", "Total Non-Incest Rape Count(s)", "Total Rape Count(s)"]
    ].sum().reset_index()

    return summary.sort_values(by="Year").reset_index(drop=True)

def generate_rape_trend_summary(summary_df, state_name=None):
    if summary_df.empty:
        return "⚠️ No data available to summarize."

    if "📊 Total Rape Cases" not in summary_df.columns or "📅 Year" not in summary_df.columns:
        return "⚠️ Required columns ('📊 Total Rape Cases', '📅 Year') are missing."

    df = summary_df.sort_values("📅 Year").reset_index(drop=True)
    total_cases = df["📊 Total Rape Cases"].dropna().tolist()
    years = df["📅 Year"].dropna().tolist()

    if not total_cases or not years:
        return "⚠️ Insufficient data to analyze trends."
    df = summary_df.sort_values("📅 Year").reset_index(drop=True)
    total_cases = df["📊 Total Rape Cases"].tolist()
    years = df["📅 Year"].tolist()
    state = f"in **{state_name.title()}**" if state_name else ""

    changes = [curr - prev for prev, curr in zip(total_cases, total_cases[1:])]
    inc_years = [years[i+1] for i, d in enumerate(changes) if d > 0]
    dec_years = [years[i+1] for i, d in enumerate(changes) if d < 0]

    max_val = max(total_cases)
    max_year = years[total_cases.index(max_val)]
    min_val = min(total_cases)
    min_year = years[total_cases.index(min_val)]

    if all(d == 0 for d in changes):
        return f"Total rape cases {state} remained unchanged across all years at **{total_cases[0]}**."
    elif all(d > 0 for d in changes):
        return f"Rape cases {state} increased steadily every year, reaching a peak of **{max_val}** in **{max_year}**."
    elif all(d < 0 for d in changes):
        return f"Rape cases {state} declined each year, falling from **{total_cases[0]}** to **{total_cases[-1]}**."
    else:
        trend = "increased most years" if len(inc_years) > len(dec_years) else "fluctuated"
        return (
            f"\nRape cases {state} {trend} from **{years[0]}** to **{years[-1]}**, "
            f"\npeaking at **{max_val}** in **{max_year}**. "
            f"\nThe lowest was **{min_val}** in **{min_year}**."
        )

def generate_detailed_insight(df, state_name=None):
    df = df.sort_values("📅 Year").reset_index(drop=True)
    years = df["📅 Year"].tolist()
    values = df["📊 Total Rape Cases"].tolist()

    max_val = max(values)
    max_year = years[values.index(max_val)]
    min_val = min(values)
    min_year = years[values.index(min_val)]

    insights = ['']
    insights.append(f"📈 **Peak Year:**\nThe highest number of rape cases was reported in **{max_year}**, with **{max_val}** cases.")

    decline_start, decline_end = None, None
    for i in range(1, len(values)):
        if values[i] < values[i-1]:
            if decline_start is None:
                decline_start = years[i-1]
            decline_end = years[i]
        elif decline_end:
            break

    if decline_start and decline_end and decline_end != decline_start:
        decline_min_val = min(values[years.index(decline_start):years.index(decline_end)+1])
        decline_percentage = ((max_val - decline_min_val) / max_val) * 100
        insights.append(
            f"📉 **Decline Phase:**\nA decline was observed from **{decline_start}** to **{decline_end}**, "
            f"with cases dropping ~{decline_percentage:.1f}% from peak."
        )

    recovery_year = None
    if decline_end:
        for i in range(years.index(decline_end)+1, len(values)):
            if values[i] > values[i-1]:
                recovery_year = years[i]
                break
    if recovery_year:
        insights.append(f"🔁 **Resurgence in Reports:**\nA reversal in trend began in **{recovery_year}**, with rising numbers post-decline.")

    delta = values[-1] - values[0]
    trend = "upward 📈" if delta > 0 else "downward 📉" if delta < 0 else "flat ➖"
    insights.append(
        f"📊 **Overall Trend:**\nFrom **{years[0]}** to **{years[-1]}**, the trend was **{trend}**, "
        f"with a net change of **{delta:+}** cases."
    )

    insights.append(
        f"📌 **Policy Note:**\nThe data suggests correlating fluctuations with **law enforcement policies**, "
        f"**public awareness**, or **reporting mechanisms** active during the mid-decade."
    )

    return "\n\n".join(insights)

def plot_interactive_age_distribution_per_year(df, state):
    state_df = pd.concat([
        df[df["UTs"].str.lower() == state.lower()],
        df[df["States"].str.lower() == state.lower()]
    ], ignore_index=True)

    vtrc_cols = [col for col in state_df.columns if col.startswith("vtrc")]

    age_dist = state_df.groupby("Year")[vtrc_cols].sum().reset_index()

    age_dist_melted = age_dist.melt(id_vars="Year", var_name="Age Group", value_name="Victim Count")

    age_dist_melted["Age Group"] = (age_dist_melted["Age Group"].str.replace("vtrc ", "").str.replace("-", "–").replace("50–dead", "50+"))


    custom_colors = {
        "0–90": "#012b44",
        "10–14": "#014e6f",
        "14–18": "#0277a8",
        "18–30": "#32a4d5",
        "30–50": "#82c7e6",
        "50+": "#b9c0c8"
    }

    fig = px.bar(
        age_dist_melted,
        x="Year",
        y="Victim Count",
        color="Age Group",
        title=f"AGE WISE DISTRIBUTION IN {state.upper()} (2001–2011)",
        labels={"Victim Count": "No. of Victims"},
        template="plotly_white",
        color_discrete_map=custom_colors
    )

    fig.update_traces(
        marker_line_color="#fff",
        marker_line_width=0.5
    )

    fig.update_layout(
        height=450,
        width=750,
        barmode="stack",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        title_font=dict(
            size=20,
            family="Segoe UI",
            color="#002b5b"
        ),
        xaxis_title="Year",
        yaxis_title="Victim Count",
        xaxis=dict(
            tickfont=dict(size=12, color="#000000", family="Segoe UI"),
            title_font=dict(size=14, color="#000000", family="Segoe UI"),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            tickfont=dict(size=12, color="#000000", family="Segoe UI"),
            title_font=dict(size=14, color="#000000", family="Segoe UI"),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        hovermode="x unified",
        margin=dict(t=60, b=40, l=60, r=30),
        legend=dict(
            font=dict(
                size=12,
                color="#000000",
                family="Segoe UI"
            ),
        ),
        legend_title=dict(
            text="Age Group",
            font=dict(
                size=13,
                color="#000000",
                family="Segoe UI"
            )
        ),
    )

    return fig

def get_top_age_group_per_year(df, state):
    """
    Returns a DataFrame with Year and Top Age Group for the given state/UT.
    """
    df_state = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    age_cols = [c for c in df_state.columns if c.startswith("vtrc")]
    records = []
    for year in sorted(df_state["Year"].unique()):
        totals = df_state[df_state["Year"] == year][age_cols].sum()
        top = totals.idxmax().replace("vtrc ", "").replace("-", "–")
        records.append({"Year": year, "Top Age Group": top, "Count": totals.max()})
    return pd.DataFrame(records)

def plot_age_group_distribution_pie(df, state):
    """
    Plots a pie chart showing age group distribution of rape victims
    in a given state across all years (2001–2011), with entire pie slightly pulled out.
    """
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    age_cols = [col for col in df.columns if col.startswith("vtrc")]
    age_totals = state_df[age_cols].sum().reset_index()
    age_totals.columns = ["Age_Group", "Victim_Count"]

    age_totals["Age_Group"] = (
        age_totals["Age_Group"]
        .str.replace("vtrc ", "", regex=False)
        .str.replace("-", "–", regex=False)
        .str.replace("50–dead", "50+")
    )
    age_totals = age_totals[age_totals["Victim_Count"] > 0]

    age_order = {
        "0–10": 0,
        "10–14": 1,
        "14–18": 2,
        "18–30": 3,
        "30–50": 4,
        "50+": 5
    }
    age_totals["SortIndex"] = age_totals["Age_Group"].map(age_order)
    age_totals = age_totals.sort_values("SortIndex").drop(columns=["SortIndex"])

    age_totals["Pull"] = [0.07] * len(age_totals)

    color_palette = ["#002b5b", "#1e3d59", "#2c5875", "#3d7292", "#4e8bae", "#5fa5cb", "#7fc1e5"]

    fig = go.Figure(
        data=[go.Pie(
            labels=age_totals["Age_Group"],
            values=age_totals["Victim_Count"],
            pull=age_totals["Pull"],
            sort=False,
            textinfo="label+percent",
            textfont=dict(size=14, color="black", family="Segoe UI"),
            marker=dict(
                colors=color_palette[:len(age_totals)],
                line=dict(color="#ffffff", width=1)
            ),
            hole=0.25
        )]
    )

    fig.update_layout(
        title="",
        title_font=dict(size=20, color="#002b5b", family="Segoe UI"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(t=70, b=30, l=50, r=50),
        legend=dict(
            font=dict(
                size=12,
                color="#000000",
                family="Segoe UI"
            ),
        ),
        legend_title=dict(
            text="Age Group",
            font=dict(
                size=13,
                color="#000000",
                family="Segoe UI"
            )
        ),
    )

    return fig

def get_key_stats(summary_df):
    """
    Generate key statistical highlights from the summary dataframe.
    """
    df = summary_df.copy()
    df = df.sort_values("📅 Year").reset_index(drop=True)
    
    years = df["📅 Year"].tolist()
    values = df["📊 Total Rape Cases"].tolist()

    if not values or not years or len(values) != len(years):
        return {
            "Peak Year": "N/A",
            "Min Year": "N/A",
            "Trend": "Insufficient Data",
            "Percent Change": "N/A"
        }

    max_val = max(values)
    max_year = years[values.index(max_val)]

    min_val = min(values)
    min_year = years[values.index(min_val)]

    percent_change = ((values[-1] - values[0]) / values[0]) * 100 if values[0] != 0 else None
    delta = values[-1] - values[0]
    trend = "Upward" if delta > 0 else "Downward" if delta < 0 else "Flat ➖"

    return {
        "Peak Year": f"{max_year} ({max_val})",
        "Min Year": f"{min_year} ({min_val})",
        "Trend": trend,
        "Percent Change": f"{percent_change:+.2f}%" if percent_change is not None else "N/A"
    }

def plot_incest_vs_nonincest_per_year(df, state):
    state_df = pd.concat([
        df[df["UTs"].str.lower() == state.lower()],
        df[df["States"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)

    yearly_summary = state_df.groupby("Year")[["Total Incest", "Total Non-Incest"]].sum().reset_index()

    melted = yearly_summary.melt(id_vars="Year", var_name="Type", value_name="Victim Count")

    fig = px.bar(
        melted,
        x="Year",
        y="Victim Count",
        color="Type",
        barmode="group",
        text="Victim Count",
        color_discrete_map={
            "Total Incest": "#004080",
            "Total Non-Incest": "#7fb3d5"
        },
        template="plotly_white"
    )

    fig.update_layout(
        title=f"👥 Incest vs Non-Incest Rape Cases in {state.title()} (2001–2011)",
        title_font=dict(
            size=22,
            family="Segoe UI",
            color="#002b5b"
        ),
        xaxis=dict(
            title="Year",
            title_font=dict(
                size=14,
                family="Segoe UI",
                color="#000000"
            ),
            tickfont=dict(
                size=12,
                family="Segoe UI",
                color="#000000"
            ),
            tickmode="linear",
            dtick=1,
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            title="Victim Count",
            title_font=dict(
                size=14,
                family="Segoe UI",
                color="#000000"
            ),
            tickfont=dict(
                size=12,
                family="Segoe UI",
                color="#000000"
            ),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",

        legend=dict(
            font=dict(
                family="Segoe UI",
                size=12,
                color="#000000"
            )
        ),
        legend_title=dict(
            text="Rape Type",
            font=dict(
                family="Segoe UI",
                size=13,
                color="#000000"
            )
        ),

        hoverlabel=dict(
            font=dict(
                family="Segoe UI",
                size=12,
                color="#000"
            ),
            bgcolor="#ffffff",
            bordercolor="#002b5b"
        ),

        margin=dict(t=60, b=40, l=60, r=30)
    )

    fig.update_traces(textposition="outside", textfont_color="#000")

    return fig

def plot_age_group_trends_linechart(df, state):
    """
    Plots a line chart showing age-group victim trends year-wise (2001–2011)
    for the selected state or UT.
    """
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    vtrc_cols = [col for col in state_df.columns if col.startswith("vtrc")]
    age_dist = state_df.groupby("Year")[vtrc_cols].sum().reset_index()

    age_dist_melted = age_dist.melt(
        id_vars="Year",
        var_name="Age Group",
        value_name="Victim Count"
    )

    age_dist_melted["Age Group"] = (
        age_dist_melted["Age Group"]
        .str.replace("vtrc ", "")
        .str.replace("-", "–")
        .replace("50–dead", "50+")
    )

    fig = px.line(
        age_dist_melted,
        x="Year",
        y="Victim Count",
        color="Age Group",
        markers=True,
        title=f"AGE GROUP TRENDS IN {state.upper()} (2001–2011)",
        template="plotly_white"
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=6))

    fig.update_layout(
        height=400,
        margin=dict(t=50, b=40, l=60, r=30),
        title_font=dict(size=18, family="Segoe UI", color="#002b5b"),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            tickfont=dict(size=12, family="Segoe UI", color="#000000"),
            title_font=dict(size=14, family="Segoe UI", color="#000000"),
            showgrid=True, gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            title="No. of Victims",
            tickfont=dict(size=12, family="Segoe UI", color="#000000"),
            title_font=dict(size=14, family="Segoe UI", color="#000000"),
            showgrid=True, gridcolor="#e5e5e5"
        ),
        legend=dict(
            title="Age Group",
            title_font=dict(size=13, family="Segoe UI", color="#000000"),
            font=dict(size=12, family="Segoe UI", color="#000000")
        ),
        hovermode="x unified",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )

    return fig

def get_age_group_percentage_distribution_table(df, state):
    """
    Returns a DataFrame showing percentage of total rape victims per age group per year
    for the selected state/UT. Uses only 'vtrc' (total rape count) columns.
    """
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    vtrc_cols = [col for col in df.columns if col.startswith("vtrc")]

    age_dist = state_df.groupby("Year")[vtrc_cols].sum().reset_index()

    total_per_year = age_dist[vtrc_cols].sum(axis=1)

    age_dist_percent = age_dist.copy()
    for col in vtrc_cols:
        age_dist_percent[col] = (age_dist_percent[col] / total_per_year * 100).round(2)

    age_dist_percent.rename(columns={
        "vtrc 0-10": "0–10",
        "vtrc 10-14": "10–14",
        "vtrc 14-18": "14–18",
        "vtrc 18-30": "18–30",
        "vtrc 30-50": "30–50",
        "vtrc 50-dead": "50+"
    }, inplace=True)

    age_dist_percent["Year"] = age_dist_percent["Year"].astype(int)

    return age_dist_percent


def render_white_theme_percentage_table(df):
    """
    Converts styled DataFrame to HTML with inline CSS for full Streamlit control.
    """
    styles = """
    <style>
    table.custom-table {
        border-collapse: collapse;
        width: 100%;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        background-color: #ffffff;
        color: #000000;
    }
    table.custom-table th, table.custom-table td {
        border: 1px solid #ddd;
        text-align: center;
        padding: 8px;
    }
    table.custom-table th {
        background-color: #002b5b;
        color: #ffffff;
    }
    table.custom-table tr:hover {
        background-color: #cedff4;
    }
    </style>
    """

    df_formatted = df.copy()
    for col in df.columns:
        if col != "Year":
            df_formatted[col] = df_formatted[col].map(lambda x: f"{x:.2f} %")

    html_table = df_formatted.to_html(classes="custom-table", index=False, escape=False)

    return styles + html_table

def generate_age_group_summary_stats(df, state):
    """
    Compute key summary statistics for a given state's age-specific rape data
    from 2001 to 2011. Returns a dictionary with labeled metrics.
    """
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    vtrc_cols = [col for col in df.columns if col.startswith("vtrc")]

    age_dist = state_df.groupby("Year")[vtrc_cols].sum().reset_index()
    age_dist_melted = age_dist.melt(id_vars="Year", var_name="Age Group", value_name="Victim Count")

    age_dist_melted["Age Group"] = (
        age_dist_melted["Age Group"]
        .str.replace("vtrc ", "")
        .str.replace("-", "–")
        .str.replace("50–dead", "50+")
    )

    total_by_age = age_dist_melted.groupby("Age Group")["Victim Count"].sum()

    most_affected = total_by_age.idxmax()
    least_affected = total_by_age.idxmin()

    underage_groups = ["0–10", "10–14", "14–18"]
    underage_df = age_dist_melted[age_dist_melted["Age Group"].isin(underage_groups)]
    underage_sum_by_year = underage_df.groupby("Year")["Victim Count"].sum()
    highest_underage_year = underage_sum_by_year.idxmax()

    age_18_30_df = age_dist_melted[age_dist_melted["Age Group"] == "18–30"]
    avg_18_30 = round(age_18_30_df["Victim Count"].mean(), 2)

    return {
        "Most Affected Age Group": most_affected,
        "Least Affected Age Group": least_affected,
        "Year with Highest Underage Victims": highest_underage_year,
        "Avg. Victims per Year in 18–30 Age": avg_18_30
    }

def plot_underage_vs_adult_bar_chart(df, state):
    """
    Plots a grouped bar chart showing comparison of Underage (0–18)
    vs Adult (18+) rape victims per year for a given state.
    Now includes counts above each bar.
    """

    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    underage_cols = ["vtrc 0-10", "vtrc 10-14", "vtrc 14-18"]
    adult_cols = ["vtrc 18-30", "vtrc 30-50", "vtrc 50-dead"]

    state_df["Underage"] = state_df[underage_cols].sum(axis=1)
    state_df["Adult"] = state_df[adult_cols].sum(axis=1)

    plot_df = state_df.groupby("Year")[["Underage", "Adult"]].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=plot_df["Year"],
        y=plot_df["Underage"],
        name="Underage",
        marker_color="#004080",
        text=plot_df["Underage"],
        textposition="outside",
        textfont=dict(color="#000", size=12, family="Segoe UI"),
        hovertemplate="<b>Year:</b> %{x}<br><b>Category:</b> Underage<br><b>Victims:</b> %{y}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=plot_df["Year"],
        y=plot_df["Adult"],
        name="Adult",
        marker_color="#82c7e6",
        text=plot_df["Adult"],
        textposition="outside",
        textfont=dict(color="#000", size=12, family="Segoe UI"),
        hovertemplate="<b>Year:</b> %{x}<br><b>Category:</b> Adult<br><b>Victims:</b> %{y}<extra></extra>"
    ))

    fig.update_layout(
        barmode="group",
        title=f"Underage (0–18) vs Adult (18+) Victims in {state.upper()} (2001–2011)",
        height=460,
        width=750,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        title_font=dict(size=20, color="#002b5b", family="Segoe UI"),
        legend_title=dict(text="Age Group", font=dict(size=13, color="#000")),
        legend=dict(font=dict(size=12, color="#000", family="Segoe UI")),
        margin=dict(t=60, b=40, l=60, r=30),
        xaxis=dict(
            title="Year",
            tickfont=dict(size=12, color="#000"),
            title_font=dict(size=14, color="#000"),
            showgrid=True,
            gridcolor="#eeeeee"
        ),
        yaxis=dict(
            title="Victim Count",
            tickfont=dict(size=12, color="#000"),
            title_font=dict(size=14, color="#000"),
            showgrid=True,
            gridcolor="#eeeeee"
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#002b5b",
            font_size=12,
            font_family="Segoe UI",
            font_color="#000000"
        ),
    )

    return fig


import pandas as pd
import plotly.express as px

def plot_age_ratio_index_per_year(df, state):
    """
    Plot the yearly ratio of rape victims aged 18–30 vs. victims aged 0–18 
    for the selected state, across 2001–2011.
    """
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    state_df["0–18"] = state_df[["vtrc 0-10", "vtrc 10-14", "vtrc 14-18"]].sum(axis=1)
    state_df["18–30"] = state_df["vtrc 18-30"]

    df_ratio = state_df.groupby("Year")[["0–18", "18–30"]].sum().reset_index()

    df_ratio["Ratio"] = (df_ratio["18–30"] / df_ratio["0–18"]).replace([float("inf"), -float("inf")], None)

    fig = px.line(
        df_ratio,
        x="Year",
        y="Ratio",
        markers=True,
        title=f"{util.return_nbsp(5)}Age Ratio Index (18–30 / 0–18)",
        labels={"Ratio": "Victim Age Ratio", "Year": "Year"},
        template="plotly_white"
    )

    fig.update_layout(
        height=400,
        width=750,
        title_font=dict(size=20, family="Segoe UI"),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        hovermode="x unified",
        margin=dict(t=50, b=40, l=50, r=30)
    )

    return fig

def plot_radar_age_distribution_over_years(df, state):
    """
    Generates a radar chart (line polar plot) showing age group distribution of
    rape victims across all years (2001–2011) for a specific state, optimized for light theme.
    """
    state_df = pd.concat([
        df[df["UTs"].str.lower() == state.lower()],
        df[df["States"].str.lower() == state.lower()]
    ], ignore_index=True)

    vtrc_cols = [col for col in df.columns if col.startswith("vtrc")]
    if "Year" not in state_df.columns:
        raise ValueError("Missing 'Year' column in dataset.")

    age_dist = state_df.groupby("Year")[vtrc_cols].sum().reset_index()

    age_dist_melted = age_dist.melt(id_vars="Year", var_name="Age Group", value_name="Victim Count")
    age_dist_melted["Age Group"] = (
        age_dist_melted["Age Group"]
        .str.replace("vtrc ", "")
        .str.replace("-", "–")
        .replace("50–dead", "50+")
    )

    category_order = ["0–10", "10–14", "14–18", "18–30", "30–50", "50+"]
    age_dist_melted["Age Group"] = pd.Categorical(age_dist_melted["Age Group"], categories=category_order, ordered=True)
    age_dist_melted = age_dist_melted.sort_values(["Year", "Age Group"])

    fig = px.line_polar(
        age_dist_melted,
        r="Victim Count",
        theta="Age Group",
        color="Year",
        line_close=True,
        template="plotly_white",
        markers=True
    )

    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        polar=dict(
            bgcolor="#ffffff",
            radialaxis=dict(
                visible=True,
                tickfont=dict(size=10, color="#000000"),
                gridcolor="#e5e5e5",
                linecolor="#000000"
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#000000"),
                gridcolor="#e5e5e5",
                linecolor="#000000"
            )
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        title=f"Radar Chart – Age Group Distribution in {state.title()} (2001–2011)",
        title_font=dict(size=18, color="#002b5b", family="Segoe UI"),
        font=dict(color="#000000", family="Segoe UI"),
        legend=dict(
            font=dict(size=12, color="#000000", family="Segoe UI")
        ),
        legend_title=dict(
            text="Year",
            font=dict(size=13, color="#000000", family="Segoe UI")
        ),
        height=500,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig

def plot_trend_line_incest_vs_nonincest(df, state):
    """
    Plots a line chart showing trends of Incest vs Non-Incest rape cases 
    from 2001 to 2011 for the selected state.
    """

    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)

    yearly_totals = state_df.groupby("Year")[["Total Incest", "Total Non-Incest"]].sum().reset_index()

    melted = yearly_totals.melt(id_vars="Year", var_name="Rape Type", value_name="Victim Count")

    fig = px.line(
        melted,
        x="Year",
        y="Victim Count",
        color="Rape Type",
        markers=True,
        line_shape="linear",
        color_discrete_map={
            "Total Incest": "#004080",
            "Total Non-Incest": "#7fb3d5"
        },
        template="plotly_white"
    )

    fig.update_layout(
        title=f"📈 Incest vs Non-Incest Rape Case Trends in {state.title()} (2001–2011)",
        title_font=dict(size=20, family="Segoe UI", color="#002b5b"),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            title_font=dict(size=14, color="#000000"),
            tickfont=dict(size=12, color="#000000"),
            gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            title="Victim Count",
            title_font=dict(size=14, color="#000000"),
            tickfont=dict(size=12, color="#000000"),
            gridcolor="#e5e5e5"
        ),
        legend=dict(
            font=dict(size=12, family="Segoe UI", color="#000000")
        ),
        legend_title=dict(
            text="Rape Type",
            font=dict(size=13, color="#000000", family="Segoe UI")
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#002b5b",
            font=dict(color="#000000", family="Segoe UI", size=12)
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(t=60, b=40, l=60, r=30)
    )

    fig.update_traces(textfont_color="#000000")

    return fig

def plot_incest_nonincest_pie(df, state):
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    total_incest = state_df[virc_cols].sum().sum()
    total_nonincest = state_df[vorc_cols].sum().sum()

    labels = ["Incest Rape", "Non-Incest Rape"]
    values = [total_incest, total_nonincest]
    colors = ["#004080", "#7fb3d5"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        hoverinfo="label+percent+value",
        textinfo="label+percent",
        textfont=dict(family="Segoe UI", size=14, color="#000000")
    )])

    fig.update_layout(
        title={
            "text": f"📌 Incest vs Non-Incest Rape Distribution in {state.title()} (2001–2011)",
            "font": dict(size=20, family="Segoe UI", color="#002b5b"),
            "x": 0.5
        },
        legend=dict(
            font=dict(size=13, color="#000000", family="Segoe UI"),
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=50, b=80),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font=dict(size=12, color="black", family="Segoe UI"),
            bordercolor="#002b5b"
        )
    )

    return fig

def plot_yoy_incest_nonincest_change(df, state):
    state_df = pd.concat([
        df[df["UTs"].str.lower() == state.lower()],
        df[df["States"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)

    yearly_summary = state_df.groupby("Year")[["Total Incest", "Total Non-Incest"]].sum().reset_index()

    yearly_summary["Incest YoY %"] = yearly_summary["Total Incest"].pct_change() * 100
    yearly_summary["Non-Incest YoY %"] = yearly_summary["Total Non-Incest"].pct_change() * 100

    melted = yearly_summary.melt(
        id_vars="Year",
        value_vars=["Incest YoY %", "Non-Incest YoY %"],
        var_name="Category",
        value_name="Change (%)"
    )

    fig = px.bar(
        melted,
        x="Year",
        y="Change (%)",
        color="Category",
        barmode="group",
        text="Change (%)",
        color_discrete_map={
            "Incest YoY %": "#004080",
            "Non-Incest YoY %": "#7fb3d5"
        },
        template="plotly_white"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        textfont=dict(color="black")
    )

    fig.update_layout(
        title="📈 Year-on-Year % Change – Incest vs Non-Incest",
        title_font=dict(size=22, family="Segoe UI", color="#002b5b"),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            title_font=dict(size=14),
            tickfont=dict(size=12),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            title="YoY Change (%)",
            title_font=dict(size=14),
            tickfont=dict(size=12),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        legend_title=dict(
            text="Category",
            font=dict(size=13, family="Segoe UI", color="#000")
        ),
        legend=dict(
            font=dict(size=12, family="Segoe UI", color="#000")
        ),
        hoverlabel=dict(
            font=dict(size=12, color="#000"),
            bgcolor="#fff",
            bordercolor="#002b5b"
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(t=60, b=40, l=60, r=30)
    )

    return fig

def plot_separate_cumulative_charts(df, state):
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)

    yearly_summary = state_df.groupby("Year")[["Total Incest", "Total Non-Incest"]].sum().reset_index()

    yearly_summary["Cum Incest"] = yearly_summary["Total Incest"].cumsum()
    yearly_summary["Cum Non-Incest"] = yearly_summary["Total Non-Incest"].cumsum()

    fig_incest = px.area(
        yearly_summary,
        x="Year",
        y="Cum Incest",
        title=f"Cumulative Incest Rape Cases – {state.title()} (2001–2011)",
        color_discrete_sequence=["#004080"],
        template="plotly_white"
    )
    fig_incest.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        title_font=dict(size=20, color="#002b5b", family="Segoe UI"),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            showgrid=True,
            gridcolor="#e5e5e5",
            title_font_color="#000",
            tickfont_color="#000"
        ),
        yaxis=dict(
            title="Cumulative Victim Count",
            showgrid=True,
            gridcolor="#e5e5e5",
            title_font_color="#000",
            tickfont_color="#000"
        ),
        hoverlabel=dict(
            font=dict(size=12, color="#000"),
            bgcolor="#ffffff",
            bordercolor="#004080"
        ),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=30)
    )

    fig_nonincest = px.area(
        yearly_summary,
        x="Year",
        y="Cum Non-Incest",
        title=f"Cumulative Non-Incest Rape Cases – {state.title()} (2001–2011)",
        color_discrete_sequence=["#7fb3d5"],
        template="plotly_white"
    )
    fig_nonincest.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        title_font=dict(size=20, color="#002b5b", family="Segoe UI"),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            showgrid=True,
            gridcolor="#e5e5e5",
            title_font_color="#000",
            tickfont_color="#000"
        ),
        yaxis=dict(
            title="Cumulative Victim Count",
            showgrid=True,
            gridcolor="#e5e5e5",
            title_font_color="#000",
            tickfont_color="#000"
        ),
        hoverlabel=dict(
            font=dict(size=12, color="#000"),
            bgcolor="#ffffff",
            bordercolor="#004080"
        ),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=30)
    )

    return fig_incest, fig_nonincest

def plot_incest_ratio_per_year(df, state):
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]

    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)

    yearly_summary = state_df.groupby("Year")[["Total Incest", "Total Non-Incest"]].sum().reset_index()

    yearly_summary["Incest Ratio"] = yearly_summary["Total Incest"] / yearly_summary["Total Non-Incest"]

    national_df = df.copy()
    national_df["Total Incest"] = national_df[virc_cols].sum(axis=1)
    national_df["Total Non-Incest"] = national_df[vorc_cols].sum(axis=1)
    national_summary = national_df.groupby("Year")[["Total Incest", "Total Non-Incest"]].sum().reset_index()
    national_summary["National Incest Ratio"] = national_summary["Total Incest"] / national_summary["Total Non-Incest"]

    yearly_summary = yearly_summary.merge(
        national_summary[["Year", "National Incest Ratio"]],
        on="Year",
        how="left"
    )

    melted = yearly_summary.melt(
        id_vars="Year",
        value_vars=["Incest Ratio", "National Incest Ratio"],
        var_name="Ratio Type",
        value_name="Ratio"
    )

    fig = px.line(
        melted,
        x="Year",
        y="Ratio",
        color="Ratio Type",
        markers=True,
        template="plotly_white",
        color_discrete_map={
            "Incest Ratio": "#004080",
            "National Incest Ratio": "#7fb3d5"
        }
    )

    fig.update_layout(
        title=f"📉 Incest-to-Non-Incest Ratio – {state.title()} vs National Avg (2001–2011)",
        title_font=dict(size=20, color="#002b5b", family="Segoe UI"),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            title_font=dict(size=14, color="#000", family="Segoe UI"),
            tickfont=dict(size=12, color="#000", family="Segoe UI"),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        yaxis=dict(
            title="Incest / Non-Incest Ratio",
            title_font=dict(size=14, color="#000", family="Segoe UI"),
            tickfont=dict(size=12, color="#000", family="Segoe UI"),
            showgrid=True,
            gridcolor="#e5e5e5"
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hoverlabel=dict(
            font=dict(family="Segoe UI", size=12, color="#000000"),
            bgcolor="#ffffff",
            bordercolor="#004080"
        ),
        legend=dict(
            font=dict(family="Segoe UI", size=12, color="#000000")
        ),
        legend_title=dict(
            text="Ratio Type",
            font=dict(family="Segoe UI", size=13, color="#000000")
        ),
        margin=dict(t=60, b=40, l=60, r=30)
    )

    return fig

def plot_rape_cluster_by_year(df, state):
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]
    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)
    state_df["Total Rape"] = state_df["Total Incest"] + state_df["Total Non-Incest"]

    yearly_summary = state_df.groupby("Year")[["Total Rape"]].sum().reset_index()

    yearly_summary["Rape Cluster"] = pd.qcut(yearly_summary["Total Rape"], q=3, labels=["Low", "Medium", "High"])

    fig = px.bar(
        yearly_summary,
        x="Year",
        y="Total Rape",
        color="Rape Cluster",
        text="Total Rape",
        barmode="group",
        color_discrete_map={
            "Low": "#a3c4f3",
            "Medium": "#4682b4",
            "High": "#0b3d91"
        },
        template="plotly_white"
    )

    fig.update_layout(
        title=f"🔍 Rape Clustering Over Years in {state.title()} (2001–2011)",
        title_font=dict(size=20, family="Segoe UI", color="#002b5b"),
        xaxis_title="Year",
        yaxis_title="Total Rape Cases",
        legend_title="Cluster Level",
        font=dict(family="Segoe UI", size=12, color="#000000"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(t=60, b=40, l=60, r=30),
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=12,
            font_family="Segoe UI",
            font_color="#000000"
        )
    )

    fig.update_traces(textposition="outside", textfont_color="#000000")
    return fig

def plot_rape_cluster_stripplot(df, state):
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    virc_cols = [col for col in df.columns if col.startswith("virc")]
    vorc_cols = [col for col in df.columns if col.startswith("vorc")]
    state_df["Total Incest"] = state_df[virc_cols].sum(axis=1)
    state_df["Total Non-Incest"] = state_df[vorc_cols].sum(axis=1)
    state_df["Total Rape"] = state_df["Total Incest"] + state_df["Total Non-Incest"]

    yearly_summary = state_df.groupby("Year")[["Total Rape"]].sum().reset_index()

    yearly_summary["Rape Cluster"] = pd.qcut(yearly_summary["Total Rape"], q=3, labels=["Low", "Medium", "High"])

    fig = px.strip(
        yearly_summary,
        x="Year",
        y="Total Rape",
        color="Rape Cluster",
        color_discrete_map={
            "Low": "#a3c4f3",
            "Medium": "#4682b4",
            "High": "#0b3d91"
        },
        hover_data=["Year", "Total Rape"],
        template="plotly_white"
    )

    fig.update_traces(jitter=0.2, marker_size=12)
    fig.update_layout(
        title=f"📍 Clustered Rape Incidence Strip Plot – {state.title()}",
        xaxis_title="Year",
        yaxis_title="Total Rape Cases",
        legend_title="Cluster Level",
        font=dict(family="Segoe UI", size=12, color="#000"),
        hoverlabel=dict(
            font_family="Segoe UI",
            font_size=12,
            font_color="#000",
            bgcolor="#ffffff",
            bordercolor="#002b5b"
        ),
        margin=dict(t=60, b=40, l=60, r=30)
    )
    return fig

def plot_heatmap_incest_vs_nonincest(df, state):
    state_df = pd.concat([
        df[df["States"].str.lower() == state.lower()],
        df[df["UTs"].str.lower() == state.lower()]
    ], ignore_index=True)

    records = []
    age_groups = ["0-10", "10-14", "14-18", "18-30", "30-50", "50-dead"]
    for _, row in state_df.iterrows():
        year = row["Year"]
        for age in age_groups:
            if f"virc {age}" in row and f"vorc {age}" in row:
                records.append({"Year": year, "Age Group": age, "Type": "Incest", "Victim Count": row[f"virc {age}"]})
                records.append({"Year": year, "Age Group": age, "Type": "Non-Incest", "Victim Count": row[f"vorc {age}"]})

    heat_df = pd.DataFrame(records)

    heat_df["Age Group"] = pd.Categorical(
        heat_df["Age Group"],
        categories=["0-10", "10-14", "14-18", "18-30", "30-50", "50-dead"],
        ordered=True
    )

    fig = px.density_heatmap(
        heat_df,
        x="Year",
        y="Age Group",
        z="Victim Count",
        facet_col="Type",
        color_continuous_scale="Blues",
        text_auto=True
    )

    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        template="plotly_white",
        font=dict(family="Segoe UI", color="black"),
        xaxis=dict(
            tickfont=dict(color='black'),
            title=dict(font=dict(color='black'))
        ),
        yaxis=dict(
            tickfont=dict(color='black'),
            title=dict(font=dict(color='black'))
        ),
        title={
            "text": f"🧩 Age Group vs Year Heatmap – {state.title()} (2001–2011)",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(family="Segoe UI", size=20, color="#002b5b")
        },
        coloraxis_colorbar=dict(
            title=dict(text="Victim Count", font=dict(color="black")),
            tickfont=dict(color="black")
        ),
        margin=dict(t=80, b=40, l=60, r=30)
    )

    for axis in fig.layout:
        if axis.startswith("xaxis") or axis.startswith("yaxis"):
            fig.layout[axis].tickfont = dict(color="black")
            fig.layout[axis].title = dict(font=dict(color="black"))

    fig.for_each_annotation(lambda a: a.update(font=dict(color='black')))

    fig.update_traces(
        hoverlabel=dict(
            bgcolor="#ffffff",
            font=dict(color="#000", family="Segoe UI")
        ),
        selector=dict(type="heatmap")
    )

    return fig

def card_container(content: str, bg: str = "#002b5b") -> str:
    return f"""
    <div style='
        background-color: {bg};
        padding: 1.25rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #ddd;
    '>
        {content}
    </div>
    """