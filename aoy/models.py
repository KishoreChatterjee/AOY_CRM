from django.db import models

class Lead(models.Model):
    # Choice options
    SESSION_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Both', 'Both'),
    ]

    LEAD_STATUS_CHOICES = [
        ('Not Attended', 'Not Attended'),
        ('Follow-Up', 'Follow-Up'),
        ('Demo Booked', 'Demo Booked'),
        ('Demo Attended', 'Demo Attended'),
        ('Converted', 'Converted'),
        ('Fake-Lead', 'Fake-Lead'),
        ('Not Interested', 'Not Interested'),
    ]

    PRIORITY_CHOICES = [
        ('Top Priority', 'Top Priority'),
        ('Medium Priority', 'Medium Priority'),
        ('Low Priority', 'Low Priority'),
    ]

    HEALTH_GOAL_CHOICES = [
        ('General Fitness', '✅ General Fitness'),
        ('Weight Loss', '⚖️ Weight Loss'),
        ('PCOD / PCOS', '♀️ PCOD / PCOS'),
        ('Thyroid', '🧬 Thyroid'),
        ('BP', '💓 BP (Blood Pressure)'),
        ('Asthma', '🌬️ Asthma'),
        ('Prenatal Yoga', '🤰 Prenatal Yoga'),
        ('Postnatal Yoga', '🤱 Postnatal Yoga'),
        ('Hormonal Imbalance', '🔄 Hormonal Imbalance'),
        ('Stress Relief', '🧘 Stress Relief'),
        ('Anxiety', '😟 Anxiety'),
        ('Belly Fat / Gut Health', '🫄 Belly Fat / Gut Health'),
        ('Other', '❓ Other'),
    ]

    # Lead fields
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    height = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    session_interest = models.CharField(max_length=10, choices=SESSION_CHOICES)
    enquiry_datetime = models.DateTimeField(null=True, blank=True)
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    health_goal = models.CharField(max_length=50, choices=HEALTH_GOAL_CHOICES)
    custom_health_goal = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"
