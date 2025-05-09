from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register Tamil font
pdfmetrics.registerFont(TTFont('NotoSansTamil', 'assets/fonts/NotoSansTamil-Regular.ttf'))

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from fastapi.exceptions import HTTPException

async def generate_pdf(events_data) -> bytes:
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        for event in events_data:
            title = Paragraph("<b>Event Report</b>", styles["Title"])
            elements.append(title)
            elements.append(Spacer(1, 12))

            data = [
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
                ["Feedback",event.get('feedback', 'N/A')]
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

            table = Table(data, colWidths=[180, 320], hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff7043')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 16),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffe0b2')),
                ('GRID', (0, 0), (-1, -1), 0.75, colors.grey),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'NotoSansTamil'),
                ('FONTSIZE', (0, 1), (-1, -1), 14),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))

            elements.append(table)

            if event.get("image"):
                try:
                    image_stream = BytesIO(event["image"])
                    img = Image(image_stream, width=500, height=400)
                    elements.append(Spacer(1, 10))
                    elements.append(img)
                except Exception as e:
                    elements.append(Paragraph(f"Image error: {e}", styles["Normal"]))

            elements.append(Spacer(1, 20))
            elements.append(PageBreak())

        doc.build(elements)
        buffer.seek(0)
        return buffer.read()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while generating PDF: {e}"
        )
