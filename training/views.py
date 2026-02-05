from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from .models import CourseEnrollment

def training_home(request):
    return render(request, "training/training.html")

def download_certificate(request, enrollment_id):
    enrollment = get_object_or_404(
        CourseEnrollment,
        id=enrollment_id,
        user=request.user,
        completed=True
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(300, 750, "Certificate of Completion")

    p.setFont("Helvetica", 16)
    p.drawCentredString(
        300, 680,
        f"This certifies that {enrollment.user.get_full_name() or enrollment.user.username}"
    )

    p.drawCentredString(
        300, 640,
        f"has successfully completed the course"
    )

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(
        300, 600,
        enrollment.course.title
    )

    p.setFont("Helvetica", 12)
    p.drawCentredString(
        300, 540,
        f"Date: {enrollment.completed_on}"
    )

    p.showPage()
    p.save()

    return response

