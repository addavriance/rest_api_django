from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Projects(BaseModel):
    name = models.TextField()
    coords = models.TextField()
    district = models.TextField()
    website = models.TextField()

    class Meta:
        db_table = 'projects'


class Houses(BaseModel):
    project = models.ForeignKey(Projects, related_name='projects', on_delete=models.CASCADE)
    name = models.TextField()
    address = models.TextField()
    built_year = models.IntegerField()
    built_quarter = models.IntegerField()

    class Meta:
        db_table = 'houses'


class Sections(BaseModel):
    house = models.ForeignKey(Houses, related_name='houses', on_delete=models.CASCADE)
    number = models.IntegerField()
    floors = models.IntegerField()
    flats_on_floor = models.IntegerField()
    starting_flat_number = models.IntegerField()

    class Meta:
        db_table = 'sections'


class Flats(BaseModel):
    section = models.ForeignKey(Sections, related_name='sections', on_delete=models.CASCADE)
    floor = models.IntegerField()
    flat_number = models.IntegerField()
    status = models.CharField(max_length=255)
    price = models.IntegerField()
    size = models.FloatField()
    rooms = models.IntegerField()

    class Meta:
        db_table = 'flats'


class Users(BaseModel):
    login = models.TextField()
    password = models.TextField()

    class Meta:
        db_table = 'users'
