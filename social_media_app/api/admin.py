from django.contrib import admin
from .models import User , Account , Post , PostLike , Comment , MarketPlace , PrivateG , Public

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(MarketPlace)
admin.site.register(PrivateG)
admin.site.register(Public)
