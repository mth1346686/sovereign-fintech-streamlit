import http.server
import socketserver
import os
import json
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_dark"
PORT = 8501

HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة إدارة الثروات • Python & Streamlit/Plotly Server</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --fin-gold: #FFD700;
            --fin-emerald: #10B981;
            --fin-cyan: #00F0FF;
            --bg-deep: #030712;
            --glass-bg: rgba(15, 23, 42, 0.75);
            --glass-border: rgba(255, 215, 0, 0.22);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Cairo', 'JetBrains Mono', sans-serif; }
        body {
            background-color: var(--bg-deep);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(255, 215, 0, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(16, 185, 129, 0.08) 0%, transparent 40%),
                linear-gradient(180deg, #030712 0%, #0B132B 50%, #020617 100%);
            color: #F8FAFC; min-height: 100vh; padding-bottom: 60px;
        }
        .laser-top {
            position: fixed; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, #FFD700, #10B981, #00F0FF);
            box-shadow: 0 0 15px #FFD700; z-index: 9999;
        }
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
            padding: 22px;
        }
        header {
            position: sticky; top: 0; z-index: 100;
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 24px; border-bottom: 1px solid var(--glass-border);
            background: rgba(11, 19, 43, 0.88); backdrop-filter: blur(20px);
        }
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 24px 0; }
        .chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; margin: 24px 0; }
        .kpi-val { font-size: 2rem; font-weight: 900; font-family: 'JetBrains Mono'; margin: 8px 0; }
        .sim-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin: 20px 0; }
        .sim-box { background: rgba(0, 0, 0, 0.45); padding: 18px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08); }
        .sim-slider { width: 100%; accent-color: var(--fin-gold); cursor: pointer; }
        .sim-banner {
            display: flex; justify-content: space-around; flex-wrap: wrap; gap: 16px;
            background: linear-gradient(90deg, rgba(255,215,0,0.1), rgba(16,185,129,0.1), rgba(0,240,255,0.1));
            padding: 20px; border-radius: 16px; border: 1px solid rgba(255,215,0,0.35); text-align: center;
        }
        .badge {
            padding: 4px 12px; border-radius: 999px; font-size: 0.72rem; font-family: 'JetBrains Mono';
            background: rgba(255, 215, 0, 0.12); color: var(--fin-gold); border: 1px solid rgba(255, 215, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="laser-top"></div>
    <header>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 12px; background: linear-gradient(135deg, #FFD700, #10B981); display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">🐍</div>
            <div>
                <h1 style="font-size: 1.1rem; font-weight: 900;">
                    منصة إدارة الثروات والأصول السيادية
                    <span class="badge">Python Server :8501</span>
                </h1>
                <p style="font-size: 0.72rem; color: #94A3B8;">خادم بايثون المحلي عالي الإنتاجية • القاهرة</p>
            </div>
        </div>
        <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #10B981; border-color: rgba(16, 185, 129, 0.4);">
            ● خادم محلي نشط 8501
        </span>
    </header>

    <main style="max-width: 1200px; margin: 0 auto; padding: 24px 16px;">
        <div class="glass-panel" style="border-right: 4px solid var(--fin-gold); margin-bottom: 24px;">
            <span style="font-size: 0.75rem; color: var(--fin-gold); font-family: 'JetBrains Mono'; font-weight: 700;">محفظة الأصول المعتمدة 2026</span>
            <h2 style="font-size: 1.6rem; font-weight: 900; margin-top: 4px;">
                إجمالي الأصول المدارة: <span style="color: var(--fin-gold); font-family: 'JetBrains Mono';">185.40</span> مليون جنيه مصري
            </h2>
            <p style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px;">
                محسوبة فورياً بخوارزميات بايثون الرياضية بنسبة عائد موزون <strong style="color: #10B981; font-family: 'JetBrains Mono';">+24.8%</strong>.
            </p>
        </div>

        <div class="kpi-grid">
            <div class="glass-panel" style="border-right: 3px solid #FFD700;">
                <span style="font-size: 0.75rem; color: #94A3B8;">أذون الخزانة المصرية (T-Bills 1Y)</span>
                <div class="kpi-val" style="color: #FFD700;">75.0 <span style="font-size: 0.9rem; color: #94A3B8;">مليون ج.م</span></div>
                <div style="font-size: 0.75rem; color: #10B981; font-family: 'JetBrains Mono'; font-weight: 700;">+27.25% عائد خالي من المخاطر</div>
            </div>
            <div class="glass-panel" style="border-right: 3px solid #F59E0B;">
                <span style="font-size: 0.75rem; color: #94A3B8;">سبائك الذهب الفعلي (24K Gold)</span>
                <div class="kpi-val" style="color: #F59E0B;">42.5 <span style="font-size: 0.9rem; color: #94A3B8;">مليون ج.م</span></div>
                <div style="font-size: 0.75rem; color: #10B981; font-family: 'JetBrains Mono'; font-weight: 700;">+38.60% تحوط تضخمي وسيولة فورية</div>
            </div>
            <div class="glass-panel" style="border-right: 3px solid #00F0FF;">
                <span style="font-size: 0.75rem; color: #94A3B8;">أسهم البورصة المصرية (EGX30)</span>
                <div class="kpi-val" style="color: #00F0FF;">38.2 <span style="font-size: 0.9rem; color: #94A3B8;">مليون ج.م</span></div>
                <div style="font-size: 0.75rem; color: #10B981; font-family: 'JetBrains Mono'; font-weight: 700;">+29.40% CIB، إي فاينانس، طلعت مصطفى</div>
            </div>
            <div class="glass-panel" style="border-right: 3px solid #10B981;">
                <span style="font-size: 0.75rem; color: #94A3B8;">أصول عقارية تجارية (Real Estate)</span>
                <div class="kpi-val" style="color: #10B981;">29.7 <span style="font-size: 0.9rem; color: #94A3B8;">مليون ج.م</span></div>
                <div style="font-size: 0.75rem; color: #10B981; font-family: 'JetBrains Mono'; font-weight: 700;">+14.80% عائد إيجاري بالتجمع والشيخ زايد</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="glass-panel">
                <h3 style="font-size: 0.95rem; margin-bottom: 12px;">📊 توزيع الأصول الرأسمالية (Plotly Donut)</h3>
                <div id="chartDonut"></div>
            </div>
            <div class="glass-panel">
                <h3 style="font-size: 0.95rem; margin-bottom: 12px;">📈 توقعات النمو التراكمي لـ 5 سنوات (Plotly Spline)</h3>
                <div id="chartGrowth"></div>
            </div>
        </div>

        <div class="glass-panel" style="border: 1px solid rgba(255, 215, 0, 0.4); margin-top: 24px;">
            <h2 style="font-size: 1.25rem; font-weight: 900; margin-bottom: 6px;">محاكي إعادة توزيع الأصول بالجنيه المصري</h2>
            <p style="font-size: 0.8rem; color: #94A3B8;">حرك نسب الأصول لمشاهدة التغير الفوري في العائد والسيولة الشهرية.</p>

            <div class="sim-grid">
                <div class="sim-box">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 8px;">
                        <span>أذون الخزانة المصرية (27.25%)</span>
                        <span id="lblTbills" style="color: #FFD700; font-family: 'JetBrains Mono'; font-weight: 700;">40%</span>
                    </div>
                    <input type="range" id="rngTbills" min="10" max="70" step="5" value="40" class="sim-slider" oninput="runSim()">
                </div>
                <div class="sim-box">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 8px;">
                        <span>سبائك الذهب الفعلي (38.6%)</span>
                        <span id="lblGold" style="color: #F59E0B; font-family: 'JetBrains Mono'; font-weight: 700;">25%</span>
                    </div>
                    <input type="range" id="rngGold" min="10" max="50" step="5" value="25" class="sim-slider" oninput="runSim()">
                </div>
                <div class="sim-box">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 8px;">
                        <span>أسهم البورصة EGX30 (29.4%)</span>
                        <span id="lblEquity" style="color: #00F0FF; font-family: 'JetBrains Mono'; font-weight: 700;">20%</span>
                    </div>
                    <input type="range" id="rngEquity" min="5" max="40" step="5" value="20" class="sim-slider" oninput="runSim()">
                </div>
            </div>

            <div class="sim-banner">
                <div>
                    <span style="font-size: 0.72rem; color: #94A3B8;">العائد السنوي الموزون</span>
                    <p id="resYield" style="font-size: 1.8rem; font-weight: 900; color: #FFD700; font-family: 'JetBrains Mono';">+25.80%</p>
                </div>
                <div>
                    <span style="font-size: 0.72rem; color: #94A3B8;">الأرباح السنوية المتوقعة</span>
                    <p id="resAnnual" style="font-size: 1.8rem; font-weight: 900; color: #10B981; font-family: 'JetBrains Mono';">47.83 M EGP</p>
                </div>
                <div>
                    <span style="font-size: 0.72rem; color: #94A3B8;">التدفق الشهري المتولد</span>
                    <p id="resMonthly" style="font-size: 1.8rem; font-weight: 900; color: #00F0FF; font-family: 'JetBrains Mono';">3,986 ألف ج.م / شهر</p>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Render Plotly Charts
        Plotly.newPlot('chartDonut', [{
            values: [75.0, 42.5, 38.2, 29.7],
            labels: ['أذون الخزانة المصرية', 'سبائك الذهب الفعلي', 'أسهم EGX30', 'أصول عقارية مدرة'],
            type: 'pie',
            hole: 0.6,
            marker: { colors: ['#FFD700', '#F59E0B', '#00F0FF', '#10B981'], line: { color: '#030712', width: 2 } },
            textinfo: 'percent+label'
        }], {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#F8FAFC', family: 'Cairo' },
            showlegend: false,
            height: 280,
            margin: { l: 10, r: 10, t: 10, b: 10 }
        });

        Plotly.newPlot('chartGrowth', [
            {
                x: ['2026', '2027', '2028', '2029', '2030'],
                y: [75.0, 95.4, 121.4, 154.5, 196.6],
                name: 'أذون الخزانة (27.25%)',
                line: { color: '#FFD700', width: 3, shape: 'spline' },
                mode: 'lines+markers'
            },
            {
                x: ['2026', '2027', '2028', '2029', '2030'],
                y: [42.5, 58.9, 81.6, 113.1, 156.8],
                name: 'سبائك الذهب (38.6%)',
                line: { color: '#F59E0B', width: 3, dash: 'dot', shape: 'spline' },
                mode: 'lines+markers'
            }
        ], {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#F8FAFC', family: 'Cairo' },
            height: 280,
            margin: { l: 30, r: 20, t: 20, b: 30 },
            xaxis: { showgrid: false },
            yaxis: { showgrid: true, gridcolor: 'rgba(255,255,255,0.06)' }
        });

        function runSim() {
            const tbills = parseInt(document.getElementById('rngTbills').value);
            const gold = parseInt(document.getElementById('rngGold').value);
            const equity = parseInt(document.getElementById('rngEquity').value);
            const re = Math.max(0, 100 - tbills - gold - equity);

            document.getElementById('lblTbills').innerText = tbills + '%';
            document.getElementById('lblGold').innerText = gold + '%';
            document.getElementById('lblEquity').innerText = equity + '%';

            const aum = 185.4;
            const y = ((tbills * 27.25) + (gold * 38.60) + (equity * 29.40) + (re * 14.80)) / 100;
            const annual = aum * (y / 100);
            const monthly = (annual / 12) * 1000;

            document.getElementById('resYield').innerText = '+' + y.toFixed(2) + '%';
            document.getElementById('resAnnual').innerText = annual.toFixed(2) + ' M EGP';
            document.getElementById('resMonthly').innerText = Math.round(monthly).toLocaleString() + ' ألف ج.م / شهر';
        }
    </script>
</body>
</html>"""

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        index_path = os.path.join(os.path.dirname(__file__), "index.html")
        if os.path.exists(index_path):
            with open(index_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(HTML_PAGE.encode("utf-8"))

if __name__ == "__main__":
    print(f"🚀 Sovereign Python Dashboard Server active at: http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
