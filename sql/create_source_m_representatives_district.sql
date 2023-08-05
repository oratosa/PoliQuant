drop table if exists poliquant.source.m_representatives_district
;

create table if not exists poliquant.source.m_representatives_district
(
  id INT64 options(description="IDs doesn't follow the rule of JIS X 0401."),
  district string options(description="This column includes prefectures and areas."),
  type string options(description="There are 2 types like '小選挙区', '比例'.")
)
;


