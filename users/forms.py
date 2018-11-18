from django import forms
from users.models import MyUser
from restfull_tutorial.settings import ALLOWED_SIGNUP_DOMAINS
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from users.models import Person


def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(
                    ','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

        except Exception:
            raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(
                ','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501


def UniqueEmailValidator(value):
    if MyUser.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-text form-control'}),
        max_length=30,
        required=True, )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-text form-control'}),
        max_length=30,
        required=True, )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'rows': 60, 'cols': 60, 'class': 'input-text form-control'}),
        label=_('Your Email'))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text form-control'}),
                               label=_('Password'), max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text form-control'}),
                                       label=_('Confirm Password'), max_length=50)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)

    def clean(self):
        super(UserRegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data


class PersonForm(forms.ModelForm):
    city = forms.CharField(required=True,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'style': 'border: #008282;border-style: double;'}),
                           max_length=255)

    description = forms.CharField(required=True, label=_('Description'), widget=CKEditorWidget(), )

    address = forms.CharField(required=True,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'style': 'border: #008282;border-style: double;'}),
                              max_length=255)

    work_internship = forms.CharField(required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'style': 'border: #008282;border-style: double;'}),
                                      max_length=255)

    phone = forms.CharField(required=True,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'style': 'border: #008282;border-style: double;'}),
                            max_length=255)

    website = forms.CharField(required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'style': 'border: #008282;border-style: double;'}),
                              max_length=255)

    zipcode = forms.CharField(required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'style': 'border: #008282;border-style: double;'}),
                              max_length=255)

    image = forms.FileField(required=True, label=_('Image'), )

    group_type = forms.ChoiceField(choices=(('person', _('Person')), ('per_group', 'Person Group')),
                                   initial='', widget=forms.Select(), required=True)


    class Meta:
        model = Person
        fields = ['group_type', 'region', 'description', 'city', 'address', 'phone', 'website', 'zipcode',
                  'work_internship',
                  'certificate', 'image', 'presentation', ]


class LoginForm(forms.Form):

    username = forms.EmailField(label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Password'),
                               max_length=50)

    class Meta:
        fields = ['username','password']
