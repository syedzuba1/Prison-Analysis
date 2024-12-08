from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

class EconomicImpactForm(forms.Form):
    age = forms.FloatField(label="Age (From 1 to 60)")
    gender = forms.CharField(label="Gender (Male or Female)")


class AdaptationPredictionForm(forms.Form):
    total_education_facilities = forms.FloatField(label="Total Education Facilities")
    escapee_rate = forms.FloatField(label="Escapee Rate (From 0 to 1)")
    mental_illness_rate = forms.FloatField(label="Mental Illness Rate (From 0 to 1)")

class CrimePredictionForm(forms.Form):
    state = forms.CharField(label="State")
    crime_type = forms.CharField(label="Crime Type (Choose from the graph)")

class BudgetPredictionForm(forms.Form):
    STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Delhi', 'Delhi'),
    ('Puducherry', 'Puducherry'),
]
    #YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, 2014)]
    state_ut = forms.ChoiceField(
        label='State/UT',
        choices=[('', 'Select a State/UT')] + STATE_CHOICES,
        required=True
    )
    #state_ut = forms.CharField(label='State/UT')
    year = forms.IntegerField(label='Base Year', min_value=2000, max_value=2030)
   # num_years = forms.IntegerField(label='Number of Years to Predict')

    

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User  # Default User model

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True, help_text="Enter your age.")  # Add age field

    class Meta:
        model = User  # Default User model
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for the username field
        self.fields['username'].help_text = None
        # Add placeholder for better UX (Optional)
        self.fields['username'].widget.attrs['placeholder'] = "Choose a unique username"

    def save(self, commit=True):
        # Save the user instance
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Ensure UserProfile exists or create one
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.age = self.cleaned_data['age']
            user_profile.save()

        return user


class CustomUserChangeForm(UserChangeForm):
    age = forms.IntegerField(
        required=True,
        help_text=None,  # Remove help text entirely
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your age'})  # Add placeholder for better UX
    )

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email', 'age']  # Include only necessary fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the password field
        if 'password' in self.fields:
            del self.fields['password']  # Exclude password from the form

        # Customize the username field to remove help text
       # self.fields['username'].help_text = None  # Remove the help text for username
       # self.fields['username'].widget.attrs['placeholder'] = "Enter your username"

        # Customize labels for better UX
        #self.fields['username'].label = "Username"
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email Address"
        self.fields['age'].label = "Age"

        # Initially hide errors by overriding widget classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """Custom clean method to ensure validation errors are displayed on save."""
        cleaned_data = super().clean()

        # Iterate over all fields to check for missing or invalid input
        for field_name in self.fields:
            if field_name not in cleaned_data or not cleaned_data[field_name]:
                self.add_error(field_name, f"{self.fields[field_name].label} is required.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)  # Save User instance without committing yet
        if commit:
            user.save()
            # Update the age in UserProfile
            if hasattr(user, 'userprofile'):  # Ensure UserProfile exists
                user.userprofile.age = self.cleaned_data.get('age', user.userprofile.age)
                user.userprofile.save()
        return user