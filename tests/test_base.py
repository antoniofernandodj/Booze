from booze import Coerce, Base, ParsingError
import pytest


class MyClass1(Base):
    name = Coerce('name').string().length(3, 10)
    age = Coerce('age').integer().strict().min(18).max(100)
    is_active = Coerce('active').boolean().strict()

class MyClass2(Base):
    email = Coerce('email').string().email()
    height = Coerce('height').float().min(0.0).max(2.5)
    favorite_numbers = Coerce('fav_nums').list().contains(42)


def test_my_class1():
    # Valid input data
    obj1 = MyClass1(name="John", age=30, is_active=True)
    assert obj1.name == "John"
    assert obj1.age == 30
    assert obj1.is_active is True
    assert obj1.to_dict() == {'name': 'John', 'age': 30, 'is_active': True}

    # Invalid input data
    with pytest.raises(ParsingError):
        MyClass1(name="Jo", age=15, is_active="True")

def test_my_class2():
    # Valid input data
    obj2 = MyClass2(email="test@example.com", height=1.75, favorite_numbers=[42, 7, 15])
    assert obj2.email == "test@example.com"
    assert obj2.height == 1.75
    assert obj2.favorite_numbers == [42, 7, 15]
    assert obj2.to_dict() == {
        'email': 'test@example.com',
        'height': 1.75,
        'favorite_numbers': [42, 7, 15]
    }

    # Invalid input data
    with pytest.raises(ParsingError):
        MyClass2(email="invalid_email", height=-1.5, favorite_numbers=[7, 15])

def test_my_class1_boolean_validation():
    # Invalid input data for boolean attribute
    with pytest.raises(ParsingError):
        MyClass1(name="John", age=30, is_active="True")

def test_my_class1_integer_validation():
    # Invalid input data for integer attribute
    with pytest.raises(ParsingError):
        MyClass1(name="John", age="30", is_active=True)

def test_my_class1_length_validation():
    # Invalid input data for string length attribute
    with pytest.raises(ParsingError):
        MyClass1(name="J", age=30, is_active=True)

def test_my_class1_min_validation():
    # Invalid input data for minimum age attribute
    with pytest.raises(ParsingError):
        MyClass1(name="John", age=16, is_active=True)

def test_my_class1_max_validation():
    # Invalid input data for maximum age attribute
    with pytest.raises(ParsingError):
        MyClass1(name="John", age=120, is_active=True)

def test_my_class1_to_dict():
    obj1 = MyClass1(name="John", age=30, is_active=True)
    assert obj1.to_dict() == {'name': 'John', 'age': 30, 'is_active': True}

def test_my_class2_email_validation():
    # Invalid input data for email attribute
    with pytest.raises(ParsingError):
        MyClass2(email="invalid_email", height=1.75, favorite_numbers=[42, 7, 15])

def test_my_class2_min_validation():
    # Invalid input data for minimum height attribute
    with pytest.raises(ParsingError):
        MyClass2(email="test@example.com", height=-1.5, favorite_numbers=[42, 7, 15])

def test_my_class2_max_validation():
    # Invalid input data for maximum height attribute
    with pytest.raises(ParsingError):
        MyClass2(email="test@example.com", height=3.0, favorite_numbers=[42, 7, 15])

def test_my_class2_contains_validation():
    # Invalid input data for list containing attribute
    with pytest.raises(ParsingError):
        MyClass2(email="test@example.com", height=1.75, favorite_numbers=[7, 15])

def test_my_class2_to_dict():
    obj2 = MyClass2(email="test@example.com", height=1.75, favorite_numbers=[42, 7, 15])
    assert obj2.to_dict() == {
        'email': 'test@example.com',
        'height': 1.75,
        'favorite_numbers': [42, 7, 15]
    }


class MyClass3(Base):
    username = Coerce('username').string().length(5, 20)
    score = Coerce('score').float().min(0.0).max(100.0)
    tags = Coerce('tags').list().contains("python")

class MyClass4(Base):
    description = Coerce('description').string().length(10, 100)
    quantity = Coerce('quantity').integer().min(1).max(1000)
    is_available = Coerce('availability').boolean()

class MyClass5(Base):
    email = Coerce('email').string().email()
    temperature = Coerce('temperature').float().min(-10.0).max(40.0)
    metadata = Coerce('metadata').dictionary().contains("version")

def test_my_class3():
    obj3 = MyClass3(username="john_doe", score=85.5, tags=["python", "coding"])
    assert obj3.username == "john_doe"
    assert obj3.score == 85.5
    assert obj3.tags == ["python", "coding"]
    assert obj3.to_dict() == {
        'username': 'john_doe',
        'score': 85.5,
        'tags': ['python', 'coding']
    }

    with pytest.raises(ParsingError):
        MyClass3(username="johnd", score="85.5", tags="python")

def test_my_class4():
    obj4 = MyClass4(description="A sample product", quantity=100, is_available=True)
    assert obj4.description == "A sample product"
    assert obj4.quantity == 100
    assert obj4.is_available is True
    assert obj4.to_dict() == {
        'description': 'A sample product',
        'quantity': 100,
        'is_available': True
    }

    with pytest.raises(ParsingError):
        MyClass4(description="Short", quantity=0, is_available="True")

def test_my_class5():
    obj5 = MyClass5(email="test@example.com", temperature=20.5, metadata={"version": "1.0"})
    assert obj5.email == "test@example.com"
    assert obj5.temperature == 20.5
    assert obj5.metadata == {"version": "1.0"}
    assert obj5.to_dict() == {
        'email': 'test@example.com',
        'temperature': 20.5,
        'metadata': {'version': '1.0'}
    }

    with pytest.raises(ParsingError):
        MyClass5(email="invalid_email", temperature=-20.5, metadata={"version": "2.0"})


def test_str_representation():
    obj1 = MyClass1(name="John", age=30, is_active=True)
    assert str(obj1) == "<MyClass1(name='John', age=30, is_active=True)>"

    obj3 = MyClass3(username="john_doe", score=85.5, tags=["python", "coding"])
    assert str(obj3) == "<MyClass3(username='john_doe', score=85.5, tags=['python', 'coding'])>"


def test_my_class6():
    class MyClass6(Base):
        username = Coerce('username').string().min_length(5).max_length(20)
        score = Coerce('score').float().min(0.0).max(100.0)
        tags = Coerce('tags').list().contains("python")

    obj6 = MyClass6(username="johndoe", score=85.5, tags=["python", "coding"])
    assert obj6.username == "johndoe"
    assert obj6.score == 85.5
    assert obj6.tags == ["python", "coding"]
    assert obj6.to_dict() == {
        'username': 'johndoe',
        'score': 85.5,
        'tags': ['python', 'coding']
    }

    with pytest.raises(ParsingError):
        MyClass6(username="john", score="85.5", tags="coding")


def test_my_class7():
    class MyClass7(Base):
        name = Coerce('name').string().length(3, 20)
        age = Coerce('age').integer().min(0).max(120)
        is_active = Coerce('active').boolean()

    obj7 = MyClass7(name="Alice", age=25, is_active=True)
    assert obj7.name == "Alice"
    assert obj7.age == 25
    assert obj7.is_active is True
    assert obj7.to_dict() == {'name': 'Alice', 'age': 25, 'is_active': True}

    with pytest.raises(ParsingError):
        MyClass7(name="A", age=150, is_active="True")


def test_my_class8():
    class MyClass8(Base):
        email = Coerce('email').string().email()
        height = Coerce('height').float().min(0.5).max(2.2)
        favorite_numbers = Coerce('fav_nums').list().contains(42)

    obj8 = MyClass8(email="test@example.com", height=1.75, favorite_numbers=[42, 7, 15])
    assert obj8.email == "test@example.com"
    assert obj8.height == 1.75
    assert obj8.favorite_numbers == [42, 7, 15]
    assert obj8.to_dict() == {
        'email': 'test@example.com',
        'height': 1.75,
        'favorite_numbers': [42, 7, 15]
    }

    with pytest.raises(ParsingError):
        MyClass8(email="invalid_email", height=-1.5, favorite_numbers=[7, 15])


def test_my_class9():
    class MyClass9(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        views = Coerce('views').integer().min(0)
        is_published = Coerce('published').boolean()

    obj9 = MyClass9(title="My Article", views=100, is_published=True)
    assert obj9.title == "My Article"
    assert obj9.views == 100
    assert obj9.is_published is True
    assert obj9.to_dict() == {
        'title': 'My Article',
        'views': 100,
        'is_published': True
    }

    with pytest.raises(ParsingError):
        MyClass9(title="Short", views=-5, is_published="True")


def test_my_class10():
    class MyClass10(Base):
        description = Coerce('description').string().length(10, 200)
        quantity = Coerce('quantity').integer().min(1).max(500)
        is_available = Coerce('availability').boolean()

    obj10 = MyClass10(description="A product description", quantity=200, is_available=True)
    assert obj10.description == "A product description"
    assert obj10.quantity == 200
    assert obj10.is_available is True
    assert obj10.to_dict() == {
        'description': 'A product description',
        'quantity': 200,
        'is_available': True
    }

    with pytest.raises(ParsingError):
        MyClass10(description="Short", quantity=0, is_available="True")


def test_my_class11():
    class MyClass11(Base):
        name = Coerce('name').string().length(2, 30)
        age = Coerce('age').integer().min(1).max(200)
        is_student = Coerce('student').boolean()

    obj11 = MyClass11(name="Alex", age=25, is_student=True)
    assert obj11.name == "Alex"
    assert obj11.age == 25
    assert obj11.is_student is True
    assert obj11.to_dict() == {'name': 'Alex', 'age': 25, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass11(name="A", age=0, is_student="True")


def test_my_class12():
    class MyClass12(Base):
        email = Coerce('email').string().email()
        height = Coerce('height').float().min(1.0).max(2.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj12 = MyClass12(email="test@example.com", height=1.85, favorite_colors=["blue", "green"])
    assert obj12.email == "test@example.com"
    assert obj12.height == 1.85
    assert obj12.favorite_colors == ["blue", "green"]
    assert obj12.to_dict() == {
        'email': 'test@example.com',
        'height': 1.85,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass12(email="invalid_email", height=0.5, favorite_colors=["red", "green"])


def test_my_class13():
    class MyClass13(Base):
        name = Coerce('name').string().length(3, 50)
        age = Coerce('age').integer().min(18).max(120)
        is_verified = Coerce('verified').boolean()

    obj13 = MyClass13(name="Alice Johnson", age=30, is_verified=True)
    assert obj13.name == "Alice Johnson"
    assert obj13.age == 30
    assert obj13.is_verified is True
    assert obj13.to_dict() == {'name': 'Alice Johnson', 'age': 30, 'is_verified': True}

    with pytest.raises(ParsingError):
        MyClass13(name="A", age=15, is_verified="True")


def test_my_class14():
    class MyClass14(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(30.0).max(200.0)
        favorite_fruits = Coerce('fav_fruits').list().contains("apple")

    obj14 = MyClass14(email="test@example.com", weight=75.5, favorite_fruits=["apple", "banana"])
    assert obj14.email == "test@example.com"
    assert obj14.weight == 75.5
    assert obj14.favorite_fruits == ["apple", "banana"]
    assert obj14.to_dict() == {
        'email': 'test@example.com',
        'weight': 75.5,
        'favorite_fruits': ['apple', 'banana']
    }

    with pytest.raises(ParsingError):
        MyClass14(email="invalid_email", weight=20.0, favorite_fruits=["orange", "banana"])


def test_my_class15():
    class MyClass15(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(1000.0).max(5000.0)
        is_manager = Coerce('manager').boolean()

    obj15 = MyClass15(title="Software Engineer", salary=4000.0, is_manager=True)
    assert obj15.title == "Software Engineer"
    assert obj15.salary == 4000.0
    assert obj15.is_manager is True
    assert obj15.to_dict() == {
        'title': 'Software Engineer',
        'salary': 4000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass15(title="Dev", salary=800.0, is_manager="True")


def test_my_class16():
    class MyClass16(Base):
        name = Coerce('name').string().length(3, 40)
        age = Coerce('age').integer().min(0).max(150)
        is_married = Coerce('married').boolean()

    obj16 = MyClass16(name="David Brown", age=45, is_married=True)
    assert obj16.name == "David Brown"
    assert obj16.age == 45
    assert obj16.is_married is True
    assert obj16.to_dict() == {'name': 'David Brown', 'age': 45, 'is_married': True}

    with pytest.raises(ParsingError):
        MyClass16(name="D", age=200, is_married="True")


def test_my_class17():
    class MyClass17(Base):
        email = Coerce('email').string().email()
        rating = Coerce('rating').float().min(1.0).max(5.0)
        tags = Coerce('tags').list().contains("python")

    obj17 = MyClass17(email="user@example.com", rating=4.5, tags=["python", "coding"])
    assert obj17.email == "user@example.com"
    assert obj17.rating == 4.5
    assert obj17.tags == ["python", "coding"]
    assert obj17.to_dict() == {
        'email': 'user@example.com',
        'rating': 4.5,
        'tags': ['python', 'coding']
    }

    with pytest.raises(ParsingError):
        MyClass17(email="invalid_email", rating=0.5, tags=["coding", "java"])


def test_my_class18():
    class MyClass18(Base):
        name = Coerce('name').string().length(5, 50)
        age = Coerce('age').integer().min(1).max(120)
        is_employed = Coerce('employed').boolean()

    obj18 = MyClass18(name="Jennifer Smith", age=35, is_employed=True)
    assert obj18.name == "Jennifer Smith"
    assert obj18.age == 35
    assert obj18.is_employed is True
    assert obj18.to_dict() == {'name': 'Jennifer Smith', 'age': 35, 'is_employed': True}

    with pytest.raises(ParsingError):
        MyClass18(name="Jenny", age=0, is_employed="True")


def test_my_class19():
    class MyClass19(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj19 = MyClass19(email="test@example.com", weight=65.5, favorite_colors=["blue", "green"])
    assert obj19.email == "test@example.com"
    assert obj19.weight == 65.5
    assert obj19.favorite_colors == ["blue", "green"]
    assert obj19.to_dict() == {
        'email': 'test@example.com',
        'weight': 65.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass19(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class20():
    class MyClass20(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(2000.0).max(8000.0)
        is_manager = Coerce('manager').boolean()

    obj20 = MyClass20(title="Data Scientist", salary=6000.0, is_manager=True)
    assert obj20.title == "Data Scientist"
    assert obj20.salary == 6000.0
    assert obj20.is_manager is True
    assert obj20.to_dict() == {
        'title': 'Data Scientist',
        'salary': 6000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass20(title="Analyst", salary=1200.0, is_manager="True")


def test_my_class21():
    class MyClass21(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_married = Coerce('married').boolean()

    obj21 = MyClass21(name="Alex Turner", age=40, is_married=True)
    assert obj21.name == "Alex Turner"
    assert obj21.age == 40
    assert obj21.is_married is True
    assert obj21.to_dict() == {'name': 'Alex Turner', 'age': 40, 'is_married': True}

    with pytest.raises(ParsingError):
        MyClass21(name="A", age=200, is_married="True")


def test_my_class22():
    class MyClass22(Base):
        email = Coerce('email').string().email()
        rating = Coerce('rating').float().min(1.0).max(5.0)
        tags = Coerce('tags').list().contains("python")

    obj22 = MyClass22(email="user@example.com", rating=4.0, tags=["python", "coding"])
    assert obj22.email == "user@example.com"
    assert obj22.rating == 4.0
    assert obj22.tags == ["python", "coding"]
    assert obj22.to_dict() == {
        'email': 'user@example.com',
        'rating': 4.0,
        'tags': ['python', 'coding']
    }

    with pytest.raises(ParsingError):
        MyClass22(email="invalid_email", rating=0.5, tags=["coding", "java"])


def test_my_class23():
    class MyClass23(Base):
        name = Coerce('name').string().length(5, 50)
        age = Coerce('age').integer().min(1).max(120)
        is_employed = Coerce('employed').boolean()

    obj23 = MyClass23(name="Jessica Williams", age=28, is_employed=True)
    assert obj23.name == "Jessica Williams"
    assert obj23.age == 28
    assert obj23.is_employed is True
    assert obj23.to_dict() == {'name': 'Jessica Williams', 'age': 28, 'is_employed': True}

    with pytest.raises(ParsingError):
        MyClass23(name="Jess", age=0, is_employed="True")


def test_my_class24():
    class MyClass24(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj24 = MyClass24(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj24.email == "test@example.com"
    assert obj24.weight == 70.5
    assert obj24.favorite_colors == ["blue", "green"]
    assert obj24.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass24(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class25():
    class MyClass25(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(2000.0).max(8000.0)
        is_manager = Coerce('manager').boolean()

    obj25 = MyClass25(title="Data Scientist", salary=6000.0, is_manager=True)
    assert obj25.title == "Data Scientist"
    assert obj25.salary == 6000.0
    assert obj25.is_manager is True
    assert obj25.to_dict() == {
        'title': 'Data Scientist',
        'salary': 6000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass25(title="Analyst", salary=1200.0, is_manager="True")


def test_my_class26():
    class MyClass26(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_married = Coerce('married').boolean()

    obj26 = MyClass26(name="Alex Turner", age=40, is_married=True)
    assert obj26.name == "Alex Turner"
    assert obj26.age == 40
    assert obj26.is_married is True
    assert obj26.to_dict() == {'name': 'Alex Turner', 'age': 40, 'is_married': True}

    with pytest.raises(ParsingError):
        MyClass26(name="A", age=200, is_married="True")


def test_my_class27():
    class MyClass27(Base):
        email = Coerce('email').string().email()
        rating = Coerce('rating').float().min(1.0).max(5.0)
        tags = Coerce('tags').list().contains("python")

    obj27 = MyClass27(email="user@example.com", rating=4.0, tags=["python", "coding"])
    assert obj27.email == "user@example.com"
    assert obj27.rating == 4.0
    assert obj27.tags == ["python", "coding"]
    assert obj27.to_dict() == {
        'email': 'user@example.com',
        'rating': 4.0,
        'tags': ['python', 'coding']
    }

    with pytest.raises(ParsingError):
        MyClass27(email="invalid_email", rating=0.5, tags=["coding", "java"])


def test_my_class28():
    class MyClass28(Base):
        name = Coerce('name').string().length(5, 50)
        age = Coerce('age').integer().min(1).max(120)
        is_employed = Coerce('employed').boolean()

    obj28 = MyClass28(name="Jessica Williams", age=28, is_employed=True)
    assert obj28.name == "Jessica Williams"
    assert obj28.age == 28
    assert obj28.is_employed is True
    assert obj28.to_dict() == {'name': 'Jessica Williams', 'age': 28, 'is_employed': True}

    with pytest.raises(ParsingError):
        MyClass28(name="Jess", age=0, is_employed="True")


def test_my_class29():
    class MyClass29(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj29 = MyClass29(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj29.email == "test@example.com"
    assert obj29.weight == 70.5
    assert obj29.favorite_colors == ["blue", "green"]
    assert obj29.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass29(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class30():
    class MyClass30(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(2000.0).max(8000.0)
        is_manager = Coerce('manager').boolean()

    obj30 = MyClass30(title="Data Scientist", salary=6000.0, is_manager=True)
    assert obj30.title == "Data Scientist"
    assert obj30.salary == 6000.0
    assert obj30.is_manager is True
    assert obj30.to_dict() == {
        'title': 'Data Scientist',
        'salary': 6000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass30(title="Analyst", salary=1200.0, is_manager="True")


def test_my_class31():
    class MyClass31(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj31 = MyClass31(name="Alice Johnson", age=25, is_student=True)
    assert obj31.name == "Alice Johnson"
    assert obj31.age == 25
    assert obj31.is_student is True
    assert obj31.to_dict() == {'name': 'Alice Johnson', 'age': 25, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass31(name="A", age=200, is_student="True")


def test_my_class32():
    class MyClass32(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(40.0).max(120.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj32 = MyClass32(email="test@example.com", weight=65.0, favorite_colors=["blue", "green"])
    assert obj32.email == "test@example.com"
    assert obj32.weight == 65.0
    assert obj32.favorite_colors == ["blue", "green"]
    assert obj32.to_dict() == {
        'email': 'test@example.com',
        'weight': 65.0,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass32(email="invalid_email", weight=30.0, favorite_colors=["red", "green"])


def test_my_class33():
    class MyClass33(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj33 = MyClass33(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj33.title == "Data Scientist"
    assert obj33.salary == 7000.0
    assert obj33.is_manager is True
    assert obj33.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass33(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class34():
    class MyClass34(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj34 = MyClass34(name="Alex Turner", age=30, is_student=True)
    assert obj34.name == "Alex Turner"
    assert obj34.age == 30
    assert obj34.is_student is True
    assert obj34.to_dict() == {'name': 'Alex Turner', 'age': 30, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass34(name="A", age=200, is_student="True")


def test_my_class35():
    class MyClass35(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj35 = MyClass35(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj35.email == "test@example.com"
    assert obj35.weight == 70.5
    assert obj35.favorite_colors == ["blue", "green"]
    assert obj35.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass35(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class36():
    class MyClass36(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj36 = MyClass36(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj36.title == "Data Scientist"
    assert obj36.salary == 7000.0
    assert obj36.is_manager is True
    assert obj36.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass36(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class37():
    class MyClass37(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj37 = MyClass37(name="Alice Johnson", age=25, is_student=True)
    assert obj37.name == "Alice Johnson"
    assert obj37.age == 25
    assert obj37.is_student is True
    assert obj37.to_dict() == {'name': 'Alice Johnson', 'age': 25, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass37(name="A", age=200, is_student="True")


def test_my_class38():
    class MyClass38(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(40.0).max(120.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj38 = MyClass38(email="test@example.com", weight=65.0, favorite_colors=["blue", "green"])
    assert obj38.email == "test@example.com"
    assert obj38.weight == 65.0
    assert obj38.favorite_colors == ["blue", "green"]
    assert obj38.to_dict() == {
        'email': 'test@example.com',
        'weight': 65.0,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass38(email="invalid_email", weight=30.0, favorite_colors=["red", "green"])


def test_my_class39():
    class MyClass39(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj39 = MyClass39(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj39.title == "Data Scientist"
    assert obj39.salary == 7000.0
    assert obj39.is_manager is True
    assert obj39.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass39(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class40():
    class MyClass40(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj40 = MyClass40(name="Alex Turner", age=30, is_student=True)
    assert obj40.name == "Alex Turner"
    assert obj40.age == 30
    assert obj40.is_student is True
    assert obj40.to_dict() == {'name': 'Alex Turner', 'age': 30, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass40(name="A", age=200, is_student="True")


def test_my_class41():
    class MyClass41(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj41 = MyClass41(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj41.email == "test@example.com"
    assert obj41.weight == 70.5
    assert obj41.favorite_colors == ["blue", "green"]
    assert obj41.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass41(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class42():
    class MyClass42(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj42 = MyClass42(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj42.title == "Data Scientist"
    assert obj42.salary == 7000.0
    assert obj42.is_manager is True
    assert obj42.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass42(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class43():
    class MyClass43(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj43 = MyClass43(name="Alice Johnson", age=25, is_student=True)
    assert obj43.name == "Alice Johnson"
    assert obj43.age == 25
    assert obj43.is_student is True
    assert obj43.to_dict() == {'name': 'Alice Johnson', 'age': 25, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass43(name="A", age=200, is_student="True")


def test_my_class44():
    class MyClass44(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(40.0).max(120.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj44 = MyClass44(email="test@example.com", weight=65.0, favorite_colors=["blue", "green"])
    assert obj44.email == "test@example.com"
    assert obj44.weight == 65.0
    assert obj44.favorite_colors == ["blue", "green"]
    assert obj44.to_dict() == {
        'email': 'test@example.com',
        'weight': 65.0,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass44(email="invalid_email", weight=30.0, favorite_colors=["red", "green"])


def test_my_class45():
    class MyClass45(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj45 = MyClass45(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj45.title == "Data Scientist"
    assert obj45.salary == 7000.0
    assert obj45.is_manager is True
    assert obj45.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass45(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class46():
    class MyClass46(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj46 = MyClass46(name="Alex Turner", age=30, is_student=True)
    assert obj46.name == "Alex Turner"
    assert obj46.age == 30
    assert obj46.is_student is True
    assert obj46.to_dict() == {'name': 'Alex Turner', 'age': 30, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass46(name="A", age=200, is_student="True")


def test_my_class47():
    class MyClass47(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj47 = MyClass47(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj47.email == "test@example.com"
    assert obj47.weight == 70.5
    assert obj47.favorite_colors == ["blue", "green"]
    assert obj47.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass47(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class48():
    class MyClass48(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj48 = MyClass48(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj48.title == "Data Scientist"
    assert obj48.salary == 7000.0
    assert obj48.is_manager is True
    assert obj48.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass48(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class49():
    class MyClass49(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj49 = MyClass49(name="Alice Johnson", age=25, is_student=True)
    assert obj49.name == "Alice Johnson"
    assert obj49.age == 25
    assert obj49.is_student is True
    assert obj49.to_dict() == {'name': 'Alice Johnson', 'age': 25, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass49(name="A", age=200, is_student="True")


def test_my_class50():
    class MyClass50(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(40.0).max(120.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj50 = MyClass50(email="test@example.com", weight=65.0, favorite_colors=["blue", "green"])
    assert obj50.email == "test@example.com"
    assert obj50.weight == 65.0
    assert obj50.favorite_colors == ["blue", "green"]
    assert obj50.to_dict() == {
        'email': 'test@example.com',
        'weight': 65.0,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass50(email="invalid_email", weight=30.0, favorite_colors=["red", "green"])

def test_my_class51():
    class MyClass51(Base):
        username = Coerce('username').string().length(5, 20)
        score = Coerce('score').float().min(0.0).max(100.0)
        tags = Coerce('tags').list().contains("python")

    obj51 = MyClass51(username="john_doe", score=85.5, tags=["python", "coding"])
    assert obj51.username == "john_doe"
    assert obj51.score == 85.5
    assert obj51.tags == ["python", "coding"]
    assert obj51.to_dict() == {
        'username': 'john_doe',
        'score': 85.5,
        'tags': ['python', 'coding']
    }

    with pytest.raises(ParsingError):
        MyClass51(username="johnd", score="85.5", tags="python")


def test_my_class52():
    class MyClass52(Base):
        description = Coerce('description').string().length(10, 100)
        quantity = Coerce('quantity').integer().min(1).max(1000)
        is_available = Coerce('availability').boolean()

    obj52 = MyClass52(description="A sample product", quantity=100, is_available=True)
    assert obj52.description == "A sample product"
    assert obj52.quantity == 100
    assert obj52.is_available is True
    assert obj52.to_dict() == {
        'description': 'A sample product',
        'quantity': 100,
        'is_available': True
    }

    with pytest.raises(ParsingError):
        MyClass52(description="Short", quantity=0, is_available="True")


def test_my_class53():
    class MyClass53(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj53 = MyClass53(name="Alex Turner", age=30, is_student=True)
    assert obj53.name == "Alex Turner"
    assert obj53.age == 30
    assert obj53.is_student is True
    assert obj53.to_dict() == {'name': 'Alex Turner', 'age': 30, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass53(name="A", age=200, is_student="True")


def test_my_class54():
    class MyClass54(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj54 = MyClass54(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj54.email == "test@example.com"
    assert obj54.weight == 70.5
    assert obj54.favorite_colors == ["blue", "green"]
    assert obj54.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass54(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])


def test_my_class55():
    class MyClass55(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj55 = MyClass55(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj55.title == "Data Scientist"
    assert obj55.salary == 7000.0
    assert obj55.is_manager is True
    assert obj55.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass55(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class56():
    class MyClass56(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj56 = MyClass56(name="Alice Johnson", age=25, is_student=True)
    assert obj56.name == "Alice Johnson"
    assert obj56.age == 25
    assert obj56.is_student is True
    assert obj56.to_dict() == {'name': 'Alice Johnson', 'age': 25, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass56(name="A", age=200, is_student="True")


def test_my_class57():
    class MyClass57(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(40.0).max(120.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj57 = MyClass57(email="test@example.com", weight=65.0, favorite_colors=["blue", "green"])
    assert obj57.email == "test@example.com"
    assert obj57.weight == 65.0
    assert obj57.favorite_colors == ["blue", "green"]
    assert obj57.to_dict() == {
        'email': 'test@example.com',
        'weight': 65.0,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass57(email="invalid_email", weight=30.0, favorite_colors=["red", "green"])


def test_my_class58():
    class MyClass58(Base):
        title = Coerce('title').string().min_length(5).max_length(100)
        salary = Coerce('salary').float().min(3000.0).max(9000.0)
        is_manager = Coerce('manager').boolean()

    obj58 = MyClass58(title="Data Scientist", salary=7000.0, is_manager=True)
    assert obj58.title == "Data Scientist"
    assert obj58.salary == 7000.0
    assert obj58.is_manager is True
    assert obj58.to_dict() == {
        'title': 'Data Scientist',
        'salary': 7000.0,
        'is_manager': True
    }

    with pytest.raises(ParsingError):
        MyClass58(title="Analyst", salary=1000.0, is_manager="True")


def test_my_class59():
    class MyClass59(Base):
        name = Coerce('name').string().length(3, 30)
        age = Coerce('age').integer().min(0).max(150)
        is_student = Coerce('student').boolean()

    obj59 = MyClass59(name="Alex Turner", age=30, is_student=True)
    assert obj59.name == "Alex Turner"
    assert obj59.age == 30
    assert obj59.is_student is True
    assert obj59.to_dict() == {'name': 'Alex Turner', 'age': 30, 'is_student': True}

    with pytest.raises(ParsingError):
        MyClass59(name="A", age=200, is_student="True")


def test_my_class60():
    class MyClass60(Base):
        email = Coerce('email').string().email()
        weight = Coerce('weight').float().min(50.0).max(150.0)
        favorite_colors = Coerce('fav_colors').list().contains("blue")

    obj60 = MyClass60(email="test@example.com", weight=70.5, favorite_colors=["blue", "green"])
    assert obj60.email == "test@example.com"
    assert obj60.weight == 70.5
    assert obj60.favorite_colors == ["blue", "green"]
    assert obj60.to_dict() == {
        'email': 'test@example.com',
        'weight': 70.5,
        'favorite_colors': ['blue', 'green']
    }

    with pytest.raises(ParsingError):
        MyClass60(email="invalid_email", weight=40.0, favorite_colors=["red", "green"])
