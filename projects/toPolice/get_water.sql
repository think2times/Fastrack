select
r.card_id,
r.reading,
r.read_state,
r.read_state_cn,
r.last_read_water,
r.last_reading,
r.last_read_state,
r.last_read_state_cn,
to_char(r.last_read_date, 'yyyy-mm-dd') last_read_date,
r.billing_month,
to_char(r.read_date, 'yyyy-mm-dd') read_date,
cu1.user_name meter_reader,
cu2.user_name record_entry_person,
to_char(r.record_entry_time, 'yyyy-mm-dd') record_entry_time,
r.record_method,
r.record_type,
r.read_water,
r.avg_water_3,
r.avg_water_6,
r.avg_water_12,
r.record_remark,
cu3.user_name check_person,
to_char(r.check_time, 'yyyy-mm-dd') check_time,
cu4.user_name modifier_id,
to_char(r.modify_time, 'yyyy-mm-dd') modify_time
from csm.mr_record r
LEFT JOIN csm.csm_users cu1 ON r.meter_reader = cu1.user_id
LEFT JOIN csm.csm_users cu2 ON r.record_entry_person = cu2.user_id
LEFT JOIN csm.csm_users cu3 ON r.check_person = cu3.user_id
LEFT JOIN csm.csm_users cu4 ON r.modifier_id = cu4.user_id
WHERE r.subcom_code IN ('011', '021', '031', '032', '041', '051', '061', '062')
      AND r.check_time >= SYSDATE-1
      AND r.check_time < SYSDATE