from datetime import datetime, timedelta, timezone
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

#User = get_user_model()

validate_digits_1_to_9 = RegexValidator(
    regex=r'^[1-9]*$',
    message='Only digits from 1 to 9 are allowed.'
    )
# SEVERITY_CHOICES = [
#         (1,"1 - Minor irritation (can run)"), # Niggle
#         (2,"2"),
#         (3,"3 - Irritation (can run)"), # Can run but concerning
#         (4,"4"),
#         (5,"5 - Inhibiting (can run), but shouldn't)"), # Can run but realy shouldn't
#         (6,"6"),
#         (7,"7 - Severe (can't run, can walk)"), # Can't run
#         (8,"8"),
#         (9,"9 - Very severe (can't walk)") # Can't walk
#         ]

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





# exercise/injury
class Injury(models.Model):
    id = models.AutoField(primary_key=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    issue = models.CharField(max_length=50)
    area = models.CharField(blank=True, default='', max_length=150)
    side = models.CharField(blank=True, default='', max_length=30)
    start_datetime = models.DateTimeField()
    severity = models.TextField(validators=[validate_digits_1_to_9])
    description = models.TextField(blank=True, default='')

    # class Meta:
        # permissions = [
        #     ('self_view_injury', 'Can view own Injury'),
        #     ('self_change_injury', 'Can change own Injury'),
        #     ('self_delete_injury', 'Can delete own Injury'),
        # ]
    #     ordering = ["-start_date"]
    #     db_table = "Injuries"
    #     verbose_name = "Injury"
    #     verbose_name_plural = "Injuries"
    
    def __str__(self):
        return self.issue + " - " + str(self.start_datetime)
    
    def save(self, *args, **kwargs):
        super(Injury, self).save(*args, **kwargs)
        # If has associated Calculated_Injury instance, update it
        if hasattr(self, 'calculated_injury'):
            self.calculated_injury.save()
        # Else create it
        else:
            Calculated_Injury.objects.create(injury=self)

    

class Calculated_Injury(models.Model):
    injury = models.OneToOneField(Injury, on_delete=models.CASCADE, related_name='calculated_injury', primary_key=True)

    max_severity = models.IntegerField()
    mode_severity = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    
        
    def save(self, *args, **kwargs):
        self.max_severity = max_digit(self.injury.severity)
        self.mode_severity = mode_digit(self.injury.severity)
        self.start_date = self.injury.start_datetime.astimezone(timezone.utc).date()
        self.end_date = self.start_date + timedelta(days=len(self.injury.severity)-1)
        super(Calculated_Injury, self).save(*args, **kwargs)
        






# exercise/illness
class Illness(models.Model):
    id = models.AutoField(primary_key=True)
    issue = models.CharField(max_length=50)
    start_datetime = models.DateTimeField()
    severity = models.TextField(validators=[validate_digits_1_to_9])
    description = models.TextField(blank=True, default='')
    # class Meta:
    #     ordering = ["-start_date"]
    #     db_table = "Illnesses"
    #     verbose_name = "Illness"
    #     verbose_name_plural = "Illnesses"
    
    def __str__(self):
        return self.issue + " - " + str(self.start_datetime)

    def save(self, *args, **kwargs):
        super(Illness, self).save(*args, **kwargs)
        # If has associated Calculated_Illness instance, update it
        if hasattr(self, 'calculated_illness'):
            self.calculated_illness.save()
        # Else create it
        else:
            Calculated_Illness.objects.create(illness=self)



class Calculated_Illness(models.Model):
    illness = models.OneToOneField(Illness, on_delete=models.CASCADE, related_name='calculated_illness', primary_key=True)

    max_severity = models.IntegerField()
    mode_severity = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    

    def save(self, *args, **kwargs):
        self.max_severity = max_digit(self.illness.severity)
        self.mode_severity = mode_digit(self.illness.severity)
        self.start_date = self.illness.start_datetime.astimezone(timezone.utc).date()
        self.end_date = self.start_date + timedelta(days=len(self.illness.severity)-1)
        super(Calculated_Illness, self).save(*args, **kwargs)