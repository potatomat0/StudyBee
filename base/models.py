# Nhập models từ django.db
from django.db import models
# Nhập AbstractUser từ django.contrib.auth.models
from django.contrib.auth.models import AbstractUser

# Tạo lớp User kế thừa từ AbstractUser
class User(AbstractUser):
    # Tạo trường tên với độ dài tối đa là 200 ký tự, có thể để trống
    name = models.CharField(max_length=200, null=True)
    # Tạo trường email là duy nhất và có thể để trống
    email = models.EmailField(unique=True, null=True)
    # Tạo trường bio có thể để trống
    bio = models.TextField(null=True)
    # Tạo trường avatar có thể để trống và mặc định là "avatar.svg"
    avatar = models.ImageField(null=True, default="avatar.svg")
    # Đặt trường email làm USERNAME_FIELD
    USERNAME_FIELD = 'email'
    # Đặt REQUIRED_FIELDS là một danh sách rỗng
    REQUIRED_FIELDS = []

# Tạo lớp Topic kế thừa từ models.Model
class Topic(models.Model):
    # Tạo trường tên với độ dài tối đa là 200 ký tự
    name = models.CharField(max_length=200)

    # Phương thức __str__ trả về tên của chủ đề
    def __str__(self):
        return self.name

# Tạo lớp Room kế thừa từ models.Model
class Room(models.Model):
    # Tạo trường host liên kết với lớp User, khi xóa sẽ đặt giá trị null và có thể để trống
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Tạo trường topic liên kết với lớp Topic, khi xóa sẽ đặt giá trị null và có thể để trống
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # Tạo trường tên với độ dài tối đa là 200 ký tự
    name = models.CharField(max_length=200)
    # Tạo trường mô tả có thể để trống và không bắt buộc nhập liệu
    description = models.TextField(null=True, blank=True)
    # Tạo trường participants liên kết nhiều-nhiều với lớp User và không bắt buộc nhập liệu
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    # Tạo trường updated tự động cập nhật khi lưu đối tượng
    updated = models.DateTimeField(auto_now=True)
    # Tạo trường created tự động cập nhật khi tạo đối tượng mới
    created = models.DateTimeField(auto_now_add=True)
    # Định nghĩa lớp Meta để sắp xếp theo thứ tự giảm dần của updated và created
    class Meta:
        ordering = ['-updated', '-created']
    # Phương thức __str__ trả về tên của phòng
    def __str__(self):
        return self.name

# Tạo lớp Message kế thừa từ models.Model
class Message(models.Model):
    # Tạo trường user liên kết với lớp User, khi xóa sẽ xóa luôn message này
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Tạo trường room liên kết với lớp Room, khi xóa sẽ xóa luôn message này
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # Tạo trường body chứa nội dung tin nhắn
    body = models.TextField()
    # Tạo trường updated tự động cập nhật khi lưu đối tượng
    updated = models.DateTimeField(auto_now=True)
    # Tạo trường created tự động cập nhật khi tạo đối tượng mới
    created = models.DateTimeField(auto_now_add=True)

     # Định nghĩa lớp Meta để sắp xếp theo thứ tự giảm dần của updated và created
    class Meta:
        ordering = ['-updated', '-created']

    # Phương thức __str__ trả về 50 ký tự đầu tiên của body
    def __str__(self):
        return self.body[0:50]
