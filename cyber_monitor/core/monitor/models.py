from django.db import models
from django.contrib.auth.models import User


# Multi-tenant company
class Company(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# User linked to company
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.company.name})"


# Network logs per company
class NetworkLog(models.Model):
    src_ip = models.GenericIPAddressField()
    dst_ip = models.GenericIPAddressField()
    protocol = models.CharField(max_length=50)
    packet_size = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.src_ip} → {self.dst_ip} ({self.company.name})"


# Alerts per company
class Alert(models.Model):
    severity = models.CharField(max_length=50)
    message = models.TextField()
    src_ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.severity}] {self.src_ip} ({self.company.name})"


# Suspicious activity logs
class SuspiciousActivity(models.Model):
    src_ip = models.GenericIPAddressField()
    activity_type = models.CharField(max_length=50)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.activity_type} by {self.src_ip}"