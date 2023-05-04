truncate table `poliquant.dwh.meeting_list`
;

insert into `poliquant.dwh.meeting_list`
select 
  unnest_meetingRecord.issueID
  ,unnest_meetingRecord.imageKind
  ,unnest_meetingRecord.searchObject
  ,unnest_meetingRecord.session
  ,unnest_meetingRecord.nameOfHouse
  ,unnest_meetingRecord.nameOfMeeting
  ,unnest_meetingRecord.issue
  ,unnest_meetingRecord.date
  ,unnest_meetingRecord.closing
  ,unnest_speechRecord.speechID
  ,unnest_speechRecord.speechOrder
  ,unnest_speechRecord.speaker
  ,unnest_speechRecord.speechURL
  ,unnest_meetingRecord.meetingURL
  ,unnest_meetingRecord.pdfURL
from `poliquant.source.meeting_list`, unnest(meetingRecord) as unnest_meetingRecord, unnest(speechRecord) as unnest_speechRecord
;