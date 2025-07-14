import os
import time
import pandas as pd
import utility as util
import streamlit as st
from pathlib import Path
import analysis_utility as analysis
import streamlit.components.v1 as components

st.set_page_config(
    page_title="National Rape Data Analytical Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'proceed' not in st.session_state:
    st.session_state.proceed = False
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = None
if 'show_state_page' not in st.session_state:
    st.session_state.show_state_page = False
    
if not st.session_state.proceed and not st.session_state.show_state_page:

    st.markdown("""
    <style>
    /* Force light theme background */
    html, body, [data-testid="stApp"] {
        background-color: white !important;
        color: black !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Header Bar with Tricolor */
    .header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 5rem 2rem;
        display: flex;
        align-items: center;
        border-radius: 20px 20px 20px 20px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        justify-content: space-between;
    }
    .header img {
        height: 60px;
        margin-right: 1rem;
    }
    .header h1 {
        font-size: 2.3rem;
        margin: 0;
        color: #002b5b;
    }
    .header p {
        margin: 0 0 0 auto;
        font-size: 1rem;
        color: #222;
        font-style: italic;
    }

    /* Info Card */
    .info-card {
        background-color: #ffffff;
        border: 1px solid #c8c8c8;
        border-radius: 6px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.05);
    }

    /* Quote Box */
    .quote-box {
        font-style: italic;
        color: #333;
        border-left: 4px solid #138808;
        padding-left: 1rem;
        background-color: #f8f8f8;
        border-radius: 6px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f1f3f5;
        color: #002b5b;
    }
    [data-testid="stSidebar"] .css-1v3fvcr {
        color: #000000 !important;
    }

    /* Section Titles */
    h2.section-title {
        color: #002b5b;
        font-weight: 700;
        border-bottom: 2px solid #138808;
        padding-bottom: 0.3rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    emblem_svg_path = Path(os.getcwd()) / 'india_emblem.svg'

    chakra_path = Path(os.getcwd()) / 'chakra.png'
    chakra_b64 = util.get_base64_image(chakra_path) if chakra_path.exists() else ""

    st.markdown(f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background-color: white !important;
        color: black !important;
        font-family: 'Segoe UI', sans-serif;
    }}

    .header {{
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 3rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        gap: 1.5rem;
        flex-wrap: wrap;
    }}
    .header h1 {{
        font-size: 2rem;
        color: #002b5b;
        margin: 0;
        flex-grow: 1;
        text-align: center;
    }}
    .header p {{
        margin: 0;
        font-size: 1rem;
        font-style: italic;
        color: #333;
        white-space: nowrap;
    }}
    .header .chakra {{
        height: 80px;
        margin: 0 auto;

    }}
    </style>

    <div class="header">
        <img src="data:image/png;base64,{chakra_b64}" class="chakra">
    </div>
    """, unsafe_allow_html=True)

    emblem_svg_b64 = util.get_base64_svg(emblem_svg_path) if emblem_svg_path.exists() else ""

    if emblem_svg_b64:
        col1, col2 = st.columns([1, 8])
        with col1:
            st.markdown(
                f'<img src="data:image/svg+xml;base64,{emblem_svg_b64}" width="60">',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown("### National Rape Data Analytical Insights (2001 - 2011)")
            st.markdown("*A Data-Driven Public Information Dashboard Aligned with Government Standards*")

    else:
        st.markdown("<h1>National Rape Data Analytical Insights</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('''
        <div class="info-card">
        <strong>🌐 About this Portal</strong><br><br>
        This dashboard is based on official government records from NCRB, presenting a factual view of rape cases reported in India over 11 years.
        <ul>
            <li><strong>Objective:</strong> Raise awareness and support policy-making.</li>
            <li><strong>Scope:</strong> State & UT Insights, Age-wise breakdown, Incest or Other.</li>
            <li><strong>Source:</strong> National Crime Records Bureau (NCRB).</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="info-card quote-box">
        "Public data empowers informed decisions and stronger communities."<br><br>
        — Government of India
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("""
            <style>
        div.stButton > button:first-child {
            background-color: #002b5b;
            color: white;
            padding: 0.7rem 1.5rem;
            font-size: 1rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            text-align: center;
            transition: background-color 0.3s ease;
            width: 23.6vw;
        }
        div.stButton > button:first-child:hover {
            background-color: #004080;
        }
    </style>
    """, unsafe_allow_html=True)

        if st.button("Proceed", key="proceed_button"):
            st.session_state.proceed = True
            st.rerun()

    st.markdown("""
        <style>
            /* Sidebar Base */
            [data-testid="stSidebar"] {
                background-color: #f7f9fa;
                padding: 0rem 1.5rem;
                font-family: 'Segoe UI', sans-serif;
                margin-top: -1.2rem;
            }

            /* Sidebar Text Styling */
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] li, 
            [data-testid="stSidebar"] a {
                color: #002b5b;
                font-size: 0.95rem;
                line-height: 1.6;
            }

            /* Highlighted Labels */
            [data-testid="stSidebar"] strong {
                color: #004080;
                font-weight: 600;
            }

            /* Email style */
            [data-testid="stSidebar"] em {
                color: #006666;
                font-style: normal;
                font-weight: 500;
            }

            /* Link Styling */
            [data-testid="stSidebar"] a {
                color: #0056b3;
                text-decoration: none;
            }

            [data-testid="stSidebar"] a:hover {
                text-decoration: underline;
                color: #003366;
            }

            /* Section Padding */
            [data-testid="stSidebar"] > div {
                margin-bottom: 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    **🏛️ Source of Data:**  
    National Crime Records Bureau (NCRB), Ministry of Home Affairs, Government of India

    **📌 Scope of Dataset:**  
    Analytical insights into reported rape cases across Indian States & Union Territories, spanning **2001 to 2011**.

    **🕒 Last Official Update:**  
    As per the latest records available in **2021**.

    **📂 Data Authenticity:**  
    Publicly accessible datasets:  
    🔗 [data.gov.in – Open Government Data Platform](https://www.data.gov.in/)

    **📧 Developer & Contact:**  
    **Rayyan Ashraf**  
    _rayyan.connects@gmail.com_
    """)

elif st.session_state.proceed and not st.session_state.show_state_page:
    
    with st.form(key="back_home_form"):
        submitted = st.form_submit_button("← Back to Home", type="primary")
        if submitted:
            st.session_state.show_state_page = False
            st.session_state.proceed = False
            st.session_state.selected_state = None
            st.session_state.active_state = None
            st.rerun()

    st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background-color: white !important;
        color: black !important;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    
    button_bg_path = Path(os.getcwd()) / 'bg_btn.jpg'
    button_bg_b64 = util.get_base64_image(button_bg_path) if button_bg_path.exists() else ""
    
    st.markdown(f"""
        <style>
            div.stButton > button {{
                background-image: linear-gradient(to bottom, #004080, #002b5b);
                color: #ffffff;
                padding: 1rem 1.5rem;
                font-size: 1.1rem;
                font-weight: 600;
                border: 1px solid #001933;
                border-radius: 8px;
                height: 72px;
                width: 100%;
                cursor: pointer;
                box-shadow: 0 2px 6px rgba(0, 43, 91, 0.3), inset 0 1px 0 rgba(255,255,255,0.08);
                transition: all 0.2s ease-in-out;
                font-family: "Segoe UI", "Arial", sans-serif;
                letter-spacing: 0.2px;
                text-shadow: 0 1px 1px rgba(0,0,0,0.2);
            }}

            div.stButton > button:hover {{
                background-image: 
                    linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url("data:image/jpeg;base64,{button_bg_b64}");
                
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;

                color: #ffffff;

                transform: translateY(-2px);
                transition: all 0.3s ease-in-out;
                border: none;
            }}

            div.stButton > button:active {{
                transform: translateY(1px);
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
        </style>

    """, unsafe_allow_html=True)

    if "selected_state" not in st.session_state:
        st.session_state.selected_state = None

    india_outline = Path(os.getcwd()) / 'india_outline.png'
    india_outline_b64 = util.get_base64_image(india_outline) if india_outline.exists() else ""

    st.markdown(f"""
<style>
.gov-section {{
    border-left: 8px solid #002b5b;
    padding: 1.2rem 1.5rem;
    background: linear-gradient(90deg, #f9fafa, #f1f4f8);
    font-family: 'Georgia', serif;
    color: #002b5b;
    margin-top: 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,43,91,0.08);
    position: relative;
    border-radius: 6px;
}}

.gov-section:before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    height: 6px;
    width: 100%;
    background: linear-gradient(to right, #FF9933, white, #138808); /* Tricolor */
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}

.gov-section h2 {{
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}}

.gov-section p {{
    font-size: 0.95rem;
    color: #333;
    margin: 0.2rem 0 0;
    font-style: italic;
}}
.gov-section img {{
    width: 3vw;
}}
</style>

<div class="gov-section">
    <h2><img src="data:image/png;base64,{india_outline_b64}" class="gov-icon">  States of the Republic of India</h2>
    <p>{util.return_nbsp(3)}{util.return_nbsp(3)}{util.return_nbsp(3)}{util.return_nbsp(3)}Official listing as per Government of India records, Ministry of Home Affairs.</p>
<div style='
        background-color: #e9ecef;
        padding: 1.2rem 1.5rem;
        border: 1px solid #c1c1c1;
        border-radius: 6px;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    '>
        <h4 style='
            margin: 0;
            color: #002b5b;
            font-weight: 700;
            font-family: "Georgia", serif;
            text-transform: uppercase;
            font-size: 1.2rem;
            letter-spacing: 0.5px;
        '>
            📍 Selection of Administrative Region for Data Exploration
        </h4>
        <p style='
            margin-top: 0.5rem;
            color: #333;
            font-size: 0.95rem;
            font-style: italic;
        '>
            Please choose a State from the options below to proceed with official data access and insights as per NCRB records.
        </p>
    </div>
        
</div>
""", unsafe_allow_html=True)
    


    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
    for i in range(0, len(states), 5):
        cols = st.columns(5)
        for idx, state in enumerate(states[i:i+5]):
            with cols[idx]:
                if st.button(state, key=state):
                    st.session_state.selected_state = state

    st.markdown(f"""
<style>
.gov-section {{
    border-left: 8px solid #002b5b;
    padding: 1.2rem 1.5rem;
    background: linear-gradient(90deg, #f9fafa, #f1f4f8);
    font-family: 'Georgia', serif;
    color: #002b5b;
    margin-top: 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,43,91,0.08);
    position: relative;
    border-radius: 6px;
}}

.gov-section:before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    height: 6px;
    width: 100%;
    background: linear-gradient(to right, #FF9933, white, #138808); /* Tricolor */
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}

.gov-section h2 {{
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}}

.gov-section p {{
    font-size: 0.95rem;
    color: #333;
    margin: 0.2rem 0 0;
    font-style: italic;
}}
</style>

<div class="gov-section">
    <h2><img src="data:image/png;base64,{india_outline_b64}" class="gov-icon">  Union Territories of India</h2>
    <p>{util.return_nbsp(3)}{util.return_nbsp(3)}{util.return_nbsp(3)}{util.return_nbsp(3)}Official listing as per Government of India records, Ministry of Home Affairs.</p>
    <div style='
        background-color: #e9ecef;
        padding: 1.2rem 1.5rem;
        border: 1px solid #c1c1c1;
        border-radius: 6px;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    '>
        <h4 style='
            margin: 0;
            color: #002b5b;
            font-weight: 700;
            font-family: "Georgia", serif;
            text-transform: uppercase;
            font-size: 1.2rem;
            letter-spacing: 0.5px;
        '>
            📍 Selection of Administrative Region for Data Exploration
        </h4>
        <p style='
            margin-top: 0.5rem;
            color: #333;
            font-size: 0.95rem;
            font-style: italic;
        '>
            Please choose a Union Territory from the options below to proceed with official data access and insights as per NCRB records.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    uts = [
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman & Diu",
        "Delhi", "Lakshadweep", "Puducherry"
    ]

    for i in range(0, len(uts), 4):
        cols = st.columns(4)
        for idx, ut in enumerate(uts[i:i+4]):
            with cols[idx]:
                if st.button(ut, key=ut):
                    st.session_state.selected_state = ut

    if st.session_state.selected_state:
        st.markdown(f"""
            <style>
                .modal {{
                    position: fixed;
                    z-index: 9999;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    overflow: auto;
                    background-color: rgba(0,0,0,0.45);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-family: 'Georgia', serif;
                }}

                .modal-content {{
                    background-color: #f9fafa; /* light gray-blue */
                    padding: 2rem 2.5rem;
                    border-left: 6px solid #002b5b; /* Navy Blue - Govt tone */
                    border-top: 4px solid #4d648d;
                    border-radius: 12px;
                    width: 92%;
                    max-width: 550px;
                    text-align: center;
                    color: #002b5b;
                    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
                }}

                .modal-content h4 {{
                    font-size: 1.2rem;
                    margin-bottom: 1rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}

                .modal-content p {{
                    font-size: 1rem;
                    margin: 0;
                    font-weight: 500;
                    color: #222;
                }}
            </style>

            <div class="modal">
                <div class="modal-content">
                    <span style='font-size: 0.95rem; font-weight: normal;'>
                        Proceeding to display official data and visual insights of
                        <strong>{st.session_state.selected_state}</strong>
                        region as per <strong>NCRB records</strong>.
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

        active_state = st.session_state.selected_state
        st.session_state.selected_state = None
        
        if active_state not in st.session_state:
            st.session_state[active_state] = False
        
        st.session_state["active_state"] = active_state
        st.session_state.proceed = False
        st.session_state["show_state_page"] = True

        st.rerun()
    

    
elif st.session_state.show_state_page:

    st.markdown('<a name="top"></a>', unsafe_allow_html=True)
    
    components.html("""
        <script>
            // Wait until full render + paint
            window.addEventListener('load', () => {
                const mainContent = window.parent.document.querySelector('.main');
                if (mainContent) {
                    setTimeout(() => {
                        anchor.scrollIntoView({ behavior: 'smooth' });
                    }, 300);  // Delay to ensure it scrolls after render
                }
            });
        </script>
    """, height=0)
    
    ncrb_logo_path = Path(os.getcwd()) / 'ncrb_logo.png'
    ncrb_logo_b64 = util.get_base64_image(ncrb_logo_path) if ncrb_logo_path.exists() else ""
    
    st.markdown("""
        <style>
        html, body, [data-testid="stApp"] {
            background-color: white !important;
        }
        section.main > div {
            background-color: white !important;
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    state = st.session_state.get("active_state", None)

    data_path = './Dataset/NCRB_2001_STATES.csv'
    rape_df = pd.read_csv(data_path)

    if st.session_state.show_state_page:
        state = st.session_state.get("active_state", None)
        if state:
            emblem_svg_path = Path(os.getcwd()) / 'india_emblem.svg'
            emblem_svg_b64 = util.get_base64_svg(emblem_svg_path) if emblem_svg_path.exists() else ""

            st.markdown(f"""
            <div style='text-align: center; margin-bottom: 1rem; margin-top: -3rem;'>
                <img src="data:image/svg+xml;base64,{emblem_svg_b64}" alt="Ashoka Emblem" width="80" style='margin-bottom: 0.5rem;' />
            </div>

            <h1 style='
                text-align: center;
                font-size: 2.8rem;
                font-weight: 900;
                color: #002b5b;
                margin-bottom: 0.2rem;
                text-transform: uppercase;
                font-family: "Segoe UI", sans-serif;
                letter-spacing: 1px;
            '>
                National <span style="color: maroon;">Rape</span> Data Analytical Insights
            </h1>

            <h3 style='
                text-align: center;
                font-size: 1.2rem;
                font-weight: 600;
                color: #3a3a3a;
                margin-bottom: 2rem;
                font-family: "Segoe UI", sans-serif;
                letter-spacing: 0.5px;
                line-height: 3rem;
            '>
                National Crime Records Bureau (NCRB)<br>
                <span style="font-weight: 500;">Under the Ministry of Home Affairs (गृह मंत्रालय), Government of India</span>
            </h3>

            """, unsafe_allow_html=True)
            st.markdown("""
            <p style='
                font-size: 1rem;
                color: #333;
                text-align: justify;
                line-height: 1.7;
                font-family: "Segoe UI", sans-serif;
                padding: 0 1rem;
            '>
                The <strong>National Crime Records Bureau (NCRB)</strong>, operating under the Ministry of Home Affairs, Government of India, is the country’s primary agency responsible for collecting, analyzing, and publishing data on crime and criminals. Established with the goal of enabling data-driven governance, the NCRB plays a crucial role in maintaining transparency, supporting law enforcement agencies, and facilitating research in criminology and policy-making. The data represented in this dashboard has been sourced from official NCRB annual reports, and reflects a serious, evidence-based attempt to highlight concerning trends—especially those related to crimes against women such as rape. While every effort has been made to ensure the accuracy and integrity of this data, it must be interpreted with the understanding that recorded cases represent only those reported to the authorities. Hence, the figures may not fully capture the prevalence or severity of the actual situation. This tool is intended solely for educational, analytical, and policy-informing purposes, and must be used with responsibility, empathy, and respect for the sensitivity of the issue.

            Each datapoint is a reflection of real lives impacted—an alarming reminder that safety, justice, and awareness are ongoing responsibilities. Let us collectively use this information not only to inform but to act, advocate, and reform where needed.
            </p>
            """, unsafe_allow_html=True)

            combined_year_data = analysis.load_all_ncrb_data('Dataset')

            st.markdown(f"""
            <div style='background-color:#002b5b;padding:1rem 1.5rem;border-radius:6px;margin-bottom:1rem'>
                <h2 style='color:white;margin:0;font-family:Segoe UI;'>NCRB Rape Case Statistics – {state.title()}</h2>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><img src="data:image/png+xml;base64,{ncrb_logo_b64}" alt="Ashoka Emblem" width="25" style='margin-bottom: 0.5rem;' />{util.return_nbsp(3)}Visual intelligence based on NCRB (2001–2011)</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Incest-Rape</b> : Offences committed by blood relatives, guardians, or close family members.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Non-Incest-Rape</b> : Offences committed by unrelated individuals, strangers, or acquaintances.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Total Rape Cases</b> : Computed as the sum of all reported Incest and Non-Incest rape incidents across all documented age groups.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Metrics</b> : The figures presented are based solely on officially registered cases. Unreported incidents, which may exist in significant numbers, are not reflected in this data.</p>
            </div>
            """, unsafe_allow_html=True)

            summary_df = analysis.get_total_summary_table_for_selected_state_only(combined_year_data, state)

            summary_df.columns = [
                "📅 Year",
                "👪 Incest Rape Cases",
                "🧍 Non-Incest Rape Cases",
                "📊 Total Rape Cases"
            ]

            styled_df = summary_df.style.set_properties(**{
                'text-align': 'left',
                'font-family': 'Segoe UI',
                'font-size': '14px'
            })

            st.markdown("""
                <style>
                .gov-wrapper {
                    max-width: 900px;
                    margin: 25px auto;
                    padding: 25px 30px;
                    background-color: #ffffff;
                    border: 1.5px solid #ccc;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.12);
                    font-family: 'Segoe UI', sans-serif;
                    color: #111;
                }
            
                .gov-header {
                    text-align: center;
                    margin-bottom: 15px;
                }
            
                .gov-header img {
                    width: 60px;
                    margin-bottom: 10px;
                }
            
                .gov-header h4 {
                    color: #002b5b;
                    font-size: 20px;
                    font-weight: 700;
                    margin: 0;
                }
            
                .gov-subtext {
                    text-align: center;
                    font-size: 13px;
                    color: #333;
                    margin-bottom: 15px;
                    font-style: italic;
                }
            
                .gov-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                }
            
                .gov-table th {
                    background-color: #1f2d3d;
                    color: #ffffff;
                    padding: 10px;
                    text-align: left;
                }
            
                .gov-table td {
                    padding: 8px 10px;
                    border: 1px solid #ccc;
                    color: #111;
                    background-color: #f9f9f9;
                }
            
                .gov-table tbody tr:nth-child(even) {
                    background-color: #eef3f7;
                }
            
                .gov-table tbody tr:hover {
                    background-color: #dde7f1;
                }
                </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="gov-wrapper">
                    <div class="gov-header">
                        <img src="data:image/svg+xml;base64,{emblem_svg_b64}" alt="Ashoka Emblem" width="60" />
                        <h4>Ministry of Home Affairs – NCRB Official Statistics</h4>
                    </div>
                    <div class="gov-subtext">
                        Rape Case Summary Report (2001–2011) – State: <strong>{state.title()}</strong>
                    </div>
                    {summary_df.to_html(classes="gov-table", index=False)}
                </div>
            """, unsafe_allow_html=True)

            summary_df = analysis.get_total_summary_table_for_selected_state_only(combined_year_data, state)

            summary_df.columns = [
                "📅 Year",
                "👪 Incest Rape Cases",
                "🧍 Non-Incest Rape Cases",
                "📊 Total Rape Cases"
            ]

            summary_text = analysis.generate_rape_trend_summary(summary_df, state)

            st.markdown(
                f"""
                <div style="
                    width: 100%;
                    text-align: center;
                    font-size: 13px;
                    font-style: italic;
                    color: #333;
                    margin-top: 6px;
                    font-family: 'Segoe UI', sans-serif;
                ">
                    {summary_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<br><br><br>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background-color:#002b5b;padding:1rem 1.5rem;border-radius:6px;margin-bottom:3rem'>
                <h2  style='color:white;margin:0;font-family:Segoe UI;'>Rape Case Timeline & Key Observations – {state.title()}</h2>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><img src="data:image/png+xml;base64,{ncrb_logo_b64}" alt="Ashoka Emblem" width="25" style='margin-bottom: 0.5rem;' />{util.return_nbsp(3)}Visual intelligence based on NCRB (2001–2011)</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Peak Year</b> : The year with the maximum number of reported rape cases, indicating a statistical high point in incident reporting.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Decline Phase</b> : A period marked by a notable drop in reported cases, often preceding a policy shift or socio-legal change.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Resurgence in Reports</b> : The phase where reporting began to increase again, reversing the earlier downward trend.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Overall Trend</b> : A summary of the direction of case progression over the decade, highlighting long-term movement (rise or fall).</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Policy Note:</b> : An analytical pointer suggesting that trends may align with changes in governance, awareness campaigns, or systemic reforms affecting reporting behavior.</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("""
                    <h1 style='
                        background-color:#f9f9f9;
                        padding: 0px 15px 15px 15px;
                        color: black;
                        font-family: "Segoe UI", sans-serif;
                        line-height: 1.6;
                        margin-top: -0.5rem;
                    '>
                    Plot Summary
                    </h1>
                """.format(state.title()), unsafe_allow_html=True)
                pyplot_summary = analysis.generate_detailed_insight(summary_df, state)
                st.markdown(f"""
                    <div style='
                        background-color:#f9f9f9;
                        padding: 15px;
                        border-left: 5px solid #002b5b;
                        color: black;
                        font-family: "Segoe UI", sans-serif;
                        font-size: 15px;
                        line-height: 1.6;
                    '>
                    {pyplot_summary}
                    </div>
                """.format(state.title()), unsafe_allow_html=True)

            with col2:
                fig = analysis.plot_interactive_rape_trend(combined_year_data, state)
                st.plotly_chart(fig, use_container_width=True)


            key_stats = analysis.get_key_stats(summary_df)

            with st.container():
                st.markdown("""
                    <h3 style='
                        color: #000;
                        '>
                        
                    </h3>
                """.format(state.title()), unsafe_allow_html=True)  
            
                col1, col2, col3, col4 = st.columns(4)
            
                def render_metric(col, label, value):
                    col.markdown(f"""
                        <div style='
                            background-color: #ffffff;
                            border: 1.8px solid #002b5b;
                            border-top: 6px solid #002b5b;
                            padding: 1rem 0.8rem;
                            border-radius: 6px;
                            text-align: center;
                            font-family: "Segoe UI", sans-serif;
                            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
                        '>
                            <div style='
                                color: #002b5b;
                                font-weight: 800;
                                font-size: 0.95rem;
                                text-transform: uppercase;
                                margin-bottom: 0.2rem;
                                letter-spacing: 0.4px;
                            '>
                                {label}
                            </div>
                            <div style='
                                color: #000000;
                                font-size: 1.45rem;
                                font-weight: 700;
                            '>
                                {value}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            
                render_metric(col1, "Peak Year", key_stats["Peak Year"])
                render_metric(col2, "Min Year", key_stats["Min Year"])
                render_metric(col3, "Trend", key_stats["Trend"])
                render_metric(col4, "% Change", key_stats["Percent Change"])

            st.markdown("<br><br><br>", unsafe_allow_html=True)
                
            st.markdown(f"""
            <div style='background-color:#002b5b;padding:1rem 1.5rem;border-radius:6px;margin-bottom:3rem'>
                <h2 style='color:white;margin:0;font-family:Segoe UI;'>Age-Specific Demographic Segmentation – {state.title()}</h2>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><img src="data:image/png+xml;base64,{ncrb_logo_b64}" alt="Ashoka Emblem" width="25" style='margin-bottom: 0.5rem;' />{util.return_nbsp(3)}Visual intelligence based on NCRB (2001–2011)</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Features</b> : Click use the 6-Shade checkboxes to include or exclude specific data groups from the visualization.</p>
            </div>
            """, unsafe_allow_html=True)
            

            st.markdown("""
            <style>
            /* All Tab Buttons */
            button[data-testid="stTab"] {
                all: unset;
                color: #002b5b !important;
                background-color: #f5f8fa !important;
                padding: 0.7rem 1.2rem !important;
                margin-right: 0.5rem;
                font-size: 15px;
                font-family: 'Segoe UI', sans-serif;
                border: none;
                border-bottom: 2px solid transparent;
                transition: all 0.3s ease;
                border-radius: 6px 6px 0 0;
            }

            /* Hover Effect */
            button[data-testid="stTab"]:hover {
                background-color: #e6eef3 !important;
                border-bottom: 2px solid #004080 !important;
                color: #003060 !important;
                cursor: pointer;
            }

            /* Active Tab */
            button[data-testid="stTab"][aria-selected="true"] {
                color: white !important;
                background-color: #002b5b !important;
                font-weight: 600 !important;
            }
            button[data-testid="stTab"][aria-selected="true"]:hover {
                cursor: default;
            }
            </style>
            """, unsafe_allow_html=True)
            
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Distribution", "Trends", "% Breakdown", "Under-Age v/s Adult", "Age Ratio Index", "Radar Based Age-Group v/s Year"])
            
            with tab1:
                components.html(
                    analysis.card_container("""
                        <h4 style="color:#002b5b; margin-bottom:0;">
                          Overall Age Group Distribution
                        </h4>
                        <p style="font-size:0.85rem; color:#444; margin-top:0.25rem;">
                          Pie and stacked bar chart showing absolute count distribution across age groups.
                        </p>
                    """, bg="#f9f9f9"),
                    height=130,
                    scrolling=False,
                )
                c1, c2 = st.columns(2)
                with c1:
                    fig = analysis.plot_age_group_distribution_pie(combined_year_data, state)
                    st.plotly_chart(fig, use_container_width=True)
            
                with c2:
                    fig = analysis.plot_interactive_age_distribution_per_year(combined_year_data, state)
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Age Group Trends Over Time</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.25rem;">Line chart tracking changes in victim counts per age group over the years.</p>
                    """, bg="#f9f9f9"),
                height=130,
                    scrolling=False,
                )
                fig = analysis.plot_age_group_trends_linechart(combined_year_data, state)
                st.plotly_chart(fig, use_container_width=True)

                summary_stats = analysis.generate_age_group_summary_stats(combined_year_data, state)

                rows = "".join([
                    f"""
                    <tr>
                        <td style='font-weight:500;color:#002b5b;font-size:0.95rem;font-family:Segoe UI;padding:0.5rem 1rem;border-bottom:1px solid #eee'>{k}</td>
                        <td style='font-weight:600;color:#000;font-size:0.95rem;font-family:Segoe UI;padding:0.5rem 1rem;border-bottom:1px solid #eee'>{v}</td>
                    </tr>
                    """ for k, v in summary_stats.items()
                ])

                st.markdown("""
                <div style='
                    background-color:#ffffff;
                    border-left:5px solid #dcdcdc;
                    border-right:5px solid #dcdcdc;
                    padding:1.5rem;
                    border-radius:10px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.06);
                    margin-top:0rem;
                    margin-bottom:2rem;
                '>
                
                <table style='width:100%;border-collapse:collapse'>
                <tr>
                    <td style='font-weight:500;color:#002b5b;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        Most Affected Age Group
                    </td>
                    <td style='font-weight:600;color:#000;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        18–30
                    </td>
                </tr>
                
                <tr>
                    <td style='font-weight:500;color:#002b5b;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        Least Affected Age Group
                    </td>
                    <td style='font-weight:600;color:#000;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        50+
                    </td>
                </tr>
                
                <tr>
                    <td style='font-weight:500;color:#002b5b;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        Year with Highest Underage Victims
                    </td>
                    <td style='font-weight:600;color:#000;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        2011
                    </td>
                </tr>
                
                <tr>
                    <td style='font-weight:500;color:#002b5b;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        Avg. Victims per Year in 18–30 Age
                    </td>
                    <td style='font-weight:600;color:#000;font-size:0.95rem;font-family:Segoe UI;
                        padding:0.5rem 1rem;border-bottom:1px solid #eee'>
                        30.73
                    </td>
                </tr>
                </table>
                
                </div>
                """, unsafe_allow_html=True)

            with tab3:
                components.html(
                    analysis.card_container("""
                    <h4 style="color:#002b5b;margin-bottom:0;">Percentage Distribution by Age Group (2001–2011)</h4>
                    <p style="font-size:0.85rem;color:#444;margin-top:0.25rem;">Table shows how age groups contributed in percentage terms to total cases each year.</p>
                """, bg="#f9f9f9"),
                height=130,
                    scrolling=False,
                )
                percentage_df = analysis.get_age_group_percentage_distribution_table(combined_year_data, state)
                styled_table_html = analysis.render_white_theme_percentage_table(percentage_df)
            
                components.html(
                    styled_table_html,
                    height=40 * len(percentage_df) + 100,
                    scrolling=True
                )
            
            with tab4:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Age Group Category (Under-Age, 18+) Trends Over Time</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.25rem;">
                        Visual comparison of yearly victim counts in underage (below 18) and adult (18+) age groups across the 2001–2011 period.
                        </p>
                    """, bg="#f9f9f9"),
                    height=130,
                    scrolling=False,
                )

                fig = analysis.plot_underage_vs_adult_bar_chart(combined_year_data, state)
                st.plotly_chart(fig, use_container_width=True)

            with tab5:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Age Ratio Index (Victims 18–30 vs. 0–18)</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">We compare victims aged <b>18–30</b> with those <b>under 18</b> because:</p>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">0–18: Minors protected under child safety laws (e.g., POCSO Act)</li>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">18–30: Young adults facing risks in workplaces, colleges, and society</li>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.25rem;">This ratio helps reveal whether the focus of crimes is shifting from children to adults over the years.</p>
                        <ul style="font-size:0.9rem; color:#444; margin-left:1rem; padding-left:1rem">
                          <li><b>Ratio > 1:</b> More adult victims than minors in that year</li>
                          <li><b>Ratio = 1:</b> Equal number of adult and minor victims</li>
                          <li><b>Ratio &lt; 1:</b> More minor victims than adult victims</li>
                        </ul>
                    """, bg="#f9f9f9"),
                    height=270,
                    scrolling=False,
                )

                fig = analysis.plot_age_ratio_index_per_year(combined_year_data, state)
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("<br><br><br>", unsafe_allow_html=True)
                
            with tab6:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Age-Wise Distribution per Year</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">We use a Radar Chart (also called a line polar plot) to visualize how different age groups of victims are affected each year from 2001 to 2011 in a circular format.</p>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">This helps users:</p>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">👁️ Visually compare age-wise impact across years in a compact, intuitive layout</li>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">📊 Identify peak victim age groups for a given year</li>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">📉 Spot sudden increases or decreases in specific age categories</li>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">🔄 Track shifting focus of crime trends across age demographics</li>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.25rem;">What to Look For:</p>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">A bulging section near a age group indicates increased victimization in those age groups.</li>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">A compressed or flat line on any segment shows lower victim counts in that age group for that year.</li>
                        <li style="font-size:0.85rem;color:#444;margin-top:0.25rem;">Crossing or diverging lines highlight shifting age-group vulnerability over the decade.</li>
                    """, bg="#f9f9f9"),
                    height=350,
                    scrolling=False,
                )

                fig = analysis.plot_radar_age_distribution_over_years(combined_year_data, state)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div style='background-color:#002b5b;padding:1rem 1.5rem;border-radius:6px;margin-bottom:3rem;margin-top:4rem'>
                <h2 style='color:white;margin:0;font-family:Segoe UI;'>Rape Category (Incest, Non-Incest) Analysis – {state.title()}</h2>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><img src="data:image/png+xml;base64,{ncrb_logo_b64}" alt="Ashoka Emblem" width="25" style='margin-bottom: 0.5rem;' />{util.return_nbsp(3)}Visual intelligence based on NCRB (2001–2011)</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Features</b> : Click use the 6-Shade checkboxes to include or exclude specific data groups from the visualization.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Incest-Rape</b> : Offences committed by blood relatives, guardians, or close family members.</p>
                <p style='color:#dcdcdc;margin:0.3rem 0 0;font-size:0.9rem'><b>ⓘ</b>{util.return_nbsp(3)}<b>Non-Incest-Rape</b> : Offences committed by unrelated individuals, strangers, or acquaintances.</p>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Bar Graph", "Line Graph", "Percentage Distribution", "Year-on-Year %", "Cumulative Figure", "Categorical Ratio", "Incidents Clustered", "Heatmap"])

            with tab1:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category Bar Graph</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">A Bar Graph demonstrating a clear magnitute and side by side comparison of Incest and Non0incest Rapes.</p>
                    """, bg="#f9f9f9"),
                    height=130,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_incest_vs_nonincest_per_year(combined_year_data, state), use_container_width=True)

            with tab2:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category Line Graph</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">A Line graph showing a clear visual of categories of rape with yearly timeline.</p>
                    """, bg="#f9f9f9"),
                    height=130,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_trend_line_incest_vs_nonincest(combined_year_data, state), use_container_width=True)
            
            with tab3:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category Pie Chart</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">A Pie Chart representing how the category based percentage distribution is there.</p>
                    """, bg="#f9f9f9"),
                    height=170,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_incest_nonincest_pie(combined_year_data, state), use_container_width=True)

            with tab4:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category YoY % Graph</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">Year-on-Year % change refers to the percentage difference in a value (e.g., total rape cases) when comparing one year to the previous year.</p>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.50rem;margin-bottom:0.25rem;">It helps identify trends—whether cases are increasing, decreasing, or remaining stable over time.</p>
                    """, bg="#f9f9f9"),
                    height=170,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_yoy_incest_nonincest_change(combined_year_data, state), use_container_width=True)
            
            with tab5:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category Cumulative Graph</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">Cumulative Incest and Cumulative Non-Incest represent the running total of respective rape cases over the years, helping track the overall growth or burden of each category from 2001 to 2011 for a selected state.</p>
                    """, bg="#f9f9f9"),
                    height=140,
                    scrolling=False,
                )

                fig1, fig2 = analysis.plot_separate_cumulative_charts(combined_year_data, state)
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(fig2, use_container_width=True)
                    
                with col2:
                    st.plotly_chart(fig1, use_container_width=True)

            with tab6:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category Category Based Ratio</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">We compare victims of <b>Incest Rape</b> with those <b>Non-Incest Rape</b> because this ratio helps reveal whether the focus of crimes is shifting from Incest to Non-Incest over the years.</p>
                        <ul style="font-size:0.9rem; color:#444; margin-left:1rem; padding-left:1rem">
                          <li><b>Ratio > 1:</b> More Non-Incest than Incest in that year</li>
                          <li><b>Ratio = 1:</b> Equal number of Non-Incest and Incest victims</li>
                          <li><b>Ratio &lt; 1:</b> More Incest than Non-Incest</li>
                        </ul>
                    """, bg="#f9f9f9"),
                    height=220,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_incest_ratio_per_year(combined_year_data, state), use_container_width=True)

            with tab7:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Clusters of <b>Low</b>, <b>Medium</b> and <b>High</b> Rape Incidents</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">Clustered Rape Incidence Strip Plot shows how individual rape incidents (incest and non-incest) are distributed across years and age groups.</p>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.5rem;margin-bottom:0.25rem;">Helps in identification of concentration patterns or outliers in victim demographics over time for a selected state.</p>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.5rem;margin-bottom:0.25rem;">It visually clusters repeated patterns and density, aiding in spotting age-specific vulnerability trends or anomalies.</p>
                    """, bg="#f9f9f9"),
                    height=200,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_rape_cluster_stripplot(combined_year_data, state), use_container_width=True)

            with tab8:
                components.html(  
                    analysis.card_container("""
                        <h4 style="color:#002b5b;margin-bottom:0;">Rape Category Based Heatmap</h4>
                        <p style="font-size:0.85rem;color:#444;margin-top:1.25rem;margin-bottom:0.25rem;">Heatmap (Incest vs Non-Incest by Age & Year) shows how rape cases are spread across different age groups over the years, separately for incest and non-incest types.</p>
                        <p style="font-size:0.85rem;color:#444;margin-top:0.5rem;margin-bottom:0.25rem;">Darker shades mean more victims, helping us spot which age groups were most affected in which years.</p>
                    """, bg="#f9f9f9"),
                    height=170,
                    scrolling=False,
                )

                st.plotly_chart(analysis.plot_heatmap_incest_vs_nonincest(combined_year_data, state), use_container_width=True)

            components.html("""
                <script>
                    setTimeout(function() {
                        const iframe = window.frameElement;
                        if(iframe) {
                            const doc = iframe.ownerDocument;
                            const anchor = doc.querySelector('a[name="top"]');
                            if(anchor) {
                                anchor.scrollIntoView({ behavior: 'smooth' });
                                console.log("✅ Scrolled to top anchor!");
                            } else {
                                console.log("❌ Anchor not found.");
                            }
                        } else {
                            console.log("❌ No iframe context.");
                        }
                    }, 600); // Delay for DOM to render
                </script>
            """, height=0)

            if st.button("← Back to State's/UT's Selection"):
                st.session_state.show_state_page = False
                st.session_state.proceed = True
                st.session_state.selected_state = None
                st.session_state["active_state"] = None
                st.session_state.scrolled_to_top = False
                st.rerun()