from typing import List

def events_field_data(events:List[dict]):

    events_fields_data=[]
    for event in events:
        events_fields_data.append(
                [
                    ["Field", "Value"],
                    ["Event Name", event['event_name']],
                    ["Date", event['event_date']],
                    ["Start Time", event['event_start_at']],
                    ["End Time", event['event_end_at']],
                    ["Description", event['event_description']],
                    ["Client Name", event['client_name']],
                    ["City", event['client_city']],
                    ["Mobile Number", event['client_mobile_number']],
                    ["Added By", event.get('event_added_by', 'N/A')],
                    ["Updated By", event.get('updated_by', 'N/A')],
                    ["Feedback",event.get('feedback', 'N/A')],
                    ["Archagar", event.get('archagar', 'N/A')],
                    ["Abisegam", event.get('abisegam', 'N/A')],
                    ["Helper", event.get('helper', 'N/A')],
                    ["Poo", event.get('poo', 'N/A')],
                    ["Read", event.get('read', 'N/A')],
                    ["Prepare", event.get('prepare', 'N/A')],
                    ["Updated Date", event.get('updated_date', 'N/A')],
                    ["Updated At", event.get('updated_at', 'N/A')],
                    ["Payment Status", event['payment_status'].value],
                    ["Payment Mode", event['payment_mode'].value],
                    ["Total Amount", event['total_amount']],
                    ["Paid Amount", event['paid_amount']],
                    ["Event Status", event['event_status'].value],
                    ["Neivethiyam Name", event["neivethiyam_name"]],
                    ["Neivethiyam Amount",event["neivethiyam_amount"]]
                ]
        )
    return events_fields_data


def workers_fields_data(workers:List[dict],amount:int):
    wrk_fields_data=[]
    for worker in workers:

        print(worker)
        wrk_fields_data.append(
        [
            ["Field", "Value"],
            ["Worker Name", worker['name']],
            ["Mobile Number",worker['mobile_number']],
            ["No of Participated Events", worker['no_of_participated_events']],
            ["Amount", amount],
            ["Total Amount", worker['total_amount']],
        ]
        )
    
    return wrk_fields_data