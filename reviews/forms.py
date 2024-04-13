from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    description = forms.CharField(required=False, label='Комментарий', widget=forms.Textarea(attrs={"class":"form-control",
                                                                                                    'placeholder': 'Впечатления, пожелания, проблемы',
                                                                                                    'rows': 5}))
    rating = forms.ChoiceField(label='choises', widget=forms.RadioSelect(),
                               choices={'5': 5, '4': 4, '3': 3, '2': 2, '1': 1},
                               error_messages={"required": "Оставьте рейтинг"}, )

    class Meta:
        model = Review
        fields = ['description', 'rating']