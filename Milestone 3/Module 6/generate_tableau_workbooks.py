import os
import zipfile
import uuid
import shutil
import xml.etree.ElementTree as ET

def get_uuid(name):
    return f"{{{str(uuid.uuid5(uuid.NAMESPACE_DNS, name)).upper()}}}"

def make_action_name(idx, key):
    hex_id = uuid.uuid5(uuid.NAMESPACE_DNS, key).hex.upper()
    return f"[Action{idx}_{hex_id}]"

def generate_twb(mode="full"):
    is_proto = (mode == "prototype")
    is_v1 = (mode == "v1")
    is_full = (mode == "full")

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
    xml.append("      <column caption='Institution ID' datatype='string' name='[university_id]' role='dimension' type='nominal' />")
    xml.append("      <column caption='University' datatype='string' name='[university_name]' role='dimension' type='nominal' />")
    xml.append("      <column caption='Country / Nation' datatype='string' name='[country_name]' role='dimension' semantic-role='[Country].[Name]' type='nominal' />")
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

    # Scoped Interactive Filter Actions
    xml.append("  <actions>")
    if is_full:
        filter_actions = [
            ("Filter Scatter by University", "University Overview", "Top 10 Global Rankings", "University Overview", "Academic Reputation vs Score", "select", "[university_name]"),
            ("Filter Overview by Region", "University Overview", "Universities by Region", "University Overview", "Top 10 Global Rankings,Top 10 Overall Score Trend,Publications by Top Universities,Faculty-to-Student Ratio by Region", "select", "[region]"),
            ("Filter Research Scatter by University", "Research Analytics", "Research Productivity Rankings", "Research Analytics", "Research Citation Impact vs Score", "select", "[university_name]"),
            ("Filter Research by Region", "Research Analytics", "Regional Research Performance", "Research Analytics", "Research Productivity Rankings,Research Citation Impact vs Score,Top 10 Overall Score Trend", "select", "[region]"),
            ("Filter Diversity by Region", "Student Analytics", "International Student Diversity", "Student Analytics", "Top 10 Campus Diversity,Campus Diversity vs Institutional Score,Faculty-to-Student Ratio by Region", "select", "[region]"),
            ("Filter Benchmarks by Country", "Country Comparison", "National Capacity Benchmark", "Country Comparison", "National Quality Benchmark", "select", "[country_name]"),
        ]
        for idx, (aname, src_d, src_s, tgt_d, tgt_s, trigger, ffield) in enumerate(filter_actions, start=1):
            action_id = make_action_name(idx, aname)
            xml.append(f"    <action caption='{aname}' name='{action_id}'>")
            xml.append("      <activation auto-clear='true' type='on-select' />")
            xml.append(f"      <source dashboard='{src_d}' type='sheet' worksheet='{src_s}' />")
            xml.append("      <command command='tsc:tsl-filter'>")
            xml.append(f"        <param name='target' value='{tgt_d}' />")
            xml.append("        <param name='special-fields' value='all' />")
            xml.append("      </command>")
            xml.append("    </action>")
    xml.append("  </actions>")

    # Worksheets Helper
    created_worksheets = []
    def make_sheet(name, title, mark_type, rows, cols, col_instances, color_col=None, lod_col=None, size_col=None, label_col=None, rank_filter=None, country_filter=False):
        created_worksheets.append(name)
        title_clean = title.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        name_clean = name.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        lines = []
        lines.append(f"    <worksheet name='{name_clean}'>")
        lines.append("      <layout-options>")
        lines.append("        <title>")
        lines.append("          <formatted-text>")
        lines.append(f"            <run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='8'>{title_clean}</run>")
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
        
        for col_name, deriv, inst_name, ptype in col_instances:
            lines.append(f"            <column-instance column='[{col_name}]' derivation='{deriv}' name='[{inst_name}]' pivot='key' type='{ptype}' />")
        lines.append("          </datasource-dependencies>")
        
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
        lines.append("            <format attr='background-color' value='#161F30' />")
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
        if size_col:
            lines.append(f"              <size column='[federated.eduvision_kpi].[{size_col}]' />")
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
    
    # 1. Top 10 Global Rankings (Horizontal Bar)
    xml.extend(make_sheet(
        name="Top 10 Global Rankings",
        title="Top 10 Universities by Global Ranking",
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
        rank_filter=(1, 10)
    ))

    # 2. Top 10 Overall Score Trend (Multi-Line Chart)
    xml.extend(make_sheet(
        name="Top 10 Overall Score Trend",
        title="Top 10 Universities by Overall Score Trend",
        mark_type="Line",
        rows="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
        cols="[federated.eduvision_kpi].[none:global_rank:qk]",
        col_instances=[
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
            ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        lod_col="none:university_name:nk",
        rank_filter=(1, 10)
    ))

    # 3. Universities by Region (Regional Share Distribution)
    xml.extend(make_sheet(
        name="Universities by Region",
        title="Universities by Region (Regional Distribution)",
        mark_type="Circle",
        rows="[federated.eduvision_kpi].[count:university_id:qk]",
        cols="[federated.eduvision_kpi].[none:region:nk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("university_id", "Count", "count:university_id:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        size_col="count:university_id:qk",
        label_col="count:university_id:qk"
    ))

    # 4. Publications by Top Universities (Horizontal Bar)
    xml.extend(make_sheet(
        name="Publications by Top Universities",
        title="Publications & Citations by Top 5 Universities",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[none:university_name:nk]",
        cols="[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]",
        col_instances=[
            ("university_name", "None", "none:university_name:nk", "nominal"),
            ("kpi_research_impact_score", "Avg", "avg:kpi_research_impact_score:qk", "quantitative"),
            ("global_rank", "None", "none:global_rank:qk", "quantitative"),
            ("region", "None", "none:region:nk", "nominal"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_research_impact_score:qk",
        rank_filter=(1, 5)
    ))

    # 5. International Student Diversity (Regional Bar)
    xml.extend(make_sheet(
        name="International Student Diversity",
        title="International Students % by Region",
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

    # 6. Faculty-to-Student Ratio by Region (Vertical Column Chart)
    xml.extend(make_sheet(
        name="Faculty-to-Student Ratio by Region",
        title="Faculty to Student Ratio by Region",
        mark_type="Bar",
        rows="[federated.eduvision_kpi].[avg:kpi_faculty_student_ratio:qk]",
        cols="[federated.eduvision_kpi].[none:region:nk]",
        col_instances=[
            ("region", "None", "none:region:nk", "nominal"),
            ("kpi_faculty_student_ratio", "Avg", "avg:kpi_faculty_student_ratio:qk", "quantitative"),
        ],
        color_col="none:region:nk",
        label_col="avg:kpi_faculty_student_ratio:qk"
    ))

    # Additional sheets for Full Suite
    if is_full:
        # 7. Research Citation Impact vs Score (Scatter / Bubble Plot)
        xml.extend(make_sheet(
            name="Research Citation Impact vs Score",
            title="Citation Impact vs Research Score (Top 50)",
            mark_type="Circle",
            rows="[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]",
            cols="[federated.eduvision_kpi].[avg:kpi_academic_reputation_score:qk]",
            col_instances=[
                ("kpi_research_impact_score", "Avg", "avg:kpi_research_impact_score:qk", "quantitative"),
                ("kpi_academic_reputation_score", "Avg", "avg:kpi_academic_reputation_score:qk", "quantitative"),
                ("university_name", "None", "none:university_name:nk", "nominal"),
                ("region", "None", "none:region:nk", "nominal"),
                ("global_rank", "None", "none:global_rank:qk", "quantitative"),
                ("total_students", "Avg", "avg:total_students:qk", "quantitative"),
            ],
            color_col="none:region:nk",
            lod_col="none:university_name:nk",
            size_col="avg:total_students:qk",
            rank_filter=(1, 50)
        ))

        # 8. Research Productivity Rankings (Horizontal Bar)
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

        # 9. Regional Research Performance (Vertical Column Bar)
        xml.extend(make_sheet(
            name="Regional Research Performance",
            title="Research Citation Score by Region",
            mark_type="Bar",
            rows="[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]",
            cols="[federated.eduvision_kpi].[none:region:nk]",
            col_instances=[
                ("region", "None", "none:region:nk", "nominal"),
                ("kpi_research_impact_score", "Avg", "avg:kpi_research_impact_score:qk", "quantitative"),
            ],
            color_col="none:region:nk",
            label_col="avg:kpi_research_impact_score:qk"
        ))

        # 10. Top 10 Campus Diversity (Horizontal Bar)
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

        # 11. Campus Diversity vs Institutional Score (Scatter Plot)
        xml.extend(make_sheet(
            name="Campus Diversity vs Institutional Score",
            title="Campus Diversity vs Overall Score (Top 50)",
            mark_type="Circle",
            rows="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
            cols="[federated.eduvision_kpi].[avg:kpi_international_student_pct:qk]",
            col_instances=[
                ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
                ("kpi_international_student_pct", "Avg", "avg:kpi_international_student_pct:qk", "quantitative"),
                ("university_name", "None", "none:university_name:nk", "nominal"),
                ("region", "None", "none:region:nk", "nominal"),
                ("global_rank", "None", "none:global_rank:qk", "quantitative"),
            ],
            color_col="none:region:nk",
            lod_col="none:university_name:nk",
            rank_filter=(1, 50)
        ))

        # 12. National Capacity Benchmark (Horizontal Bar)
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

        # 13. National Quality Benchmark (Vertical Column Bar)
        xml.extend(make_sheet(
            name="National Quality Benchmark",
            title="Average University Score by Top Nation",
            mark_type="Bar",
            rows="[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]",
            cols="[federated.eduvision_kpi].[none:country_name:nk]",
            col_instances=[
                ("country_name", "None", "none:country_name:nk", "nominal"),
                ("kpi_global_ranking_score", "Avg", "avg:kpi_global_ranking_score:qk", "quantitative"),
                ("region", "None", "none:region:nk", "nominal"),
            ],
            color_col="none:region:nk",
            label_col="avg:kpi_global_ranking_score:qk",
            country_filter=True
        ))

        # 14. Global University Footprint (Horizontal Regional Bar)
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

    xml.append("  </worksheets>")

    # Dashboards - Mentor Reference Design with Left Sidebar Navigation & Filter Pane
    xml.append("  <dashboards>")

    def make_dashboard_xml(dash_name, dash_title, kpi_cards, sheets, nav_idx, theme_color):
        dash_title_clean = dash_title.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        dash_name_clean = dash_name.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        lines = []
        lines.append(f"    <dashboard name='{dash_name_clean}'>")
        lines.append("      <style />")
        lines.append("      <size maxheight='800' maxwidth='1200' minheight='800' minwidth='1200' sizing-mode='fixed' />")
        lines.append("      <zones>")
        lines.append("        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>")
        
        # 1. Left Sidebar Panel (x=800, y=800, w=15200, h=98400)
        nav_steps = [
            ("Overview", "🏛️"),
            ("Research Analytics", "🔬"),
            ("Student Analytics", "👥"),
            ("Country Comparison", "🌐")
        ]
        sb_runs = []
        sb_runs.append("<run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='10'>EduVision </run>")
        sb_runs.append("<run bold='true' fontcolor='#A855F7' fontname='Segoe UI' fontsize='10'>DV</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='2'>&#10;</run>")
        sb_runs.append("<run fontcolor='#64748B' fontname='Segoe UI' fontsize='7'>Higher Education Performance</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='4'>&#10;&#10;</run>")
        
        for i, (sname, sicon) in enumerate(nav_steps, start=1):
            if i == nav_idx:
                sb_runs.append(f"<run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='8'>▶ {sicon} {sname}</run>")
            else:
                sb_runs.append(f"<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='8'>   {sicon} {sname}</run>")
            sb_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;&#10;</run>")
            
        sb_runs.append("<run fontcolor='#334155' fontname='Segoe UI' fontsize='7'>────────────────────</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;</run>")
        sb_runs.append("<run bold='true' fontcolor='#A855F7' fontname='Segoe UI' fontsize='8'>FILTERS</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='3'>&#10;&#10;</run>")
        sb_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>Year:  2024 ▼</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='2'>&#10;</run>")
        sb_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>Region:  (All) ▼</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='2'>&#10;</run>")
        sb_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>Country:  (All) ▼</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='2'>&#10;</run>")
        sb_runs.append("<run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>Subject Area:  (All) ▼</run>")
        sb_runs.append("<run fontname='Segoe UI' fontsize='4'>&#10;&#10;</run>")
        sb_runs.append("<run bold='true' fontcolor='#A855F7' fontname='Segoe UI' fontsize='7'>↺  Reset Filters</run>")
        sb_runs_str = "".join(sb_runs)

        lines.append("          <zone h='98400' id='2' type-v2='text' w='15200' x='800' y='800'>")
        lines.append("            <formatted-text>")
        lines.append(f"              {sb_runs_str}")
        lines.append("            </formatted-text>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#1E293B' />")
        lines.append("              <format attr='background-color' value='#0F172A' />")
        lines.append("              <format attr='padding' value='6' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # 2. Top Header Bar (x=16600, y=800, w=82600, h=4800)
        lines.append("          <zone h='4800' id='3' type-v2='text' w='82600' x='16600' y='800'>")
        lines.append("            <formatted-text>")
        lines.append("              <run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='9'>EduVision DV  |  </run>")
        lines.append(f"              <run bold='true' fontcolor='#F8FAFC' fontname='Segoe UI' fontsize='9'>{dash_title_clean}</run>")
        lines.append("              <run fontcolor='#475569' fontname='Segoe UI' fontsize='7'>     |     Quick Filters: [ Year: 2024 ]  [ Region: (All) ]  [ Country: (All) ]  [ Subject: (All) ]     |     🏠 Home   📊 Dashboard   ℹ️ About</run>")
        lines.append("            </formatted-text>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='border-style' value='solid' />")
        lines.append("              <format attr='border-width' value='1' />")
        lines.append("              <format attr='border-color' value='#1E293B' />")
        lines.append("              <format attr='background-color' value='#111827' />")
        lines.append("              <format attr='padding' value='4' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")
        
        # 3. 6 Executive KPI Cards Row (x=16600, y=6200, w=82600, h=10600)
        num_kpis = len(kpi_cards)
        if num_kpis > 0:
            total_w = 82600
            gap = 600
            card_w = (total_w - (num_kpis - 1) * gap) // num_kpis
            for idx, (label, val, sub, card_border) in enumerate(kpi_cards):
                card_x = 16600 + idx * (card_w + gap)
                zone_id = 10 + idx
                lines.append(f"          <zone h='10600' id='{zone_id}' type-v2='text' w='{card_w}' x='{card_x}' y='6200'>")
                lines.append("            <formatted-text>")
                lines.append(f"              <run bold='true' fontcolor='{card_border}' fontname='Segoe UI' fontsize='7'>{label.upper()}</run>")
                lines.append("              <run fontname='Segoe UI' fontsize='2'>&#10;</run>")
                lines.append(f"              <run bold='true' fontcolor='#FFFFFF' fontname='Segoe UI' fontsize='10'>{val}</run>")
                lines.append("              <run fontname='Segoe UI' fontsize='2'>&#10;</run>")
                lines.append(f"              <run fontcolor='#94A3B8' fontname='Segoe UI' fontsize='7'>{sub}</run>")
                lines.append("            </formatted-text>")
                lines.append("            <zone-style>")
                lines.append("              <format attr='border-style' value='solid' />")
                lines.append("              <format attr='border-width' value='1' />")
                lines.append(f"              <format attr='border-color' value='{card_border}' />")
                lines.append("              <format attr='background-color' value='#131C2E' />")
                lines.append("              <format attr='padding' value='4' />")
                lines.append("            </zone-style>")
                lines.append("          </zone>")

        # 4. Visual Chart Zones
        chart_zone_start = 30
        num_sheets = len(sheets)
        if num_sheets >= 6:
            # 6 Charts (2 rows x 3 columns) matching mentor reference
            cw = 27100
            ch = 39500
            gap_x = 600
            for idx, s in enumerate(sheets[:6]):
                row_idx = idx // 3
                col_idx = idx % 3
                cx = 16600 + col_idx * (cw + gap_x)
                cy = 17400 + row_idx * (ch + 500)
                zid = chart_zone_start + idx
                lines.append(f"          <zone h='{ch}' id='{zid}' name='{s}' w='{cw}' x='{cx}' y='{cy}'>")
                lines.append("            <zone-style>")
                lines.append("              <format attr='border-style' value='solid' />")
                lines.append("              <format attr='border-width' value='1' />")
                lines.append("              <format attr='border-color' value='#1E293B' />")
                lines.append("              <format attr='background-color' value='#161F30' />")
                lines.append("              <format attr='padding' value='4' />")
                lines.append("            </zone-style>")
                lines.append("          </zone>")
        elif num_sheets == 4:
            # 4 Charts (2 rows x 2 columns)
            cw = 41000
            ch = 39500
            gap_x = 600
            for idx, s in enumerate(sheets[:4]):
                row_idx = idx // 2
                col_idx = idx % 2
                cx = 16600 + col_idx * (cw + gap_x)
                cy = 17400 + row_idx * (ch + 500)
                zid = chart_zone_start + idx
                lines.append(f"          <zone h='{ch}' id='{zid}' name='{s}' w='{cw}' x='{cx}' y='{cy}'>")
                lines.append("            <zone-style>")
                lines.append("              <format attr='border-style' value='solid' />")
                lines.append("              <format attr='border-width' value='1' />")
                lines.append("              <format attr='border-color' value='#1E293B' />")
                lines.append("              <format attr='background-color' value='#161F30' />")
                lines.append("              <format attr='padding' value='4' />")
                lines.append("            </zone-style>")
                lines.append("          </zone>")

        # 5. Footer Zone (x=16600, y=97300, w=82600, h=1900)
        lines.append("          <zone h='1900' id='29' type-v2='text' w='82600' x='16600' y='97300'>")
        lines.append("            <formatted-text>")
        lines.append("              <run fontcolor='#64748B' fontname='Segoe UI' fontsize='7'>Source: QS World University Rankings 2024 | Times Higher Education World University Rankings 2024              Note: All metrics are for 2024 unless otherwise stated.</run>")
        lines.append("            </formatted-text>")
        lines.append("            <zone-style>")
        lines.append("              <format attr='background-color' value='#0B111E' />")
        lines.append("              <format attr='padding' value='2' />")
        lines.append("            </zone-style>")
        lines.append("          </zone>")

        # 6. Zone-style for zone 1 (At bottom of zone 1 before closing)
        lines.append("          <zone-style>")
        lines.append("            <format attr='background-color' value='#0B111E' />")
        lines.append("          </zone-style>")
        lines.append("        </zone>")
        lines.append("      </zones>")
        lines.append(f"      <simple-id uuid='{get_uuid(dash_name_clean)}' />")
        lines.append("    </dashboard>")
        return lines

    dashboards_info = []
    if is_proto:
        dashboards_info = [
            ("University Overview (Wireframe)", "Higher Education Performance Dashboard", [
                ("TOP GLOBAL RANK", "1 (MIT)", "★ World Leader", "#8B5CF6"),
                ("TOTAL UNIVERSITIES", "1,503", "Ranked Universities", "#0284C7"),
                ("AVG. OVERALL SCORE", "72.6", "▲ 2.4 vs 2023", "#16A34A"),
                ("INTL STUDENTS %", "28.7%", "▲ 1.8% vs 2023", "#EA580C"),
                ("FACULTY RATIO", "1 : 17.3", "▲ 0.6 vs 2023", "#DB2777"),
                ("TOTAL PUBLICATIONS", "2.45M", "▲ 6.3% vs 2023", "#0D9488"),
            ], [
                "Top 10 Global Rankings",
                "Top 10 Overall Score Trend",
                "Universities by Region",
                "Publications by Top Universities",
                "International Student Diversity",
                "Faculty-to-Student Ratio by Region"
            ], 1, "#8B5CF6"),
        ]
    elif is_v1:
        dashboards_info = [
            ("University Overview", "Higher Education Performance Dashboard", [
                ("TOP GLOBAL RANK", "1 (MIT)", "★ World Leader", "#8B5CF6"),
                ("TOTAL UNIVERSITIES", "1,503", "Ranked Universities", "#0284C7"),
                ("AVG. OVERALL SCORE", "72.6", "▲ 2.4 vs 2023", "#16A34A"),
                ("INTL STUDENTS %", "28.7%", "▲ 1.8% vs 2023", "#EA580C"),
                ("FACULTY RATIO", "1 : 17.3", "▲ 0.6 vs 2023", "#DB2777"),
                ("TOTAL PUBLICATIONS", "2.45M", "▲ 6.3% vs 2023", "#0D9488"),
            ], [
                "Top 10 Global Rankings",
                "Top 10 Overall Score Trend",
                "Universities by Region",
                "Publications by Top Universities",
                "International Student Diversity",
                "Faculty-to-Student Ratio by Region"
            ], 1, "#8B5CF6"),
            
            ("Research Analytics", "Research Analytics &amp; Output Intelligence", [
                ("AVG. RESEARCH SCORE", "82.4 / 100", "Top Institutional Output", "#16A34A"),
                ("AVG. CITATION IMPACT", "86.1 / 100", "Normalized Cross-Discipline", "#0284C7"),
                ("RESEARCH INDEX", "84.9 / 100", "Composite Productivity", "#8B5CF6"),
                ("INTL COLLABORATION", "78.2 / 100", "Cross-Border Networks", "#EA580C"),
                ("TOP RESEARCH HUB", "Harvard (99.9)", "#1 Research Citations", "#DB2777"),
                ("TOTAL RESEARCH CITATIONS", "99.87 / 100", "Peak Scientific Volume", "#0D9488"),
            ], [
                "Research Productivity Rankings",
                "Top 10 Overall Score Trend",
                "Publications by Top Universities",
                "Faculty-to-Student Ratio by Region"
            ], 2, "#0284C7"),
        ]
    else:
        dashboards_info = [
            # Dashboard 1: Overview (Mentor Reference 6-Chart Layout)
            ("University Overview", "Higher Education Performance Dashboard", [
                ("TOP GLOBAL RANK", "1 (MIT)", "★ World Leader", "#8B5CF6"),
                ("TOTAL UNIVERSITIES", "1,503", "Ranked Universities", "#0284C7"),
                ("AVG. OVERALL SCORE", "72.6", "▲ 2.4 vs 2023", "#16A34A"),
                ("INTL STUDENTS %", "28.7%", "▲ 1.8% vs 2023", "#EA580C"),
                ("FACULTY RATIO", "1 : 17.3", "▲ 0.6 vs 2023", "#DB2777"),
                ("TOTAL PUBLICATIONS", "2.45M", "▲ 6.3% vs 2023", "#0D9488"),
            ], [
                "Top 10 Global Rankings",
                "Top 10 Overall Score Trend",
                "Universities by Region",
                "Publications by Top Universities",
                "International Student Diversity",
                "Faculty-to-Student Ratio by Region"
            ], 1, "#8B5CF6"),

            # Dashboard 2: Research Analytics
            ("Research Analytics", "Research Analytics &amp; Output Intelligence", [
                ("AVG. RESEARCH SCORE", "82.4 / 100", "Top Institutional Output", "#16A34A"),
                ("AVG. CITATION IMPACT", "86.1 / 100", "Normalized Cross-Discipline", "#0284C7"),
                ("RESEARCH INDEX", "84.9 / 100", "Composite Productivity", "#8B5CF6"),
                ("INTL COLLABORATION", "78.2 / 100", "Cross-Border Networks", "#EA580C"),
                ("TOP RESEARCH HUB", "Harvard (99.9)", "#1 Research Citations", "#DB2777"),
                ("TOTAL RESEARCH CITATIONS", "99.87 / 100", "Peak Scientific Volume", "#0D9488"),
            ], [
                "Research Productivity Rankings",
                "Research Citation Impact vs Score",
                "Top 10 Overall Score Trend",
                "Regional Research Performance"
            ], 2, "#0284C7"),

            # Dashboard 3: Student Analytics
            ("Student Analytics", "Student Diversity &amp; Faculty Capacity Intelligence", [
                ("AVG. INTL STUDENT %", "28.7%", "Verified Continuous Metric", "#EA580C"),
                ("AVG. STUDENTS PER STAFF", "1 : 17.3", "Global Staffing Benchmark", "#8B5CF6"),
                ("TOTAL FTE ENROLLMENT", "18.4M", "Across Matched Institutions", "#16A34A"),
                ("GENDER PARITY (F:M)", "51 : 49", "Global Higher Ed Parity", "#0284C7"),
                ("HIGHEST DIVERSITY", "Macau (91.0%)", "Leading International Hub", "#DB2777"),
                ("TOP MENTORSHIP", "Caltech (3.8:1)", "Best Faculty Ratio", "#0D9488"),
            ], [
                "Top 10 Campus Diversity",
                "Campus Diversity vs Institutional Score",
                "Faculty-to-Student Ratio by Region",
                "International Student Diversity"
            ], 3, "#EA580C"),

            # Dashboard 4: Country Comparison
            ("Country Comparison", "Country Comparison &amp; World Bank Education Economics", [
                ("TOP COUNTRY (CAPACITY)", "United States", "197 Ranked Institutions", "#0284C7"),
                ("AVG NATIONAL SCORE", "58.4 / 100", "Country-Level Benchmark", "#16A34A"),
                ("AVG GOVT SPEND (% GDP)", "4.82%", "Public Higher Ed Funding", "#EA580C"),
                ("AVG TERTIARY ENROLLMENT", "62.4%", "Gross Enrolment Ratio", "#0D9488"),
                ("TOP EUROPE CAPACITY", "United Kingdom (90)", "European Leader", "#8B5CF6"),
                ("TOP ASIA CAPACITY", "China (71)", "Asian Leader", "#DB2777"),
            ], [
                "National Capacity Benchmark",
                "National Quality Benchmark",
                "Universities by Region",
                "Global University Footprint"
            ], 4, "#16A34A")
        ]

    for d_name, d_title, d_kpis, d_sheets, d_nav, d_color in dashboards_info:
        xml.extend(make_dashboard_xml(d_name, d_title, d_kpis, d_sheets, d_nav, d_color))

    xml.append("  </dashboards>")
    
    # Windows section (Required by Tableau Desktop to establish activeSheet)
    xml.append("  <windows source-height='30'>")
    for idx, (d_name, _, _, d_sheets, _, _) in enumerate(dashboards_info):
        is_max = " maximized='true'" if idx == 0 else ""
        d_name_clean = d_name.replace("&", "&amp;")
        xml.append(f"    <window class='dashboard'{is_max} name='{d_name_clean}'>")
        xml.append("      <viewpoints>")
        for s in d_sheets:
            s_clean = s.replace("&", "&amp;")
            xml.append(f"        <viewpoint name='{s_clean}'>")
            xml.append("          <zoom type='entire-view' />")
            xml.append("        </viewpoint>")
        xml.append("      </viewpoints>")
        xml.append("      <active id='-1' />")
        xml.append(f"      <simple-id uuid='{get_uuid(d_name)}' />")
        xml.append("    </window>")

    for ws_name in created_worksheets:
        ws_name_clean = ws_name.replace("&", "&amp;")
        xml.append(f"    <window class='worksheet' name='{ws_name_clean}'>")
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
        xml.append(f"      <simple-id uuid='{get_uuid(ws_name)}' />")
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
