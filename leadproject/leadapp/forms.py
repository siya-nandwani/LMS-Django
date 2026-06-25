

from django import forms
from .models import Product, Region, ProductCategory , Lead , Territory , LeadStatus,LeadSource
import re
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
class ProductForm(forms.ModelForm):

    categoryid = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        empty_label="Select Category"
    )

    IS_ACTIVE_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive')
    ]

    is_active = forms.ChoiceField(
        choices=IS_ACTIVE_CHOICES
    )

    class Meta:
        model = Product
        fields = [ 'productname', 'categoryid', 'is_active']

class ProductExcelUploadForm(forms.Form):

    excel_file = forms.FileField(
        label="Upload Excel File"
    )

class RegionForm(forms.ModelForm):

    regionname = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label="Select Region"
    )

    class Meta:
        model = Region
        fields = ['regionname']

class LeadForm(forms.ModelForm):
    STATE_CHOICES = [
        ('', 'Select State'),

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
        ('Dadra and Nagar Haveli and Daman and Diu',
        'Dadra and Nagar Haveli and Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Ladakh', 'Ladakh'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Puducherry', 'Puducherry')
    ]


    CITY_CHOICES = [
        ('', 'Select City'),

        ('Ahmedabad', 'Ahmedabad'),
        ('Amritsar', 'Amritsar'),
        ('Bengaluru', 'Bengaluru'),
        ('Bhopal', 'Bhopal'),
        ('Chandigarh', 'Chandigarh'),
        ('Chennai', 'Chennai'),
        ('Coimbatore', 'Coimbatore'),
        ('Dehradun', 'Dehradun'),
        ('Delhi', 'Delhi'),
        ('Faridabad', 'Faridabad'),
        ('Ghaziabad', 'Ghaziabad'),
        ('Gurugram', 'Gurugram'),
        ('Hyderabad', 'Hyderabad'),
        ('Indore', 'Indore'),
        ('Jaipur', 'Jaipur'),
        ('Jalandhar', 'Jalandhar'),
        ('Jammu', 'Jammu'),
        ('Kanpur', 'Kanpur'),
        ('Kochi', 'Kochi'),
        ('Kolkata', 'Kolkata'),
        ('Lucknow', 'Lucknow'),
        ('Ludhiana', 'Ludhiana'),
        ('Mumbai', 'Mumbai'),
        ('Mysuru', 'Mysuru'),
        ('Nagpur', 'Nagpur'),
        ('Noida', 'Noida'),
        ('Panipat', 'Panipat'),
        ('Patna', 'Patna'),
        ('Pune', 'Pune'),
        ('Raipur', 'Raipur'),
        ('Ranchi', 'Ranchi'),
        ('Shimla', 'Shimla'),
        ('Surat', 'Surat'),
        ('Thane', 'Thane'),
        ('Vadodara', 'Vadodara'),
        ('Varanasi', 'Varanasi'),
        ('Visakhapatnam', 'Visakhapatnam')
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    state = forms.ChoiceField(choices=STATE_CHOICES)
    city = forms.ChoiceField(choices=CITY_CHOICES)
    
    productid = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Select Product"
    )

    regionid = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label="Select Region"
    )
    territoryid = forms.ModelChoiceField(
        queryset=Territory.objects.all(),
        empty_label="Select Territory"
    )

    statusid = forms.ModelChoiceField(
        queryset=LeadStatus.objects.all(),
        empty_label="Select Status"
    )

    leadsourceid = forms.ModelChoiceField(
        queryset=LeadSource.objects.all(),
        empty_label="Select Lead Source"
    )
    class Meta:
        model = Lead

        exclude = [
            'leadid',
            'added_by',
            'added_dts'
        ]

    def clean_personname(self):
        name = self.cleaned_data['personname']

        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError(
                "Name should contain only letters and spaces."
            )

        return name

    def clean_contactno(self):
        contact = str(self.cleaned_data['contactno'])

        if not contact.isdigit():
            raise forms.ValidationError(
                "Contact number must contain only digits."
            )

        if len(contact) != 10:
            raise forms.ValidationError(
                "Contact number must be 10 digits."
            )

        return contact

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(
                "Email is required"
            )

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, email):
            raise forms.ValidationError(
                "Enter a valid email address"
            )

        return email

    def clean_city(self):
        city = self.cleaned_data['city']

        if not re.match(r'^[A-Za-z ]+$', city):
            raise forms.ValidationError(
                "City should contain only letters."
            )

        return city

    def clean_state(self):
        state = self.cleaned_data['state']

        if not re.match(r'^[A-Za-z ]+$', state):
            raise forms.ValidationError(
                "State should contain only letters."
            )

        return state

    def clean_companyname(self):
        companyname = self.cleaned_data.get('companyname')

        if not companyname:
            raise forms.ValidationError(
                "Company name is required"
            )

        if not re.match(r'^[A-Za-z0-9 ]+$', companyname):
            raise forms.ValidationError(
                "Company name should contain only letters and numbers"
            )

        return companyname


    def clean_executiveid(self):
        executiveid = self.cleaned_data.get('executiveid')

        if not executiveid:
            raise forms.ValidationError(
                "Executive ID is required"
            )

        if not str(executiveid).isdigit():
            raise forms.ValidationError(
                "Executive ID must be an integer"
            )

        return executiveid


    def clean_businessneed(self):
        businessneed = self.cleaned_data.get('businessneed')

        if not businessneed:
            raise forms.ValidationError(
                "Business need is required"
            )

        return businessneed


    def clean(self):
        cleaned_data = super().clean()

        required_fields = [
            'gender',
            'territoryid',
            'regionid',
            'productid',
            'statusid',
            'leadsourceid'
        ]

        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(
                    field,
                    f"{field} is required"
                )

        return cleaned_data