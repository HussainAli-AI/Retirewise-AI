"""Plotly charts and UI presentation components for RetireWise AI."""
from typing import List
import plotly.graph_objects as go
from models.assessment import ScenarioResult, CashFlowYearProjection


def create_capital_trajectory_chart(scenarios: List[ScenarioResult]) -> go.Figure:
    """Creates multi-scenario capital depletion curves over time."""
    fig = go.Figure()

    colors = {
        "Base Case": "#1b5e20",              # Green
        "High Inflation Shock": "#d32f2f",    # Red
        "Early Market Drawdown": "#f57c00",   # Orange
        "Major Medical Expense Shock": "#7b1fa2", # Purple
        "Early Retirement Shock": "#0288d1",  # Blue
    }

    for sc in scenarios:
        ages = [p.client_age for p in sc.yearly_trajectory]
        capitals = [p.ending_capital_pkr for p in sc.yearly_trajectory]
        line_color = colors.get(sc.scenario_type.value, "#555555")

        fig.add_trace(
            go.Scatter(
                x=ages,
                y=capitals,
                mode="lines+markers",
                name=sc.scenario_name,
                line=dict(color=line_color, width=2.5),
                marker=dict(size=4),
                hovertemplate="Age %{x}: PKR %{y:,.0f}<extra>" + sc.scenario_name + "</extra>",
            )
        )

    fig.update_layout(
        title=dict(
            text="<b>Modeled Retirement Capital Trajectory Across Scenarios</b>",
            font=dict(size=16),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        xaxis_title="Client Age (Years)",
        yaxis_title="Retirement Capital (PKR)",
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=40, r=40, t=50, b=90),
        height=480,
    )
    # Zero baseline line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Capital Depletion")

    return fig


def create_cash_flow_breakdown_chart(trajectory: List[CashFlowYearProjection]) -> go.Figure:
    """Creates stacked/grouped bars of expenses, guaranteed income, and net portfolio withdrawal."""
    ages = [p.client_age for p in trajectory]
    expenses = [p.total_expenses_pkr for p in trajectory]
    income = [p.guaranteed_income_pkr for p in trajectory]
    withdrawals = [p.net_withdrawal_pkr for p in trajectory]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=ages,
            y=income,
            name="Guaranteed Retirement Income",
            marker=dict(color="#2e7d32"),
            hovertemplate="Age %{x}: PKR %{y:,.0f}",
        )
    )

    fig.add_trace(
        go.Bar(
            x=ages,
            y=withdrawals,
            name="Net Portfolio Withdrawal (Gap)",
            marker=dict(color="#f57c00"),
            hovertemplate="Age %{x}: PKR %{y:,.0f}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=ages,
            y=expenses,
            name="Total Annual Living Expenses",
            line=dict(color="#0288d1", width=2.5, dash="dot"),
            hovertemplate="Age %{x}: PKR %{y:,.0f}",
        )
    )

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="<b>Annual Cash Flow Breakdown (Income vs. Portfolio Withdrawals)</b>",
            font=dict(size=15),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        xaxis_title="Client Age",
        yaxis_title="PKR / Year",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=40, r=40, t=50, b=90),
        height=460,
    )
    return fig


def create_risk_vs_capacity_matrix(risk_score: float, capacity_score: float) -> go.Figure:
    """Visualizes psychological Risk Tolerance vs. objective Capacity for Loss."""
    fig = go.Figure()

    # Highlight Conflict Danger Zone (High Risk + Low Capacity)
    fig.add_shape(
        type="rect",
        x0=50, x1=100,
        y0=0, y1=45,
        fillcolor="rgba(239, 83, 80, 0.25)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_annotation(
        x=75, y=22.5,
        text="<b>SUITABILITY CONFLICT ZONE</b><br>(High Risk Attitude + Low Capacity)",
        showarrow=False,
        font=dict(color="#b71c1c", size=11),
    )

    # Balanced / Suitable Zone
    fig.add_shape(
        type="rect",
        x0=0, x1=100,
        y0=45, y1=100,
        fillcolor="rgba(129, 199, 132, 0.15)",
        line=dict(width=0),
        layer="below",
    )

    # Client Point
    is_conflict = (risk_score >= 60.0 and capacity_score <= 45.0)
    point_color = "#d32f2f" if is_conflict else "#1565c0"

    fig.add_trace(
        go.Scatter(
            x=[risk_score],
            y=[capacity_score],
            mode="markers+text",
            marker=dict(size=18, color=point_color, line=dict(width=2, color="white")),
            text=["<b>Client Position</b>"],
            textposition="top center",
            hovertemplate="Risk Tolerance: %{x}<br>Capacity for Loss: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="<b>Suitability Matrix: Risk Attitude vs. Financial Capacity</b>",
            font=dict(size=15),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        xaxis=dict(title="Psychological Risk Tolerance (0 = Low, 100 = Aggressive)", range=[0, 100]),
        yaxis=dict(title="Objective Capacity for Loss (0 = Low, 100 = High)", range=[0, 100]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=50, b=40),
        height=400,
    )
    return fig


def create_monte_carlo_fan_chart(mc_result) -> go.Figure:
    """Creates a 1,000-trial percentile fan chart with shaded 10th-90th confidence cone."""
    points = mc_result.percentile_trajectories
    ages = [p.age for p in points]
    p10 = [p.p10_capital_pkr for p in points]
    p50 = [p.p50_capital_pkr for p in points]
    p90 = [p.p90_capital_pkr for p in points]

    fig = go.Figure()

    # Upper bound (90th percentile)
    fig.add_trace(
        go.Scatter(
            x=ages,
            y=p90,
            mode="lines",
            line=dict(color="rgba(2, 136, 209, 0.2)", width=1),
            name="90th Percentile (Bull Case)",
            hovertemplate="Age %{x}: PKR %{y:,.0f}<extra>90th Percentile</extra>",
            showlegend=True,
        )
    )

    # Lower bound (10th percentile) filled to upper bound
    fig.add_trace(
        go.Scatter(
            x=ages,
            y=p10,
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(2, 136, 209, 0.15)",
            line=dict(color="rgba(2, 136, 209, 0.2)", width=1),
            name="10th Percentile (Bear Case)",
            hovertemplate="Age %{x}: PKR %{y:,.0f}<extra>10th Percentile</extra>",
            showlegend=True,
        )
    )

    # Median (50th percentile)
    fig.add_trace(
        go.Scatter(
            x=ages,
            y=p50,
            mode="lines+markers",
            line=dict(color="#0288d1", width=3.5),
            marker=dict(size=5, color="#0288d1"),
            name="50th Percentile (Median)",
            hovertemplate="Age %{x}: PKR %{y:,.0f}<extra>Median Trajectory</extra>",
            showlegend=True,
        )
    )

    fig.add_hline(y=0, line_dash="dash", line_color="#d32f2f", annotation_text="Capital Exhaustion")

    fig.update_layout(
        title=dict(
            text=f"<b>Monte Carlo 1,000-Trial Confidence Cone (Success Rate: {mc_result.probability_of_success_pct}%)</b>",
            font=dict(size=16),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        xaxis_title="Client Age (Years)",
        yaxis_title="Portfolio Capital (PKR)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=40, r=40, t=50, b=90),
        height=480,
    )
    return fig


def create_asset_allocation_chart(shariah_result) -> go.Figure:
    """Creates a donut chart of recommended Pakistani asset allocations."""
    labels = [item.asset_class for item in shariah_result.recommended_allocations]
    values = [item.recommended_pct for item in shariah_result.recommended_allocations]
    amounts = [item.allocation_amount_pkr for item in shariah_result.recommended_allocations]

    palette = ["#1b5e20", "#0288d1", "#f57c00", "#7b1fa2", "#555555"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.45,
                marker=dict(colors=palette),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Allocation: %{percent}<br>PKR %{customdata:,.0f}<extra></extra>",
                customdata=amounts,
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="<b>Recommended Portfolio Asset Allocation</b>",
            font=dict(size=15),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=50, b=30),
        height=380,
        showlegend=False,
    )
    return fig

