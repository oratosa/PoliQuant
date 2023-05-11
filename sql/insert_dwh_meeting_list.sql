truncate table `poliquant.dwh.meeting_list`
;

insert into `poliquant.dwh.meeting_list`
select 
  unnest_meetingRecord.issueID
  ,unnest_meetingRecord.imageKind
  ,cast(unnest_meetingRecord.searchObject as INT64)
  ,cast(unnest_meetingRecord.session as INT64)
  ,unnest_meetingRecord.nameOfHouse
  ,unnest_meetingRecord.nameOfMeeting
  ,unnest_meetingRecord.issue
  ,cast(unnest_meetingRecord.date as DATE FORMAT "YYYY-MM-DD")
  ,unnest_meetingRecord.closing
  ,unnest_speechRecord.speechID
  ,cast(unnest_speechRecord.speechOrder as INT64)
  ,unnest_speechRecord.speaker
  ,unnest_speechRecord.speechURL
  ,unnest_meetingRecord.meetingURL
  ,unnest_meetingRecord.pdfURL
from `poliquant.source.meeting_list`, unnest(meetingRecord) as unnest_meetingRecord, unnest(speechRecord) as unnest_speechRecord
;