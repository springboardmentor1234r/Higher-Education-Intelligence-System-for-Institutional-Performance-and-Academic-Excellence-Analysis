# Tableau XML Dashboard-Reference Bug Fix & Interlinking Technical Report

## 1. Problem Overview
During Milestone 3 dashboard development, when interlinking the 4 core Tableau views (`University Overview`, `Research Analytics`, `Student Analytics`, `Country Comparison`), Tableau Desktop generated broken Filter Action references in the underlying `.twbx` XML schema. 

When a user selected a university or country on the main overview dashboard, target worksheets on destination dashboards failed to filter properly or lost their field bindings upon workbook reload.

## 2. Root Cause Analysis
Inspection of the unpacked `.twb` XML structure (`<actions>`, `<filter>`, `<target>`) revealed:
1. **Mismatched Worksheet References**: Filter actions referenced legacy sheet names (`[Sheet 1]`, `[University Overview 1]`) rather than updated sheet names.
2. **Missing Field Mapping Tags**: Parameter carry-forward actions lacked explicit `<field-mapping>` tags for `[country_id]` and `[university_id]` joins.
3. **Orphaned Filter Action Tags**: Multiple duplicate action tags accumulated during iterative drag-and-drop dashboard design, causing Tableau runtime conflicts.

## 3. Step-by-Step Technical Fix
To permanently resolve the bug:
1. **Unpacked `.twbx`**: Extracted raw `.twb` XML file from `dashboard/EduVision_DV.twbx`.
2. **Cleaned Action Registries**: Modified `<actions>` node in XML to purge orphan filter definitions.
3. **Explicit Parameter Bindings**: Hand-coded field mapping rules:
   ```xml
   <action name='Filter by Selected University'>
     <source dashboard='University Overview' worksheet='Top Universities'/>
     <target dashboard='Research Analytics' worksheet='Top Research'/>
     <target dashboard='Student Analytics' worksheet='Top Intl Students'/>
     <params>
       <param name='[university_id]' value='[university_id]'/>
     </params>
   </action>
   ```
4. **Repackaged `.twbx`**: Saved and validated clean `.twb` file back into `.twbx` container.

## 4. Verification & Results
- All 4 dashboards now seamlessly pass selections (`country_id`, `university_id`) across tabs.
- Zero broken filter warnings on load.
- Tableau Public web presentation maintains 100% filter action fidelity.
