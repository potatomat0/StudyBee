# Nhập module path từ django.urls
from django.urls import path
# Nhập module views từ thư mục hiện tại
from . import views

# Tạo một danh sách các đường dẫn (path) cho ứng dụng
urlpatterns = [
    # Đường dẫn đến trang đăng nhập, gọi hàm loginPage từ views, đặt tên là "login"
    path('login/', views.loginPage, name="login"),
    # Đường dẫn đến trang đăng xuất, gọi hàm logoutUser từ views, đặt tên là "logout"
    path('logout/', views.logoutUser, name="logout"),
    # Đường dẫn đến trang đăng ký, gọi hàm registerPage từ views, đặt tên là "register"
    path('register/', views.registerPage, name="register"),

    # Đường dẫn đến trang chủ, gọi hàm home từ views, đặt tên là "home"
    path('', views.home, name="home"),
    # Đường dẫn đến trang phòng, gọi hàm room từ views với tham số pk là id của phòng, đặt tên là "room"
    path('room/<str:pk>/', views.room, name="room"),
    # Đường dẫn đến trang hồ sơ người dùng, gọi hàm userProfile từ views với tham số pk là id của người dùng, đặt tên là "user-profile"
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    # Đường dẫn đến trang tạo phòng mới, gọi hàm createRoom từ views, đặt tên là "create-room"
    path('create-room/', views.createRoom, name="create-room"),
    # Đường dẫn đến trang cập nhật phòng, gọi hàm updateRoom từ views với tham số pk là id của phòng, đặt tên là "update-room"
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    # Đường dẫn đến trang xóa phòng, gọi hàm deleteRoom từ views với tham số pk là id của phòng, đặt tên là "delete-room"
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    # Đường dẫn đến trang xóa tin nhắn, gọi hàm deleteMessage từ views với tham số pk là id của tin nhắn, đặt tên là "delete-message"
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    # Đường dẫn đến trang cập nhật người dùng, gọi hàm updateUser từ views, đặt tên là "update-user"
    path('update-user/', views.updateUser, name="update-user"),

    # Đường dẫn đến trang chủ đề, gọi hàm topicsPage từ views, đặt tên là "topics"
    path('topics/', views.topicsPage, name="topics"),
    # Đường dẫn đến trang hoạt động, gọi hàm activityPage từ views, đặt tên là "activity"
    path('activity/', views.activityPage, name="activity"),
]
