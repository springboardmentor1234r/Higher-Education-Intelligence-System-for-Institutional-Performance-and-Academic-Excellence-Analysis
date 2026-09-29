#!/usr/bin/env python3
"""
EduVision_DV: Interactive Executive Dashboard Application Generator
Builds a standalone, responsive, high-performance HTML/JS dashboard suite
implementing all 4 dashboards, KPI cards, charts, filters, and cross-filtering actions.
"""

import json
import os
import pandas as pd

def build_dashboard():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'university_final_dataset.csv')
    if not os.path.exists(csv_path):
        csv_path = 'university_final_dataset.csv'
        
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Filter only the columns needed for the dashboards
    keep_cols = [
        'RANK_2025', 'Rank_2025_Numeric', 'Institution_Name', 'Location', 'Region',
        'SIZE', 'FOCUS', 'RES.', 'Overall_Score', 'KPI_Global_Ranking_Score',
        'KPI_Academic_Reputation_Score', 'KPI_Research_Impact_Score',
        'KPI_Faculty_to_Student_Ratio', 'KPI_International_Student_Pct',
        'KPI_Research_Productivity_Proxy', 'THE_No_of_FTE_Students',
        'Display_Students_per_Staff', 'Display_Int_Student_Pct', 'Display_Research_Productivity'
    ]
    df_clean = df[keep_cols].copy()
    
    # Country alias mapping for Plotly choropleth
    country_map_alias = {
        'China (Mainland)': 'China',
        'Hong Kong SAR': 'Hong Kong',
        'Macau SAR': 'Macao',
        'Iran, Islamic Republic of': 'Iran',
        'Russia': 'Russia',
        'South Korea': 'South Korea',
        'United States': 'United States',
        'United Kingdom': 'United Kingdom',
        'Syrian Arab Republic': 'Syria',
        'Czech Republic': 'Czech Republic'
    }
    df_clean['Plotly_Country'] = df_clean['Location'].map(lambda x: country_map_alias.get(x, x))
    
    data_json = df_clean.to_json(orient='records')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduVision_DV: Global Higher Education Performance Analytics</title>
    <!-- Plotly.js CDN -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        :root {{
            --bg-canvas: #12161A;
            --bg-card: #1B2026;
            --bg-card-hover: #222932;
            --border: #28323D;
            --text-primary: #FFFFFF;
            --text-secondary: #CFD6DF;
            --text-muted: #8A9BA8;
            --accent-overview: #00D2C4;
            --accent-research: #FF9F1C;
            --accent-student: #2EC4B6;
            --accent-country: #00D2C4;
            --accent-alert: #E71D36;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}

        body {{
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        /* Header Bar */
        header {{
            background-color: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .brand {{
            display: flex;
            flex-direction: column;
        }}

        .brand h1 {{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #FFFFFF;
        }}

        .brand h1 span {{
            color: var(--accent-overview);
        }}

        .brand p {{
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        .meta-badges {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}

        .badge {{
            background: rgba(0, 210, 196, 0.12);
            border: 1px solid rgba(0, 210, 196, 0.3);
            color: var(--accent-overview);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}

        /* Navigation Tabs */
        nav {{
            background-color: #161B21;
            border-bottom: 1px solid var(--border);
            display: flex;
            padding: 0 32px;
            gap: 8px;
            overflow-x: auto;
        }}

        .tab-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            padding: 14px 20px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s ease;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .tab-btn:hover {{
            color: #FFFFFF;
            background-color: rgba(255, 255, 255, 0.03);
        }}

        .tab-btn.active {{
            color: #FFFFFF;
            border-bottom-color: var(--accent-overview);
            background-color: rgba(0, 210, 196, 0.06);
        }}

        .tab-btn[data-tab="research"].active {{
            border-bottom-color: var(--accent-research);
            background-color: rgba(255, 159, 28, 0.06);
        }}

        .tab-btn[data-tab="student"].active {{
            border-bottom-color: var(--accent-student);
            background-color: rgba(46, 196, 182, 0.06);
        }}

        .tab-btn[data-tab="country"].active {{
            border-bottom-color: var(--accent-country);
            background-color: rgba(0, 210, 196, 0.06);
        }}

        /* Filter Toolbar */
        .filter-bar {{
            background-color: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 14px 32px;
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .filter-group label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .filter-select {{
            background-color: #12161A;
            border: 1px solid var(--border);
            color: #FFFFFF;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            outline: none;
            min-width: 150px;
            transition: border-color 0.2s;
        }}

        .filter-select:focus {{
            border-color: var(--accent-overview);
        }}

        .filter-actions {{
            display: flex;
            align-items: flex-end;
            margin-left: auto;
            gap: 12px;
        }}

        .reset-btn {{
            background: #252D37;
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .reset-btn:hover {{
            background: #2E3743;
            color: #FFFFFF;
        }}

        .active-filter-pill {{
            font-size: 12px;
            color: var(--text-muted);
            align-self: center;
        }}

        /* Main Container */
        main {{
            padding: 24px 32px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        .tab-panel {{
            display: none;
            flex-direction: column;
            gap: 24px;
        }}

        .tab-panel.active {{
            display: flex;
        }}

        /* KPI Cards Container */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}

        .kpi-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background-color: var(--accent-overview);
        }}

        .kpi-card.research::before {{
            background-color: var(--accent-research);
        }}

        .kpi-card.student::before {{
            background-color: var(--accent-student);
        }}

        .kpi-card.country::before {{
            background-color: var(--accent-country);
        }}

        .kpi-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 700;
            color: var(--text-muted);
        }}

        .kpi-value {{
            font-size: 32px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.5px;
        }}

        .kpi-sub {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        /* Grid Layout for Charts */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 20px;
        }}

        .chart-box {{
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chart-title {{
            font-size: 15px;
            font-weight: 700;
            color: #FFFFFF;
        }}

        .chart-desc {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .chart-content {{
            width: 100%;
            min-height: 380px;
            position: relative;
        }}

        .col-4 {{ grid-column: span 4; }}
        .col-6 {{ grid-column: span 6; }}
        .col-8 {{ grid-column: span 8; }}
        .col-12 {{ grid-column: span 12; }}

        @media (max-width: 1100px) {{
            .col-4, .col-6, .col-8 {{ grid-column: span 12; }}
        }}

        /* Notice banner */
        .notice-banner {{
            background: rgba(255, 159, 28, 0.08);
            border-left: 4px solid var(--accent-research);
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 13px;
            color: var(--text-secondary);
        }}

        /* Table formatting */
        .table-container {{
            overflow-x: auto;
            max-height: 480px;
            border: 1px solid var(--border);
            border-radius: 6px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}

        th {{
            background-color: #161B21;
            color: var(--text-secondary);
            padding: 12px 16px;
            position: sticky;
            top: 0;
            font-weight: 600;
            border-bottom: 1px solid var(--border);
        }}

        td {{
            padding: 10px 16px;
            border-bottom: 1px solid rgba(40, 50, 61, 0.5);
            color: #FFFFFF;
        }}

        tr:hover {{
            background-color: var(--bg-card-hover);
            cursor: pointer;
        }}

        tr.selected-country {{
            background-color: rgba(0, 210, 196, 0.15) !important;
            border-left: 3px solid var(--accent-overview);
        }}

        .search-box {{
            background: #12161A;
            border: 1px solid var(--border);
            color: #FFFFFF;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            width: 100%;
            max-width: 300px;
        }}
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <h1>EduVision_DV <span>Performance Analytics</span></h1>
            <p>Infosys Springboard Virtual Internship Project • Global Higher Education Intelligence</p>
        </div>
        <div class="meta-badges">
            <div class="badge" id="institutionCountBadge">1,503 Institutions</div>
            <div class="badge" style="color: #FF9F1C; border-color: rgba(255,159,28,0.3); background: rgba(255,159,28,0.12);">106 Countries</div>
            <div class="badge" style="color: #2EC4B6; border-color: rgba(46,196,182,0.3); background: rgba(46,196,182,0.12);">QS 2025 + THE Rankings</div>
        </div>
    </header>

    <nav>
        <button class="tab-btn active" data-tab="overview">🌐 1. University Overview</button>
        <button class="tab-btn" data-tab="research">🔬 2. Research Analytics</button>
        <button class="tab-btn" data-tab="student">🎓 3. Student Analytics</button>
        <button class="tab-btn" data-tab="country">🗺️ 4. Country Comparison</button>
    </nav>

    <!-- Global Interactive Filter Toolbar -->
    <div class="filter-bar">
        <div class="filter-group">
            <label for="filterRegion">Region</label>
            <select id="filterRegion" class="filter-select">
                <option value="ALL">All Regions</option>
            </select>
        </div>
        <div class="filter-group">
            <label for="filterLocation">Location (Country)</label>
            <select id="filterLocation" class="filter-select">
                <option value="ALL">All Locations</option>
            </select>
        </div>
        <div class="filter-group">
            <label for="filterSize">Size</label>
            <select id="filterSize" class="filter-select">
                <option value="ALL">All Sizes</option>
            </select>
        </div>
        <div class="filter-group">
            <label for="filterFocus">Subject Focus</label>
            <select id="filterFocus" class="filter-select">
                <option value="ALL">All Focus Areas</option>
            </select>
        </div>
        <div class="filter-actions">
            <span class="active-filter-pill" id="filterStatus">Showing 1,503 / 1,503 universities</span>
            <button class="reset-btn" id="btnResetFilters">↺ Reset Filters</button>
        </div>
    </div>

    <main>
        <!-- ============================================== -->
        <!-- DASHBOARD 1: UNIVERSITY OVERVIEW -->
        <!-- ============================================== -->
        <section id="panel-overview" class="tab-panel active">
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-title">Top Ranked University</div>
                    <div class="kpi-value" id="d1_top_uni" style="color: var(--accent-overview); font-size: 24px;">MIT</div>
                    <div class="kpi-sub">#1 in World Rankings 2025</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Total Universities</div>
                    <div class="kpi-value" id="d1_total_unis">1,503</div>
                    <div class="kpi-sub" id="d1_countries_covered">106 Countries Covered</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Average Global Score</div>
                    <div class="kpi-value" id="d1_avg_score">41.84</div>
                    <div class="kpi-sub">Avg. of Top 600 Scored Institutions</div>
                </div>
            </div>

            <div class="charts-grid">
                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Top 10 Universities by Global Score</div>
                            <div class="chart-desc">Highest composite scores in QS World University Rankings 2025</div>
                        </div>
                    </div>
                    <div id="chart-d1-top10" class="chart-content"></div>
                </div>

                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Universities by Region</div>
                            <div class="chart-desc">Continental distribution across 1,503 institutions</div>
                        </div>
                    </div>
                    <div id="chart-d1-region" class="chart-content"></div>
                </div>

                <div class="chart-box col-12">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Geographic Institutional Distribution</div>
                            <div class="chart-desc">Global concentration and university density per country</div>
                        </div>
                    </div>
                    <div id="chart-d1-map" class="chart-content" style="min-height: 480px;"></div>
                </div>
            </div>
        </section>

        <!-- ============================================== -->
        <!-- DASHBOARD 2: RESEARCH ANALYTICS -->
        <!-- ============================================== -->
        <section id="panel-research" class="tab-panel">
            <div class="kpi-row">
                <div class="kpi-card research">
                    <div class="kpi-title">Highest Research Impact</div>
                    <div class="kpi-value" id="d2_max_impact" style="color: var(--accent-research);">100.0</div>
                    <div class="kpi-sub">Citations per Faculty Max</div>
                </div>
                <div class="kpi-card research">
                    <div class="kpi-title">Average Citation Score</div>
                    <div class="kpi-value" id="d2_avg_citation">23.5</div>
                    <div class="kpi-sub">Citations per Faculty (All Scored)</div>
                </div>
                <div class="kpi-card research">
                    <div class="kpi-title">Average Research Productivity (Proxy)</div>
                    <div class="kpi-value" id="d2_avg_productivity">61.2</div>
                    <div class="kpi-sub">THE Environment Metric (Matched Sample)</div>
                </div>
            </div>

            <div class="notice-banner">
                <strong>Analytical Disclosure:</strong> Research Productivity (Proxy) uses THE Research Environment and is available only for matched QS-THE institutions.
            </div>

            <div class="charts-grid">
                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Research Impact vs Research Productivity (Proxy)</div>
                            <div class="chart-desc">Correlation between research environment and citations per faculty</div>
                        </div>
                    </div>
                    <div id="chart-d2-scatter" class="chart-content"></div>
                </div>

                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Research Intensity Comparison</div>
                            <div class="chart-desc">Distribution of citation impact across institutional intensity levels (RES.)</div>
                        </div>
                    </div>
                    <div id="chart-d2-box" class="chart-content"></div>
                </div>

                <div class="chart-box col-12">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Top 10 Research Institutions</div>
                            <div class="chart-desc">Comparing Research Impact Score vs Research Productivity Proxy</div>
                        </div>
                    </div>
                    <div id="chart-d2-top10" class="chart-content"></div>
                </div>
            </div>
        </section>

        <!-- ============================================== -->
        <!-- DASHBOARD 3: STUDENT ANALYTICS -->
        <!-- ============================================== -->
        <section id="panel-student" class="tab-panel">
            <div class="kpi-row">
                <div class="kpi-card student">
                    <div class="kpi-title">Average Students per Staff</div>
                    <div class="kpi-value" id="d3_students_staff" style="color: var(--accent-student);">17.4</div>
                    <div class="kpi-sub">Faculty-to-Student Ratio (Students per Staff)</div>
                </div>
                <div class="kpi-card student">
                    <div class="kpi-title">Average International Student %</div>
                    <div class="kpi-value" id="d3_intl_pct">25.5%</div>
                    <div class="kpi-sub">Global Student Mobility Footprint</div>
                </div>
                <div class="kpi-card student">
                    <div class="kpi-title">Total FTE Student Headcount</div>
                    <div class="kpi-value" id="d3_fte_total">5.46M</div>
                    <div class="kpi-sub">Total Enrollment Across Matched Sample</div>
                </div>
            </div>

            <div class="charts-grid">
                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Average Students per Staff by Region</div>
                            <div class="chart-desc">Institutional teaching load comparison by continent</div>
                        </div>
                    </div>
                    <div id="chart-d3-region-ratio" class="chart-content"></div>
                </div>

                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Internationalization Scatter</div>
                            <div class="chart-desc">International Student % vs Student-to-Faculty Ratio</div>
                        </div>
                    </div>
                    <div id="chart-d3-scatter" class="chart-content"></div>
                </div>

                <div class="chart-box col-12">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Top 10 Universities by Enrollment</div>
                            <div class="chart-desc">Institutions with highest Full-Time Equivalent (FTE) student volume</div>
                        </div>
                    </div>
                    <div id="chart-d3-enrollment" class="chart-content"></div>
                </div>
            </div>
        </section>

        <!-- ============================================== -->
        <!-- DASHBOARD 4: COUNTRY COMPARISON -->
        <!-- ============================================== -->
        <section id="panel-country" class="tab-panel">
            <div class="kpi-row">
                <div class="kpi-card country">
                    <div class="kpi-title">Top Country by Average QS Score</div>
                    <div class="kpi-value" id="d4_top_country" style="color: var(--accent-country); font-size: 26px;">Hong Kong SAR</div>
                    <div class="kpi-sub" id="d4_top_country_sub">Avg Score: 71.52 (Scored subset)</div>
                </div>
                <div class="kpi-card country">
                    <div class="kpi-title">Total Ranked Countries</div>
                    <div class="kpi-value" id="d4_total_countries">106</div>
                    <div class="kpi-sub">Global Analytical Coverage</div>
                </div>
                <div class="kpi-card country">
                    <div class="kpi-title">Most Represented Country</div>
                    <div class="kpi-value" id="d4_most_rep" style="font-size: 26px;">United States</div>
                    <div class="kpi-sub">197 Ranked Universities</div>
                </div>
            </div>

            <div class="notice-banner" style="border-color: var(--accent-overview); background: rgba(0, 210, 196, 0.08);">
                <strong>Interactive Dashboard Action:</strong> Click any country in the benchmarking table below to highlight that country and zoom the map directly!
                <button id="btnClearCountryAction" class="reset-btn" style="margin-left: 16px; padding: 4px 10px; font-size: 11px;">Show All Countries</button>
            </div>

            <div class="charts-grid">
                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Country Benchmarking Scorecard</div>
                            <div class="chart-desc">Click a country to filter geographic map</div>
                        </div>
                        <input type="text" id="tableSearch" class="search-box" placeholder="🔍 Search country...">
                    </div>
                    <div class="table-container">
                        <table id="countryTable">
                            <thead>
                                <tr>
                                    <th>Country / Territory</th>
                                    <th>Universities</th>
                                    <th>Avg Global Score</th>
                                    <th>Avg Academic Rep</th>
                                    <th>Avg Research Impact</th>
                                </tr>
                            </thead>
                            <tbody id="countryTableBody">
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="chart-box col-6">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Geographic Country Performance Map</div>
                            <div class="chart-desc" id="mapHeaderDesc">World map showing university footprint by nation</div>
                        </div>
                    </div>
                    <div id="chart-d4-map" class="chart-content" style="min-height: 480px;"></div>
                </div>
            </div>
        </section>
    </main>

    <!-- Master Inlined JSON Data -->
    <script>
        const rawData = {data_json};
        let selectedCountryAction = null;

        // Dark theme layout template for Plotly
        const darkPlotLayout = {{
            paper_bgcolor: '#1B2026',
            plot_bgcolor: '#1B2026',
            font: {{
                color: '#CFD6DF',
                family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            }},
            margin: {{ l: 50, r: 30, t: 30, b: 50 }},
            xaxis: {{
                gridcolor: '#28323D',
                linecolor: '#28323D',
                tickfont: {{ color: '#8A9BA8' }},
                zerolinecolor: '#28323D'
            }},
            yaxis: {{
                gridcolor: '#28323D',
                linecolor: '#28323D',
                tickfont: {{ color: '#8A9BA8' }},
                zerolinecolor: '#28323D'
            }}
        }};

        // Initialize Filter Options
        function initFilters() {{
            const regions = Array.from(new Set(rawData.map(d => d.Region).filter(Boolean))).sort();
            const regSelect = document.getElementById('filterRegion');
            regions.forEach(r => {{
                const opt = document.createElement('option');
                opt.value = r;
                opt.textContent = r;
                regSelect.appendChild(opt);
            }});

            const sizes = ['S', 'M', 'L', 'XL'];
            const sizeSelect = document.getElementById('filterSize');
            sizes.forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s;
                opt.textContent = s;
                sizeSelect.appendChild(opt);
            }});

            const focuses = ['FC', 'FO', 'CO', 'SP'];
            const focusLabels = {{
                'FC': 'FC - Fully Comprehensive',
                'CO': 'CO - Comprehensive',
                'FO': 'FO - Focused',
                'SP': 'SP - Specialist'
            }};
            const focusSelect = document.getElementById('filterFocus');
            focuses.forEach(f => {{
                const opt = document.createElement('option');
                opt.value = f;
                opt.textContent = focusLabels[f] || f;
                focusSelect.appendChild(opt);
            }});

            updateLocationDropdown();
        }}

        // Cascading Location dropdown based on Region
        function updateLocationDropdown() {{
            const selectedRegion = document.getElementById('filterRegion').value;
            const locSelect = document.getElementById('filterLocation');
            const currentLoc = locSelect.value;
            
            locSelect.innerHTML = '<option value="ALL">All Locations</option>';
            
            let filtered = rawData;
            if (selectedRegion !== 'ALL') {{
                filtered = filtered.filter(d => d.Region === selectedRegion);
            }}
            
            const locations = Array.from(new Set(filtered.map(d => d.Location).filter(Boolean))).sort();
            locations.forEach(loc => {{
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = loc;
                locSelect.appendChild(opt);
            }});

            if (locations.includes(currentLoc)) {{
                locSelect.value = currentLoc;
            }} else {{
                locSelect.value = 'ALL';
            }}
        }}

        // Get currently filtered records
        function getFilteredData() {{
            const reg = document.getElementById('filterRegion').value;
            const loc = document.getElementById('filterLocation').value;
            const size = document.getElementById('filterSize').value;
            const focus = document.getElementById('filterFocus').value;

            return rawData.filter(d => {{
                if (reg !== 'ALL' && d.Region !== reg) return false;
                if (loc !== 'ALL' && d.Location !== loc) return false;
                if (size !== 'ALL' && d.SIZE !== size) return false;
                if (focus !== 'ALL' && d.FOCUS !== focus) return false;
                return true;
            }});
        }}

        // Helper calculations
        const avg = arr => arr.length ? (arr.reduce((a, b) => a + b, 0) / arr.length) : null;
        const sum = arr => arr.reduce((a, b) => a + b, 0);

        // Update all KPI Cards & Charts across all tabs
        function renderAll() {{
            const data = getFilteredData();
            document.getElementById('filterStatus').textContent = `Showing ${{data.length.toLocaleString()}} / ${{rawData.length.toLocaleString()}} universities`;
            document.getElementById('institutionCountBadge').textContent = `${{data.length.toLocaleString()}} Institutions`;

            renderDashboard1(data);
            renderDashboard2(data);
            renderDashboard3(data);
            renderDashboard4(data);
        }}

        // ==========================================
        // RENDER DASHBOARD 1: UNIVERSITY OVERVIEW
        // ==========================================
        function renderDashboard1(data) {{
            // Top Ranked
            const sortedRank = [...data].filter(d => d.Rank_2025_Numeric != null).sort((a, b) => a.Rank_2025_Numeric - b.Rank_2025_Numeric);
            const topUni = sortedRank.length ? sortedRank[0].Institution_Name : 'N/A';
            document.getElementById('d1_top_uni').textContent = topUni.length > 28 ? topUni.substring(0, 26) + '...' : topUni;
            document.getElementById('d1_top_uni').title = topUni;

            // Total Unis & Countries
            document.getElementById('d1_total_unis').textContent = data.length.toLocaleString();
            const countries = new Set(data.map(d => d.Location).filter(Boolean));
            document.getElementById('d1_countries_covered').textContent = `${{countries.size}} Countries Covered`;

            // Avg Global Score (valid non-null top 600)
            const scores = data.map(d => d.KPI_Global_Ranking_Score).filter(s => s != null && !isNaN(s));
            const meanScore = avg(scores);
            document.getElementById('d1_avg_score').textContent = meanScore != null ? meanScore.toFixed(2) : 'N/A';

            // Chart 1: Top 10 by Global Score
            const top10 = [...data].filter(d => d.KPI_Global_Ranking_Score != null)
                                   .sort((a, b) => b.KPI_Global_Ranking_Score - a.KPI_Global_Ranking_Score)
                                   .slice(0, 10)
                                   .reverse();

            const traceTop10 = {{
                type: 'bar',
                orientation: 'h',
                x: top10.map(d => d.KPI_Global_Ranking_Score),
                y: top10.map(d => d.Institution_Name.length > 25 ? d.Institution_Name.substring(0, 23) + '...' : d.Institution_Name),
                text: top10.map(d => d.KPI_Global_Ranking_Score.toFixed(1)),
                textposition: 'auto',
                marker: {{
                    color: '#00D2C4',
                    line: {{ color: '#00B4A7', width: 1 }}
                }},
                hovertext: top10.map(d => `${{d.Institution_Name}}<br>Score: ${{d.KPI_Global_Ranking_Score}}<br>Location: ${{d.Location}}`),
                hoverinfo: 'text'
            }};

            Plotly.newPlot('chart-d1-top10', [traceTop10], {{
                ...darkPlotLayout,
                margin: {{ l: 180, r: 40, t: 10, b: 40 }},
                xaxis: {{ ...darkPlotLayout.xaxis, title: 'Global Ranking Score', range: [80, 102] }}
            }}, {{ responsive: true, displayModeBar: false }});

            // Chart 2: Universities by Region (Donut)
            const regionCounts = {{}};
            data.forEach(d => {{
                const r = d.Region || 'Unclassified';
                regionCounts[r] = (regionCounts[r] || 0) + 1;
            }});

            const traceDonut = {{
                type: 'pie',
                hole: 0.6,
                labels: Object.keys(regionCounts),
                values: Object.values(regionCounts),
                marker: {{
                    colors: ['#00D2C4', '#FF9F1C', '#2EC4B6', '#3A86FF', '#8338EC', '#E71D36']
                }},
                textinfo: 'label+percent',
                insidetextfont: {{ color: '#FFFFFF' }},
                hoverinfo: 'label+value+percent'
            }};

            Plotly.newPlot('chart-d1-region', [traceDonut], {{
                ...darkPlotLayout,
                annotations: [{{
                    font: {{ size: 20, color: '#FFFFFF', weight: 'bold' }},
                    showarrow: false,
                    text: data.length.toLocaleString(),
                    x: 0.5,
                    y: 0.5
                }}],
                showlegend: false,
                margin: {{ l: 20, r: 20, t: 20, b: 20 }}
            }}, {{ responsive: true, displayModeBar: false }});

            // Chart 3: World Map (Institutional Distribution)
            const countryCounts = {{}};
            data.forEach(d => {{
                if (d.Plotly_Country) {{
                    countryCounts[d.Plotly_Country] = (countryCounts[d.Plotly_Country] || 0) + 1;
                }}
            }});

            const traceMap = {{
                type: 'choropleth',
                locationmode: 'country names',
                locations: Object.keys(countryCounts),
                z: Object.values(countryCounts),
                colorscale: [
                    [0, '#162832'],
                    [0.1, '#005B60'],
                    [0.4, '#008E85'],
                    [0.7, '#00B4A7'],
                    [1, '#00D2C4']
                ],
                colorbar: {{
                    title: 'Universities',
                    tickfont: {{ color: '#CFD6DF' }},
                    titlefont: {{ color: '#CFD6DF' }}
                }},
                hovertext: Object.entries(countryCounts).map(([c, count]) => `${{c}}: ${{count}} institutions`),
                hoverinfo: 'text'
            }};

            Plotly.newPlot('chart-d1-map', [traceMap], {{
                ...darkPlotLayout,
                geo: {{
                    bgcolor: '#12161A',
                    lakecolor: '#12161A',
                    landcolor: '#1B2026',
                    showland: true,
                    showocean: true,
                    oceancolor: '#12161A',
                    showcountries: true,
                    countrycolor: '#28323D',
                    projection: {{ type: 'natural earth' }}
                }},
                margin: {{ l: 0, r: 0, t: 0, b: 0 }}
            }}, {{ responsive: true, displayModeBar: false }});
        }}

        // ==========================================
        // RENDER DASHBOARD 2: RESEARCH ANALYTICS
        // ==========================================
        function renderDashboard2(data) {{
            // KPI 1: Highest Research Impact
            const impacts = data.map(d => d.KPI_Research_Impact_Score).filter(s => s != null && !isNaN(s));
            const maxImpact = impacts.length ? Math.max(...impacts) : 0;
            document.getElementById('d2_max_impact').textContent = maxImpact.toFixed(1);

            // KPI 2: Average Citation Score
            const avgCitation = avg(impacts);
            document.getElementById('d2_avg_citation').textContent = avgCitation != null ? avgCitation.toFixed(1) : 'N/A';

            // KPI 3: Average Research Productivity Proxy
            const prodScores = data.map(d => d.KPI_Research_Productivity_Proxy).filter(s => s != null && !isNaN(s));
            const avgProd = avg(prodScores);
            document.getElementById('d2_avg_productivity').textContent = avgProd != null ? avgProd.toFixed(1) : 'N/A';

            // Chart 1: Scatter Plot (Impact vs Productivity Proxy)
            const matched = data.filter(d => d.KPI_Research_Productivity_Proxy != null && d.KPI_Research_Impact_Score != null);
            
            const regionGroups = {{}};
            matched.forEach(d => {{
                const r = d.Region || 'Other';
                if (!regionGroups[r]) regionGroups[r] = [];
                regionGroups[r].push(d);
            }});

            const scatterTraces = Object.entries(regionGroups).map(([reg, items]) => ({{
                type: 'scatter',
                mode: 'markers',
                name: reg,
                x: items.map(d => d.KPI_Research_Productivity_Proxy),
                y: items.map(d => d.KPI_Research_Impact_Score),
                hovertext: items.map(d => `<b>${{d.Institution_Name}}</b><br>Location: ${{d.Location}}<br>Productivity (Proxy): ${{d.KPI_Research_Productivity_Proxy}}<br>Citation Score: ${{d.KPI_Research_Impact_Score}}`),
                hoverinfo: 'text',
                marker: {{ size: 8, opacity: 0.8 }}
            }}));

            Plotly.newPlot('chart-d2-scatter', scatterTraces, {{
                ...darkPlotLayout,
                xaxis: {{ ...darkPlotLayout.xaxis, title: 'Research Productivity (Proxy)' }},
                yaxis: {{ ...darkPlotLayout.yaxis, title: 'Research Impact (Citation Score)' }},
                legend: {{ font: {{ color: '#CFD6DF' }} }}
            }}, {{ responsive: true, displayModeBar: false }});

            // Chart 2: Research Intensity Box Plot (RES: VH, HI, MD, LO)
            const resOrder = ['VH', 'HI', 'MD', 'LO'];
            const resTraces = resOrder.map(r => ({{
                type: 'box',
                name: r,
                y: data.filter(d => d['RES.'] === r && d.KPI_Research_Impact_Score != null).map(d => d.KPI_Research_Impact_Score),
                marker: {{ color: '#FF9F1C' }},
                boxmean: true
            }}));

            Plotly.newPlot('chart-d2-box', resTraces, {{
                ...darkPlotLayout,
                xaxis: {{ ...darkPlotLayout.xaxis, title: 'Research Intensity Classification' }},
                yaxis: {{ ...darkPlotLayout.yaxis, title: 'Research Impact Score' }},
                showlegend: false
            }}, {{ responsive: true, displayModeBar: false }});

            // Chart 3: Top 10 Research Institutions (Grouped Bars)
            const top10Research = [...data].filter(d => d.KPI_Research_Impact_Score != null)
                                          .sort((a, b) => b.KPI_Research_Impact_Score - a.KPI_Research_Impact_Score)
                                          .slice(0, 10);

            const traceImpactBar = {{
                type: 'bar',
                name: 'Citation Impact Score',
                x: top10Research.map(d => d.Institution_Name.length > 20 ? d.Institution_Name.substring(0, 18) + '...' : d.Institution_Name),
                y: top10Research.map(d => d.KPI_Research_Impact_Score),
                marker: {{ color: '#FF9F1C' }}
            }};

            const traceProdBar = {{
                type: 'bar',
                name: 'Research Productivity Proxy',
                x: top10Research.map(d => d.Institution_Name.length > 20 ? d.Institution_Name.substring(0, 18) + '...' : d.Institution_Name),
                y: top10Research.map(d => d.KPI_Research_Productivity_Proxy || 0),
                marker: {{ color: '#48CAE4' }}
            }};

            Plotly.newPlot('chart-d2-top10', [traceImpactBar, traceProdBar], {{
                ...darkPlotLayout,
                barmode: 'group',
                yaxis: {{ ...darkPlotLayout.yaxis, title: 'Score (0 - 100)' }},
                legend: {{ font: {{ color: '#CFD6DF' }} }}
            }}, {{ responsive: true, displayModeBar: false }});
        }}

        // ==========================================
        // RENDER DASHBOARD 3: STUDENT ANALYTICS
        // ==========================================
        function renderDashboard3(data) {{
            // KPI 1: Avg Students per Staff
            const staffRatios = data.map(d => d.KPI_Faculty_to_Student_Ratio).filter(s => s != null && !isNaN(s));
            const avgStaff = avg(staffRatios);
            document.getElementById('d3_students_staff').textContent = avgStaff != null ? `${{avgStaff.toFixed(1)}} students/staff` : 'N/A';

            // KPI 2: Avg International Student %
            const intlPcts = data.map(d => d.KPI_International_Student_Pct).filter(s => s != null && !isNaN(s));
            const avgIntl = avg(intlPcts);
            document.getElementById('d3_intl_pct').textContent = avgIntl != null ? `${{avgIntl.toFixed(1)}}%` : 'N/A';

            // KPI 3: Total FTE Student Headcount (Summed directly from dataset)
            const fteStudents = data.map(d => d.THE_No_of_FTE_Students).filter(s => s != null && !isNaN(s));
            const totalFte = sum(fteStudents);
            document.getElementById('d3_fte_total').textContent = (totalFte / 1e6).toFixed(2) + 'M';

            // Chart 1: Average Students per Staff by Region
            const regionRatioSums = {{}};
            const regionRatioCounts = {{}};
            data.forEach(d => {{
                if (d.KPI_Faculty_to_Student_Ratio != null && d.Region) {{
                    regionRatioSums[d.Region] = (regionRatioSums[d.Region] || 0) + d.KPI_Faculty_to_Student_Ratio;
                    regionRatioCounts[d.Region] = (regionRatioCounts[d.Region] || 0) + 1;
                }}
            }});

            const regRatioAvg = Object.keys(regionRatioSums).map(r => ({{
                region: r,
                val: regionRatioSums[r] / regionRatioCounts[r]
            }})).sort((a, b) => a.val - b.val);

            const traceRegionRatio = {{
                type: 'bar',
                orientation: 'h',
                x: regRatioAvg.map(d => d.val),
                y: regRatioAvg.map(d => d.region),
                text: regRatioAvg.map(d => d.val.toFixed(1)),
                textposition: 'auto',
                marker: {{ color: '#2EC4B6' }}
            }};

            Plotly.newPlot('chart-d3-region-ratio', [traceRegionRatio], {{
                ...darkPlotLayout,
                margin: {{ l: 120, r: 40, t: 10, b: 40 }},
                xaxis: {{ ...darkPlotLayout.xaxis, title: 'Average Students per Staff' }}
            }}, {{ responsive: true, displayModeBar: false }});

            // Chart 2: Internationalization Scatter
            const validStudentScatter = data.filter(d => d.KPI_Faculty_to_Student_Ratio != null && d.KPI_International_Student_Pct != null);
            const studentRegGroups = {{}};
            validStudentScatter.forEach(d => {{
                const r = d.Region || 'Other';
                if (!studentRegGroups[r]) studentRegGroups[r] = [];
                studentRegGroups[r].push(d);
            }});

            const studentScatterTraces = Object.entries(studentRegGroups).map(([reg, items]) => ({{
                type: 'scatter',
                mode: 'markers',
                name: reg,
                x: items.map(d => d.KPI_Faculty_to_Student_Ratio),
                y: items.map(d => d.KPI_International_Student_Pct),
                hovertext: items.map(d => `<b>${{d.Institution_Name}}</b><br>Location: ${{d.Location}}<br>Students/Staff: ${{d.KPI_Faculty_to_Student_Ratio}}<br>Int'l Students: ${{d.KPI_International_Student_Pct}}%`),
                hoverinfo: 'text',
                marker: {{ size: 8, opacity: 0.8 }}
            }}));

            Plotly.newPlot('chart-d3-scatter', studentScatterTraces, {{
                ...darkPlotLayout,
                xaxis: {{ ...darkPlotLayout.xaxis, title: 'Students per Staff' }},
                yaxis: {{ ...darkPlotLayout.yaxis, title: 'International Student %' }},
                legend: {{ font: {{ color: '#CFD6DF' }} }}
            }}, {{ responsive: true, displayModeBar: false }});

            // Chart 3: Top 10 Universities by Enrollment Headcount
            const top10Enroll = [...data].filter(d => d.THE_No_of_FTE_Students != null)
                                        .sort((a, b) => b.THE_No_of_FTE_Students - a.THE_No_of_FTE_Students)
                                        .slice(0, 10)
                                        .reverse();

            const traceEnroll = {{
                type: 'bar',
                orientation: 'h',
                x: top10Enroll.map(d => d.THE_No_of_FTE_Students),
                y: top10Enroll.map(d => d.Institution_Name.length > 25 ? d.Institution_Name.substring(0, 23) + '...' : d.Institution_Name),
                text: top10Enroll.map(d => (d.THE_No_of_FTE_Students / 1000).toFixed(1) + 'k'),
                textposition: 'auto',
                marker: {{ color: '#2EC4B6' }},
                hovertext: top10Enroll.map(d => `${{d.Institution_Name}}<br>FTE Students: ${{d.THE_No_of_FTE_Students.toLocaleString()}}<br>Location: ${{d.Location}}`),
                hoverinfo: 'text'
            }};

            Plotly.newPlot('chart-d3-enrollment', [traceEnroll], {{
                ...darkPlotLayout,
                margin: {{ l: 200, r: 50, t: 10, b: 40 }},
                xaxis: {{ ...darkPlotLayout.xaxis, title: 'Number of FTE Students' }}
            }}, {{ responsive: true, displayModeBar: false }});
        }}

        // ==========================================
        // RENDER DASHBOARD 4: COUNTRY COMPARISON
        // ==========================================
        function renderDashboard4(data) {{
            // Compute Country Aggregates
            const countryMap = {{}};
            data.forEach(d => {{
                const c = d.Location;
                if (!c) return;
                if (!countryMap[c]) {{
                    countryMap[c] = {{
                        country: c,
                        plotlyCountry: d.Plotly_Country,
                        count: 0,
                        globalScores: [],
                        acadRep: [],
                        impact: []
                    }};
                }}
                countryMap[c].count += 1;
                if (d.KPI_Global_Ranking_Score != null) countryMap[c].globalScores.push(d.KPI_Global_Ranking_Score);
                if (d.KPI_Academic_Reputation_Score != null) countryMap[c].acadRep.push(d.KPI_Academic_Reputation_Score);
                if (d.KPI_Research_Impact_Score != null) countryMap[c].impact.push(d.KPI_Research_Impact_Score);
            }});

            const countryList = Object.values(countryMap).map(c => ({{
                country: c.country,
                plotlyCountry: c.plotlyCountry,
                count: c.count,
                avgGlobal: avg(c.globalScores),
                avgAcad: avg(c.acadRep),
                avgImpact: avg(c.impact)
            }}));

            // KPI 1: Top Country by Avg Global Score
            const scoredCountries = countryList.filter(c => c.avgGlobal != null).sort((a, b) => b.avgGlobal - a.avgGlobal);
            if (scoredCountries.length) {{
                document.getElementById('d4_top_country').textContent = scoredCountries[0].country;
                document.getElementById('d4_top_country_sub').textContent = `Avg Score: ${{scoredCountries[0].avgGlobal.toFixed(2)}} (Scored subset)`;
            }}

            // KPI 2: Total Ranked Countries
            document.getElementById('d4_total_countries').textContent = countryList.length;

            // KPI 3: Most Represented Country
            const mostRep = [...countryList].sort((a, b) => b.count - a.count)[0];
            if (mostRep) {{
                document.getElementById('d4_most_rep').textContent = `${{mostRep.country}} (${{mostRep.count}})`;
            }}

            // Populate Table
            renderCountryTable(countryList);

            // Populate Map with interactive highlighting
            renderCountryMap(countryList);
        }}

        function renderCountryTable(list) {{
            const tbody = document.getElementById('countryTableBody');
            const searchVal = document.getElementById('tableSearch').value.toLowerCase();
            tbody.innerHTML = '';

            const filtered = list.filter(c => c.country.toLowerCase().includes(searchVal))
                                 .sort((a, b) => b.count - a.count);

            filtered.forEach(c => {{
                const tr = document.createElement('tr');
                if (selectedCountryAction === c.country) {{
                    tr.classList.add('selected-country');
                }}
                tr.innerHTML = `
                    <td><strong>${{c.country}}</strong></td>
                    <td>${{c.count}}</td>
                    <td>${{c.avgGlobal != null ? c.avgGlobal.toFixed(1) : '-'}}</td>
                    <td>${{c.avgAcad != null ? c.avgAcad.toFixed(1) : '-'}}</td>
                    <td>${{c.avgImpact != null ? c.avgImpact.toFixed(1) : '-'}}</td>
                `;

                // Interactive Action: Clicking table row filters map
                tr.onclick = () => {{
                    if (selectedCountryAction === c.country) {{
                        selectedCountryAction = null;
                    }} else {{
                        selectedCountryAction = c.country;
                    }}
                    renderCountryTable(list);
                    renderCountryMap(list);
                }};
                tbody.appendChild(tr);
            }});
        }}

        function renderCountryMap(list) {{
            const desc = document.getElementById('mapHeaderDesc');
            if (selectedCountryAction) {{
                desc.innerHTML = `Filtered highlight: <b style="color: var(--accent-overview);">${{selectedCountryAction}}</b>`;
            }} else {{
                desc.textContent = 'World map showing university footprint by nation';
            }}

            const trace = {{
                type: 'choropleth',
                locationmode: 'country names',
                locations: list.map(c => c.plotlyCountry),
                z: list.map(c => {{
                    if (selectedCountryAction) {{
                        return c.country === selectedCountryAction ? 100 : 1;
                    }}
                    return c.count;
                }}),
                colorscale: selectedCountryAction ? [
                    [0, '#1B2026'],
                    [0.05, '#28323D'],
                    [0.9, '#00A89D'],
                    [1, '#00D2C4']
                ] : [
                    [0, '#162832'],
                    [0.1, '#005B60'],
                    [0.4, '#008E85'],
                    [0.7, '#00B4A7'],
                    [1, '#00D2C4']
                ],
                hovertext: list.map(c => `<b>${{c.country}}</b><br>Universities: ${{c.count}}<br>Avg Global Score: ${{c.avgGlobal != null ? c.avgGlobal.toFixed(1) : 'N/A'}}`),
                hoverinfo: 'text',
                showscale: !selectedCountryAction
            }};

            Plotly.newPlot('chart-d4-map', [trace], {{
                ...darkPlotLayout,
                geo: {{
                    bgcolor: '#12161A',
                    lakecolor: '#12161A',
                    landcolor: '#1B2026',
                    showland: true,
                    showocean: true,
                    oceancolor: '#12161A',
                    showcountries: true,
                    countrycolor: '#28323D',
                    projection: {{ type: 'natural earth' }}
                }},
                margin: {{ l: 0, r: 0, t: 0, b: 0 }}
            }}, {{ responsive: true, displayModeBar: false }});
        }}

        // Setup Events & Listeners
        window.addEventListener('DOMContentLoaded', () => {{
            initFilters();
            renderAll();

            // Filter Change Handlers
            document.getElementById('filterRegion').addEventListener('change', () => {{
                updateLocationDropdown();
                renderAll();
            }});
            document.getElementById('filterLocation').addEventListener('change', renderAll);
            document.getElementById('filterSize').addEventListener('change', renderAll);
            document.getElementById('filterFocus').addEventListener('change', renderAll);

            // Reset Filters
            document.getElementById('btnResetFilters').addEventListener('click', () => {{
                document.getElementById('filterRegion').value = 'ALL';
                updateLocationDropdown();
                document.getElementById('filterLocation').value = 'ALL';
                document.getElementById('filterSize').value = 'ALL';
                document.getElementById('filterFocus').value = 'ALL';
                selectedCountryAction = null;
                renderAll();
            }});

            // Tab Navigation
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

                    btn.classList.add('active');
                    const tabId = btn.getAttribute('data-tab');
                    document.getElementById(`panel-${{tabId}}`).classList.add('active');

                    // Trigger resize for Plotly charts in newly visible tab
                    window.dispatchEvent(new Event('resize'));
                }});
            }});

            // Table Search Handler
            document.getElementById('tableSearch').addEventListener('input', () => {{
                renderDashboard4(getFilteredData());
            }});

            // Clear Country Map Action
            document.getElementById('btnClearCountryAction').addEventListener('click', () => {{
                selectedCountryAction = null;
                renderDashboard4(getFilteredData());
            }});
        }});
    </script>
</body>
</html>
"""
    # Output to two convenient locations:
    out_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'EduVision_Dashboard.html'),
        os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'index.html'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'EduVision_Dashboard.html')
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully generated dashboard at: {os.path.abspath(p)}")

if __name__ == '__main__':
    build_dashboard()
