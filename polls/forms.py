from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class WeeklyReportForm(forms.Form):
    your_name = forms.CharField(label='本周預計工作項目', max_length=200)
