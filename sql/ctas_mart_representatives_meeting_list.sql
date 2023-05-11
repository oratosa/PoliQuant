drop table if exists `poliquant.mart.representatives_meeting_list`
;

create table `poliquant.mart.representatives_meeting_list` as
select 
  m.issue_id
  ,m.session
  ,m.name_of_house
  ,m.name_of_meeting
  ,m.issue
  ,m.date
  ,m.speech_id
  ,m.speech_order
  ,m.speaker
  ,r.profile_url
  ,r.party
  ,r.district
  ,r.elected_times
  ,m.speech_url
  ,m.meeting_url
  ,m.pdf_url
from 
  (select 
    issue_id
    ,session
    ,name_of_house
    ,name_of_meeting
    ,issue
    ,`date`
    ,speech_id
    ,speech_order
    ,speaker
    ,speech_url
    ,meeting_url
    ,pdf_url
  from `poliquant.dwh.meeting_list`
  where name_of_house = "衆議院" 
    and speaker != "会議録情報"
  ) as m
left join `poliquant.source.m_representatives` as r
  on  m.speaker = r.name
;