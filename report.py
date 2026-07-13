from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_report(df, insights):

    filename = "AI_Data_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI DATA ANALYST REPORT</b>", styles["Title"]))

    story.append(
        Paragraph(
            f"Generated on: {datetime.now()}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/><b>Dataset Summary</b>", styles["Heading2"]))

    story.append(
        Paragraph(f"Rows : {df.shape[0]}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Columns : {df.shape[1]}", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"Missing Values : {df.isnull().sum().sum()}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Duplicate Rows : {df.duplicated().sum()}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/><b>AI Insights</b>", styles["Heading2"]))

    for insight in insights:

        story.append(
            Paragraph(insight, styles["Normal"])
        )

    doc.build(story)

    return filename