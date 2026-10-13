import streamlit as st
import pandas as pd
import plotly.express as px\


st.set_page_config(
    page_title="RTU CALCULATOR",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    .stSelectbox label {
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 2. RTU GRADING SYSTEM CONSTANTS

GRADE_POINTS = {
    "A++ (10)": 10.0,
    "A+ (9)": 9.0,
    "A (8)": 8.0,
    "B+ (7)": 7.0,
    "B (6)": 6.0,
    "C+ (5)": 5.0,
    "C (4)": 4.0,
    "F (0)": 0.0
}


DEFAULT_SEMESTER_DATA = {
    "Semester 1": [
        {"subject": "Engineering Physics / Chemistry", "credit": 4.0},
        {"subject": "Engineering Mathematics-I", "credit": 4.0},
        {"subject": "Programming for Problem Solving / Mechanical Engineering ", "credit": 2.0},
        {"subject": "Basic Electrical Engineering / Civil Engineering", "credit": 2.0},
        {"subject": "Human Values / Communication Skills","credit":2.0},
        {"subject": "Engineering Physics / Chemistry Lab", "credit": 1.0},
        {"subject": "Language Lab/ Human Values Activities  ", "credit": 1.0},
        {"subject": "Computer Programming Lab/ Manufacturing Practices Workshop ", "credit": 1.5},
        {"subject": "Basic Electrical Engineering Lab/ Basic Civil Engineering Lab", "credit": 1.0},
        {"subject":  "Computer Aided Engineering Graphics/ Computer Aided Machine Drawing ", "credit": 1.5},
        {"subject": "Sports", "credit": 0.5},
    ],
    "Semester 2": [
        {"subject": "Engineering Chemistry / Physics", "credit": 4.0},
        {"subject": "Engineering Mathematics-II", "credit": 4.0},
        {"subject": "Programming for Problem Solving / Mechanical Engineering ", "credit": 2.0},
        {"subject": "Basic Civil / Electrical Engineering", "credit": 2.0},
        {"subject": "Human Values / Communication Skills","credit":2.0},
        {"subject": "Engineering Chemistry / Physics Lab", "credit": 1.0},
        {"subject": "Language Lab/ Human Values Activities  ", "credit": 1.0},
        {"subject": "Computer Programming Lab/ Manufacturing Practices Workshop ", "credit": 1.5},
        {"subject": "Basic Electrical Engineering Lab/ Basic Civil Engineering Lab", "credit": 1.0},
        {"subject":  "Computer Aided Engineering Graphics/ Computer Aided Machine Drawing ", "credit": 1.5},
        {"subject": "Sports", "credit": 0.5},
        
    ],
    "Semester 3": [
        {"subject": "Advanced Engineering Mathematics", "credit": 3.0},
        {"subject": "Technical Communication", "credit": 2.0},
        {"subject": "Digital Electronics", "credit": 3.0},
        {"subject": "Data Structures and Algorithms", "credit": 3.0},
        {"subject": "Object Oriented Programming", "credit": 3.0},
        {"subject": "Software Engineering", "credit": 3.0},
        {"subject": "Data Structures Lab", "credit": 1.5},
        {"subject": "Object Oriented Programming Lab", "credit": 1.5},
        {"subject": "Software Engineering Lab ", "credit":1.5},
        {"subject": "Digital Electronics Lab", "credit": 1.5},
        {"subject": "Industrial Training (30 Days)", "credit": 1.0},
        {"subject": "Anandam / SODECA", "credit": 0.5},
    ],
    "Semester 4": [
        {"subject": "Discrete Mathematics", "credit": 3.0},
        {"subject": "Managerial Economics & Financial Analysis", "credit": 2.0},
        {"subject": "Microprocessor & Interfaces", "credit": 3.0},
        {"subject": "Database Management Systems", "credit": 3.0},
        {"subject": "Theory of Computation", "credit": 3.0},
        {"subject": "Data Communication  and Computer Networks", "credit": 3.0},
        {"subject": "Microprocessor and Interfaces Lab ", "credit":1.0},
        {"subject": "Linux Shell Programming Lab", "credit":1.0},
        {"subject": "Database Management Systems Lab", "credit": 1.5},
        {"subject": "Network Programming Lab", "credit": 1.5},
        {"subject": "Java Programming Lab", "credit": 1.0},
        {"subject": "Anandam / SODECA", "credit": 0.5},
    ],
    "Semester 5": [
        {"subject": "Data Mining Concepts & Techniques", "credit": 3.0},
        {"subject": "Operating Systems", "credit": 3.0},
        {"subject": "Machine Learning", "credit": 3.0},
        {"subject": "Data Science & Visualization", "credit": 3.0},
        {"subject": "Program Elective - I", "credit": 3.0},
        {"subject": "Machine Learning Lab", "credit": 1.5},
        {"subject": "Data Science & Visualization Lab", "credit": 1.5},
        {"subject": "Operating System Lab", "credit": 1.0},
        {"subject": "Industrial Training", "credit": 1.0},
        {"subject": "Anandam / SODECA", "credit": 0.5},
    ],
    "Semester 6": [
        {"subject": "Digital Image Processing", "credit": 3.0},
        {"subject": "Natural Language Processing", "credit": 3.0},
        {"subject": "Artificial Neural Networks", "credit": 3.0},
        {"subject": "Deep Learning", "credit": 3.0},
        {"subject": "Program Elective - II", "credit": 3.0},
        {"subject": "NLP & Text Mining Lab", "credit": 1.5},
        {"subject": "Deep Learning Lab", "credit": 1.5},
        {"subject": "Image Processing Lab", "credit": 1.0},
        {"subject": "Anandam / SODECA", "credit": 0.5},
    ],
    "Semester 7": [
        {"subject": "Big Data Analytics", "credit": 3.0},
        {"subject": "Cloud Computing", "credit": 3.0},
        {"subject": "Open Elective - I", "credit": 3.0},
        {"subject": "Big Data Analytics Lab", "credit": 2.0},
        {"subject": "Seminar", "credit": 2.0},
        {"subject": "Major Project Phase 1", "credit": 4.0},
        {"subject": "Practical Training (45 Days)", "credit": 2.5},
        {"subject": "Anandam / SODECA", "credit": 0.5},
    ],
    "Semester 8": [
        {"subject": "Advanced AI / Reinforcement Learning", "credit": 3.0},
        {"subject": "Open Elective - II", "credit": 3.0},
        {"subject": "Major Project Phase 2", "credit": 8.0},
        {"subject": "Anandam / SODECA", "credit": 1.0},
    ]
}

# -----------------------------------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "sem_data" not in st.session_state:
    st.session_state.sem_data = {}
    for sem_name, subjects in DEFAULT_SEMESTER_DATA.items():
        st.session_state.sem_data[sem_name] = [
            {"subject": s["subject"], "credit": float(s["credit"]), "grade": "A+ (9)"}
            for s in subjects
        ]

# -----------------------------------------------------------------------------
# 5. CORE CALCULATION FUNCTIONS
# -----------------------------------------------------------------------------
def calculate_sgpa(subject_list):
    total_credits = sum(s["credit"] for s in subject_list)
    if total_credits == 0:
        return 0.0, 0.0
    
    weighted_points = sum(s["credit"] * GRADE_POINTS[s["grade"]] for s in subject_list)
    sgpa = weighted_points / total_credits
    return round(sgpa, 2), round(total_credits, 2)

def calculate_cgpa(sem_results):
    total_credits = sum(res["credits"] for res in sem_results.values() if res["included"])
    if total_credits == 0:
        return 0.0, 0.0
    
    total_weighted_sgpa = sum(res["sgpa"] * res["credits"] for res in sem_results.values() if res["included"])
    cgpa = total_weighted_sgpa / total_credits
    return round(cgpa, 2), round(total_credits, 2)

# -----------------------------------------------------------------------------
# 6. APP UI & NAVIGATION
# -----------------------------------------------------------------------------
st.title("🧮 RTU AI & DS B.Tech Academic Calculator")
st.caption("Custom tailored for Artificial Intelligence & Data Science Engineering (Rajasthan Technical University)")

# Sidebar Configuration Options
st.sidebar.header(" Global Settings")
conversion_multiplier = st.sidebar.radio(
    "Percentage Conversion Formula:",
    options=[9.5, 10.0],
    format_func=lambda x: f"Percentage = CGPA × {x} ({'Official RTU' if x == 9.5 else 'Alternative Standard'})",
    index=0
)

st.sidebar.divider()
st.sidebar.markdown("""
### 📌 RTU Grading Scale
* **A++** : 10 Grade Points
* **A+**  : 9 Grade Points
* **A**   : 8 Grade Points
* **B+**  : 7 Grade Points
* **B**   : 6 Grade Points
* **C+**  : 5 Grade Points
* **C**   : 4 Grade Points
* **F**   : 0 Grade Points
""")

# Tabs Layout
tab1, tab2 = st.tabs(["📝 Semester SGPA & Subject Editor", "📊 Overall CGPA & Performance Insights"])

# -----------------------------------------------------------------------------
# TAB 1: SGPA CALCULATOR & SUBJECT MANAGEMENT
# -----------------------------------------------------------------------------
with tab1:
    selected_sem = st.selectbox("Select Semester:", list(DEFAULT_SEMESTER_DATA.keys()))
    st.write(f"### Grade Input - {selected_sem}")
    
    current_subjects = st.session_state.sem_data[selected_sem]
    
    # Expandable section to add new subject
    with st.expander("➕ Add Custom Subject / Elective"):
        col_a, col_b = st.columns([3, 1])
        new_sub_name = col_a.text_input("Subject Name", key=f"new_sub_{selected_sem}")
        new_sub_credit = col_b.number_input("Credits", min_value=0.5, max_value=10.0, step=0.5, value=3.0, key=f"new_cred_{selected_sem}")
        
        if st.button("Add Subject", use_container_width=True):
            if new_sub_name.strip():
                st.session_state.sem_data[selected_sem].append({
                    "subject": new_sub_name.strip(),
                    "credit": float(new_sub_credit),
                    "grade": "A+ (9)"
                })
                st.toast(f"Added {new_sub_name}!", icon="✅")
                st.rerun()
            else:
                st.error("Please enter a valid subject name.")

    # Form to update grades and credits dynamically
    updated_subjects = []
    
    st.write("---")
    header_col1, header_col2, header_col3, header_col4 = st.columns([4, 2, 3, 1])
    header_col1.markdown("**Subject Title**")
    header_col2.markdown("**Credits**")
    header_col3.markdown("**Grade Earned**")
    header_col4.markdown("**Action**")
    
    for idx, item in enumerate(current_subjects):
        c1, c2, c3, c4 = st.columns([4, 2, 3, 1])
        
        sub_name = c1.text_input(f"Sub_{idx}", value=item["subject"], label_visibility="collapsed", key=f"name_{selected_sem}_{idx}")
        sub_credit = c2.number_input(f"Cred_{idx}", min_value=0.5, max_value=12.0, step=0.5, value=float(item["credit"]), label_visibility="collapsed", key=f"cred_{selected_sem}_{idx}")
        sub_grade = c3.selectbox(f"Grade_{idx}", list(GRADE_POINTS.keys()), index=list(GRADE_POINTS.keys()).index(item["grade"]), label_visibility="collapsed", key=f"grade_{selected_sem}_{idx}")
        
        # Delete action
        if c4.button("🗑️", key=f"del_{selected_sem}_{idx}"):
            st.session_state.sem_data[selected_sem].pop(idx)
            st.rerun()
            
        updated_subjects.append({
            "subject": sub_name,
            "credit": float(sub_credit),
            "grade": sub_grade
        })

    st.session_state.sem_data[selected_sem] = updated_subjects
    
    # Calculate SGPA for current semester
    sgpa, total_sem_credits = calculate_sgpa(updated_subjects)
    
    st.write("---")
    st.markdown(f"### Results for {selected_sem}")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Semester SGPA", value=f"{sgpa:.2f}")
    m2.metric(label="Total Credits", value=f"{total_sem_credits}")
    m3.metric(label="Equivalent Percentage", value=f"{round(sgpa * conversion_multiplier, 2)}%")

# -----------------------------------------------------------------------------
# TAB 2: OVERALL CGPA & DASHBOARD
# -----------------------------------------------------------------------------
with tab2:
    st.write("### Cumulative Grade Point Average (CGPA) Summary")
    st.info("Uncheck any semester that you have not completed yet to omit it from the overall CGPA computation.")
    
    sem_results = {}
    cols = st.columns(2)
    
    for idx, (sem_name, subjects) in enumerate(st.session_state.sem_data.items()):
        col = cols[idx % 2]
        with col:
            is_included = st.checkbox(f"Include **{sem_name}** in CGPA", value=(idx == 0 or calculate_sgpa(subjects)[0] > 0), key=f"inc_{sem_name}")
            sem_sgpa, sem_credits = calculate_sgpa(subjects)
            sem_results[sem_name] = {
                "sgpa": sem_sgpa,
                "credits": sem_credits,
                "included": is_included
            }
            if is_included:
                st.caption(f"SGPA: **{sem_sgpa:.2f}** | Credits: **{sem_credits}**")
            st.divider()

    # Calculate Cumulative Stats
    cgpa, total_cumulative_credits = calculate_cgpa(sem_results)
    percentage = round(cgpa * conversion_multiplier, 2)
    
    # Display CGPA Metric Cards
    st.markdown("## 🎯 Overall Academic Performance")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric(label="Overall CGPA", value=f"{cgpa:.2f}")
    res_c2.metric(label="Total Credits Earned", value=f"{total_cumulative_credits}")
    res_c3.metric(label=f"Equivalent Percentage (×{conversion_multiplier})", value=f"{percentage}%")

    # Trend Chart
    st.write("---")
    st.markdown("### 📈 SGPA Progression Chart")
    
    chart_data = [
        {"Semester": sem, "SGPA": res["sgpa"]} 
        for sem, res in sem_results.items() if res["included"]
    ]
    
    if chart_data:
        df = pd.DataFrame(chart_data)
        fig = px.bar(
            df, 
            x="Semester", 
            y="SGPA", 
            text="SGPA",
            color="SGPA", 
            color_continuous_scale="Blues",
            range_y=[0, 10]
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Semester", 
            yaxis_title="SGPA Score", 
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Select at least one semester above to generate the performance chart.")