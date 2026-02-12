from wtforms import (
    Form, StringField, IntegerField, FloatField, BooleanField,
    DateField, DateTimeField, SelectField, RadioField, PasswordField,
    TextAreaField, EmailField, URLField, validators
)


class GenericForm(Form):
    """
    Generic WTForms class featuring templates for main fields and validators.
    """

    # Text fields
    string_field = StringField('String Field', [validators.Length(min=1, max=255, message="Deve essere compreso tra 1 e 255 caratteri.")])

    # Numeric fields
    integer_field = IntegerField('Integer Field', [validators.NumberRange(min=0, max=1000, message="Deve essere tra 0 e 1000.")])
    float_field = FloatField('Float Field', [validators.NumberRange(min=0.0, max=1000.0, message="Deve essere tra 0.0 e 1000.0.")])

    # Boolean fields
    boolean_field = BooleanField('Boolean Field')

    # Date and time fields
    date_field = DateField('Date Field', [validators.Optional()], format='%Y-%m-%d')
    datetime_field = DateTimeField('Datetime Field', [validators.Optional()], format='%Y-%m-%d %H:%M:%S')

    # Selection fields
    select_field = SelectField('Select Field', choices=[('option1', 'Option 1'), ('option2', 'Option 2')])
    radio_field = RadioField('Radio Field',choices=[('yes', 'Yes'), ('no', 'No')])

    # Security fields
    password_field = PasswordField('Password Field', [validators.DataRequired(), validators.Length(min=6, message="Minimo 6 caratteri.")])

    # Advanced text fields
    text_area_field = TextAreaField('Text Area Field', [validators.Optional(), validators.Length(max=500, message="Massimo 500 caratteri.")])

    # Special fields
    email_field = EmailField('Email Field', [validators.Email(message="Inserisci un'email valida.")])
    url_field = URLField('URL Field', [validators.URL(message="Inserisci un URL valido.")])

    # Common validators
    required_field = StringField('Required Field', [validators.DataRequired(message="Questo campo è obbligatorio.")])
    optional_field = StringField('Optional Field', [validators.Optional()])

    # Converter data -> dictionary
    def to_dict(self):
        """
        Returns form data as dictionary.
        """
        return {field.name: field.data for field in self}

    # (Pre-)Populate form data using a dictionary
    def from_dict(self, data):
        """
        Populates form fields (in advance) starting from a dictionary.
        """
        for field_name, value in data.items():
            if hasattr(self, field_name):
                getattr(self, field_name).data = value

    # Request data validation
    def validate_on_submit(self, request_form):
        """
        Validates data coming from Flask request.
        """
        return self.validate(request_form)
