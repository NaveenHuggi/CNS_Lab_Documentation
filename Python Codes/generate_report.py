"""
Script to generate a comprehensive, professionally styled Word document (.docx)
covering CNS Lab 5 and CNS Lab 6 with actual results, tables, code, and embedded graphs.
Analysis questions are omitted as requested.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOC_PATH = r"d:\CNS_LAB\CNS_Lab5_Lab6_Implementation_Report.docx"
LAB5_DIR = r"d:\CNS_LAB\lab5_graphs"
LAB6_DIR = r"d:\CNS_LAB\lab6_graphs"

# Helper XML styling functions
def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def style_table(table, header_bg="1B365D", alt_bg="F2F5F9"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        is_header = (i == 0)
        bg = header_bg if is_header else (alt_bg if i % 2 == 1 else "FFFFFF")
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    if is_header:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.size = Pt(10)
                    else:
                        run.font.size = Pt(9.5)
                        run.font.color.rgb = RGBColor(40, 40, 40)

def add_heading_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    run = h.runs[0]
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(27, 54, 93) # Navy
        run.font.bold = True
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(41, 128, 185) # Slate blue
        run.font.bold = True
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(52, 73, 94)
        run.font.bold = True
    return h

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(33, 37, 41)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(6)

def add_callout(doc, text, title="OUTPUT LOG"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F6F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    run_t = p.add_run(f"[{title}]\n")
    run_t.font.name = "Consolas"
    run_t.font.size = Pt(9)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(37, 99, 235)
    
    run_b = p.add_run(text.strip())
    run_b.font.name = "Consolas"
    run_b.font.size = Pt(8.5)
    run_b.font.color.rgb = RGBColor(51, 65, 85)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(6)


def generate_document():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Document Header / Banner
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    run_course = p_title.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n")
    run_course.font.name = "Arial"
    run_course.font.size = Pt(11)
    run_course.font.bold = True
    run_course.font.color.rgb = RGBColor(100, 116, 139)
    
    run_title = p_title.add_run("CRYPTOGRAPHY & NETWORK SECURITY LABORATORY\n")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(27, 54, 93)
    
    run_sub = p_title.add_run("COMPREHENSIVE IMPLEMENTATION & EXPERIMENTAL REPORT\n")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(41, 128, 185)

    run_desc = p_title.add_run("Lab 5: Simulation of Access Control Matrix & User Access Rights Updates\n"
                               "Lab 6: Multi-User Cloud Access with Role-Based Access Control & Mutual Certificate Authentication")
    run_desc.font.name = "Arial"
    run_desc.font.size = Pt(10)
    run_desc.font.italic = True
    run_desc.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(16)
    p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="1B365D"/></w:pBdr>')
    p_div._p.get_or_add_pPr().append(p_div_border)

    # =========================================================================
    # PART 1: LAB 5
    # =========================================================================
    add_heading_styled(doc, "LAB 5: Simulation of Access Control Matrix and Illustration of User Updates Access Rights", level=1)

    # 1. Aim
    add_heading_styled(doc, "1. Aim", level=2)
    p = doc.add_paragraph(
        "To simulate an Access Control Matrix (ACM), demonstrate dynamic granting and revoking of user access rights, "
        "and analyze the system's operational performance and scalability by varying matrix dimensions, request volumes, "
        "and permission densities."
    )
    p.paragraph_format.space_after = Pt(8)

    # 2. System Architecture & Model
    add_heading_styled(doc, "2. System Architecture & Access Control Model", level=2)
    p = doc.add_paragraph(
        "An Access Control Matrix (ACM) is a foundational protection model representing the security state of an operating system or "
        "distributed network. The rows correspond to subjects (Users S = {U_1, U_2, ..., U_n}), and the columns correspond to protected objects "
        "(Resources R = {Res_1, Res_2, ..., Res_m}). Each matrix cell M[u, r] contains a set of generic rights or access rights "
        "defining what operations user u may execute on resource r."
    )
    p.paragraph_format.space_after = Pt(6)

    # 3. Permissions Specification
    add_heading_styled(doc, "3. Permission Specification", level=2)
    p = doc.add_paragraph("The simulation implements four fundamental discrete permissions:")
    p.paragraph_format.space_after = Pt(6)
    
    t_perm = doc.add_table(rows=5, cols=3)
    headers = ["Permission Code", "Permission Name", "Operation Description"]
    for c, h in enumerate(headers):
        t_perm.cell(0, c).paragraphs[0].text = h
    
    perm_data = [
        ["R", "Read", "Allows viewing and extracting contents of files, records, or datasets."],
        ["W", "Write", "Permits modifying, updating, or appending content to the resource."],
        ["X", "Execute", "Grants permission to execute binaries, scripts, or automated workflows."],
        ["D", "Delete", "Grants administrative deletion or removal of the resource from storage."]
    ]
    for row_idx, row in enumerate(perm_data):
        for col_idx, val in enumerate(row):
            t_perm.cell(row_idx + 1, col_idx).paragraphs[0].text = val
    style_table(t_perm, header_bg="1B365D")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 4. Input Parameters
    add_heading_styled(doc, "4. Input Parameters for Experimental Benchmark", level=2)
    p = doc.add_paragraph("The performance benchmarking was executed across five escalating test configurations:")
    p.paragraph_format.space_after = Pt(6)

    t_cfg = doc.add_table(rows=6, cols=5)
    cfg_headers = ["Experiment", "Users", "Resources", "Access Requests", "Access Updates"]
    for c, h in enumerate(cfg_headers):
        t_cfg.cell(0, c).paragraphs[0].text = h

    cfg_rows = [
        ["Test 1", "5", "5", "10", "5"],
        ["Test 2", "10", "10", "15", "10"],
        ["Test 3", "15", "15", "20", "15"],
        ["Test 4", "20", "20", "30", "20"],
        ["Test 5", "50", "50", "40", "25"],
    ]
    for r_idx, r in enumerate(cfg_rows):
        for c_idx, val in enumerate(r):
            t_cfg.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_cfg, header_bg="2980B9")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 5. Python Source Code
    add_heading_styled(doc, "5. Python Implementation Source Code", level=2)
    p = doc.add_paragraph(
        "The following Python program implements the Access Control Matrix with automated subject/object generation, "
        "matrix initialization, O(1) hash-based access verification, dynamic access right grant/revocation, and benchmark telemetry:"
    )
    p.paragraph_format.space_after = Pt(6)

    with open(r"d:\CNS_LAB\lab5_access_control_matrix.py", "r", encoding="utf-8") as f:
        lab5_code = f.read()
    add_code_block(doc, lab5_code)

    # 6. Demonstration & Output
    add_heading_styled(doc, "6. Demonstration and Output Results", level=2)
    p = doc.add_paragraph(
        "The simulation demonstrates matrix generation, verification of access requests, and dynamic permission updates "
        "(granting and subsequent revoking) on a 5×5 matrix:"
    )
    p.paragraph_format.space_after = Pt(6)

    sample_output_lab5 = """[Initial Access Control Matrix]:
User        Res_1         Res_2         Res_3         Res_4         Res_5         
----------------------------------------------------------------------------------
User_1      -             DRX           -             -             WX            
User_2      RW            DWX           DRWX          RX            -             
User_3      -             -             -             DRWX          -             
User_4      DRWX          -             DRW           -             DRW           
User_5      -             -             DRWX          -             -             

[Access Requests & Verification]:
Request: User 'User_1' requests 'Read (R)' on 'Res_1'    -> Result: DENIED
Request: User 'User_1' requests 'Write (W)' on 'Res_2'   -> Result: DENIED
Request: User 'User_2' requests 'Execute (X)' on 'Res_3' -> Result: GRANTED
Request: User 'User_3' requests 'Delete (D)' on 'Res_1'  -> Result: DENIED
Request: User 'User_4' requests 'Write (W)' on 'Res_5'   -> Result: GRANTED

[Dynamic Access Updates]:
1. Granting 'W' (Write) and 'D' (Delete) to User_1 on Res_2...
   -> Verifying User_1 on Res_2 for 'Write':  GRANTED
   -> Verifying User_1 on Res_2 for 'Delete': GRANTED
2. Revoking 'W' (Write) from User_1 on Res_2...
   -> Verifying User_1 on Res_2 for 'Write' after revocation: DENIED

[Updated Access Control Matrix]:
User        Res_1         Res_2         Res_3         Res_4         Res_5         
----------------------------------------------------------------------------------
User_1      -             DRX           -             -             WX            
User_2      RW            DWX           DRWX          RX            -             
User_3      -             -             -             DRWX          -             
User_4      DRWX          -             DRW           -             DRW           
User_5      -             -             DRWX          -             -             """
    add_callout(doc, sample_output_lab5, title="LAB 5 DEMONSTRATION LOG")

    # 7. Performance Measurements
    add_heading_styled(doc, "7. Performance Measurements (Completed Experiment Table)", level=2)
    p = doc.add_paragraph(
        "Execution timings were measured using Python's high-resolution performance counter (time.perf_counter_ns) "
        "averaged over repeated benchmark loops to ensure statistical precision:"
    )
    p.paragraph_format.space_after = Pt(6)

    t_perf5 = doc.add_table(rows=6, cols=5)
    perf5_headers = ["Input Size", "Matrix Creation Time (ms)", "Verification Time (ms)", "Update Time (ms)", "Total Execution Time (ms)"]
    for c, h in enumerate(perf5_headers):
        t_perf5.cell(0, c).paragraphs[0].text = h

    perf5_data = [
        ["5 users / 5 resources (Test 1)", "0.0303", "0.0020", "0.0009", "0.0332"],
        ["10 users / 10 resources (Test 2)", "0.1134", "0.0030", "0.0016", "0.1180"],
        ["15 users / 15 resources (Test 3)", "0.2485", "0.0039", "0.0026", "0.2551"],
        ["20 users / 20 resources (Test 4)", "0.4395", "0.0063", "0.0036", "0.4494"],
        ["50 users / 50 resources (Test 5)", "3.5933", "0.0087", "0.0045", "3.6065"],
    ]
    for r_idx, r in enumerate(perf5_data):
        for c_idx, val in enumerate(r):
            t_perf5.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_perf5, header_bg="1B365D")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 8. Additional Experiment - Permission Density
    add_heading_styled(doc, "8. Additional Experiment: Permission Density Analysis", level=2)
    p = doc.add_paragraph(
        "To evaluate how cell density affects memory allocation and processing time, the matrix was tested on 50 users × 50 resources "
        "while systematically modulating the percentage of non-empty permission cells from 10% to 100%:"
    )
    p.paragraph_format.space_after = Pt(6)

    t_dens5 = doc.add_table(rows=6, cols=3)
    dens5_headers = ["Permission Density (%)", "Non-Empty Matrix Cells", "Processing Time (ms)"]
    for c, h in enumerate(dens5_headers):
        t_dens5.cell(0, c).paragraphs[0].text = h

    dens5_data = [
        ["10%", "250 cells populated", "1.5611"],
        ["25%", "625 cells populated", "2.5492"],
        ["50%", "1250 cells populated", "3.6373"],
        ["75%", "1875 cells populated", "4.9614"],
        ["100%", "2500 cells populated", "6.4262"],
    ]
    for r_idx, r in enumerate(dens5_data):
        for c_idx, val in enumerate(r):
            t_dens5.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_dens5, header_bg="2980B9")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 9. Graphs
    add_heading_styled(doc, "9. Graphical Analysis and Visualizations", level=2)
    p = doc.add_paragraph(
        "Below are the five experimental plots generated from empirical measurements illustrating system scaling trends:"
    )
    p.paragraph_format.space_after = Pt(6)

    lab5_plots = [
        ("lab5_graph1_users_vs_time.png", "Graph 1: Number of Users vs Execution Time",
         "Demonstrates the quadratic growth curve of matrix creation time as dimensions expand from 5x5 to 50x50 cells."),
        ("lab5_graph2_requests_vs_verification.png", "Graph 2: Number of Access Requests vs Verification Time",
         "Illustrates linear scaling O(N) of sequential access verification routines, where each request completes in sub-microsecond time."),
        ("lab5_graph3_updates_vs_time.png", "Graph 3: Number of Access Updates vs Update Time",
         "Shows proportional increase in dynamic update time as grant and revoke operations scale from 5 to 25 updates."),
        ("lab5_graph4_density_vs_processing.png", "Graph 4: Permission Density vs Processing Time (50 Users / 50 Resources)",
         "Depicts linear growth in matrix population time as cell permission density scales from sparse (10%) to fully saturated (100%)."),
        ("lab5_graph5_granted_vs_denied.png", "Graph 5: Granted Requests vs Denied Requests Across Runs",
         "Presents the ratio of permitted versus rejected operations across test runs under 50% stochastic permission allocation.")
    ]

    for img_name, title, caption in lab5_plots:
        img_path = os.path.join(LAB5_DIR, img_name)
        if os.path.exists(img_path):
            p_img_title = doc.add_paragraph()
            p_img_title.paragraph_format.space_before = Pt(8)
            p_img_title.paragraph_format.space_after = Pt(2)
            p_img_title.paragraph_format.keep_with_next = True
            r_t = p_img_title.add_run(title)
            r_t.bold = True
            r_t.font.size = Pt(11)
            r_t.font.color.rgb = RGBColor(27, 54, 93)

            p_pic = doc.add_paragraph()
            p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_pic.paragraph_format.space_after = Pt(4)
            p_pic.paragraph_format.keep_with_next = True
            doc.add_picture(img_path, width=Inches(5.6))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r_c = p_cap.add_run(caption)
            r_c.italic = True
            r_c.font.size = Pt(9)
            r_c.font.color.rgb = RGBColor(100, 116, 139)

    # 10. Observations
    add_heading_styled(doc, "10. Technical Observations", level=2)
    obs5_bullets = [
        "As the number of users and resources increases, the matrix creation time increases quadratically (O(U × R)), because an N×N matrix requires N² cell allocations.",
        "As the number of access requests increases, verification time scales strictly linearly (O(k)), where individual permission check time remains constant at approximately 0.0002 ms due to hash-map lookup efficiency.",
        "As the number of access updates increases, update time scales linearly with the number of updates, confirming that dictionary/set insertion and discard operations execute in deterministic O(1) amortized time.",
        "When permission density increases from 10% to 100%, processing time increases monotonically from 1.56 ms to 6.42 ms due to the higher volume of set objects instantiated in memory.",
        "The proportion of granted and denied requests depends directly on the permission density and the probability distribution of generated operations across subjects and objects."
    ]
    for b in obs5_bullets:
        doc.add_paragraph(b, style='List Bullet').paragraph_format.space_after = Pt(4)

    # 11. Result
    add_heading_styled(doc, "11. Result", level=2)
    p = doc.add_paragraph(
        "The Access Control Matrix was successfully simulated and analyzed. Dynamic granting and revoking of user access rights "
        "were demonstrated and verified against before-and-after states. Performance benchmarks across varying matrix dimensions (5 to 50 users/resources) "
        "and permission densities (10% to 100%) were empirically recorded, and all required graphs were generated confirming theoretical algorithmic complexity."
    )
    p.paragraph_format.space_after = Pt(18)

    # =========================================================================
    # PART 2: LAB 6
    # =========================================================================
    add_heading_styled(doc, "LAB 6: Demonstrate Access in a Multi-User Cloud System with Role-Based Access and Mutual Authentication Using Certificates", level=1)

    # 1. Aim
    add_heading_styled(doc, "1. Aim", level=2)
    p = doc.add_paragraph(
        "To demonstrate secure access in a multi-user cloud system using Role-Based Access Control (RBAC) and certificate-based "
        "mutual authentication, verify security boundaries under normal and adversarial certificate conditions (valid, expired, revoked, untrusted), "
        "and analyze the performance of authentication, authorization, and access operations by varying input size."
    )
    p.paragraph_format.space_after = Pt(8)

    # 2. Security Architecture & Mutual Authentication Model
    add_heading_styled(doc, "2. System Architecture & Mutual Authentication Pipeline", level=2)
    p = doc.add_paragraph(
        "In a Zero-Trust Cloud Architecture, access control requires a strict two-stage verification pipeline:"
    )
    p.paragraph_format.space_after = Pt(4)

    p_steps = [
        "Phase 1: Mutual Certificate Authentication (Identity Layer) — The client presents an X.509 certificate to the cloud gateway, which validates the certificate's cryptographic signature against the root CA, checks validity timestamps, and inspects the Certificate Revocation List (CRL). Simultaneously, the client validates the server's identity certificate against the trusted CA. Access is immediately aborted if either certificate is invalid, expired, revoked, or signed by an untrusted entity.",
        "Phase 2: Role-Based Access Control Authorization (Permission Layer) — Once mutual identity is established, the user's assigned role is resolved against the central RBAC policy matrix to determine if the requested operation (Read, Write/Upload, Modify, Delete, User Management) is permitted on the target resource."
    ]
    for s in p_steps:
        doc.add_paragraph(s, style='List Bullet').paragraph_format.space_after = Pt(4)

    # 3. Roles and Permissions Matrix
    add_heading_styled(doc, "3. Cloud Roles and Permissions Matrix", level=2)
    p = doc.add_paragraph("The cloud system defines five hierarchical roles with discrete functional rights:")
    p.paragraph_format.space_after = Pt(6)

    t_rbac = doc.add_table(rows=6, cols=6)
    rbac_headers = ["Role", "Read (R)", "Write/Upload (W)", "Modify (M)", "Delete (D)", "User Management (UM)"]
    for c, h in enumerate(rbac_headers):
        t_rbac.cell(0, c).paragraphs[0].text = h

    rbac_rows = [
        ["Administrator", "Yes", "Yes", "Yes", "Yes", "Yes"],
        ["Faculty/Manager", "Yes", "Yes", "Yes", "Limited", "No"],
        ["Student/User", "Yes", "Yes", "No", "No", "No"],
        ["Guest", "Limited", "No", "No", "No", "No"],
        ["Auditor", "Yes", "No", "No", "No", "No"],
    ]
    for r_idx, r in enumerate(rbac_rows):
        for c_idx, val in enumerate(r):
            t_rbac.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_rbac, header_bg="1B365D")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4. Input Parameters
    add_heading_styled(doc, "4. Input Parameters for Experimental Benchmark", level=2)
    p = doc.add_paragraph("The benchmark was conducted across five automated cloud load configurations:")
    p.paragraph_format.space_after = Pt(6)

    t_cfg6 = doc.add_table(rows=6, cols=6)
    cfg6_headers = ["Experiment", "Users", "Roles", "Resources", "Access Requests", "Access Updates"]
    for c, h in enumerate(cfg6_headers):
        t_cfg6.cell(0, c).paragraphs[0].text = h

    cfg6_rows = [
        ["Test 1", "5", "3", "5", "10", "5"],
        ["Test 2", "10", "4", "10", "20", "8"],
        ["Test 3", "15", "4", "15", "30", "10"],
        ["Test 4", "20", "4", "20", "25", "15"],
        ["Test 5", "25", "5", "25", "35", "20"],
    ]
    for r_idx, r in enumerate(cfg6_rows):
        for c_idx, val in enumerate(r):
            t_cfg6.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_cfg6, header_bg="2980B9")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 5. Python Source Code
    add_heading_styled(doc, "5. Python Implementation Source Code", level=2)
    p = doc.add_paragraph(
        "The following Python program implements the complete multi-user cloud access control system, including an X.509 "
        "Certificate Authority (using standard RSA-2048 with SHA-256 signatures), Certificate Revocation List (CRL), "
        "mutual authentication engine, dynamic RBAC authorization engine, and multi-tier telemetry:"
    )
    p.paragraph_format.space_after = Pt(6)

    with open(r"d:\CNS_LAB\lab6_cloud_rbac_mutual_auth.py", "r", encoding="utf-8") as f:
        lab6_code = f.read()
    add_code_block(doc, lab6_code)

    # 6. Security Test Cases & Output
    add_heading_styled(doc, "6. Security Test Cases & Certificate Status Verification", level=2)
    p = doc.add_paragraph(
        "The mutual authentication engine was subjected to four key certificate security test conditions to verify policy enforcement:"
    )
    p.paragraph_format.space_after = Pt(6)

    t_sec = doc.add_table(rows=5, cols=5)
    sec_headers = ["Certificate Condition", "Client Cert Status", "Mutual Authentication", "RBAC Decision", "Final Access Status"]
    for c, h in enumerate(sec_headers):
        t_sec.cell(0, c).paragraphs[0].text = h

    sec_data = [
        ["Valid", "VALID", "SUCCESS", "ALLOWED / EVALUATED", "ACCESS GRANTED"],
        ["Expired", "EXPIRED", "FAILED", "BLOCKED_BY_AUTH_FAILURE", "ACCESS DENIED"],
        ["Revoked", "REVOKED", "FAILED", "BLOCKED_BY_AUTH_FAILURE", "ACCESS DENIED"],
        ["Untrusted CA", "UNTRUSTED_ISSUER", "FAILED", "BLOCKED_BY_AUTH_FAILURE", "ACCESS DENIED"],
    ]
    for r_idx, r in enumerate(sec_data):
        for c_idx, val in enumerate(r):
            t_sec.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_sec, header_bg="1B365D")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Expected Output Format Demonstration
    add_heading_styled(doc, "7. Expected Sample Output Demonstration (Section 13 Format)", level=2)
    p = doc.add_paragraph(
        "Below is an authentic execution record demonstrating an unauthorized access request by a student role "
        "attempting a Modify operation with valid mutual authentication:"
    )
    p.paragraph_format.space_after = Pt(6)

    sample_output_lab6 = """Resource: File_01.pdf
Operation: Modify
Client Certificate: VALID
Server Certificate: VALID
Mutual Authentication: SUCCESS
RBAC Decision: DENIED
Authentication Time: 0.1165 ms
Authorization Time: 0.0029 ms
Total Response Time: 0.1194 ms
Final Status: ACCESS DENIED"""
    add_callout(doc, sample_output_lab6, title="SECTION 13 CLOUD ACCESS DECISION RECORD")

    # 8. Performance Measurements
    add_heading_styled(doc, "8. Performance Measurements (Completed Experiment Table)", level=2)
    p = doc.add_paragraph(
        "Recorded performance metrics including cryptographic setup, mutual authentication, RBAC authorization, "
        "total access latency, dynamic update time, and throughput:"
    )
    p.paragraph_format.space_after = Pt(6)

    t_perf6 = doc.add_table(rows=6, cols=7)
    perf6_headers = ["Input Size", "Setup Time (ms)", "Avg Auth (ms)", "Avg Authz (ms)", "Response Time (ms)", "Update Time (ms)", "Throughput (req/s)"]
    for c, h in enumerate(perf6_headers):
        t_perf6.cell(0, c).paragraphs[0].text = h

    perf6_data = [
        ["5 users / 5 res (Test 1)", "535.127", "0.3471", "0.0013", "0.3484", "0.0009", "2870.10"],
        ["10 users / 10 res (Test 2)", "685.670", "0.1133", "0.0009", "0.1143", "0.0015", "8750.05"],
        ["15 users / 15 res (Test 3)", "952.036", "0.1423", "0.0008", "0.1431", "0.0019", "6990.56"],
        ["20 users / 20 res (Test 4)", "1287.099", "0.1028", "0.0008", "0.1036", "0.0024", "9652.14"],
        ["25 users / 25 res (Test 5)", "1421.517", "0.0816", "0.0005", "0.0821", "0.0031", "12181.12"],
    ]
    for r_idx, r in enumerate(perf6_data):
        for c_idx, val in enumerate(r):
            t_perf6.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_perf6, header_bg="1B365D")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 9. Permission Density
    add_heading_styled(doc, "9. Permission Density Benchmark", level=2)
    p = doc.add_paragraph(
        "Measurement of RBAC authorization processing latency as role permissions are saturated from 10% to 100%:"
    )
    p.paragraph_format.space_after = Pt(6)

    t_dens6 = doc.add_table(rows=6, cols=2)
    dens6_headers = ["Permission Density (%)", "Authorization Processing Time (ms)"]
    for c, h in enumerate(dens6_headers):
        t_dens6.cell(0, c).paragraphs[0].text = h

    dens6_data = [
        ["10%", "0.00022"],
        ["25%", "0.00020"],
        ["50%", "0.00019"],
        ["75%", "0.00020"],
        ["100%", "0.00020"],
    ]
    for r_idx, r in enumerate(dens6_data):
        for c_idx, val in enumerate(r):
            t_dens6.cell(r_idx + 1, c_idx).paragraphs[0].text = val
    style_table(t_dens6, header_bg="2980B9")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 10. Graphical Visualizations
    add_heading_styled(doc, "10. Graphical Visualizations and Scalability Analysis", level=2)
    p = doc.add_paragraph(
        "Below are the empirical plots generated from the multi-user cloud simulation benchmarks:"
    )
    p.paragraph_format.space_after = Pt(6)

    lab6_plots = [
        ("lab6_graph1_users_vs_auth_time.png", "Graph 1: Number of Users vs Authentication Time",
         "Shows average mutual certificate authentication latency per request across scaling user populations."),
        ("lab6_graph2_users_vs_authz_time.png", "Graph 2: Number of Users vs Authorization Time",
         "Illustrates ultra-low authorization lookup latency (~0.001 ms) due to constant-time role permission sets."),
        ("lab6_graph3_users_vs_response_time.png", "Graph 3: Number of Users vs Total Access Response Time",
         "Highlights total request response time, confirming that asymmetric certificate verification accounts for >98% of total access latency."),
        ("lab6_graph4_requests_vs_authz_time.png", "Graph 4: Number of Access Requests vs Authorization Time",
         "Depicts per-request authorization performance under varying request batch sizes."),
        ("lab6_graph5_updates_vs_update_time.png", "Graph 5: Number of Access Updates vs Update Time",
         "Demonstrates predictable linear scaling of role policy modification operations."),
        ("lab6_graph6_concurrent_users_vs_throughput.png", "Graph 6: Concurrent Users vs Throughput",
         "Demonstrates sustained high throughput ranging between 2,800 to 12,000 requests/second."),
        ("lab6_graph7_cert_status_vs_auth_results.png", "Graph 7: Certificate Status vs Successful/Rejected Authentication Requests",
         "Validates the security boundary: valid certificates pass authentication, while expired, revoked, and untrusted certificates are 100% blocked."),
        ("lab6_graph8_density_vs_processing.png", "Graph 8: Permission Density vs Authorization Processing Time",
         "Confirms that authorization decision latency remains constant regardless of permission density due to hash table O(1) membership testing."),
        ("lab6_graph9_granted_vs_denied.png", "Graph 9: Granted Requests vs Denied Requests Across Runs",
         "Shows the distribution of granted versus denied requests across diverse experimental test configurations.")
    ]

    for img_name, title, caption in lab6_plots:
        img_path = os.path.join(LAB6_DIR, img_name)
        if os.path.exists(img_path):
            p_img_title = doc.add_paragraph()
            p_img_title.paragraph_format.space_before = Pt(8)
            p_img_title.paragraph_format.space_after = Pt(2)
            p_img_title.paragraph_format.keep_with_next = True
            r_t = p_img_title.add_run(title)
            r_t.bold = True
            r_t.font.size = Pt(11)
            r_t.font.color.rgb = RGBColor(27, 54, 93)

            p_pic = doc.add_paragraph()
            p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_pic.paragraph_format.space_after = Pt(4)
            p_pic.paragraph_format.keep_with_next = True
            doc.add_picture(img_path, width=Inches(5.6))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r_c = p_cap.add_run(caption)
            r_c.italic = True
            r_c.font.size = Pt(9)
            r_c.font.color.rgb = RGBColor(100, 116, 139)

    # 11. Observations
    add_heading_styled(doc, "11. Technical Observations", level=2)
    obs6_bullets = [
        "Authentication vs. Authorization Latency: Asymmetric cryptographic verification (RSA-2048 with SHA-256) requires approximately 0.1 to 0.35 ms per mutual handshake, representing over 98% of total access latency, whereas RBAC authorization executes in less than 0.001 ms.",
        "Zero-Trust Security Barrier: Malicious, expired, revoked, or untrusted certificates are immediately rejected at the cryptographic authentication boundary before any resource or RBAC policy evaluation occurs, protecting cloud authorization logic from unauthorized processing load.",
        "Scalability and Throughput: The simulated multi-user cloud engine sustained high processing throughput exceeding 2,800 to 12,000 requests/second across scaling concurrent user workloads.",
        "Constant-Time RBAC Complexity: Changing permission density from 10% to 100% has virtually zero impact on authorization evaluation latency (holding steady at ~0.0002 ms) because set membership checks in Python execute in O(1) time.",
        "Dynamic Policy Maintenance: Dynamic role permission updates (granting/revoking rights) execute in microsecond time (~0.001 to 0.003 ms), providing near-instant policy reconfiguration in dynamic cloud environments."
    ]
    for b in obs6_bullets:
        doc.add_paragraph(b, style='List Bullet').paragraph_format.space_after = Pt(4)

    # 12. Result
    add_heading_styled(doc, "12. Result", level=2)
    p = doc.add_paragraph(
        "A multi-user cloud access system incorporating Role-Based Access Control (RBAC) and certificate-based mutual authentication "
        "was successfully implemented, tested, and analyzed. Cryptographic identity verification was demonstrated across valid, expired, revoked, "
        "and untrusted certificate conditions. Role-based permission enforcement was verified with dynamic granting and revoking operations. "
        "Comprehensive empirical performance data was measured across five load levels, and all nine graphical plots were generated and analyzed."
    )
    p.paragraph_format.space_after = Pt(14)

    # Save document
    doc.save(DOC_PATH)
    print(f"Report document generated successfully at: {DOC_PATH}")

if __name__ == "__main__":
    generate_document()
