from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('collections/', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('collections/<str:cname>/<str:pname>/', views.product_details, name='product_details'),
    # path('fav/', views.fav_page, name="fav"),
    path('cart/', views.cart_page, name="cart"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('addtocart/', views.add_to_cart, name="addtocart"),
    path('check/', views.check_page, name="check"),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('search/', views.product_search, name='product_search'),
    # path('success/', views.success_page, name='success_page'),
    # path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('track-order/', views.track_order, name='track_order'),
]


