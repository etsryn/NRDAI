import os
import base64
import pandas as pd
import streamlit.components.v1 as components

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def get_base64_svg(path):
    with open(path, "r", encoding="utf-8") as svg_file:
        svg_content = svg_file.read()
        return base64.b64encode(svg_content.encode("utf-8")).decode()

def return_nbsp(count):
    return "&nbsp;" * count

def load_all_state_data(folder_path="data"):
    combined_data = []
    for year in range(2001, 2012):
        file_path = os.path.join(folder_path, f"NCRB_{year}_STATES.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['Year'] = year
            combined_data.append(df)
    return pd.concat(combined_data, ignore_index=True)

def load_all_ut_data(folder_path="data"):
    combined_data = []
    for year in range(2001, 2012):
        file_path = os.path.join(folder_path, f"NCRB_{year}_UTs.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['Year'] = year
            combined_data.append(df)
    return pd.concat(combined_data, ignore_index=True)

def get_region_data(df, region_name):
    return df[df['States'] == region_name].copy()


def scroll_to_top():
    components.html(
        """
        <script>
        window.addEventListener('load', function() {
            window.scrollTo(0, 0);
        });
        </script>
        """,
        height=0,
    )