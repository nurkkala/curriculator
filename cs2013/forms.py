from django import forms

from .models import Course

class CourseCheckForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CourseCheckForm, self).__init__(*args, **kwargs)

        for course in Course.objects.all():
            self.fields[course.designation] = forms.BooleanField(label=course.designation)
