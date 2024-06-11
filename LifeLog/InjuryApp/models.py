from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

validate_digits_1_to_9 = RegexValidator(
    regex=r'^[1-9]*$',
    message='Only digits from 1 to 9 are allowed.'
    )
SEVERITY_CHOICES = [
        (1,"1 - Minor irritation (can run)"), # Niggle
        (2,"2"),
        (3,"3 - Irritation (can run)"), # Can run but concerning
        (4,"4"),
        (5,"5 - Inhibiting (can run), but shouldn't)"), # Can run but realy shouldn't
        (6,"6"),
        (7,"7 - Severe (can't run, can walk)"), # Can't run
        (8,"8"),
        (9,"9 - Very severe (can't walk)") # Can't walk
        ]


class Injury(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    issue = models.CharField(max_length=50)
    area = models.CharField(blank=True, default='', max_length=150)
    side = models.CharField(blank=True, default='', max_length=30)
    start_datetime = models.DateTimeField()
    severity = models.TextField(validators=[validate_digits_1_to_9])
    notes = models.TextField(blank=True, default='')

    # class Meta:
    #     ordering = ["-start_date"]
    #     db_table = "Injuries"
    #     verbose_name = "Injury"
    #     verbose_name_plural = "Injuries"
    
    def save(self, *args, **kwargs):
        super(Injury, self).save(*args, **kwargs)
        # If has associated Calculated_Injury instance, update it
        if hasattr(self, 'calculated_injury'):
            self.calculated_injury.save()
        # Else create it
        else:
            Calculated_Injury.objects.create(model_a=self)

    

class Calculated_Injury(models.Model):
    injury = models.OneToOneField(Injury, on_delete=models.CASCADE, related_name='calculated_injury')

    max_severity = models.IntegerField()
    mode_severity = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def max_digit(textField):
        # Filter out non-digit characters and convert remaining characters to integers
        digits = [int(char) for char in textField if char.isdigit()]

        if digits:  # Check if there are any digits
            return max(digits)  # Return the maximum digit
        else:
            return None  # Return None if there are no digits
    def mode_digit(textField):
        # Filter out non-digit characters and convert remaining characters to integers
        digits = [int(char) for char in textField if char.isdigit()]

        if digits:  # Check if there are any digits
            return max(set(digits), key=digits.count)  # Return the mode digit
        else:
            return None  # Return None if there are no digits
        
    def save(self, *args, **kwargs):
        self.max_severity = self.max_digit(self.injury.severity)
        self.mode_severity = self.mode_digit(self.injury.severity)
        self.start_date = self.injury.start_datetime.astimezone(datetime.utc).date()
        self.end_date = self.start_date + datetime.timedelta(days=len(self.injury.severity)-1)
        super(Calculated_Injury, self).save(*args, **kwargs)