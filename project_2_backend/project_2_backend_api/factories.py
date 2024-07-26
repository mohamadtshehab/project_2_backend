from factory.django import DjangoModelFactory
from factory import Faker, Sequence, LazyFunction, Dict, post_generation, lazy_attribute
import json
import random
from django.db import transaction
from .models import Texture, Category, TDModel, Room, Object, ObjectImage
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_staff = False
    is_superuser = False

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('defaultpassword')
            
class TextureFactory(DjangoModelFactory):
    class Meta:
        model = Texture

    name = Faker('word')
    image = Faker('image_url')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Sequence(lambda n: f"Category {n}")


class TDModelFactory(DjangoModelFactory):
    class Meta:
        model = TDModel

    name = Sequence(lambda n: f"TDModel {n}")
    description = Faker('paragraph', nb_sentences=3)
    scaling = LazyFunction(lambda: json.dumps({'x': random.uniform(0, 1), 'y': random.uniform(0, 1), 'z': random.uniform(0, 1)}))
    rotation = LazyFunction(lambda: json.dumps({'x': random.uniform(0, 360), 'y': random.uniform(0, 360), 'z': random.uniform(0, 360)}))
    translation = LazyFunction(lambda: json.dumps({'x': random.uniform(-100, 100), 'y': random.uniform(-100, 100), 'z': random.uniform(-100, 100)}))
    color = LazyFunction(lambda: json.dumps({'r': random.uniform(0, 1), 'g': random.uniform(0, 1), 'b': random.uniform(0, 1), 'a': random.uniform(0, 1)}))
    type = LazyFunction(lambda: random.choice(['room', 'object']))


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    @lazy_attribute
    def td_model(self):
        all_td_models = TDModel.objects.all()
        if not all_td_models.exists():
            new_td_model = TDModelFactory()
            new_td_model.save()
            return new_td_model
        return random.choice(all_td_models)

    @lazy_attribute
    def user(self):
        all_users = User.objects.all()
        if not all_users.exists():
            new_user = UserFactory()
            new_user.save()
            return new_user
        return random.choice(all_users)


class ObjectFactory(DjangoModelFactory):
    class Meta:
        model = Object

    @lazy_attribute
    def td_model(self):
        all_td_models = TDModel.objects.filter(type='room')
        if not all_td_models.exists():
            new_td_model = TDModelFactory(type='room')
            new_td_model.save()
            return new_td_model
        return random.choice(all_td_models)

    category = LazyFunction(lambda: CategoryFactory(name='new_cat'))

    @lazy_attribute
    def room(self):
        all_rooms = Room.objects.all()
        if not all_rooms.exists():
            new_room = RoomFactory()
            new_room.save()
            return new_room
        return random.choice(all_rooms)

    url = Faker('file_url')

    @post_generation
    def textures(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for texture in extracted:
                self.textures.add(texture)
        else:
            for _ in range(3):
                self.textures.add(TextureFactory())

    material = Faker('file_url')


class ObjectImageFactory(DjangoModelFactory):
    class Meta:
        model = ObjectImage

    @lazy_attribute
    def object(self):
        all_objects = Object.objects.all()
        if not all_objects.exists():
            new_object = ObjectFactory()
            new_object.save()
            return new_object
        return random.choice(all_objects)

    url = Faker('image_url')
    
    
class FactoryLauncher:
    def create_all_instances(num_textures=10, num_categories=5, num_tdmodels=5, num_rooms=5, num_objects=10, num_object_images=10):
        with transaction.atomic():
            textures = [TextureFactory() for _ in range(num_textures)]
            print(f"Created {len(textures)} textures.")
            
            categories = [CategoryFactory() for _ in range(num_categories)]
            print(f"Created {len(categories)} categories.")
            
            tdmodels = [TDModelFactory() for _ in range(num_tdmodels)]
            print(f"Created {len(tdmodels)} TD models.")
            
            rooms = [RoomFactory() for _ in range(num_rooms)]
            print(f"Created {len(rooms)} rooms.")
            
            objects = [ObjectFactory() for _ in range(num_objects)]
            print(f"Created {len(objects)} objects.")
            
            object_images = [ObjectImageFactory() for _ in range(num_object_images)]
            print(f"Created {len(object_images)} object images.")
