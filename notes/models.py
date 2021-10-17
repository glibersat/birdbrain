from django.db import models


class Literal(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"L<{self.label}>"


class Predicate(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"P<{self.label}>"


class Statement(models.Model):
    subject = models.ForeignKey(
        Literal, on_delete=models.CASCADE, related_name="statements_subjects"
    )
    predicate = models.ForeignKey(Predicate, on_delete=models.CASCADE)
    object = models.ForeignKey(
        Literal, on_delete=models.CASCADE, related_name="statements_objects"
    )

    def __str__(self):
        return f"{self.subject} {self.predicate} {self.object}"


class Note(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    statements = models.ManyToManyField(Statement, blank=True)
    source = models.CharField(max_length=1000, blank=True, null=True)
