from django import forms
from weeklyReport.models import Customer

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class WeeklyReportForm(forms.Form):
    #your_name = forms.CharField(label='報告者', max_length=100, )
    items_lastweek = forms.CharField(label='上周工作完成狀況', widget=forms.Textarea)
    items_comingweek = forms.CharField(label='本周預計工作項目', widget=forms.Textarea)
    others = forms.CharField(label='其他事項', widget=forms.Textarea)
    #sender = forms.EmailField()
    #cc_myself = forms.BooleanField(required=False)


class TaskForm(forms.Form):
    customers= (("1", "泉創"), \
               ("2","日月光"), \
               ("3","眾福"), ('4', '盛齊'))
    taskName = forms.CharField(label='任務名稱')
    description = forms.CharField(label='說明', widget= forms.Textarea)
    customer = forms.ModelChoiceField(label='相關客戶', queryset=Customer.objects.all())
    progress = forms.IntegerField(label='進度(0~100%)', initial=1, label_suffix='%')


    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        #customerset =
        #self.fields['customer'] = forms.ModelChoiceField(queryset = customerset)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()