
from django.contrib import admin
from django.urls import path, include
from accounts import views as accountsViews 
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('', include('base.urls')),
    path('accounts/', include('accounts.urls')),
    path('login/', accountsViews.signin, name='login'),
    path('logout/', accountsViews.signout, name='logout'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('medicines/', include('medicines.urls')),
    path('animals/', include('animals.urls')),
    path('inventory/', include('inventory.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)