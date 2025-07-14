# 📊 Indian Rape Data Analytics Dashboard (2001–2011)

This project is a **Streamlit-powered interactive analytics dashboard** built to present a **state-wise and age-segmented visualization of rape case statistics in India** between 2001 and 2011. It combines **data storytelling**, **in-depth trends**, and **insightful visualizations** to foster public awareness, academic research, and policy analysis.

---

## 🚀 Features

### 1. 📊 **State-wise Trends and Summary**

* Line charts showing **total rape trends** across years for a selected state/UT.
* **Automatic summary generation** for peak/low years, fluctuations, and net trends.
* Narrative-style insights with emojis for engaging storytelling.

### 2. 🔹 **Incest vs Non-Incest Case Analysis**

* **Grouped bar charts** to show case counts by category each year.
* **YoY percentage change** plot for both categories.
* **Trend line chart** and **pie chart** for total distribution.
* **Incest ratio line chart** for year-wise proportional analysis.
* **Cumulative area charts** for both case types.

### 3. 📊 **Victim Age Group Analysis**

* **Stacked bar chart** showing age group victim distribution per year.
* **Line graph** of age group trends across the decade.
* **Radar chart** to visualize year-on-year distribution for all age groups.
* **Underage (0–18) vs Adult (18+) comparison** via grouped bar chart.
* **Pie chart** for most affected age groups in selected state.
* **Percentage distribution table** of victims by age.

### 4. 📈 **Statistics and Summaries**

* **Narrative-based trend insights** including rise, fall, and recovery years.
* **Table-based insights** of age group ratios, averages, and distributions.
* **Highlight cards** for most/least affected age groups and underage severity.

### 5. 🌎 **Clustering and Patterns (Coming Soon)**

* Heatmaps and strip plots to **cluster states by trend behavior**.
* Visual tools to **detect abnormal outliers or sudden shifts** in patterns.

---

## 📝 Project Structure

```
.
├── app.py
├── utility.py
├── data/
│   └── rape_data_2001_2001.csv
│   └── ...
│   └── ...
│   └── ...
│   └── rape_data_2001_2011.csv
├── components/
│   ├── visuals.py
│   └── insights.py
├── styles/
│   └── white_theme.css
├── README.md
└── requirements.txt
```

---

## 📊 Dataset Overview

* **Source**: Government-published NCRB data (2001–2011)
* **Level**: State and Union Territory level
* **Breakdown**:

  * Total rape cases per year
  * Age-wise victim categorization
  * Incest vs Non-Incest tagging
  * Derived columns: Cumulative, YoY %, Ratios

---

## 🚀 Getting Started

### 🔧 Installation

```bash
pip install -r requirements.txt
```

### 🌐 Launch the App

```bash
streamlit run app.py
```

---

## 📊 Visualizations Used

* **Plotly Express + Graph Objects** for interactive charts.
* **Seaborn + Matplotlib** for exploratory visuals (backend).
* **HTML-styled tables** for percentage summaries.

---

## 🕵️ Intended Users

* **Policy Analysts**: Understand regional and demographic impact.
* **Researchers/Academics**: Use structured data for ML/NLP.
* **Journalists & Activists**: Present fact-based evidence and stories.
* **General Public**: Create awareness and data transparency.

---

## 🚀 Future Scope

* Add **clustering insights** using K-Means/DBSCAN.
* Build **forecasting modules** using Time Series methods (ARIMA, Prophet).
* Enable **national vs state comparisons**.
* Create **PDF/PNG export** of reports.

---

## 📖 License & Credits

* This project is open-sourced for **educational, ethical, and awareness purposes**.
* Data is obtained from **NCRB Government sources**.

---

## ✨ Author

**Rayyan Ashraf**
B.Tech CSE Final Year | Aspiring IIT-B M.Tech (DS/AI)
Building data systems that serve **social justice and national awareness**.

Connect: [LinkedIn](https://www.linkedin.com/in/rayyan-ashraf/) | [Email](mailto:ryshashraf@gmail.com)
