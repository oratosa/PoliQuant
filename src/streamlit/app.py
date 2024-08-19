import streamlit as st
from google.cloud import bigquery

# Streamlitのヘッダーを設定
st.title("発言を伴う会議出席回数")

# BigQueryクライアントを作成
client = bigquery.Client()

# クエリを記述
query = """
SELECT 
  district
  ,district_detail
  ,name
  ,party
  ,elected_times
  ,array_agg(num_of_attendance order by session) as num_of_attendance
  ,profile_url
FROM `poliquant.mart.m_representatives_aggregated` 
where name_of_house = "衆議院" or name_of_house is null
group by
  name
  ,party
  ,district_id
  ,district
  ,district_detail
  ,elected_times
  ,profile_url
order by district_id, district_detail, party, name
;
"""

# クエリの結果を取得
query_job = client.query(query)
df = query_job.to_dataframe()

selected_values = st.selectbox(
    label="選挙区",
    options=df["district"].unique(),
    index=0,
    placeholder="選挙区を選んでください",
    label_visibility="hidden",
)

filtered_df = df[df["district"] == selected_values]

st.dataframe(
    filtered_df,
    column_config={
        "district": "選挙区",
        "district_detail": st.column_config.NumberColumn("選挙区詳細"),
        "name": "議員名",
        "party": "政党",
        "elected_times": st.column_config.NumberColumn("当選回数"),
        "num_of_attendance": st.column_config.LineChartColumn(
            "発言を行った会議出席回数（会期別）", y_min=0, y_max=30
        ),
        "profile_url": st.column_config.LinkColumn("プロファイル"),
    },
    hide_index=True,
)
