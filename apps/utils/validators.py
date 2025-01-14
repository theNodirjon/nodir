from django.core.exceptions import ValidationError

def validate_file_type(value):
    valid_extensions = ['.pdf', '.epub', '.docx']

    if any([value.name.endswith(i) for i in valid_extensions]):
        raise ValidationError(
            f"Fayl turi ruxsat etilmagan. Faqat quyidagi formatlarga ruxsat beriladi: {', '.join(valid_extensions)}."
        )
