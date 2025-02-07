from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index,add_members,members_view,add_transactions,view_transactions,pay_transactions,view_transactions_due,transactions_report,admin_login_page,addmembersprocess,view_member_details,updatememberdetails,editmembersprocess,removememberdetails,add_transactionsprocess,get_member_data,pay_transactionsprocess

urlpatterns=[
    path('', index, name='index'),      # '' is initial url and index is function of views.py and index is name of parameter(optional), if you mentioned like {% url 'index' %} at template it will helps.
    path('add_members',add_members,name='add_members'), # add_members_view is url and add_members_view is function of views.py and add_member_view is name of parameter(optional), if you mentioned like {% url 'add_members_view' %} at template it will helps.
    
    path('members_view',members_view,name='members_view'),
    path('add_transactions',add_transactions,name='add_transactions'),
    path('view_transactions',view_transactions,name='view_transactions'),
    path('pay_transactions',pay_transactions,name='pay_transactions'),
    path('view_transactions_due',view_transactions_due,name='view_transactions_due'),
    path('transactions_report',transactions_report,name='transactions_report'),
    path('admin_login_page',admin_login_page),
    path('addmembersprocess',addmembersprocess,name='addmembersprocess'),
    path('viewmemberdetails/<str:memberid>',view_member_details,name='view_member_details'),
    path('updatememberdetails/<str:memberid>',updatememberdetails,name='updatememberdetails'),
    path('editmembersprocess/<str:memberid>',editmembersprocess,name='editmembersprocess'),
    path('removememberdetails/<str:memberid>',removememberdetails,name='removememberdetails'),
    path('add_transactionsprocess',add_transactionsprocess,name='add_transactionsprocess'),
    path('get_member_data/',get_member_data,name='get_member_data'),
    path('pay_transactionsprocess',pay_transactionsprocess,name='pay_transactionsprocess')
]


# Add these lines at the end of the file for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)