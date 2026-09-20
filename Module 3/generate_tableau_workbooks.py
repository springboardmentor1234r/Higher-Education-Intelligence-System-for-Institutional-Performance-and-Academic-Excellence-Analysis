"""
EduVision_DV - Tableau Workbook Generator
Generates valid Tableau XML workbooks (.twb) and packages them into .twbx files:
1. eduvision_prototype.twbx (Module 4 Prototype)
2. eduvision_dashboard_v1.twbx (Module 5: Dashboards 1 & 2)
3. EduVision_DV.twbx (Module 6: Final Integrated Suite with 4 Interlinked Dashboards)
"""

import os
import zipfile
import shutil
import xml.etree.ElementTree as ET

def generate_twb_content(mode="full"):
    """
    mode: 'prototype', 'v1', 'full'
    """
    is_proto = (mode == "prototype")
    is_v1 = (mode == "v1")
    is_full = (mode == "full")

    # Define dashboards according to mode
    dashboards = []
    if is_proto:
        dashboards = ["University Overview (Wireframe)", "Research Analytics (Wireframe)"]
    elif is_v1:
        dashboards = ["University Overview", "Research Analytics"]
    else:
        dashboards = ["University Overview", "Research Analytics", "Student Analytics", "Country Comparison"]

    xml_lines = [
        "<?xml version='1.0' encoding='utf-8' ?>",
        "<workbook source-build='2024.1.0' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>",
        "  <document-format-change-manifest>",
        "    <AccessibleZoneTabOrder />",
        "    <AnimationOnByDefault />",
        "    <MarkAnimation />",
        "    <ObjectModelEncapsulateLegacy />",
        "    <ObjectModelTableType />",
        "    <SchemaViewerProjectCurrent />",
        "    <SheetIdentifierTracking />",
        "    <WindowsPersistSimpleIdentifiers />",
        "  </document-format-change-manifest>",
        "  <preferences>",
        "    <preference name='ui.encoding.shelf.height' value='24' />",
        "    <preference name='ui.shelf.height' value='26' />",
        "  </preferences>",
        "  <datasources>",
        "    <datasource caption='KPI_Master (university_final_dataset)' inline='true' name='federated.eduvision_kpi' version='18.1'>",
        "      <connection class='federated'>",
        "        <named-connections>",
        "          <named-connection caption='university_final_dataset' name='excel-direct.dataset'>",
        "            <connection class='excel-direct' cleaning='no' compat='no' dataRefreshTime='' filename='Data/university_final_dataset.xlsx' interpretationMode='0' password='' server='' validate='no' />",
        "          </named-connection>",
        "        </named-connections>",
        "        <relation connection='excel-direct.dataset' name='KPI_Master' table='[KPI_Master$]' type='table'>",
        "          <columns gridOrigin='A1:P1504:no:A1:P1504:0' header='yes' outcome='2'>",
        "            <column datatype='string' name='university_id' ordinal='0' />",
        "            <column datatype='string' name='university_name' ordinal='1' />",
        "            <column datatype='string' name='country_id' ordinal='2' />",
        "            <column datatype='string' name='country_name' ordinal='3' />",
        "            <column datatype='string' name='region' ordinal='4' />",
        "            <column datatype='integer' name='global_rank' ordinal='5' />",
        "            <column datatype='real' name='kpi_global_ranking_score' ordinal='6' />",
        "            <column datatype='real' name='kpi_research_impact_score' ordinal='7' />",
        "            <column datatype='real' name='kpi_faculty_student_ratio' ordinal='8' />",
        "            <column datatype='real' name='kpi_international_student_pct' ordinal='9' />",
        "            <column datatype='real' name='kpi_academic_reputation_score' ordinal='10' />",
        "            <column datatype='real' name='kpi_research_productivity_index' ordinal='11' />",
        "            <column datatype='real' name='total_students' ordinal='12' />",
        "            <column datatype='real' name='international_students_count' ordinal='13' />",
        "            <column datatype='real' name='international_students_score' ordinal='14' />",
        "            <column datatype='string' name='female_male_ratio' ordinal='15' />",
        "          </columns>",
        "        </relation>",
        "      </connection>",
        "      <aliases enabled='yes' />",
        "      <column datatype='string' name='[country_name]' role='dimension' semantic-role='[Country].[Name]' type='nominal' />",
        "      <column datatype='string' name='[university_name]' role='dimension' type='nominal' />",
        "      <column datatype='string' name='[university_id]' role='dimension' type='nominal' />",
        "      <column datatype='string' name='[country_id]' role='dimension' type='nominal' />",
        "      <column datatype='string' name='[region]' role='dimension' type='nominal' />",
        "      <column datatype='integer' name='[global_rank]' role='measure' type='quantitative' />",
        "      <column datatype='real' name='[kpi_global_ranking_score]' role='measure' type='quantitative' />",
        "      <column datatype='real' name='[kpi_research_impact_score]' role='measure' type='quantitative' />",
        "      <column datatype='real' name='[kpi_faculty_student_ratio]' role='measure' type='quantitative' />",
        "      <column datatype='real' name='[kpi_international_student_pct]' role='measure' type='quantitative' />",
        "      <column datatype='real' name='[kpi_academic_reputation_score]' role='measure' type='quantitative' />",
        "      <column datatype='real' name='[kpi_research_productivity_index]' role='measure' type='quantitative' />",
        "    </datasource>",
        "  </datasources>",
        "  <worksheets>"
    ]

    # Helper function to generate a worksheet
    def make_worksheet(sheet_name, title, mark_type, rows, cols, color_field=None):
        return [
            f"    <worksheet name='{sheet_name}'>",
            "      <table>",
            "        <view>",
            "          <datasources>",
            "            <datasource caption='KPI_Master (university_final_dataset)' name='federated.eduvision_kpi' />",
            "          </datasources>",
            "          <datasource-dependencies datasource='federated.eduvision_kpi'>",
            "            <column datatype='string' name='[university_id]' role='dimension' type='nominal' />",
            "            <column datatype='string' name='[university_name]' role='dimension' type='nominal' />",
            "            <column datatype='string' name='[country_name]' role='dimension' semantic-role='[Country].[Name]' type='nominal' />",
            "            <column datatype='string' name='[region]' role='dimension' type='nominal' />",
            "            <column datatype='integer' name='[global_rank]' role='measure' type='quantitative' />",
            "            <column datatype='real' name='[kpi_global_ranking_score]' role='measure' type='quantitative' />",
            "            <column datatype='real' name='[kpi_research_impact_score]' role='measure' type='quantitative' />",
            "            <column datatype='real' name='[kpi_faculty_student_ratio]' role='measure' type='quantitative' />",
            "            <column datatype='real' name='[kpi_international_student_pct]' role='measure' type='quantitative' />",
            "            <column datatype='real' name='[kpi_academic_reputation_score]' role='measure' type='quantitative' />",
            "            <column datatype='real' name='[kpi_research_productivity_index]' role='measure' type='quantitative' />",
            "          </datasource-dependencies>",
            "          <aggregation value='true' />",
            "        </view>",
            "        <style />",
            "        <panes>",
            "          <pane id='1' selection-relaxation-option='selection-relaxation-allow'>",
            "            <view>",
            "              <breakdown value='auto' />",
            "            </view>",
            f"            <mark class='{mark_type}' />",
            (f"            <encodings><color column='[federated.eduvision_kpi].[{color_field}]' /></encodings>" if color_field else "            <encodings />"),
            "          </pane>",
            "        </panes>",
            f"        <rows>{rows}</rows>",
            f"        <cols>{cols}</cols>",
            "      </table>",
            "      <simple-id uuid='{" + sheet_name + "}' />",
            "    </worksheet>"
        ]

    # Generate worksheets
    # Sheet 1: Top 10 Universities
    xml_lines.extend(make_worksheet("Top_10_Universities", "Top 10 Global Universities", "Bar", "[federated.eduvision_kpi].[none:university_name:nk]", "[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]", "region"))
    # Sheet 2: Global Distribution Map
    xml_lines.extend(make_worksheet("Global_University_Map", "Global University Distribution", "Multipolygon", "[federated.eduvision_kpi].[none:country_name:nk]", "[federated.eduvision_kpi].[sum:global_rank:qk]", "region"))
    # Sheet 3: Academic vs Overall Scatter
    xml_lines.extend(make_worksheet("Academic_vs_Overall", "Academic Reputation vs Overall Score", "Circle", "[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]", "[federated.eduvision_kpi].[avg:kpi_academic_reputation_score:qk]", "region"))
    # Sheet 4: KPI Summary Cards
    xml_lines.extend(make_worksheet("KPI_Summary_Cards", "Executive KPI Cards", "Text", "[federated.eduvision_kpi].[none:university_id:nk]", "[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]"))
    # Sheet 5: Institutional Comparison Table
    xml_lines.extend(make_worksheet("Institutional_Comparison_Table", "Institutional Comparison", "Text", "[federated.eduvision_kpi].[none:university_name:nk]", "[federated.eduvision_kpi].[none:region:nk]"))

    if not is_proto:
        # Sheet 6: Research Productivity Ranking
        xml_lines.extend(make_worksheet("Research_Productivity_Rank", "Top Research Productivity Institutions", "Bar", "[federated.eduvision_kpi].[none:university_name:nk]", "[federated.eduvision_kpi].[avg:kpi_research_productivity_index:qk]", "region"))
        # Sheet 7: Citations vs Research Score
        xml_lines.extend(make_worksheet("Citations_vs_Research", "Research Score vs Citation Performance", "Circle", "[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]", "[federated.eduvision_kpi].[avg:kpi_research_productivity_index:qk]", "region"))
        # Sheet 8: International Research Collaboration
        xml_lines.extend(make_worksheet("Research_Collaboration_Overview", "International Research Impact", "Bar", "[federated.eduvision_kpi].[none:region:nk]", "[federated.eduvision_kpi].[avg:kpi_research_impact_score:qk]", "region"))

    if is_full:
        # Sheet 9: Student Analytics - International Student %
        xml_lines.extend(make_worksheet("Intl_Student_Distribution", "International Student Percentage Distribution", "Bar", "[federated.eduvision_kpi].[none:university_name:nk]", "[federated.eduvision_kpi].[avg:kpi_international_student_pct:qk]", "region"))
        # Sheet 10: Faculty-to-Student Ratio Benchmark
        xml_lines.extend(make_worksheet("Faculty_Student_Benchmark", "Students Per Staff Benchmark", "Bar", "[federated.eduvision_kpi].[none:university_name:nk]", "[federated.eduvision_kpi].[avg:kpi_faculty_student_ratio:qk]", "region"))
        # Sheet 11: Regional Student Diversity
        xml_lines.extend(make_worksheet("Regional_Student_Diversity", "Regional Student Mobility", "Pie", "[federated.eduvision_kpi].[none:region:nk]", "[federated.eduvision_kpi].[avg:kpi_international_student_pct:qk]", "region"))
        # Sheet 12: Country Comparison - University Capacity
        xml_lines.extend(make_worksheet("Country_University_Capacity", "Ranked Universities by Nation", "Bar", "[federated.eduvision_kpi].[none:country_name:nk]", "[federated.eduvision_kpi].[count:university_id:qk]", "region"))
        # Sheet 13: Country Performance Benchmarking
        xml_lines.extend(make_worksheet("Country_Avg_Performance", "Average National University Score", "Bar", "[federated.eduvision_kpi].[none:country_name:nk]", "[federated.eduvision_kpi].[avg:kpi_global_ranking_score:qk]", "region"))

    xml_lines.append("  </worksheets>")

    # Helper function for dashboard construction
    xml_lines.append("  <dashboards>")
    
    # Dashboard 1: University Overview
    xml_lines.extend([
        "    <dashboard name='University Overview'>",
        "      <style />",
        "      <size maxheight='900' maxwidth='1440' minheight='900' minwidth='1440' preset-index='0' type='fixed' />",
        "      <zones>",
        "        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>",
        "          <zone h='6000' id='2' type-v2='title' w='100000' x='0' y='0' />",
        "          <zone h='94000' id='3' type-v2='layout-flow' w='100000' x='0' y='6000'>",
        "            <zone h='94000' id='4' name='KPI_Summary_Cards' w='100000' x='0' y='6000' />",
        "            <zone h='45000' id='5' name='Top_10_Universities' w='50000' x='0' y='20000' />",
        "            <zone h='45000' id='6' name='Academic_vs_Overall' w='50000' x='50000' y='20000' />",
        "            <zone h='35000' id='7' name='Global_University_Map' w='50000' x='0' y='65000' />",
        "            <zone h='35000' id='8' name='Institutional_Comparison_Table' w='50000' x='50000' y='65000' />",
        "          </zone>",
        "        </zone>",
        "      </zones>",
        "    </dashboard>"
    ])

    # Dashboard 2: Research Analytics
    if not is_proto:
        xml_lines.extend([
            "    <dashboard name='Research Analytics'>",
            "      <style />",
            "      <size maxheight='900' maxwidth='1440' minheight='900' minwidth='1440' preset-index='0' type='fixed' />",
            "      <zones>",
            "        <zone h='100000' id='11' type-v2='layout-basic' w='100000' x='0' y='0'>",
            "          <zone h='6000' id='12' type-v2='title' w='100000' x='0' y='0' />",
            "          <zone h='94000' id='13' type-v2='layout-flow' w='100000' x='0' y='6000'>",
            "            <zone h='45000' id='14' name='Research_Productivity_Rank' w='50000' x='0' y='6000' />",
            "            <zone h='45000' id='15' name='Citations_vs_Research' w='50000' x='50000' y='6000' />",
            "            <zone h='49000' id='16' name='Research_Collaboration_Overview' w='100000' x='0' y='51000' />",
            "          </zone>",
            "        </zone>",
            "      </zones>",
            "    </dashboard>"
        ])

    # Dashboard 3 & 4 (Full mode)
    if is_full:
        xml_lines.extend([
            "    <dashboard name='Student Analytics'>",
            "      <style />",
            "      <size maxheight='900' maxwidth='1440' minheight='900' minwidth='1440' preset-index='0' type='fixed' />",
            "      <zones>",
            "        <zone h='100000' id='21' type-v2='layout-basic' w='100000' x='0' y='0'>",
            "          <zone h='6000' id='22' type-v2='title' w='100000' x='0' y='0' />",
            "          <zone h='94000' id='23' type-v2='layout-flow' w='100000' x='0' y='6000'>",
            "            <zone h='45000' id='24' name='Intl_Student_Distribution' w='50000' x='0' y='6000' />",
            "            <zone h='45000' id='25' name='Faculty_Student_Benchmark' w='50000' x='50000' y='6000' />",
            "            <zone h='49000' id='26' name='Regional_Student_Diversity' w='100000' x='0' y='51000' />",
            "          </zone>",
            "        </zone>",
            "      </zones>",
            "    </dashboard>",
            "    <dashboard name='Country Comparison'>",
            "      <style />",
            "      <size maxheight='900' maxwidth='1440' minheight='900' minwidth='1440' preset-index='0' type='fixed' />",
            "      <zones>",
            "        <zone h='100000' id='31' type-v2='layout-basic' w='100000' x='0' y='0'>",
            "          <zone h='6000' id='32' type-v2='title' w='100000' x='0' y='0' />",
            "          <zone h='94000' id='33' type-v2='layout-flow' w='100000' x='0' y='6000'>",
            "            <zone h='47000' id='34' name='Country_University_Capacity' w='100000' x='0' y='6000' />",
            "            <zone h='47000' id='35' name='Country_Avg_Performance' w='100000' x='0' y='53000' />",
            "          </zone>",
            "        </zone>",
            "      </zones>",
            "    </dashboard>"
        ])

    xml_lines.append("  </dashboards>")

    # Dashboard Actions (Interlinking)
    if is_full:
        xml_lines.extend([
            "  <actions>",
            "    <action caption='Filter Research by University' name='Action_Filter_Research'>",
            "      <activation type='on-select' />",
            "      <source dashboard='University Overview' type='sheet' worksheet='Top_10_Universities' />",
            "      <command format-link='target-sheet' target='Research Analytics'>",
            "        <link-field field='[federated.eduvision_kpi].[university_id]' />",
            "      </command>",
            "    </action>",
            "    <action caption='Filter Student by University' name='Action_Filter_Student'>",
            "      <activation type='on-select' />",
            "      <source dashboard='University Overview' type='sheet' worksheet='Top_10_Universities' />",
            "      <command format-link='target-sheet' target='Student Analytics'>",
            "        <link-field field='[federated.eduvision_kpi].[university_id]' />",
            "      </command>",
            "    </action>",
            "    <action caption='Filter Country Comparison' name='Action_Filter_Country'>",
            "      <activation type='on-select' />",
            "      <source dashboard='University Overview' type='sheet' worksheet='Global_University_Map' />",
            "      <command format-link='target-sheet' target='Country Comparison'>",
            "        <link-field field='[federated.eduvision_kpi].[country_name]' />",
            "      </command>",
            "    </action>",
            "  </actions>"
        ])

    # Windows & Tab controls
    xml_lines.extend([
        "  <windows>",
        "    <window class='dashboard' maximized='true' name='University Overview'>",
        "      <viewpoints />",
        "      <active id='-1' />",
        "    </window>",
        "  </windows>",
        "</workbook>"
    ])

    return "\n".join(xml_lines)

def build_twbx(twb_content, data_filepaths, output_twbx_path):
    temp_dir = output_twbx_path + "_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    data_dir = os.path.join(temp_dir, "Data")
    os.makedirs(data_dir, exist_ok=True)

    # Save twb
    base_name = os.path.splitext(os.path.basename(output_twbx_path))[0]
    twb_path = os.path.join(temp_dir, base_name + ".twb")
    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(twb_content)

    # Copy data files
    for src in data_filepaths:
        shutil.copy2(src, os.path.join(data_dir, os.path.basename(src)))

    # Create zip as .twbx
    os.makedirs(os.path.dirname(output_twbx_path), exist_ok=True)
    if os.path.exists(output_twbx_path):
        os.remove(output_twbx_path)

    with zipfile.ZipFile(output_twbx_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                zipf.write(full_path, rel_path)

    shutil.rmtree(temp_dir)
    print(f"[SUCCESS] Packaged Tableau Workbook (.twbx) created: {output_twbx_path}")

def main():
    print("================================================================================")
    print("   EduVision_DV - Building Tableau Deliverables (.twbx)")
    print("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_files = [
        os.path.join(base_dir, "04_kpi_dataset", "university_final_dataset.xlsx"),
        os.path.join(base_dir, "04_kpi_dataset", "kpi_master.csv")
    ]

    # 1. Module 4: eduvision_prototype.twbx
    proto_twb = generate_twb_content("prototype")
    proto_twbx = os.path.join(base_dir, "dashboard", "eduvision_prototype.twbx")
    build_twbx(proto_twb, data_files, proto_twbx)

    # 2. Module 5: eduvision_dashboard_v1.twbx
    v1_twb = generate_twb_content("v1")
    v1_twbx = os.path.join(base_dir, "dashboard", "eduvision_dashboard_v1.twbx")
    build_twbx(v1_twb, data_files, v1_twbx)

    # 3. Module 6: EduVision_DV.twbx (Final Integrated Deliverable)
    full_twb = generate_twb_content("full")
    full_twbx1 = os.path.join(base_dir, "dashboard", "EduVision_DV.twbx")
    full_twbx2 = os.path.join(base_dir, "EduVision_DV.twbx")
    build_twbx(full_twb, data_files, full_twbx1)
    shutil.copy2(full_twbx1, full_twbx2)
    print(f"[SUCCESS] Final integrated workbook mirrored to root: {full_twbx2}")

if __name__ == "__main__":
    main()
