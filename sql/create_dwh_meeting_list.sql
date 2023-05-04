drop table if exists `poliquant.dwh.meeting_list`
;
CREATE TABLE `poliquant.dwh.meeting_list`
(
  issue_id STRING,
  image_kind STRING,
  search_object INT64,
  session INT64,
  name_of_house STRING,
  name_of_meeting STRING,
  issue STRING,
  date DATE,
  closing STRING,
  speech_id STRING,
  speech_order INT64,
  speaker STRING,
  speech_url STRING,
  meeting_url STRING,
  pdf_url STRING
)
;