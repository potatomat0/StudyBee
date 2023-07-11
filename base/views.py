# Provides several shortcuts to common functions, such as `render` and `redirect`.
from django.shortcuts import render, redirect
# Contains classes for handling HTTP requests and responses, such as `HttpResponse`.
from django.http import HttpResponse
# A collection of Django's "contrib" apps, which are bundled with Django but are considered optional.
from django.contrib import messages
# Provides decorators for views that require authentication, such as `login_required`.
from django.contrib.auth.decorators import login_required
# Provides an abstraction layer for interacting with the database, including the `Q` object for complex queries.
from django.db.models import Q
# Provides authentication-related functions, such as `authenticate`, `login`, and `logout`.
from django.contrib.auth import authenticate, login, logout
# Imports the models defined in the local `models.py` file, including `Room`, `Topic`, `Message`, and `User`.
from .models import Room, Topic, Message, User
# Imports the forms defined in the local `forms.py` file, including `RoomForm`, `UserForm`, and `MyUserCreationForm`.
from .forms import RoomForm, UserForm, MyUserCreationForm


# Create your views here.


import re

def loginPage(request):
    # Đặt tên trang là 'login'
    page = 'login'
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if request.user.is_authenticated:
        # Nếu đã đăng nhập, chuyển hướng đến trang chủ
        return redirect('home')
    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, lấy email và mật khẩu từ request.POST
        email = request.POST.get('username')
        password = request.POST.get('password')
        # Kiểm tra xem email có hợp lệ hay không
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            # Nếu không hợp lệ, tìm người dùng có tên người dùng trùng với email
            user = User.objects.filter(username=email).first()
            # Nếu tìm thấy người dùng, lấy email của người dùng đó
            if user:
                email = user.email
        # In ra email để kiểm tra
        print(f'email: {email}')
        # Xác thực người dùng với email và mật khẩu
        user = authenticate(request, email=email, password=password)
        # Kiểm tra xem người dùng có tồn tại hay không
        if user is not None:
            # Nếu tồn tại, đăng nhập người dùng
            login(request, user)
            # Chuyển hướng đến trang chủ
            return redirect('home')
        else:
            # Nếu không tồn tại, hiển thị thông báo lỗi
            messages.error(request, 'Username OR password does not exit')
    # Tạo một từ điển context chứa giá trị page
    context = {'page': page}
     # Hiển thị trang đăng nhập với context được truyền vào
    return render(request, 'base/login_register.html', context)





def logoutUser(request):
    # Đăng xuất người dùng hiện tại
    logout(request)
    # Chuyển hướng đến trang chủ
    return redirect('home')



def registerPage(request):
    # Khởi tạo một biểu mẫu đăng ký mới
    form = MyUserCreationForm()
    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, khởi tạo biểu mẫu với dữ liệu từ request.POST
        form = MyUserCreationForm(request.POST)
        # Kiểm tra xem biểu mẫu có hợp lệ hay không
        if form.is_valid():
            # Nếu hợp lệ, lưu người dùng mới vào cơ sở dữ liệu nhưng chưa commit
            user = form.save(commit=False)
            # Chuyển tên người dùng thành chữ thường
            user.username = user.username.lower()
            # Lưu người dùng vào cơ sở dữ liệu
            user.save()
            # Đăng nhập người dùng mới
            login(request, user)
            # Chuyển hướng đến trang chủ
            return redirect('home')
        else:
            # Nếu biểu mẫu không hợp lệ, hiển thị thông báo lỗi
            messages.error(request, 'An error occurred during registration')
    # Hiển thị trang đăng ký với biểu mẫu được truyền vào
    return render(request, 'base/login_register.html', {'form': form})



def home(request):
    # Lấy giá trị của tham số q từ GET request nếu có, nếu không thì gán cho nó một chuỗi rỗng
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Truy vấn cơ sở dữ liệu để lấy các phòng (Room) có tên chủ đề, tên hoặc mô tả chứa giá trị của q
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    # Lấy 5 chủ đề đầu tiên (Topic) từ cơ sở dữ liệu
    topics = Topic.objects.all()[0:5]
    # Đếm số lượng phòng (rooms) được trả về từ truy vấn
    room_count = rooms.count()
    # Truy vấn cơ sở dữ liệu để lấy 3 tin nhắn đầu tiên (Message) có tên chủ đề của phòng chứa giá trị của q
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    # Tạo một từ điển context chứa các giá trị rooms, topics, room_count và room_messages
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    # Sử dụng hàm render để hiển thị trang base/home.html với context được truyền vào
    return render(request, 'base/home.html', context)



# Định nghĩa một hàm có tên là room, nhận vào 2 tham số là request và pk
def room(request, pk):
    # Lấy ra đối tượng Room có id bằng với pk
    room = Room.objects.get(id=pk)
    # Lấy ra tất cả các tin nhắn trong phòng
    room_messages = room.message_set.all()
    # Lấy ra tất cả người tham gia trong phòng
    participants = room.participants.all()
    # Kiểm tra nếu phương thức của request là POST
    if request.method == 'POST':
        # Tạo một đối tượng Message mới
        message = Message.objects.create(
            user=request.user,  # người dùng gửi tin nhắn là người dùng hiện tại
            room=room,  # phòng gửi tin nhắn là phòng hiện tại
            body=request.POST.get('body')  # nội dung tin nhắn lấy từ dữ liệu POST
        )
        # Thêm người dùng hiện tại vào danh sách người tham gia của phòng
        room.participants.add(request.user)
        # Chuyển hướng đến trang của phòng với id của phòng hiện tại
        return redirect('room', pk=room.id)
    # Định nghĩa một biến context chứa các thông tin cần thiết để hiển thị trên trang
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    # Trả về kết quả là một HttpResponse được tạo ra bởi hàm render, sử dụng template base/room.html và biến context
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    # Lấy người dùng có id bằng với pk từ cơ sở dữ liệu
    user = User.objects.get(id=pk)
    # Lấy tất cả các phòng (Room) của người dùng
    rooms = user.room_set.all()
    # Lấy tất cả các tin nhắn (Message) của người dùng
    room_messages = user.message_set.all()
    # Lấy tất cả các chủ đề (Topic) từ cơ sở dữ liệu
    topics = Topic.objects.all()
    # Tạo một từ điển context chứa các giá trị user, rooms, room_messages và topics
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    # Hiển thị trang profile.html với context được truyền vào
    return render(request, 'base/profile.html', context)

# Sử dụng decorator login_required để yêu cầu người dùng phải đăng nhập trước khi truy cập hàm này
# Nếu người dùng chưa đăng nhập, họ sẽ được chuyển hướng đến trang đăng nhập
@login_required(login_url='login')
def createRoom(request):
    # Khởi tạo một biểu mẫu tạo phòng mới
    form = RoomForm()
    # Lấy tất cả các chủ đề (Topic) từ cơ sở dữ liệu
    topics = Topic.objects.all()
    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, lấy tên chủ đề từ request.POST
        topic_name = request.POST.get('topic')
        # Lấy hoặc tạo một chủ đề mới với tên là topic_name
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # Tạo một phòng mới với thông tin từ request.POST và người dùng hiện tại làm chủ phòng
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # Chuyển hướng đến trang chủ
        return redirect('home')
    # Tạo một từ điển context chứa các giá trị form và topics
    context = {'form': form, 'topics': topics}
    # Hiển thị trang room_form.html với context được truyền vào
    return render(request, 'base/room_form.html', context)



# Sử dụng decorator login_required để yêu cầu người dùng phải đăng nhập trước khi truy cập hàm này
# Nếu người dùng chưa đăng nhập, họ sẽ được chuyển hướng đến trang đăng nhập
@login_required(login_url='login')
def updateRoom(request, pk):
    # Lấy phòng có id bằng với pk từ cơ sở dữ liệu
    room = Room.objects.get(id=pk)
    # Khởi tạo một biểu mẫu cập nhật phòng với thông tin của phòng hiện tại
    form = RoomForm(instance=room)
    # Lấy tất cả các chủ đề (Topic) từ cơ sở dữ liệu
    topics = Topic.objects.all()
    # Kiểm tra xem người dùng hiện tại có phải là chủ phòng hay không
    if request.user != room.host:
        # Nếu không phải, trả về thông báo lỗi
        return HttpResponse('Your are not allowed here!!')
    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, lấy tên chủ đề từ request.POST
        topic_name = request.POST.get('topic')
        # Lấy hoặc tạo một chủ đề mới với tên là topic_name
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # Cập nhật thông tin của phòng với dữ liệu từ request.POST
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        # Lưu thay đổi vào cơ sở dữ liệu
        room.save()
        # Chuyển hướng đến trang chủ
        return redirect('home')

    # Tạo một từ điển context chứa các giá trị form, topics và room
    context = {'form': form, 'topics': topics, 'room': room}
    # Hiển thị trang room_form.html với context được truyền vào
    return render(request, 'base/room_form.html', context)


# Sử dụng decorator login_required để yêu cầu người dùng phải đăng nhập trước khi truy cập hàm này
# Nếu người dùng chưa đăng nhập, họ sẽ được chuyển hướng đến trang đăng nhập
@login_required(login_url='login')
def deleteRoom(request, pk):
    # Lấy phòng có id bằng với pk từ cơ sở dữ liệu
    room = Room.objects.get(id=pk)

    # Kiểm tra xem người dùng hiện tại có phải là chủ phòng hay không
    if request.user != room.host:
        # Nếu không phải, trả về thông báo lỗi
        return HttpResponse('Your are not allowed here!!')

    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, xóa phòng khỏi cơ sở dữ liệu
        room.delete()
        # Chuyển hướng đến trang chủ
        return redirect('home')
    # Hiển thị trang delete.html với obj là room được truyền vào
    return render(request, 'base/delete.html', {'obj': room})


# Sử dụng decorator login_required để yêu cầu người dùng phải đăng nhập trước khi truy cập hàm này
# Nếu người dùng chưa đăng nhập, họ sẽ được chuyển hướng đến trang đăng nhập
@login_required(login_url='login')
def deleteMessage(request, pk):
    # Lấy tin nhắn có id bằng với pk từ cơ sở dữ liệu
    message = Message.objects.get(id=pk)

    # Kiểm tra xem người dùng hiện tại có phải là người gửi tin nhắn hay không
    if request.user != message.user:
        # Nếu không phải, trả về thông báo lỗi
        return HttpResponse('Your are not allowed here!!')

    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, xóa tin nhắn khỏi cơ sở dữ liệu
        message.delete()
        # Chuyển hướng đến trang chủ
        return redirect('home')
    # Hiển thị trang delete.html với obj là message được truyền vào
    return render(request, 'base/delete.html', {'obj': message})


# Sử dụng decorator login_required để yêu cầu người dùng phải đăng nhập trước khi truy cập hàm này
# Nếu người dùng chưa đăng nhập, họ sẽ được chuyển hướng đến trang đăng nhập
@login_required(login_url='login')
def updateUser(request):
    # Lấy người dùng hiện tại
    user = request.user
    # Khởi tạo một biểu mẫu cập nhật người dùng với thông tin của người dùng hiện tại
    form = UserForm(instance=user)

    # Kiểm tra xem request có phải là POST hay không
    if request.method == 'POST':
        # Nếu là POST, khởi tạo biểu mẫu với dữ liệu từ request.POST và request.FILES
        form = UserForm(request.POST, request.FILES, instance=user)
        # Kiểm tra xem biểu mẫu có hợp lệ hay không
        if form.is_valid():
            # Nếu hợp lệ, lưu thay đổi vào cơ sở dữ liệu
            form.save()
            # Chuyển hướng đến trang hồ sơ người dùng với id của người dùng hiện tại
            return redirect('user-profile', pk=user.id)

    # Hiển thị trang update-user.html với form được truyền vào
    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    # Lấy giá trị của tham số q từ GET request nếu có, nếu không thì gán cho nó một chuỗi rỗng
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Truy vấn cơ sở dữ liệu để lấy các chủ đề (Topic) có tên chứa giá trị của q
    topics = Topic.objects.filter(name__icontains=q)
    # Hiển thị trang topics.html với topics được truyền vào
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    # Lấy tất cả các tin nhắn (Message) từ cơ sở dữ liệu
    room_messages = Message.objects.all()
    # Hiển thị trang activity.html với room_messages được truyền vào
    return render(request, 'base/activity.html', {'room_messages': room_messages})
