from tortoise.models import Model
from tortoise import fields


class Book(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    published_date = fields.DateField()

    class Meta:
        table = "books"
