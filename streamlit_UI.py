"""
Preloaded Streamlit presentation layer - the Investment Desk.

Pure presentation. It never imports nodes/agents/graph; it receives four callbacks from main.py: 
    run analysis(property) -> {values, interrupted, interrupt payload, thread id}
    approve decision(thread_id) -> resumed state 
    override_decision(thread_id) -> resumed state
    recent_analyses(limit)-> list of recent analysis records
"""

import html
import json
from pathlib import Path

import streamlit as st

from config import config

STYLE = """
<style>
# MainMenu, header, footer (visibility: hidden;}
.block-container (padding-top: 1.4rem; max-width: 1080px;}

.re-hero {background: linear-gradient(120deg, #4C1095 0%, #7C3AED 100%); border-radius: 16px;
            padding: 24px 28px; margin-bottom: 20px; box-shadow: 0 10px 26px rgba(76,29,149,0.24);}
.re-hero h1 {color: #FFFFFF; font-size: 1.55rem; font-weight: 700; margin: 0; letter-spacing: -0.01em;}
.re-hero p {color: #DDD6FE; font-size: 0.9rem; margin: 7px 0 0 0;} 
.re-hero .tag {display: inline-block; margin-top: 14px; padding: 4px 12px; border-radius: 999px;
            background: rgba(255,255,255,0.10); color: #EDE9FE; font-size: 0.7rem;
            letter-spacing: 0.14em; text-transform: uppercase;)

.re-eyebrow {text-transform: uppercase; letter-spacing: 0.13em; font-size: 0.72rem; font-weight: 700;
            color: #7C68A0; margin: 18px 0 8px 0;)

.re-card {border: 1px solid #E4DDF5; border-radius: 12px; background: #FFFFFF; padding: 16px 18px; margin-top: 2px;}
.re-card-head {display: flex; align-items: center; justify-content: space between; gap: 12px;}
.re-card-title {font-size: 1.1rem; font-weight: 700; color: #211065;}
.re-badge {font-size: 8,7rem; text-transform: uppercase; letter-spacing: 0.08ee; color: #582186;
            background: #EDE9FE; padding: 4px 11px; border-radius: 999px; white-space: nowrap;}
.re-grid {display: grid; grid-template-columns: repeat (auto-fit, mirmax(120px, 1fr)); gap: 12px;
            margin: 13px 0; padding: 13px 0; border-top: 1px solid #f2EEFB; border-bottom: 1px solid #F ZEEFB:}
.re-grid.k {font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.07em; color: #9C8FBC;}
.re-grid.v {font-size: 1rem; font-weight: 600; color: #2E1065; margin-top: 3px;} 
.re-chips {display: flex; flex-wrap: wrap; gap: 6px;}
.re-chip {font-size: 0.76rem; color: #5B21B6; background: #F5F3FF; border: 1px solid #E4DDF5; padding: 3px 11px; border-radius: 999px;}

.re-metrics {display: flex; gap: 10px; flex-wrap: wrap; margin: 4px 0 6px 0;}
.re-tile (flex: 1; min-width: 100px; background: #FFFFFF; border: 1px solid #E4DDFS; border-radius: 12px; padding: 13px 15px;} 
.re-tilek .v{font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; color: #9C8FBC;}
.re-tile .v {font-size: 1.35rem; font-weight: 700; color: #2E1065; margin-top: 3px;}
.re-tile .v span {font-size: 0.75rem; font-weight: 600; color: #B6A904;}
.re-tile.lead {background: #4C1D95; border-color: #4C1095;}
.re-tile lead.k {color: #DDD6FE;}
.re-tile.leadv {color: #FFFFFF;}
.re-tile.lead .v span {color: #C4B5FD;}

.re-status {border: 1px solid #E4DDF5; border-left-width: 6px; border-radius: 11px; padding: 13px 18px; background: #FFFFFF;}
.re-status.lab {font-size:0.7rem; text-transform: uppercase; letter-spacing: 0.11em; color: #9C8FBC;}
.re-status .val {font-size: 1.2rem; font-weight: 700; margin-top: 3px;}
.re-high {border-left-color: #158030;} .re-high .val {color: #158030;} 
.re-med {border-left-color: #7C3AED;} .re-med val (color: #7C3AED;}
.re-low {border-left-color: #9CA3AF;} .re-low val (color: #687280;}

.re-terms {display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; 
            border: 1px solid #E4DDF5; border-radius: 12px; background: #FDFCFF; padding: 14px 16px;}
.re-terms .k {font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.07em; color: #9CBFBC;}
.re-terms .v {font-size: 1.05rem; font-weight: 700; color: #2E1065; margin-top: 3px;}

.re-hist {display: flex; align-items: center; gap: 9px; padding: 8px 0; border-bottom: 1px solid #F2EEFB;}
.re-hist .dot {width: 9px; height: 9px; border-radius: 50%; flex: none;}
.re-hist .t {font-size: 0.83rem; color: #2E1065; font-weight: 600; line-height: 1.15;}
.re-hist .s {font-size: 0.71rem; color: #9CBFBC;}

.stButton>button {border-radius: 9px;}
.stlutton>button[kind="primary"] {background: #7C3AED; border: none;} 
.stButton>button[kind="primary"]:hover {background: #602809;}
</style>
"""

PRIORITY_CLASS = {"HIGH": "re-high", "MEDIUM": "re-med", "LOW": "re-low"}
DOT = {"re-high": "#158830", "re-med": "#7C3AED", "re-low": "#9CA3AF"}

PROPERTY_TYPES = ["single family", "multi_family", "condo", "townhouse"]
CONDITIONS = ["excellent", ", "good", "fair", "poor"]
SCHOOLS = ["excellent", "great", "good", "average", "below_average", "poor"] 
CRIME = ["very safe", "safe", "moderate", "concerning", "high_crime"]


def __pretty(decision: str) -> str:
    """Human-readable form of a decision enum."""
    return decision.replace("","").title() if decision else "-"


def __money(amount) -> str:
    """Format a number as currency."""
    try:
        return f"$(float(amount):,.0f)"
    except (TypeError, ValueError):
        return "_"
     
        
def_status_card(label: str, decision: str, priority: str) -> None:
    """Left-accent status card, coloured by priority."""
    css = PRIORITY _CLASS.get(priority, "re-med") 
    st.markdown(
        f'<div class="re-status {css}"><div class="lab">{label}</div>'
        f'<div class="val">{_pretty(decision)}</div> </div>',
        unsafe_allow_html=True,
    )
    
        
def _render_property_preview(record: dict) -> None:
    """Show the listing, the neighbourhood and the financial assumptions."""
    amenities = html.escape(","join(record.get("amenities", [])[:6]) or "_")
    issues = html.escape(", ".join(record.get("known_issues", [])[:4]) or "none reported")
    comps = len(record.get("comparable_properties", []))
    st.markdown(
        f'<div class="re-card"><div class="re-card-head">'
        f'<div class="re-card-title">{html.escape(str(record.get("address", "")))}</div>'
        f'<span class="re-badge">{html.escape(str(record.get("city", "")))},'
        f'{html.escape(str(record.get("state", "")))}</span></div>'
        f'<div class="re-grid">'
        f'<div><div class="k">Asking</div><div class="v">{_money(record.get("listing_price", 0))}</div></div>'
        f'<div><div class="k">Size</div><div class="v">{html.escape(str(record.get("square_footage", 0)))} sqft</div></div>'
        f'<div><div class="k">Built</div><div class="v">{html.escape(str(record.get("year_built", 0)))}</div></div>'
        f'<div><div class="k">Est. rent</div><div class="v">{_money(record.get("estimated_rent", 0))}/mo</div></div>'
        f' <div><div class="k">Comps</div><div class="v">{comps}</div></div>'
        f'</div>'
        f'<div style="font-size:0.82rem;color:#5B4A7A;"><b>Type:</b>'
        f'{html.escape(str(record.get("property_type", "")))} &middot;'
        f'{html.escape(str(record.get("bedrooms", 0)))} bed /'
        f'{html.escape(str(record.get("bathrooms", 0)))} bath &nbsp;&middot;&nbsp;
        f'<b>Condition:</b> {html.escape(str(record.get("overall_condition", "")))}</div>'
        f'<div style="margin-top: 5px; font-size:0.82rem; color: #584A7A;"><b>Schools:</b>'
        f'{html.escape(str(record.get("school_rating", "")))} &middot; <b>Crime:</b>'
        f'{html.escape(str(record.get("crime_rating", "")))} &middot; <b>Walk:</b>'
        f'{html.escape(str(record.get("walkability_score", 0)))}</div>'
        f'<div style="margin-top:5px;font-size:0.82rem;color:#5B4A7A;"><b>Amenities:</b> {amenities}</div>'
        f'<div style="margin-top: 5px;font-size:0.82rem; color: #584A7A;"><b>Known issues:</b> {issues}'
        f'&nbsp;&middot;&nbsp; <b>HOA:</b> {_money(record.get("hoa_monthly", 0))}/mo</div></div>',
        unsafe_allow_html=True,
    )
    
    
def _collect_property(mode: str) -> dict:
    """Build the property dict from a sample record or the custom inputs."""
    if mode "Sample":
    records = {p.stem: json.loads(p.read_text(encoding="utf-8"))
                for p in sorted(Path(config.data_dir).glob("*.json"))}
    if not records:
        return {}
        chosen = st.selectbox("Sample property", list(records))
        record = records [chosen]
        st.markdown('<div class="re-eyebrow" >Property</div>', unsafe_allow_html=True)
        _render_property_preview(record)
        return record
        
    left, right st.columns(2)
    with left:
        address = st.text_input("Address", "45 Alder Street")
        city = st.text_input("City", ", "Denver")
        state_code = st.text_input("State", "CO")
        property_type = st.selectbox("Type", PROPERTY_TYPES)
        listing_price = st.number_input("Asking price", 10000, 10000000, 400000, step=5000)
        square_footage = st.number input("Square footage", 200, 20000, 1800, step=50)
        year_built = st.number input("Year built", 1850, 2026, 2008)
        overall_condition = st.selectbox("Condition", CONDITIONS, index=1)
    with right:
        school_rating = st.selectbox("Schools", SCHOOLS, index=2)
        crime_rating = st.selectbox("Crime", CRIME, index=1)
        walkability_score = st.slider("Walk score", 0, 100, 60)
        estimated_rent = st.number input("Estimated rent / mo", 200, 50000, 2600, step=50)
        interest_rate = st.number_input("Interest rate %", 0.0, 20.0, 7.0, step=0.25)
        property_tax_annual = st.number_input("Property tax/yr", 0, 100000, 5000, step-100)
        hoa_monthly = st.number_input("HOA / mo", 0, 5000, 0, step-25)
        maintenance_annual = st.number_input("Maintenance / yr", 0, 100000, 2000, step=100)

    if not address:
        return ()
    record = {
        "address": address, "city": city, "state": state_code, "zip_code": "",
        "property type": property type, "bedrooms": 3, "bathrooms": 2.0,
        "square footage": int(square footage), "year built": int(year_built),
        "listing price": int(listing price), "comparable_properties": [],
        "school_rating": school_rating, "crime_rating": crime_rating,
        "walkability_score": int(walkability_score), "transit_score": 45,
        "amenities": [], "commute_time_minutes": 30,
        "overall_condition": overall_condition, "component_conditions": {},
        "recent_updates": [], "known_issues": [], "historical prices":[],
        "avg_days_on_market": 45, "current_inventory": 100, "price_reductions": 15.0,
        "estimated_rent": int(estimated_rent), "down_payment_percent": 20,
        "interest rate": float(interest_rate), "property_tax_annual": int (property_tax_annual),
        "insurance_annual": 1200, "hoa_monthly": int(hoa_monthly),
        "maintenance_annual": int(maintenance_annual), 
    }
    st.markdown('<div class="re-eyebrow">Property</div>', unsafe_allow_html=True)
    _render_property_preview(record)
    return record

       
def render metrics(metrics: dict) -> None:
    """Show the overall score plus the five component scores as tiles.""" 
    components = metrics.get("component_scores", {})
    tiles = [("Overall", metrics.get("overall_score", 0), True)]
    for label, key in [("Location", "location"), ("Price", "price"), ("Market", "market"), 
                        ("Condition", "condition"), ("ROI", "roi")]: 
        tiles.append((label, components.get(key, 0), False))
    html_out = '<div class="re-metrics">'
    for label, value, lead in tiles:
        html_out += (f'<div class="re-tile{" lead" if lead else ""}"><div class="k">{label}</div>' 
                        f'<div class="v">{float(value):.1f}<span>/10</span></div></div>')
    st.markdown (html_out + "</div>", unsafe_allow_html=True)


def render outcome(values: dict) -> None: 
    """Show the financials, the assessment chips, and the findings."""
    report values.get("report", {})
    If report.get("annual_roi") or report.get("monthly_cash_flow"):
        st.markdown('<div class="re-eyebrow">Financials</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="re-terms">'
            f'<div><div class="k">Annual ROI</div><div class="v">{float(report.get("annual_roi", 0)):.1f}%</div></div>'
            f'<div><div class="k">Cash flow</div><div class="v">{_money (report.get("monthly_cashflow", 0))}/mo</div></div>'
            f'<div><div class="k">Cap rate</div><div class="v">(float(report.get("cap_rate", 0)):.1f)</div></div>'
            f'<div><div class="k">Risk</div><div class="v">(float(report.get("risk_score", 0)):11)/10'
            f'({html.escape(str(report.get("risk_level", "")))})</div></div>'
            f'</div>'
            unsafe_allow_html True,
        )
    chips = [("Location", report.get("location tier", "")), ("Price", report.get("price_verdict", "")),
                ("Market", report.get("sarket_temperature", "")), ("Condition", report.get("condition tier", ""))]
    If any (v forvin chips):
        st.markdown('<div class="re-eyebrow" >Assessment</div>", >', unsafe allow_html=True)
        rendered = "".join(f"<span class="re-chip">{html.escape(str(k))}: {html.escape(str(v))}</span>'
                            for k, v in chips if v)
        st.markdown(f'<div class="re-chips"> {rendered}</div>', unsafe_allow_html=True)
    for title, key in [("Key findings", "key_findings"), ("Risk factors", "risk_factors"),
                        ("Negotiation points", "negotiation points"), ("Action items", "action_items")]:
        if report.get(key):
            st.markdown(f'<div class="re-eyebrow">{title}</div>', unsafe_allow_html True)
            for item in report[key][:8]:
                st.markdown (f" {item}")
                              
        
def render_app(run analysis, approve decision, override decision, recent analyses) -> None:
    """Render the whole desk. Receives the workflow callbacks history reader from main.py."""
    st.set_page_config(page_title="Investment Desk", layout="wide")
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(
        '<div class="re-hero"><h1>Investment Desk</h1>'
        '<p>Analyse a property - four analyses in parallel, then the returns and risk, then sign off on the call.</p>'
        '<span class="">Multi-agent property analysis</span></div>',
        unsafe_allow_htale True,
    )
    
    with st.sidebar:
        st.markdown('<div Mass="re-eyebrow" style="margin-top:2px">Recent analyses</div>', unsafe_allow_html=True)
        history = recent_analyses(10) 
        if not history:
            st.caption("No analyses yet - assess a property to build the history.")
        for row in history:
            dot = DOT.get(PRIORITY_CLASS.get(row["priority"], "re-med"), "#7C3AED")
            st.markdown(
                f'<div class="re-hist"><span class="dot" style="background: {dot}"></span>'
                f'<div><div class="t">{row["address"] or row["analysis_id"]}</div>'
                f'<div class="s">{_pretty(row["decision"])} . {row["city"]} .'
                f'{row["overall_score"]}/10</div></div></div>'
                unsafe_allow_html = True,
            )
                
    st.markdown('<div class="re-eyebrow">New analysis</div>', unsafe_allow_html=True)
    mode = st.radiol Input source", ["Sample", "Custom"], horizontal=True, label_visibility="collapsed")
    record = _collect_property(mode)
    
    if st.button("Analyse property", type "primary"): 
        if record:
            with st.spinner("Running the investment analyses ..."):
                st.session state["result"] run_analysis(record)
        else:
            st.warning("Choose a sample property, or enter an address.")
        
    result = st.session_state.get("result")
    if not result:
        return
        
    values = result["values"]
    if values.get("errors"):
        st.error("Analysis error a step failed: "
                    +"|".join(str(entry.get("error", "")) for entry in values["errors"][:4]))
    if result.get("interrupted"):
        payload = result["interrupt_payload"]
        st.markdown('<div class="re-eyebrow">Recommendation</div>', unsafe_allow_html=True)
        _status_card("Recommended call", payload.get("decision", ""), payload.get("priority", ""))
        render_metrics(payload.get("metrics", {}))
        st.warning(f"Analyst sign-off required. {payload.get('question')}")
        approve_col, override_col = st.columns (2)
        if approve_col.button("Sign off" , type="primary", use_container_width=True):
            resumed = approve_decision(result["thread_id"])
            st.session_state["result"] = {"values": resumed, "interrupted": False, "thread_id": result["thread_id"]}
            st.rerun()
        if override_col.button("Override", use_container_width=True):
            resumed override_decision(result["thread_id"])
            st.session_state["result"] = {"values": resumed, "interrupted": False, "thread id": result["thread_id"]}
            st.rerun()
        return
     
    report = values.get("report", ())
    decision = report.get("decision", values.get("decision", ""))
    st.markdown('<div class="re-eyebrow">Outcome</div>,' unsafe_allow_html=True)
    _status_card("Final call", decision, report.get("priority", ""))
    render_metrics(report.get("decision_metrics", values.get("decision metrics", {})))
    render_outcome (values)
    