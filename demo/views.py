from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from .forms import MemberForm,TransactionsForm,PaymentsForm
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from .models import Member,transactions,payments



# Create your views here.
def index(request):
    return render(request,'index.html')

def add_members(request):
   
    # Generate a unique identifier(ID)
    unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    memberid='FIN'+unique_identifier

    # Ensure the generated unique_id is indeed unique
    while Member.objects.filter(memberid=memberid).exists():
        unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        memberid='FIN'+unique_identifier

    # Pass the unique_id as context data to the template
    context={'memberid':memberid}
    
    return render(request,'add-members.html',context)

def members_view(request):
    
    # Retrieve all fields from the database
    members = Member.objects.all()                  # Member is Name of Model class in models.py
    
    # Pass the members to the template context
    context={'members':members}
    
    # Render the template with the context
    return render(request,'view-members.html',context)








def view_transactions_due(request):
    return render(request,'view-transactions-due.html')

def transactions_report(request):
    return render(request,'transactions-report.html')

def admin_login_page(request):
    return render(request,'adminlogin.html')

def addmembersprocess(request):
    if request.method == "POST":
        form =MemberForm(request.POST,request.FILES)

        if form.is_valid():
            #member_id=form.cleaned_data['memberid']
            #print(member_id)

            # Print some debugging information
            #print(request.FILES)

            form.save() # This line handles the database insertion automatically if the form is valid
            
            
            # Return a JSON response indicating success
            return JsonResponse({'status':200})
        
        else:
            error_messages=form.errors.as_text()
            #print(error_messages)
           
            return JsonResponse({'status':400,'error':error_messages})
    
    # If the request method is not POST or the form is not valid, render the form page
    return render(request,'add-members.html',{'form':MemberForm()})

def view_member_details(request,memberid):

    #Retrieve member details from database based on (or) where member_id
    member=get_object_or_404(Member,memberid=memberid)

    # Pass the retrieved member details to the template context
    context={'memberid':memberid,'member':member}

    return render(request,'view-member-details.html',context)

def updatememberdetails(request,memberid):

    #Retrieve member details from database based on (or) where member_id
    member=get_object_or_404(Member,memberid=memberid)

    #Pass the retrieved member details to the template context
    context={"memberid":memberid,'member':member}

    return render(request,'edit-members.html',context)

def editmembersprocess(request,memberid):
    
    
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)

        if form.is_valid():
            # Retrieve joiningdate from the form data
            joiningdate = form.cleaned_data.get('joiningdate')

            # Get existing record(for ex: where memberid="FINAE364") or create a new one
            instance, created = Member.objects.get_or_create(memberid=memberid, defaults=form.cleaned_data)

            # If the record was not created, update it with the new form data
            if not created:
                for field, value in form.cleaned_data.items():
                    # Exclude updating joiningdate if it is empty
                    if field == 'joiningdate' and not value:
                        continue
                    setattr(instance, field, value)

                instance.save()
            

            return JsonResponse({'status': 200})

        return JsonResponse({'status': 400, 'error': form.errors.as_text()})

    return JsonResponse({'status': 400, 'error': 'Invalid request'})

def removememberdetails(request,memberid):

    # Retrieve the existing record(for ex: where memberid="FINAE364") or return a 404 if not found 
    member=get_object_or_404(Member, memberid=memberid)

    # Delete the record
    member.delete()


    #After Removing record,  Retrieve all members from the database
    members = Member.objects.all()                                    # Member is Name of Model class in models.py
    
    # Pass the members to the template context
    context={'members':members}
    
    # Render the template with the context
    return render(request,'view-members.html',context)

def add_transactions(request):
    
    #Retrieve particular fields(memberid, membername) from database
    members=Member.objects.values('memberid','membername')
    
    currentperiod=1

    # Generate a unique identifier(ID)
    unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    paymentid='PAY'+unique_identifier

    # Ensure the generated unique_id is indeed unique--checking generated unique_id is already exists in the database or not.
    while transactions.objects.filter(paymentid=paymentid).exists():
        unique_identifier=get_random_string(length=5,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        paymentid='FIN'+unique_identifier
    
    # Pass the context data in a dictionary
    context={'members':members,"paymentid":paymentid,'currentperiod':currentperiod}
    return render(request,'add-transactions.html',context)

def add_transactionsprocess(request):

    if request.method=="POST":
        form=TransactionsForm(request.POST)

        

        if form.is_valid():
            
            # Save data in transactionstable
            transactions_instance=form.save()      

            # Create an instance of payments and populate it with the same data
            payment_instance = payments(
                memberidwithname=transactions_instance.memberidwithname,
                paymentid=transactions_instance.paymentid,
                #noofperiods=transactions_instance.noofperiods,
                #paymentdurationtype=transactions_instance.paymentdurationtype,
                basisamounttopay=transactions_instance.basisamounttopay,
                basisamounttopayable=transactions_instance.basisamounttopayable,
                totalamounttopay=transactions_instance.totalamounttopay,
                balanceamounttopay=transactions_instance.balanceamounttopay,
                currentperiod=transactions_instance.currentperiod,
                description=transactions_instance.description,
                transactiondate=transactions_instance.transactiondate,
            )

            # Save data in paymentstable
            payment_instance.save()


            #After saving(insertion), Retrieve all fields from the table(transactionstable)
            transactionsdetail=transactions.objects.all  # transactionsdetail is Name of Model class in models.py

            # Pass the members to the template context
            context={'transactionsdetail':transactionsdetail}

            # Render the template with the context
            return render(request,'view-transactions.html',context)
        
        else:
            error_messages=form.errors.as_text()
            return JsonResponse({'status':400,'error':error_messages})
    
    # If the request method is not POST or the form is not valid, render the form page
    return render(request,'add-members.html',{'form':MemberForm()})

def view_transactions(request):


    # Retrieve all fields from the database
    transactionsdetail=transactions.objects.all  # transactionsdetail is Name of Model class in models.py

    # Pass the members to the template context
    context={'transactionsdetail':transactionsdetail}

    # Render the template with the context
    return render(request,'view-transactions.html',context)

def pay_transactions(request):
    
    #Retrieve particular fields(memberidwithname) from database
    transactionsdetail=transactions.objects.values('memberidwithname')

    return render(request,'pay-transactions.html',{'transactionsdetail':transactionsdetail})

def get_member_data(request):
    memberidwithname=request.GET.get('memberidwithname',None)

    if memberidwithname is not None:
        member_data=transactions.objects.filter(memberidwithname=memberidwithname).first()
        
        
        if member_data:
            combined_period_info=f"{member_data.currentperiod} out of {member_data.noofperiods} {member_data.paymentdurationtype}"
            
            data={
                
                "paymentid":member_data.paymentid,
                "totalamounttopay": member_data.totalamounttopay,
                "balanceamounttopay": member_data.balanceamounttopay,
                "basisamounttopayable":member_data.basisamounttopayable,
                "basisamounttopay": member_data.basisamounttopay,
                "currentperiod":member_data.currentperiod,
                "combined_period_info": combined_period_info,
                "noofperiods":member_data.noofperiods,
                "paymentdurationtype":member_data.paymentdurationtype
            }
            
            return JsonResponse(data)
        return HttpResponse(status=400)
    
def pay_transactionsprocess(request):

    if request.method =="POST":
       form=PaymentsForm(request.POST)
       
       if form.is_valid():
        payment_instance=form.save()

        # Check if currentperiod is 10
        if payment_instance.balanceamounttopay == 0:
            status = "Payments Completed"
            # Update values in the transactions table
            transactions.objects.filter(memberidwithname=payment_instance.memberidwithname).update(balanceamounttopay=payment_instance.balanceamounttopay,currentperiod=payment_instance.currentperiod,status=status)
        
        else:
            status = "Incomplete Payment"
            # Update values in the transactions table
            transactions.objects.filter(memberidwithname=payment_instance.memberidwithname).update(balanceamounttopay=payment_instance.balanceamounttopay,currentperiod=payment_instance.currentperiod,status=status)
        
        
        return render(request,'view-transactions-due.html')
       
       
       else:
        error_messages=form.errors.as_text()
        return JsonResponse({'status':400,'error':error_messages})
        
