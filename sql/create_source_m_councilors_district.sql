create table if not exists poliquant.source.m_councilors_district
(
  id string options(description="The code of '小選挙区' in type column follows the rule of JIS X 0401. In addition, the number 99 means '比例' in type column."),
  district string options(description="This column includes prefectures and areas."),
  type string options(description="There are 2 types like '小選挙区', '比例'.")
)
;
