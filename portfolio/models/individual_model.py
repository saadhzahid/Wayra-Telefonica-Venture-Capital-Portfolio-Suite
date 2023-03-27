from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from phonenumber_field.modelfields import PhoneNumberField


## PolymorphicQuerySetClass
class PolymorphicQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(PolymorphicQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_child_class()
        else:
            return result

    def __iter__(self):
        for item in super(PolymorphicQuerySet, self).__iter__():
            yield item.as_child_class()


## Individual Manager Override
class IndividualManager(models.Manager):
    def get_query_set(self):
        return PolymorphicQuerySet(self.model)


class Individual(models.Model):
    """Individual model used by admins to create new client/individual."""

    def __str__(self):
        return f'{self.name}'

    content_type = models.ForeignKey(ContentType, editable=False, null=True, on_delete=models.CASCADE)
    objects = IndividualManager()

    name = models.CharField("name", max_length=200)
    AngelListLink = models.URLField("Angellist link", max_length=200)
    CrunchbaseLink = models.URLField("Crunchbase link", max_length=200)
    LinkedInLink = models.URLField("Linkedin link", max_length=200)
    Company = models.CharField("Company", max_length=100)
    Position = models.CharField("Company position", max_length=100)
    Email = models.EmailField(blank=False)
    PrimaryNumber = PhoneNumberField("Primary phone number", blank=False)
    SecondaryNumber = PhoneNumberField("Secondary phone number", blank=True)
    is_archived = models.BooleanField(default=False)
    profile_pic = models.ImageField("Profile picture", upload_to='profilepics', blank=True)

    def save(self, *args, **kwargs):
        if (not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)

        super(Individual, self).save(*args, **kwargs)

    def as_child_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Individual):
            return self
        return model.objects.get(id=self.id)

    def archive(self):
        self.is_archived = True
        self.save()

    def unarchive(self):
        self.is_archived = False
        self.save()
