"""
Email Service for sending notifications via SendGrid
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)



# Import Student model for bulk email sending
from .models import Student

def send_result_published_email(student, result, attempt):
    """
    Send email notification when exam result is published
    
    Args:
        student: Student instance
        result: Result instance
        attempt: StudentExamAttempt instance
    """
    try:
        subject = f"Exam Result Published - {attempt.exam_paper.title}"
        
        # Create HTML message
        html_message = f"""
        <html>
        <body>
            <h2>Dear {student.name},</h2>
            <p>Your exam result for <strong>{attempt.exam_paper.title}</strong> ({attempt.exam_paper.subject}) has been published.</p>
            
            <h3>Result Summary:</h3>
            <ul>
                <li><strong>Total Marks:</strong> {result.total_marks}</li>
                <li><strong>Marks Obtained:</strong> {result.marks_obtained}</li>
                <li><strong>Percentage:</strong> {result.percentage}%</li>
                <li><strong>Grade:</strong> {result.grade}</li>
            </ul>
            
            {f'<p><strong>Remarks:</strong> {result.remarks}</p>' if result.remarks else ''}
            
            <p>Please login to your dashboard to view detailed results.</p>
            
            <p>Best regards,<br>
            Exam Proctoring Team</p>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Result published email sent to {student.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send result email to {student.email}: {str(e)}")
        return False


def send_approval_email(student, approved_by):
    """
    Send email notification when student account is approved
    
    Args:
        student: Student instance
        approved_by: User who approved the account
    """
    try:
        subject = "Account Approved - Online Exam Proctoring System"
        
        html_message = f"""
        <html>
        <body>
            <h2>Dear {student.name},</h2>
            <p>Congratulations! Your account has been <strong>approved</strong>.</p>
            
            <p>You can now login and access available exams.</p>
            
            <h3>Account Details:</h3>
            <ul>
                <li><strong>Name:</strong> {student.name}</li>
                <li><strong>Email:</strong> {student.email}</li>
                <li><strong>Status:</strong> Approved</li>
            </ul>
            
            <p>Please login to your dashboard to view available exams.</p>
            
            <p>Best regards,<br>
            Exam Proctoring Team</p>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Approval email sent to {student.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send approval email to {student.email}: {str(e)}")
        return False


def send_rejection_email(student, rejection_reason=None):
    """
    Send email notification when student account is rejected
    
    Args:
        student: Student instance
        rejection_reason: Optional reason for rejection
    """
    try:
        subject = "Account Status - Online Exam Proctoring System"
        
        html_message = f"""
        <html>
        <body>
            <h2>Dear {student.name},</h2>
            <p>We regret to inform you that your account registration could not be approved at this time.</p>
            
            {f'<p><strong>Reason:</strong> {rejection_reason}</p>' if rejection_reason else ''}
            
            <p>If you believe this is an error or need further assistance, please contact the administration.</p>
            
            <p>Best regards,<br>
            Exam Proctoring Team</p>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Rejection email sent to {student.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send rejection email to {student.email}: {str(e)}")
        return False




def send_exam_published_email(student, exam_paper):
    """
    Send email notification when a new exam is published
    
    Args:
        student: Student instance
        exam_paper: ExamPaper instance
    """
    try:
        from django.utils import timezone
        
        # Format the exam date and time
        exam_datetime = exam_paper.exam_date.strftime('%d %B %Y at %I:%M %p')
        
        # Calculate when exam will close
        exam_end_time = exam_paper.exam_date + timezone.timedelta(minutes=exam_paper.duration_minutes)
        exam_end_datetime = exam_end_time.strftime('%I:%M %p')
        
        subject = f"New Exam Published - {exam_paper.title}"
        
        html_message = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .exam-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #6366f1; }}
                .detail-row {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #6366f1; }}
                .value {{ color: #333; }}
                .warning {{ background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0; }}
                .button {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 14px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0; font-size: 28px;">📚 New Exam Published!</h1>
                </div>
                <div class="content">
                    <h2 style="color: #333;">Dear {student.name},</h2>
                    <p style="font-size: 16px;">A new exam has been published and is now available for you to take.</p>
                    
                    <div class="exam-details">
                        <h3 style="margin-top: 0; color: #6366f1;">📝 Exam Details</h3>
                        <div class="detail-row">
                            <span class="label">Exam Title:</span>
                            <span class="value">{exam_paper.title}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Subject:</span>
                            <span class="value">{exam_paper.subject}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">📅 Exam Date & Time:</span>
                            <span class="value" style="font-size: 18px; font-weight: bold; color: #10b981;">{exam_datetime}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">⏱️ Duration:</span>
                            <span class="value">{exam_paper.duration_minutes} minutes (Ends at {exam_end_datetime})</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Total Marks:</span>
                            <span class="value">{exam_paper.total_marks}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Passing Marks:</span>
                            <span class="value">{exam_paper.passing_marks}</span>
                        </div>
                    </div>
                    
                    {f'<div class="warning"><strong>📋 Instructions:</strong><br>{exam_paper.instructions}</div>' if exam_paper.instructions else ''}
                    
                    <div class="warning">
                        <strong>⚠️ Important Reminders:</strong>
                        <ul style="margin: 10px 0;">
                            <li>Please login at least 10 minutes before the scheduled time</li>
                            <li>Ensure you have a stable internet connection</li>
                            <li>Keep your camera ON throughout the exam (AI Proctoring Active)</li>
                            <li>Do not switch tabs or leave the exam window</li>
                            <li>Make sure your face is clearly visible in good lighting</li>
                        </ul>
                    </div>
                    
                    <center>
                        <a href="#" class="button" style="color: white;">Login to Dashboard</a>
                    </center>
                    
                    <div class="footer">
                        <p>Good luck with your exam! 🎓</p>
                        <p style="margin: 5px 0;">Best regards,<br><strong>Exam Proctoring Team</strong></p>
                        <p style="font-size: 12px; color: #999; margin-top: 20px;">This is an automated notification. Please do not reply to this email.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Exam published email sent to {student.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send exam published email to {student.email}: {str(e)}")
        return False


def send_exam_published_bulk(exam_paper):
    """
    Send exam published notification to all approved students
    
    Args:
        exam_paper: ExamPaper instance
    
    Returns:
        dict: Statistics of email sending (success_count, failed_count, total_count)
    """
    try:
        # Get all approved students
        approved_students = Student.objects.filter(approval_status='approved')
        
        success_count = 0
        failed_count = 0
        total_count = approved_students.count()
        
        for student in approved_students:
            if send_exam_published_email(student, exam_paper):
                success_count += 1
            else:
                failed_count += 1
        
        logger.info(f"Bulk exam notification sent: {success_count}/{total_count} successful")
        
        return {
            'success_count': success_count,
            'failed_count': failed_count,
            'total_count': total_count
        }
        
    except Exception as e:
        logger.error(f"Failed to send bulk exam notifications: {str(e)}")
        return {
            'success_count': 0,
            'failed_count': 0,
            'total_count': 0
        }