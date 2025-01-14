from django.core.management import BaseCommand
from faker import Faker
import random, os
from apps.models import Author, Book, Category
from django.core.files import File
from accounts.models import User

class Command(BaseCommand):
    help = 'Faker yordamida Book va Category modellarini namunaviy ma\'lumotlar bilan to\'ldiradi'

    def handle(self, *args, **kwargs):
        fake = Faker()
        user = User.objects.filter(email='javlonbekdeveloper7@gmail.com').first()
        images_path = 'apps/static/assets/images/books/'
        image_files = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]
        self.stdout.write("Category ma'lumotlarini kiritish boshlandi...")
        categories = []
        for _ in range(6):
            category = Category(name=fake.name())
            category.save()
            categories.append(category)

        self.stdout.write("Author va User ma'lumotlarini kiritish boshlandi...")
        author = Author.objects.create(name=fake.name())

        self.stdout.write("Book ma'lumotlarini kiritish boshlandi...")
        for _ in range(17):
            book = Book.objects.create(
                title=fake.sentence(nb_words=4),
                author=author,
                price=round(random.uniform(10, 100), 2),
                availability=random.choice(Book.Availability.choices)[0],
                format=random.choice(Book.Format.choices)[0],
                owner= user,
                average_rating=round(random.uniform(0, 5), 1),
                language=fake.language_name(),
                pages=random.randint(100, 1000),
                description=fake.text(),
                publisher=fake.company(),
                isbn=fake.isbn13(),
                quantity=random.randint(1, 20)
            )
            random_image = random.choice(image_files)
            image_path = os.path.join(images_path, random_image)
            with open(image_path, 'rb') as img_file:
                book.book_image.save(random_image, File(img_file), save=False)

            book.save()
            book.category.set(random.sample(categories, random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("Ma'lumotlar muvaffaqiyatli kiritildi!"))