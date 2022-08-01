from django import forms
Medium=[
    ("online","online"),
    ("offline","offline")
]
class register_as_tutor(forms.Form):
    topic=forms.CharField()
    entryprice=forms.IntegerField()
    medium=forms.RadioSelect(choices=Medium)
    duration=forms.DateTimeField()
    maximum_enroll=forms.IntegerField()
    description=forms.Textarea()
   