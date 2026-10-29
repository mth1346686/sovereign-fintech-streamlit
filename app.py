import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sovereign Fintech & Wealth Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Luxury Cyber CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', 'JetBrains Mono', sans-serif;
    }
    .main {
        background-color: #030712;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 215, 0, 0.25);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(255, 215, 0, 0.6);
        box-shadow: 0 14px 40px rgba(255, 215, 0, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏛️ منصة إدارة الثروات والأصول السيادية")
st.caption("Python & Streamlit Edition • محفظة استثمارات النخبة والأصول المصرية")

# Portfolio Metrics
st.markdown("### 💼 المؤشرات المالية الحيوية (محفظة 185.40 مليون ج.م)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="أذون الخزانة المصرية (T-Bills)", value="75.0 M EGP", delta="+27.25% Yield")
with col2:
    st.metric(label="سبائك الذهب الفعلي (24K Gold)", value="42.5 M EGP", delta="+38.60% Alpha")
with col3:
    st.metric(label="أسهم البورصة (EGX30)", value="38.2 M EGP", delta="+29.40% YoY")
with col4:
    st.metric(label="عقارات تجارية مدرة", value="29.7 M EGP", delta="+14.80% Rental")

# Visual Charts
st.markdown("---")
st.markdown("### 📊 التحليلات التفاعلية وتوزيع الأصول (Plotly Dark Luxury)")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Asset Allocation Donut
    labels = ['أذون الخزانة المصرية', 'سبائك الذهب الفعلي', 'أسهم EGX30', 'أصول عقارية مدرة']
    values = [75.0, 42.5, 38.2, 29.7]
    colors = ['#FFD700', '#F59E0B', '#00F0FF', '#10B981']

    fig_donut = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.6,
        marker=dict(colors=colors, line=dict(color='#030712', width=2)),
        textinfo='percent+label',
        hoverinfo='label+value+percent'
    )])
    fig_donut.update_layout(
        title="توزيع رأس المال الحالي (بالمليون جنيه)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Cairo'),
        showlegend=False,
        dragmode=False,
        height=320,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_donut, config={'scrollZoom': False, 'displayModeBar': False, 'doubleClick': False}, use_container_width=True)

with chart_col2:
    # 5-Year Cumulative Yield Forecast
    years = ['2026', '2027', '2028', '2029', '2030']
    tbills_grow = [75.0, 95.4, 121.4, 154.5, 196.6]
    gold_grow = [42.5, 58.9, 81.6, 113.1, 156.8]

    fig_grow = go.Figure()
    fig_grow.add_trace(go.Scatter(
        x=years, y=tbills_grow, name='أذون الخزانة (27.25%)',
        line=dict(color='#FFD700', width=3, shape='spline'),
        mode='lines+markers'
    ))
    fig_grow.add_trace(go.Scatter(
        x=years, y=gold_grow, name='سبائك الذهب (38.6%)',
        line=dict(color='#F59E0B', width=3, dash='dot', shape='spline'),
        mode='lines+markers'
    ))
    fig_grow.update_layout(
        title="توقعات نمو رأس المال التراكمي لـ 5 سنوات",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Cairo'),
        dragmode=False,
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', fixedrange=True)
    )
    st.plotly_chart(fig_grow, config={'scrollZoom': False, 'displayModeBar': False, 'doubleClick': False}, use_container_width=True)

# Interactive Rebalancing Simulator
st.markdown("---")
st.markdown("### 🎛️ محاكي إعادة توزيع المحفظة الاستثمارية")

with st.sidebar:
    st.markdown("### ⚙️ تخصيص نسب المحفظة")
    t_val = st.slider("نسبة أذون الخزانة (27.25%)", min_value=10, max_value=70, value=40, step=5)
    g_val = st.slider("نسبة سبائك الذهب (38.6%)", min_value=10, max_value=50, value=25, step=5)
    e_val = st.slider("نسبة أسهم البورصة (29.4%)", min_value=5, max_value=40, value=20, step=5)
    re_val = max(0, 100 - t_val - g_val - e_val)
    st.info(f"المتبقي للعقارات المدرة: {re_val}%")

# Compute
total_aum = 185.4
weighted_yield = ((t_val * 27.25) + (g_val * 38.60) + (e_val * 29.40) + (re_val * 14.80)) / 100
annual_flow = total_aum * (weighted_yield / 100)
monthly_flow = (annual_flow / 12) * 1000

res_col1, res_col2, res_col3 = st.columns(3)
with res_col1:
    st.metric(label="العائد السنوي الموزون", value=f"+{weighted_yield:.2f}%")
with res_col2:
    st.metric(label="الأرباح السنوية الصافية", value=f"{annual_flow:.2f} M EGP")
with res_col3:
    st.metric(label="التدفق النقدي الشهري", value=f"{monthly_flow:,.0f} ألف ج.م / شهر")

st.success("تم حساب المحاكاة بالكامل عبر محرك بايثون الرياضي الفوري.")
