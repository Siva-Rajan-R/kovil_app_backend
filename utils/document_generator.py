from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from fastapi.exceptions import HTTPException

async def generate_pdf(events_data, output_file='events_report.pdf'):
    try:
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        for event in events_data:
            elements.append(Paragraph(f"<b>Event:</b> {event['event_name']}", styles["Heading2"]))
            elements.append(Paragraph(f"<b>Date:</b> {event['event_date']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Time:</b> {event['event_start_at']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Description:</b> {event['event_description']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Client:</b> {event['client_name']} ({event['client_city']})", styles["Normal"]))
            elements.append(Paragraph(f"<b>Mobile:</b> {event['client_mobile_number']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Payment:</b> {event['payment_status']} - {event['payment_mode']} ({event['paid_amount']}/{event['total_amount']})", styles["Normal"]))
            elements.append(Paragraph(f"<b>Status:</b> {event['event_status']}", styles["Normal"]))

            # Binary image from DB
            if event.get("image"):
                if event['image']!="":
                    try:
                        image_stream = BytesIO(event["image"])
                        img = Image(image_stream, width=200, height=150)
                        elements.append(Spacer(1, 10))
                        elements.append(img)
                    except Exception as e:
                        elements.append(Paragraph(f"Image could not be loaded: {e}", styles["Normal"]))

            elements.append(Spacer(1, 20))
            elements.append(PageBreak())

        doc.build(elements)
        print(f"✅ PDF saved to: {output_file}")
        return True
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while generating pdf {e}"
        )


