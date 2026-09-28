import os
import zipfile
import uuid
import shutil
import subprocess
import time

def get_uuid(name):
    return f"{{{str(uuid.uuid5(uuid.NAMESPACE_DNS, name)).upper()}}}"

def generate_twb(mode="full"):
    is_proto = (mode == "prototype")
    is_v1 = (mode == "v1")
    is_full = (mode == "full")

    dashboards_info = [
        # Dashboard 1: University Overview
        ("University Overview", "UNIVERSITY OVERVIEW", [
            ("TOP GLOBAL RANK", "#1 (MIT)", "★ World Leader", "#C084FC"),
            ("TOTAL UNIVERSITIES", "1,503", "106 Sovereign Nations", "#38BDF8"),
            ("AVERAGE SCORE", "72.6 / 100", "+2.4% vs Baseline", "#A855F7"),
            ("INTL STUDENTS %", "28.7%", "Global Student Mobility", "#F59E0B"),
            ("FACULTY RATIO", "1 : 11.2", "Teaching Staff Benchmark", "#34D399"),
            ("RESEARCH IMPACT", "84.3 / 100", "Normalized Citations", "#F43F5E"),
        ], ["Top 10 Global Rankings", "Academic Reputation vs Score", "Global University Footprint", "National Capacity Benchmark"], 1),

        # Dashboard 2: Research Analytics
        ("Research Analytics", "RESEARCH ANALYTICS", [
            ("AVG RESEARCH SCORE", "82.4 / 100", "Scholarly Environment", "#C084FC"),
            ("CITATION VELOCITY", "86.1 / 100", "Cross-Field Citations", "#38BDF8"),
            ("PRODUCTIVITY INDEX", "84.9 / 100", "Composite Derivation", "#A855F7"),
            ("INTL RESEARCH COLLAB", "78.2 / 100", "Cross-Border Networks", "#F59E0B"),
            ("TOP RESEARCH HUB", "Harvard (99.9)", "#1 Research Volume", "#34D399"),
            ("PEAK CITATION LEADER", "99.87 / 100", "Global Impact Leader", "#F43F5E"),
        ], ["Research Productivity Rankings", "Citation Impact vs Research", "Regional Academic Performance", "Regional Research Performance"], 2),

        # Dashboard 3: Student Analytics
        ("Student Analytics", "STUDENT ANALYTICS", [
            ("TOTAL STUDENTS", "18.4M", "Across Matched Institutions", "#C084FC"),
            ("AVG INTL STUDENTS %", "28.7%", "Continuous Metric", "#38BDF8"),
            ("STUDENTS PER STAFF", "1 : 11.2", "Staffing Benchmark", "#A855F7"),
            ("GENDER PARITY (F:M)", "51 : 49", "Global Equality Ratio", "#F59E0B"),
            ("TOP DIVERSITY HUB", "Macau (91.0%)", "Leading Global Hub", "#34D399"),
            ("TOP FACULTY RATIO", "Caltech (3.8:1)", "Best Tutorial Staffing", "#F43F5E"),
        ], ["Top 10 Campus Diversity", "Faculty-to-Student Ratio", "International Student Diversity", "Regional Academic Performance"], 3),

        # Dashboard 4: Country Comparison
        ("Country Comparison", "COUNTRY COMPARISON", [
            ("TOP CAPACITY NATION", "United States (197)", "Ranked Institutions", "#C084FC"),
            ("AVG NATIONAL SCORE", "58.4 / 100", "Country Benchmark", "#38BDF8"),
            ("GOVT SPEND (% GDP)", "4.82%", "Public Tertiary Spend", "#A855F7"),
            ("TERTIARY ENROLLMENT", "62.4%", "Gross Enrolment Ratio", "#F59E0B"),
            ("EUROPE CAPACITY", "United Kingdom (90)", "European Leader", "#34D399"),
            ("ASIA CAPACITY", "China (71)", "Asian Leader", "#F43F5E"),
        ], ["National Capacity Benchmark", "National Quality Benchmark", "Global University Footprint", "Regional Academic Performance"], 4)
    ]

    target_dashboards = []
    if is_proto:
        target_dashboards = dashboards_info[:1]
    elif is_v1:
        target_dashboards = dashboards_info[:2]
    else:
        target_dashboards = dashboards_info

    dash_names = [d[0] for d in target_dashboards]

    xml = []
    xml.append("<?xml version='1.0' encoding='utf-8' ?>")
    xml.append("<workbook source-build='2024.1.0' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>")
    xml.append("  <document-format-change-manifest>")
    xml.append("    <AccessibleZoneTabOrder />")
    xml.append("    <AnimationOnByDefault />")
    xml.append("    <MarkAnimation />")
    xml.append("    <ObjectModelEncapsulateLegacy />")
    xml.append("    <ObjectModelTableType />")
    xml.append("    <SheetIdentifierTracking />")
    xml.append("    <WindowsPersistSimpleIdentifiers />")
    xml.append("  </document-format-change-manifest>")
    xml.append("  <preferences>")
    xml.append("    <preference name='ui.encoding.shelf.height' value='24' />")
    xml.append("    <preference name='ui.shelf.height' value='26' />")
    xml.append("  </preferences>")
    
    # Datasource
    xml.append("  <datasources>")
    xml.append("    <datasource caption='KPI_Master (university_final_dataset)' inline='true' name='federated.eduvision_kpi' version='18.1'>")
    xml.append("      <connection class='federated'>")
    xml.append("        <named-connections>")
    xml.append("          <named-connection caption='university_final_dataset' name='excel-direct.dataset'>")
    xml.append("            <connection class='excel-direct' cleaning='no' compat='no' dataRefreshTime='' filename='Data/university_final_dataset.xlsx' interpretationMode='0' password='' server='' validate='no' />")
    xml.append("          </named-connection>")
    xml.append("        </named-connections>")
    xml.append("        <relation connection='excel-direct.dataset' name='KPI_Master' table='[KPI_Master$]' type='table'>")
    xml.append("          <columns gridOrigin='A1:P1504:no:A1:P1504:0' header='yes' outcome='2'>")
    xml.append("            <column datatype='string' name='university_id' ordinal='0' />")
    xml.append("            <column datatype='string' name='university_name' ordinal='1' />")
    xml.append("            <column datatype='string' name='country_id' ordinal='2' />")
    xml.append("            <column datatype='string' name='country_name' ordinal='3' />")
    xml.append("            <column datatype='string' name='region' ordinal='4' />")
    xml.append("            <column datatype='integer' name='global_rank' ordinal='5' />")
    xml.append("            <column datatype='real' name='kpi_global_ranking_score' ordinal='6' />")
    xml.append("            <column datatype='real' name='kpi_research_impact_score' ordinal='7' />")
    xml.append("            <column datatype='real' name='kpi_faculty_student_ratio' ordinal='8' />")
    xml.append("            <column datatype='real' name='kpi_international_student_pct' ordinal='9' />")
    xml.append("            <column datatype='real' name='kpi_academic_reputation_score' ordinal='10' />")
    xml.append("            <column datatype='real' name='kpi_research_productivity_index' ordinal='11' />")
    xml.append("            <column datatype='real' name='total_students' ordinal='12' />")
    xml.append("            <column datatype='real' name='international_students_count' ordinal='13' />")
    xml.append("            <column datatype='real' name='international_students_score' ordinal='14' />")
    xml.append("            <column datatype='string' name='female_male_ratio' ordinal='15' />")
    xml.append("          </columns>")
    xml.append("        </relation>")
    xml.append("      </connection>")
    xml.append("      <aliases enabled='yes' />")
    xml.append("      <column caption='Country / Nation' datatype='string' name='[country_name]' role='dimension' semantic-role='[Country].[Name]' type='nominal' />")
    xml.append("      <column caption='University' datatype='string' name='[university_name]' role='dimension' type='nominal' />")
    xml.append("      <column caption='Institution ID' datatype='string' name='[university_id]' role='dimension' type='nominal' />")
    xml.append("      <column caption='Country Code' datatype='string' name='[country_id]' role='dimension' type='nominal' />")
    xml.append("      <column caption='Geographic Region' datatype='string' name='[region]' role='dimension' type='nominal' />")
    xml.append("      <column caption='Global Rank' datatype='integer' default-format='n#,##0' name='[global_rank]' role='measure' type='quantitative' />")
    xml.append("      <column caption='Overall Score' datatype='real' default-format='n#,##0.0' name='[kpi_global_ranking_score]' role='measure' type='quantitative' />")
    xml.append("      <column caption='Research Citation Score' datatype='real' default-format='n#,##0.0' name='[kpi_research_impact_score]' role='measure' type='quantitative' />")
    xml.append("      <column caption='Faculty-to-Student Ratio' datatype='real' default-format='n#,##0.0&quot; : 1&quot;' name='[kpi_faculty_student_ratio]' role='measure' type='quantitative' />")
    xml.append("      <column caption='International Students (%)' datatype='real' default-format='n#,##0.0&quot;%&quot;' name='[kpi_international_student_pct]' role='measure' type='quantitative' />")
    xml.append("      <column caption='Academic Reputation Score' datatype='real' default-format='n#,##0.0' name='[kpi_academic_reputation_score]' role='measure' type='quantitative' />")
    xml.append("      <column caption='Research Productivity Index' datatype='real' default-format='n#,##0.0' name='[kpi_research_productivity_index]' role='measure' type='quantitative' />")
    xml.append("      <column caption='Total FTE Students' datatype='real' default-format='n#,##0' name='[total_students]' role='measure' type='quantitative' />")
    xml.append("    </datasource>")
    xml.append("  </datasources>")

    # Interconnected Cross-Dashboard Filter and Highlight Actions Block
    xml.append("  <actions>")
    for s_idx, src_dash in enumerate(dash_names):
        # Intra-dashboard filter action
        act_id_self = f"[Action_Filter_{s_idx}_Self]"
        xml.append(f"    <action caption='Filter {src_dash} Views' name='{act_id_self}'>")
        xml.append("      <activation auto-clear='true' type='on-select' />")
        xml.append(f"      <source dashboard='{src_dash}' type='sheet' />")
        xml.append("      <command command='tsc:tsl-filter'>")
        xml.append("        <param name='special-fields' value='all' />")
        xml.append(f"        <param name='target' value='{src_dash}' />")
        xml.append("      </command>")
        xml.append("    </action>")

        # Interconnected cross-dashboard actions to other dashboards
        for t_idx, tgt_dash in enumerate(dash_names):
            if tgt_dash != src_dash:
                act_id_cross = f"[Action_Cross_{s_idx}_{t_idx}]"
                xml.append(f"    <action caption='Cross-Filter: {src_dash} to {tgt_dash}' name='{act_id_cross}'>")
                xml.append("      <activation auto-clear='true' type='on-select' />")
                xml.append(f"      <source dashboard='{src_dash}' type='sheet' />")
                xml.append("      <command command='tsc:tsl-filter'>")
                xml.append("        <param name='special-fields' value='all' />")
                xml.append(f"        <param name='target' value='{tgt_dash}' />")
                xml.append("      </command>")
                xml.append("    </action>")

    # Geographic Region Highlight Action
    xml.append("    <action caption='Highlight Geographic Region Across Dashboards' name='[Action_Highlight_Region]'>")
    xml.append("      <activation auto-clear='true' type='on-hover' />")
    xml.append(f"      <source dashboard='{dash_names[0]}' type='sheet' />")
    xml.append("      <command command='tsc:brush'>")
    xml.append("        <param name='field-captions' value='Geographic Region' />")
    xml.append(f"        <param name='target' value='{','.join(dash_names)}' />")
    xml.append("      </command>")
    xml.append("    </action>")

    xml.append("    <datasources>")
    xml.append("      <datasource caption='KPI_Master (university_final_dataset)' name='federated.eduvision_kpi' />")
    xml.append("    </datasources>")
    xml.append("    <datasource-dependencies datasource='federated.eduvision_kpi'>")
    xml.append("      <column datatype='string' name='[country_name]' role='dimension' semantic-role='[Country].[Name]' type='nominal' />")
    xml.append("      <column datatype='string' name='[region]' role='dimension' type='nominal' />")
    xml.append("      <column datatype='string' name='[university_name]' role='dimension' type='nominal' />")
    xml.append("    </datasource-dependencies>")
    xml.append("  </actions>")

    # Helper for worksheets - tracks created sheets
    created_sheet_names = []

    def make_sheet(name, title, mark_type, rows, cols, col_instances, color_col=None, lod_col=None, label_col=None, rank_filter=None, country_filter=False):
        created_sheet_names.append(name)
        lines = []
        lines.append(f"    <worksheet name='{name}'>")
        lines.append("      <layout-options>")
        lines.append("        <title>")
        lines.append("          <formatted-text>")
        lines.append(f"            <run bold='true' fontcolor='#E2E8F0' fontname='Segoe UI' fontsize='9'>{title}</run>")
        lines.append("          </formatted-text>")
        lines.append("        </title>")
        lines.append("      </layout-options>")
        lines.append("      <table>")
        lines.append("        <view>")
        lines.append("          <datasources>")
        lines.append("            <datasource caption='KPI_Master (university_final_dataset)' name='federated.eduvision_kpi' />")
        lines.append("          </datasources>")
        lines.append("          <datasource-dependencies datasource='federated.eduvision_kpi'>")
        lines.append("            <column caption='Institution ID' datatype='string' name='[university_id]' role='dimension' type='nominal' />")
        lines.append("            <column caption='University' datatype='string' name='[university_name]' role='dimension' type='nominal' />")
        lines.append("            <column caption='Country / Nation' datatype='string' name='[country_name]' role='dimension' semantic-role='[Country].[Name]' type='nominal' />")
        lines.append("            <column caption='Geographic Region' datatype='string' name='[region]' role='dimension' type='nominal' />")
        lines.append("            <column caption='Global Rank' datatype='integer' default-format='n#,##0' name='[global_rank]' role='measure' type='quantitative' />")
        lines.append("            <column caption='Overall Score' datatype='real' default-format='n#,##0.0' name='[kpi_global_ranking_score]' role='measure' type='quantitative' />")
        lines.append("            <column caption='Research Citation Score' datatype='real' default-format='n#,##0.0' name='[kpi_research_impact_score]' role='measure' type='quantitative' />")
        lines.append("            <column caption='Faculty-to-Student Ratio' datatype='real' default-format='n#,##0.0&quot; : 1&quot;' name='[kpi_faculty_student_ratio]' role='measure' type='quantitative' />")
        lines.append("            <column caption='International Students (%)' datatype='real' default-format='n#,##0.0&quot;%&quot;' name='[kpi_international_student_pct]' role='measure' type='quantitative' />")
        lines.append("            <column caption='Academic Reputation Score' datatype='real' default-format='n#,##0.0' name='[kpi_academic_reputation_score]' role='measure' type='quantitative' />")
        lines.append("            <column caption='Research Productivity Index' datatype='real' default-format='n#,##0.0' name='[kpi_research_productivity_index]' role='measure' type='quantitative' />")
        lines.append("            <column caption='Total FTE Students' datatype='real' default-format='n#,##0' name='[total_students]' role='measure' type='quantitative' />")
        
        # Ensure column instances has none:region:nk so filtering by region works on all sheets
        instances_set = {inst[2] for inst in col_instances}
        all_instances = list(col_instances)
        if "none:region:nk" not in instances_set:
            all_instances.append(("region", "None", "none:region:nk", "nominal"))

        for col_name, deriv, inst_name, ptype in all_instances:
            lines.append(f"            <column-instance column='[{col_name}]' derivation='{deriv}' name='[{inst_name}]' pivot='key' type='{ptype}' />")
        lines.append("          </datasource-dependencies>")
        
        # Shared categorical region filter across all sheets
        lines.append("          <filter class='categorical' column='[federated.eduvision_kpi].[none:region:nk]' filter-group='2'>")
        lines.append("            <groupfilter function='level-members' level='[none:region:nk]' user:ui-enumeration='all' user:ui-marker='enumerate' />")
        lines.append("          </filter>")

        if rank_filter:
            r_min, r_max = rank_filter
            lines.append("          <filter class='quantitative' column='[federated.eduvision_kpi].[none:global_rank:qk]' included-values='in-range'>")
            lines.append(f"            <min>{r_min}</min>")
            lines.append(f"            <max>{r_max}</max>")
            lines.append("          </filter>")

        if country_filter:
            lines.append("          <filter class='categorical' column='[federated.eduvision_kpi].[none:country_name:nk]'>")
            lines.append("            <groupfilter function='union' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate'>")
            top_countries = [
                "United States", "United Kingdom", "China", "Germany",
                "Japan", "Australia", "Canada", "Italy"
            ]
            for c in top_countries:
                lines.append(f"              <groupfilter function='member' level='[none:country_name:nk]' member='&quot;{c}&quot;' />")
            lines.append("            </groupfilter>")
            lines.append("          </filter>")

        lines.append("          <aggregation value='true' />")
        lines.append("        </view>")
        lines.append("        <style>")
        lines.append("          <style-rule element='table'>")
        lines.append("            <format attr='background-color' value='#150F2E' />")
        lines.append("          </style-rule>")
        lines.append("          <style-rule element='gridline'>")
        lines.append("            <format attr='line-visibility' value='off' />")
        lines.append("          </style-rule>")
        lines.append("          <style-rule element='zeroline'>")
        lines.append("            <format attr='line-visibility' value='off' />")
        lines.append("          </style-rule>")
        lines.append("          <style-rule element='header'>")
        lines.append("            <format attr='color' value='#F8FAFC' />")
        lines.append("            <format attr='font-family' value='Segoe UI' />")
        lines.append("          </style-rule>")
        lines.append("          <style-rule element='axis'>")
        lines.append("            <format attr='color' value='#94A3B8' />")
        lines.append("            <format attr='font-family' value='Segoe UI' />")
        lines.append("          </style-rule>")
        lines.append("          <style-rule element='label'>")
        lines.append("            <format attr='color' value='#FFFFFF' />")
        lines.append("            <format attr='font-family' value='Segoe UI' />")
        lines.append("          </style-rule>")
        lines.append("        </style>")
        lines.append("        <panes>")
        lines.append("          <pane selection-relaxation-option='selection-relaxation-allow'>")
        lines.append("            <view>")
        lines.append("              <breakdown value='auto' />")
        lines.append("            </view>")
        lines.append(f"            <mark class='{mark_type}' />")
        lines.append("            <encodings>")
        if color_col:
            lines.append(f"              <color column='[federated.eduvision_kpi].[{color_col}]' />")
        if lod_col:
            lines.append(f"              <lod column='[federated.eduvision_kpi].[{lod_col}]' />")
        if label_col:
            lines.append(f"              <text column='[federated.eduvision_kpi].[{label_col}]' />")
        lines.append("            </encodings>")
        if label_col:
            lines.append("            <style>")
            lines.append("              <style-rule element='mark'>")
            lines.append("                <format attr='mark-labels-show' value='true' />")
            lines.append("                <format attr='mark-labels-cull' value='true' />")
            lines.append("              </style-rule>")
            lines.append("            </style>")
        lines.append("          </pane>")
        lines.append("        </panes>")
        lines.append(f"        <rows>{rows}</rows>")
        lines.append(f"        <cols>{cols}</cols>")
        lines.append("      </table>")
        lines.append(f"      <simple-id uuid='{get_uuid(name)}' />")
        lines.append("    </worksheet>")
        return lines

    xml.append("  <worksheets>")
    
    # 1. Top 10 Global Rankings (Top 8 universities horizontal bars)
    xml.extend(make_sheet(
        name="Top 10 Global Rankings",
        title="Top Global Universities by Overall Score",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:university_name:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
        col_instances=[
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_global_ranking_score:qk",
        rank_filter=(1, 8)
    ))

    # 2. Global University Footprint (5 continental regions horizontal bars)
    xml.extend(make_sheet(
        name="Global University Footprint",
        title="Global University Distribution by Region",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:region:nk]",
        cols="[federated.eduvision_kpi].[count:university_id:qk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("university_id", "Count", "count:university_id:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        label_col="count:university_id:qk"
    ))

    # 3. Academic Reputation vs Score (Top 50 Scatter Plot)
    xml.extend(make_sheet(
        name="Academic Reputation vs Score",
        title="Academic Reputation vs Research Citations (Top 50)",
        mark_type="Circle",
        rows="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
        cols="[federated.eduvision_kpi].[avg:kpi_academic_reputation_score:qk]",
        col_instances=[
            ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
            ("kpi_academic_reputation_score", "Avg", "avg:kpi_academic_reputation_score:qk", "quantitative"),
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("region", "None", "none:region:nk", "nominal"),
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        lod_col="none:university_name:nk",
        rank_filter=(1, 50)
    ))

    # 4. Research Productivity Rankings (Top 8 research hubs)
    xml.extend(make_sheet(
        name="Research Productivity Rankings",
        title="Top Research Institutions by Productivity Index",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:university_name:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_research_productivity_index:qk]",
        col_instances=[
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("kpi_research_productivity_index", "Avg", "avg:kpi_research_productivity_index:qk", "quantitative"),
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_research_productivity_index:qk",
        rank_filter=(1, 8)
    ))

    # 5. Citation Impact vs Research (Top 50 Scatter Plot)
    xml.extend(make_sheet(
        name="Citation Impact vs Research",
        title="Research Citation Impact vs Productivity (Top 50)",
        mark_type="Circle",
        rows="[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]",
        cols="[federated.eduvision_kpi].[avg:kpi_research_productivity_index:qk]",
        col_instances=[
            ("kpi_research_impact_score", "Avg", "avg:kpi_research_impact_score:qk", "quantitative"),
            ("kpi_research_productivity_index", "Avg", "avg:kpi_research_productivity_index:qk", "quantitative"),
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("region", "None", "none:region:nk", "nominal"),
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        lod_col="none:university_name:nk",
        rank_filter=(1, 50)
    ))

    # 6. International Student Diversity (5 regions horizontal bars)
    xml.extend(make_sheet(
        name="International Student Diversity",
        title="International Student Percentage by Region",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:region:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_international_student_pct:qk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("kpi_international_student_pct", "Avg", "avg:kpi_international_student_pct:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_international_student_pct:qk"
    ))

    # 7. Faculty-to-Student Ratio (5 regions horizontal bars)
    xml.extend(make_sheet(
        name="Faculty-to-Student Ratio",
        title="Students Per Faculty Benchmark by Region",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:region:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_faculty_student_ratio:qk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("kpi_faculty_student_ratio", "Avg", "avg:kpi_faculty_student_ratio:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_faculty_student_ratio:qk"
    ))

    # 8. National Capacity Benchmark (Top 8 nations)
    xml.extend(make_sheet(
        name="National Capacity Benchmark",
        title="Top Nations by Number of Ranked Universities",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:country_name:nk]",
        cols="[federated.eduvision_kpi].[count:university_id:qk]",
        col_instances=[
            ("country_name", "None", "none:country_name:nk", "nominal"),
            ("university_id", "Count", "count:university_id:qk", "quantitative"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        label_col="count:university_id:qk",
        country_filter=True
    ))

    # 9. Regional Academic Performance (5 regions horizontal bars)
    xml.extend(make_sheet(
        name="Regional Academic Performance",
        title="Average Institutional Score by Region",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:region:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_global_ranking_score:qk"
    ))

    # 10. Regional Research Performance (5 regions horizontal bars)
    xml.extend(make_sheet(
        name="Regional Research Performance",
        title="Research Citation Score by Region",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:region:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("kpi_research_impact_score", "Avg", "avg:kpi_research_impact_score:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_research_impact_score:qk"
    ))

    # 11. Top 10 Campus Diversity (Top 8 diversity leaders)
    xml.extend(make_sheet(
        name="Top 10 Campus Diversity",
        title="Top Institutions by International Student Percentage",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:university_name:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_international_student_pct:qk]",
        col_instances=[
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("kpi_international_student_pct", "Avg", "avg:kpi_international_student_pct:qk", "quantitative"),
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_international_student_pct:qk",
        rank_filter=(1, 8)
    ))

    # 12. National Quality Benchmark (Top 8 nations)
    xml.extend(make_sheet(
        name="National Quality Benchmark",
        title="Average University Score by Top Nation",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:country_name:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
        col_instances=[
            ("country_name", "None", "none:country_name:nk", "nominal"),
            ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_global_ranking_score:qk",
        country_filter=True
    ))

    xml.append("  </worksheets>")

    # Dashboards - Inspired by Sample (Sidebar + Top Bar + 6 KPIs + Visual Quadrants)
    xml.append("  <dashboards>")

    def make_dashboard_xml(dash_name, dash_title_upper, kpi_cards, sheets, nav_idx):
        lines = []
        lines.append(f"    <dashboard name='{dash_name}'>")
        lines.append("      <style />")
        lines.append("      <size maxheight='800' maxwidth='1200' minheight='800' minwidth='1200' sizing-mode='fixed' />")
        lines.append("      <zones>")
        lines.append("        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>")
        
        # =========================================================================
        # 1. LEFT SIDEBAR (x=800, y=800, w=14200, h=98400)
        # =========================================================================
        nav_items = [
            ("University Overview", "🏛️"),
            ("Research Analytics", "🔬"),
            ("Student Analytics", "👥"),
            ("Country Comparison", "🌐")
        ]
        
        sidebar_runs = []
        sidebar_runs.append("<run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='10'>EduVision DV</run>")
        sidebar_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;</run>")
        sidebar_runs.append("<run fontcolor='#A855F7' fontname='Segoe UI' fontsize='7'>Higher Education Performance</run>")
        sidebar_runs.append("<run fontname='Segoe UI' fontsize='5'>&#10;&#10;</run>")
        
        for idx, (sname, sicon) in enumerate(nav_items, start=1):
            if idx == nav_idx:
                sidebar_runs.append(f"<run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='8'> {sicon}  {sname}</run>")
            else:
                sidebar_runs.append(f"<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='8'> {sicon}  {sname}</run>")
            sidebar_runs.append("<run fontname='Segoe UI' fontsize='4'>&#10;&#10;</run>")
            
        sidebar_runs.append("<run fontcolor='#2D1C59' fontname='Segoe UI' fontsize='6'>───────────────────</run>")
        sidebar_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;</run>")
        sidebar_runs.append("<run bold='true' fontcolor='#C084FC' fontname='Segoe UI' fontsize='8'>REGION FILTER:</run>")
        sidebar_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;</run>")
        sidebar_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>Select Geographic Region:</run>")

        sidebar_str = "".join(sidebar_runs)

        # Upper Sidebar Text Box (Brand + Nav + Filter Title)
        lines.append("          <zone h='46000' id='2' type-v2='text' w='14200' x='800' y='800'>")
        lines.append("            <formatted-text>")
        lines.append(f"              {sidebar_str}")
        lines.append("            </formatted-text>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#120B24' />")
        lines.append("              <format attr='padding' value='8' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # Interactive Filter Control (Live Dropdown with Checkboxes)
        first_sheet = sheets[0]
        lines.append(f"          <zone h='6500' id='25' mode='checkdropdown' name='{first_sheet}' param='[federated.eduvision_kpi].[none:region:nk]' type-v2='filter' w='13000' x='1400' y='47200'>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#120B24' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # Lower Sidebar Text Box (Cross-Filter Guide + Reset Instructions)
        lower_runs = []
        lower_runs.append("<run bold='true' fontcolor='#C084FC' fontname='Segoe UI' fontsize='8'>INTERACTIONS:</run>")
        lower_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;</run>")
        lower_runs.append("<run fontcolor='#38BDF8' fontname='Segoe UI' fontsize='7'>• Live Cross-Filtering:</run>")
        lower_runs.append("<run fontname='Segoe UI' fontsize='2'>&#10;</run>")
        lower_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='6'>Click any bar or data point in any chart to filter all 4 dashboards.</run>")
        lower_runs.append("<run fontname='Segoe UI' fontsize='4'>&#10;&#10;</run>")
        lower_runs.append("<run fontcolor='#38BDF8' fontname='Segoe UI' fontsize='7'>• Auto-Clear / Reset:</run>")
        lower_runs.append("<run fontname='Segoe UI' fontsize='2'>&#10;</run>")
        lower_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='6'>Click mark again or select '(All)' in region dropdown to reset.</run>")
        lower_str = "".join(lower_runs)

        lines.append("          <zone h='44500' id='26' type-v2='text' w='14200' x='800' y='54700'>")
        lines.append("            <formatted-text>")
        lines.append(f"              {lower_str}")
        lines.append("            </formatted-text>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#120B24' />")
        lines.append("              <format attr='padding' value='8' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # =========================================================================
        # 2. TOP HEADER BANNER (x=15600, y=800, w=83600, h=5200)
        # =========================================================================
        lines.append("          <zone h='5200' id='3' type-v2='text' w='83600' x='15600' y='800'>")
        lines.append("            <formatted-text>")
        lines.append(f"              <run bold='true' fontcolor='#E879F9' fontname='Georgia' fontsize='11'>           {dash_title_upper}           </run>")
        lines.append("              <run fontcolor='#475569' fontname='Segoe UI' fontsize='8'>                  |   </run>")
        lines.append("              <run fontcolor='#38BDF8' fontname='Segoe UI' fontsize='7'>🏠 Home   </run>")
        lines.append("              <run fontcolor='#C084FC' fontname='Segoe UI' fontsize='7'>📊 Dashboard   </run>")
        lines.append("              <run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>ℹ️ Info</run>")
        lines.append("            </formatted-text>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#130D28' />")
        lines.append("              <format attr='padding' value='4' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # =========================================================================
        # 3. 6 KPI CARDS ROW (x=15600, y=6600, w=83600, h=10600)
        # =========================================================================
        num_kpis = len(kpi_cards)
        total_w = 83600
        gap = 500
        card_w = (total_w - (num_kpis - 1) * gap) // num_kpis
        for idx, (label, val, sub, card_accent) in enumerate(kpi_cards):
            card_x = 15600 + idx * (card_w + gap)
            zone_id = 10 + idx
            lines.append(f"          <zone h='10600' id='{zone_id}' type-v2='text' w='{card_w}' x='{card_x}' y='6600'>")
            lines.append("            <formatted-text>")
            lines.append(f"              <run bold='true' fontcolor='{card_accent}' fontname='Segoe UI' fontsize='7'>{label.upper()}</run>")
            lines.append("              <run fontname='Segoe UI' fontsize='2'>&#10;</run>")
            lines.append(f"              <run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='10'>{val}</run>")
            lines.append("              <run fontname='Segoe UI' fontsize='2'>&#10;</run>")
            lines.append(f"              <run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>{sub}</run>")
            lines.append("            </formatted-text>")
            lines.append("            <zone-style>")
            lines.append("              <format attr='border-style' value='solid' />")
            lines.append("              <format attr='border-width' value='1' />")
            lines.append("              <format attr='border-color' value='#2D1C59' />")
            lines.append("              <format attr='background-color' value='#170F33' />")
            lines.append("              <format attr='padding' value='3' />")
            lines.append("            </zone-style>")
            lines.append("          </zone>")

        # =========================================================================
        # 4. ROW 1 VISUAL ZONES (y=17800, h=39800)
        # =========================================================================
        chart_w = 41300
        c_gap = 1000
        x_col1 = 15600
        x_col2 = x_col1 + chart_w + c_gap
        
        s1, s2, s3, s4 = sheets[:4]
        
        # Chart 1: Top-Left
        lines.append(f"          <zone h='39800' id='30' name='{s1}' w='{chart_w}' x='{x_col1}' y='17800'>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#150F2E' />")
        lines.append("              <format attr='padding' value='4' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # Chart 2: Top-Right
        lines.append(f"          <zone h='39800' id='31' name='{s2}' w='{chart_w}' x='{x_col2}' y='17800'>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#150F2E' />")
        lines.append("              <format attr='padding' value='4' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # =========================================================================
        # 5. ROW 2 VISUAL ZONES (y=58200, h=41000)
        # =========================================================================
        # Chart 3: Bottom-Left
        lines.append(f"          <zone h='41000' id='32' name='{s3}' w='{chart_w}' x='{x_col1}' y='58200'>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#150F2E' />")
        lines.append("              <format attr='padding' value='4' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # Chart 4: Bottom-Right
        lines.append(f"          <zone h='41000' id='33' name='{s4}' w='{chart_w}' x='{x_col2}' y='58200'>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#2D1C59' />")
        lines.append("              <format attr='background-color' value='#150F2E' />")
        lines.append("              <format attr='padding' value='4' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        lines.append("          <zone-style>")
        lines.append("            <format attr='background-color' value='#0A0717' />")
        lines.append("          </zone-style>")
        lines.append("        </zone>")
        lines.append("      </zones>")
        lines.append(f"      <simple-id uuid='{get_uuid(dash_name)}' />")
        lines.append("    </dashboard>")
        return lines

    for d_name, d_title, d_kpis, d_sheets, d_nav in target_dashboards:
        xml.extend(make_dashboard_xml(d_name, d_title, d_kpis, d_sheets, d_nav))

    xml.append("  </dashboards>")
    xml.append("  <windows>")
    
    # 1. Dashboard windows with explicit viewpoints for their constituent sheets
    for idx, (d_name, d_title, d_kpis, d_sheets, d_nav) in enumerate(target_dashboards):
        max_attr = " maximized='true'" if idx == 0 else ""
        d_win_uuid = get_uuid(d_name + "_win")
        xml.append(f"    <window class='dashboard'{max_attr} name='{d_name}'>")
        xml.append("      <viewpoints>")
        for s in d_sheets:
            xml.append(f"        <viewpoint name='{s}'>")
            xml.append("          <zoom type='entire-view' />")
            xml.append("        </viewpoint>")
        xml.append("      </viewpoints>")
        xml.append("      <active id='-1' />")
        xml.append(f"      <simple-id uuid='{d_win_uuid}' />")
        xml.append("    </window>")

    # 2. Worksheet windows (hidden from tabs so only the dashboards appear in tab bar)
    for s_name in created_sheet_names:
        s_win_uuid = get_uuid(s_name + "_win")
        xml.append(f"    <window class='worksheet' hidden='true' name='{s_name}'>")
        xml.append("      <cards>")
        xml.append("        <edge name='left'>")
        xml.append("          <strip size='160'>")
        xml.append("            <card type='pages' />")
        xml.append("            <card type='filters' />")
        xml.append("            <card type='marks' />")
        xml.append("          </strip>")
        xml.append("        </edge>")
        xml.append("        <edge name='top'>")
        xml.append("          <strip size='2147483647'>")
        xml.append("            <card type='columns' />")
        xml.append("          </strip>")
        xml.append("          <strip size='2147483647'>")
        xml.append("            <card type='rows' />")
        xml.append("          </strip>")
        xml.append("          <strip size='31'>")
        xml.append("            <card type='title' />")
        xml.append("          </strip>")
        xml.append("        </edge>")
        xml.append("      </cards>")
        xml.append(f"      <simple-id uuid='{s_win_uuid}' />")
        xml.append("    </window>")

    xml.append("  </windows>")
    xml.append("</workbook>")
    return "\n".join(xml)

def package_twbx(twb_content, data_files, output_path):
    temp_dir = output_path + "_pkg_tmp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(os.path.join(temp_dir, "Data"), exist_ok=True)

    twb_path = os.path.join(temp_dir, "workbook.twb")
    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(twb_content)

    for df in data_files:
        shutil.copy2(df, os.path.join(temp_dir, "Data", os.path.basename(df)))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if os.path.exists(output_path):
        os.remove(output_path)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                p = os.path.join(root, file)
                z.write(p, os.path.relpath(p, temp_dir))

    shutil.rmtree(temp_dir)
    print(f"[OK] Packaged: {output_path}")

def main():
    root_dirs = [
        r"c:\Users\sujay\OneDrive\Desktop\Info_Intern_11",
        r"c:\Users\sujay\OneDrive\Desktop\EduVision_DV"
    ]

    for root_dir in root_dirs:
        print(f"\n==================================================")
        print(f"Deploying workbooks to: {root_dir}")
        print(f"==================================================")

        data_files = [
            os.path.join(root_dir, "Milestone 2", "Module 3", "university_final_dataset.xlsx"),
            os.path.join(root_dir, "Milestone 2", "Module 3", "kpi_master.csv")
        ]

        # 1. Module 4 Prototype
        proto_xml = generate_twb("prototype")
        proto_path = os.path.join(root_dir, "Milestone 2", "Module 4", "eduvision_prototype.twbx")
        package_twbx(proto_xml, data_files, proto_path)

        # 2. Module 5 v1
        v1_xml = generate_twb("v1")
        v1_path = os.path.join(root_dir, "Milestone 3", "Module 5", "eduvision_dashboard_v1.twbx")
        package_twbx(v1_xml, data_files, v1_path)

        # 3. Module 6 Final Integrated Suite
        full_xml = generate_twb("full")
        full_path = os.path.join(root_dir, "Milestone 3", "Module 6", "EduVision_DV.twbx")
        package_twbx(full_xml, data_files, full_path)

        # Mirror deliverables to Milestone 5 and Screenshots
        for src_path, fname in [
            (proto_path, "eduvision_prototype.twbx"),
            (v1_path, "eduvision_dashboard_v1.twbx"),
            (full_path, "EduVision_DV.twbx")
        ]:
            for folder in ["Milestone 5", "Screenshots"]:
                dst = os.path.join(root_dir, folder, fname)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src_path, dst)
                print(f"[MIRRORED] {fname} -> {folder}/")

if __name__ == "__main__":
    main()
