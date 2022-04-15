from django import forms
from announce.models import Category_Announcement

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class WeeklyReportForm(forms.Form):
    #your_name = forms.CharField(label='報告者', max_length=100, )
    items_lastweek = forms.CharField(label='上周工作完成狀況', widget=forms.Textarea)
    items_comingweek = forms.CharField(label='本周預計工作項目', widget=forms.Textarea)
    others = forms.CharField(label='其他事項', widget=forms.Textarea)
    #sender = forms.EmailField()
    #cc_myself = forms.BooleanField(required=False)


class AnnouncementForm(forms.Form):
    announcementName = forms.CharField(label='公告名稱')
    category = forms.ModelChoiceField(label='公告類別', queryset=Category_Announcement.objects.all())
    description = forms.CharField(label='說明', widget= forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()