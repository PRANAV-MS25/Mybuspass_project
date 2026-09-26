from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, BusRoute, BusPassApplication


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    roll_number = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    year = forms.ChoiceField(choices=[(1,'1st Year'),(2,'2nd Year'),(3,'3rd Year'),(4,'4th Year')])
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        return username

    def clean_roll_number(self):
        roll = self.cleaned_data['roll_number']
        if StudentProfile.objects.filter(roll_number=roll).exists():
            raise forms.ValidationError('Roll number already registered.')
        return roll

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned


class BusPassApplicationForm(forms.ModelForm):
    class Meta:
        model = BusPassApplication
        fields = ['route', 'pickup_point', 'duration_months']
        widgets = {
            'route': forms.Select(attrs={'id': 'id_route'}),
            'pickup_point': forms.Select(attrs={'id': 'id_pickup'}),
            'duration_months': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route'].queryset = BusRoute.objects.filter(is_active=True)
        self.fields['pickup_point'] = forms.CharField(max_length=200)


class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ['route_number', 'route_name', 'pickup_points', 'start_time',
                  'end_time', 'distance_km', 'monthly_fee', 'is_active']
        widgets = {
            'pickup_points': forms.Textarea(attrs={'rows': 3,
                'placeholder': 'e.g., Main Gate, Library, Hostel Block A'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
