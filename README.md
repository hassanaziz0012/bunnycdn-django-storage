# bunnycdn-django-storage
A Custom Django Storage class implemented for use with the Bunny.net CDN.

## How to use?
1. For files you want to store on BunnyCDN, just set the `storage` attribute of your `FileField` like so:
```python
class MyModel(models.Model):
  file = models.FileField(storage=BunnyStorage())
```

## Author
- Hassan Aziz
- Web Developer and Designer
- Website: https://www.hassandev.me
- Check out my other [web projects](https://www.hassandev.me/projects)
