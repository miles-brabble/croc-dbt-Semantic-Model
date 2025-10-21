import streamlit as st
import subprocess
import pandas as pd
import io
import os

st.title("MetricFlow Explorer (local)")

# Sidebar inputs
st.sidebar.header("dbt paths")
project_dir = st.sidebar.text_input("DBT_PROJECT_DIR", value="/Users/fizban4/Desktop/Models/brabble_dbt/brabble_dbt")
profiles_dir = st.sidebar.text_input("DBT_PROFILES_DIR", value="/Users/fizban4/.dbt")

st.sidebar.header("Query")
metrics = st.sidebar.text_input("Metrics (space-separated)", value="total_observations average_length_m")
groups = st.sidebar.text_input("Group by (space-separated)", value="date_day species")
start_time = st.sidebar.text_input("Start time (YYYY-MM-DD)", value="2024-01-01")
end_time = st.sidebar.text_input("End time (YYYY-MM-DD)", value="2024-12-31")
limit = st.sidebar.number_input("Limit", value=100, step=10)
run = st.sidebar.button("Run query")

# Function to execute metricflow query
def run_metricflow_query():
    args = [
    "dbt-metricflow", "query",
    "--metrics", ",".join(metrics.split()),
    "--group-by", ",".join(groups.split()),
    "--start-time", start_time,
    "--end-time", end_time,
    "--limit", str(limit)
]

    env = os.environ.copy()
    env["DBT_PROJECT_DIR"] = project_dir
    env["DBT_PROFILES_DIR"] = profiles_dir

    result = subprocess.run(args, env=env, capture_output=True, text=True)
    return result.stdout, result.stderr

# Display results
if run:
    st.write("⏳ Initiating query...")
    out, err = run_metricflow_query()

    if err:
        st.error(f"MetricFlow CLI error:\n\n{err}")
    else:
        # Try to parse MetricFlow text table output
        try:
            # Find the first line that looks like a header (pipe-separated)
            lines = [l for l in out.splitlines() if "|" in l]
            if lines:
                # Clean up pipes and split into columns
                header = [h.strip() for h in lines[0].split("|") if h.strip()]
                data = [
                    [c.strip() for c in l.split("|") if c.strip()]
                    for l in lines[2:]
                    if "|" in l
                ]
                df = pd.DataFrame(data, columns=header)
                st.dataframe(df)
            else:
                st.text(out)
        except Exception as e:
            st.error(f"Could not parse output:\n\n{out}\n\n{e}")
