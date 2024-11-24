from celery import shared_task
from .models import CoursePopularity

@shared_task
def update_course_popularity(course_id):
    course = CoursePopularity.objects.get(course_id=course_id)
    course.views += 1
    course.save()
