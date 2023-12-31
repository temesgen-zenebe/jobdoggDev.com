from django.template import Library
register = Library()

@register.filter
def mask_ssn(value):
    if value:
        masked_value = '#' * 5 + value[5:]  # Replace the first five digits with "#" signs
        return masked_value[:3] + '-' + masked_value[3:5] + '-' + value[-4:]
    return ''


@register.filter
def format_phone_number(value):
    # Remove any non-digit characters from the phone number
    phone_number = ''.join(filter(str.isdigit, str(value)))

    # Apply the desired phone number format (e.g., XXX-XXX-XXXX)
    formatted_number = '-'.join([phone_number[:3], phone_number[3:6], phone_number[6:]])

    return formatted_number