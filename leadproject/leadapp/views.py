
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from .models import Product, Region , Lead , ProductCategory
from .forms import ProductForm, RegionForm ,LeadForm,RegisterForm
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .serializers import LeadSerializer
from .serializers import RegionSerializer
import getpass
import logging
import openpyxl
from .forms import ProductExcelUploadForm
from django.contrib.auth import logout
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response({
            "success": True,
            "count": products.count(),
            "message": "Products fetched successfully",
            "data": serializer.data
        }, status=200)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Get Products API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@api_view(['GET'])
def get_product_by_id(request, productid):
    try:

        product = Product.objects.get(
            productid=productid
        )

        serializer = ProductSerializer(product)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=200)

    except Product.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Get Product By ID API | Product {productid} not found"
        )

        return Response({
            "success": False,
            "message": "Product not found"
        }, status=404)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Get Product By ID API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@api_view(['GET'])
def get_leads(request):
    try:

        leads = Lead.objects.all()

        serializer = LeadSerializer(
            leads,
            many=True
        )

        return Response({
            "success": True,
            "count": leads.count(),
            "data": serializer.data
        }, status=200)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Get Leads API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@api_view(['GET'])
def get_regions(request):
    try:

        regions = Region.objects.all()

        serializer = RegionSerializer(
            regions,
            many=True
        )

        return Response({
            "success": True,
            "count": regions.count(),
            "data": serializer.data
        }, status=200)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Get Regions API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

from .utils import (
    log_validation_error,
    log_not_found,
    log_exception
)


@api_view(['POST'])
def add_product_api(request):
    try:

        data = request.data.copy()

        data['added_by'] = getpass.getuser()
        data['added_dts'] = datetime.now().time()

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "success": True,
                "message": "Product added successfully",
                "data": serializer.data
            }, status=201)

        log_validation_error(
            "Add Product API",
            serializer.errors
        )

        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=400)

    except Exception as e:

        log_exception(
            "Add Product API",
            e
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@csrf_exempt
@api_view(['POST'])
def add_region_api(request):
    try:
        data = request.data.copy()

        data['added_by'] = getpass.getuser()
        data['added_dts'] = datetime.now().time()

        serializer = RegionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "success": True,
                "message": "Region added successfully",
                "data": serializer.data
            }, status=201)

        logger.error(
            f"Status Code: 400 | Add Region API | Validation Error | {serializer.errors}"
        )

        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=400)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Add Region API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)
    
@csrf_exempt
@api_view(['POST'])
def add_lead_api(request):
    try:
        data = request.data.copy()

        data['added_by'] = getpass.getuser()
        data['added_dts'] = datetime.now().time()

        serializer = LeadSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "success": True,
                "message": "Lead added successfully",
                "data": serializer.data
            }, status=201)

        logger.error(
            f"Status Code: 400 | Add Lead API | Validation Error | {serializer.errors}"
        )

        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=400)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Add Lead API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@csrf_exempt
@api_view(['PUT'])
def update_product_api(request, pk):

    try:

        product = Product.objects.get(
            productid=pk
        )

        data = request.data.copy()
        data['added_by'] = getpass.getuser()
        data['added_dts'] = datetime.now().time()

        serializer = ProductSerializer(
            product,
            data=data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "success": True,
                "message": "Product updated successfully",
                "data": serializer.data
            })

        logger.error(
            f"Status Code: 400 | Update Product API | Validation Error | {serializer.errors}"
        )

        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=400)

    except Product.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Update Product API | Product {pk} not found"
        )

        return Response({
            "success": False,
            "message": "Product not found"
        }, status=404)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Update Product API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)
    
@csrf_exempt
@api_view(['PUT'])
def update_region_api(request, pk):

    try:

        region = Region.objects.get(
            regionid=pk
        )
        data = request.data.copy()

        data['added_by'] = getpass.getuser()
        data['added_dts'] = datetime.now().time()

        serializer = RegionSerializer(
            region,
            data=data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "success": True,
                "message": "Region updated successfully",
                "data": serializer.data
            })

        logger.error(
            f"Status Code: 400 | Update Region API | Validation Error | {serializer.errors}"
        )

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    except Region.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Update Region API | Region {pk} not found"
        )

        return Response({
            "success": False,
            "message": "Region not found"
        }, status=404)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Update Region API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@csrf_exempt
@api_view(['PUT'])
def update_lead_api(request, pk):

    try:

        lead = Lead.objects.get(
            leadid=pk
        )
        data = request.data.copy()

        data['added_by'] = getpass.getuser()
        data['added_dts'] = datetime.now().time()
        serializer = LeadSerializer(
            lead,
            data=data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "success": True,
                "message": "Lead updated successfully",
                "data": serializer.data
            })

        logger.error(
            f"Status Code: 400 | Update Lead API | Validation Error | {serializer.errors}"
        )

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    except Lead.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Update Lead API | Lead {pk} not found"
        )

        return Response({
            "success": False,
            "message": "Lead not found"
        }, status=404)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Update Lead API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@csrf_exempt
@api_view(['DELETE'])
def delete_product_api(request, pk):

    try:

        product = Product.objects.get(
            productid=pk
        )

        product.delete()

        return Response({
            "success": True,
            "message": "Product deleted successfully"
        })

    except Product.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Delete Product API | Product {pk} not found"
        )

        return Response({
            "success": False,
            "message": "Product not found"
        }, status=404)

    except IntegrityError as e:

        logger.error(
            f"Status Code: 400 | Delete Product API | Integrity Error | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Cannot delete this product because it is being used."
        }, status=400)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Delete Product API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@csrf_exempt
@api_view(['DELETE'])
def delete_region_api(request, pk):

    try:

        region = Region.objects.get(
            regionid=pk
        )

        region.delete()

        return Response({
            "success": True,
            "message": "Region deleted successfully"
        })

    except Region.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Delete Region API | Region {pk} not found"
        )

        return Response({
            "success": False,
            "message": "Region not found"
        }, status=404)

    except IntegrityError as e:

        logger.error(
            f"Status Code: 400 | Delete Region API | Integrity Error | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Cannot delete this region because it is being used."
        }, status=400)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Delete Region API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

@csrf_exempt
@api_view(['DELETE'])
def delete_lead_api(request, pk):

    try:

        lead = Lead.objects.get(
            leadid=pk
        )

        lead.delete()

        return Response({
            "success": True,
            "message": "Lead deleted successfully"
        })

    except Lead.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Delete Lead API | Lead {pk} not found"
        )

        return Response({
            "success": False,
            "message": "Lead not found"
        }, status=404)

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Delete Lead API | {str(e)}"
        )

        return Response({
            "success": False,
            "message": "Internal Server Error"
        }, status=500)

def login_view(request):
    
    print("USER:", request.user)
    print("AUTH:", request.user.is_authenticated)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("LOGIN SUCCESS")
            return redirect('/home/')   # ✅ redirect works only here

        else:
            print("LOGIN FAILED")
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_user(request):

    logout(request)

    return redirect('login')  

@login_required(login_url='/')
def home(request):
    return render(request, 'home.html')

def register(request):

    form = RegisterForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect('login')

    return render(
        request,
        'register.html',
        {'form': form}
    )

def product_list(request):
    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(
            productname__icontains=search
        )
    else:
        products = Product.objects.all()
    
    return render(request, 'product_list.html', {'products': products})

def add_product(request):
    form = ProductForm(request.POST or None)

    try:

        if request.method == 'POST':

            if form.is_valid():

                product = form.save(commit=False)

                max_id = Product.objects.aggregate(
                    Max('productid')
                )['productid__max']

                product.productid = (
                    1 if max_id is None else max_id + 1
                )

                product.added_by = request.user.username
                product.added_dts = datetime.now().time()

                product.save()

                messages.success(
                    request,
                    "Product added successfully."
                )

                return redirect('product_list')

            logger.error(
                f"Status Code: 400 | Add Product Page | Validation Error | {form.errors}"
            )

            messages.error(
                request,
                "Please correct the errors in the form."
            )

    except IntegrityError as e:

        logger.error(
            f"Status Code: 400 | Add Product Page | Integrity Error | {str(e)}"
        )

        messages.error(
            request,
            "Unable to add product."
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Add Product Page | {str(e)}"
        )

        messages.error(
            request,
            "An unexpected error occurred."
        )

    return render(
        request,
        'product_form.html',
        {'form': form}
    )

def upload_products(request):

    form = ProductExcelUploadForm()


    try:

        if request.method == "POST":

            form = ProductExcelUploadForm(
                request.POST,
                request.FILES
            )


            if form.is_valid():

                excel_file = request.FILES['excel_file']


                workbook = openpyxl.load_workbook(
                    excel_file
                )


                sheet = workbook.active


                errors = []


                for row in sheet.iter_rows(
                    min_row=2,
                    values_only=True
                ):

                    productname = row[0]
                    category = row[1]
                    is_active = row[2]


                    # 1. Product name validation

                    if not productname:

                        errors.append(
                            "Product name cannot be empty"
                        )

                        continue



                    # 2. Duplicate validation

                    if Product.objects.filter(
                        productname=productname
                    ).exists():

                        errors.append(
                            f"{productname} already exists"
                        )

                        continue



                    # 3. Category validation

                    if not category:

                        errors.append(
                            f"Category missing for {productname}"
                        )

                        continue



                    # Get category object

                    try:
                        category_obj = ProductCategory.objects.get(
                            categoryname=category
                        )

                    except ProductCategory.DoesNotExist:

                        errors.append(
                            f"Category {category} does not exist"
                        )

                        continue

                    # 4. isactive default

                    if is_active in [None, ""]:

                        is_active = 1



                    max_id = Product.objects.aggregate(
                        Max('productid')
                    )['productid__max']


                    new_id = (
                        1
                        if max_id is None
                        else max_id + 1
                    )


                    Product.objects.create(

                        productid=new_id,

                        productname=productname,

                        categoryid=category_obj,

                        is_active=is_active,

                        added_by=request.user.username,

                        added_dts=datetime.now().time()

                    )


                if errors:

                    return render(
                        request,
                        'upload_products.html',
                        {
                            'form':form,
                            'errors':errors
                        }
                    )


                messages.success(
                    request,
                    "Products uploaded successfully"
                )


                return redirect(
                    'product_list'
                )


    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Product Excel Upload Error | {str(e)}"
        )

        messages.error(
            request,
            "Unable to upload products."
        )


    return render(
        request,
        'upload_products.html',
        {
            'form':form
        }
    )

def edit_product(request, pk):

    try:

        product = get_object_or_404(
            Product,
            pk=pk
        )

        form = ProductForm(
            request.POST or None,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                'product_list'
            )

        if request.method == 'POST':

            logger.error(
                f"Status Code: 400 | Edit Product Page | Validation Error | {form.errors}"
            )

            messages.error(
                request,
                "Please correct the errors in the form."
            )

        return render(
            request,
            'product_form.html',
            {'form': form}
        )

    except Http404:

        logger.error(
            f"Status Code: 404 | Edit Product Page | Product {pk} not found"
        )

        messages.error(
            request,
            "Product not found."
        )

        return redirect('product_list')

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Edit Product Page | {str(e)}"
        )

        messages.error(
            request,
            "Unable to update product."
        )

        return redirect('product_list')

def delete_product(request, pk):
    logger.error("DELETE PRODUCT VIEW CALLED")
    try:

        product = get_object_or_404(
            Product,
            pk=pk
        )

        if Lead.objects.filter(
            productid=product
        ).exists():

            logger.error(
                f"Status Code: 400 | Delete Product Page | Product {pk} is used by leads"
            )

            messages.error(
                request,
                "Cannot delete this product because it is used by one or more leads."
            )

            return redirect(
                'product_list'
            )

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect(
            'product_list'
        )

    except Http404:

        logger.error(
            f"Status Code: 404 | Delete Product Page | Product {pk} not found"
        )

        messages.error(
            request,
            "Product not found."
        )

        return redirect(
            'product_list'
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Delete Product Page | {str(e)}"
        )

        messages.error(
            request,
            "Unable to delete product."
        )

        return redirect(
            'product_list'
        )
    

def region_list(request):
    search = request.GET.get('search')

    if search:
        regions = Region.objects.filter(
            regionname__icontains=search
        )
    else:
        regions = Region.objects.all()

    return render(request, 'region_list.html', {'regions': regions})

def add_region(request):
    form = RegionForm(request.POST or None)

    try:

        if request.method == 'POST':

            if form.is_valid():

                region = form.save(commit=False)

                max_id = Region.objects.aggregate(
                    Max('regionid')
                )['regionid__max']

                region.regionid = (
                    1 if max_id is None else max_id + 1
                )

                region.added_by = request.user.username
                region.added_dts = datetime.now().time()

                region.save()

                messages.success(
                    request,
                    "Region added successfully."
                )

                return redirect('region_list')

            logger.error(
                f"Status Code: 400 | Add Region Page | Validation Error | {form.errors}"
            )

            messages.error(
                request,
                "Please correct the errors in the form."
            )

    except IntegrityError as e:

        logger.error(
            f"Status Code: 400 | Add Region Page | Integrity Error | {str(e)}"
        )

        messages.error(
            request,
            "Unable to add region."
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Add Region Page | {str(e)}"
        )

        messages.error(
            request,
            "An unexpected error occurred."
        )

    return render(
        request,
        'region_form.html',
        {'form': form}
    )


def edit_region(request, pk):

    try:

        region = get_object_or_404(
            Region,
            pk=pk
        )

        form = RegionForm(
            request.POST or None,
            instance=region
        )

        if request.method == 'POST':

            if form.is_valid():

                form.save()

                messages.success(
                    request,
                    "Region updated successfully."
                )

                return redirect(
                    'region_list'
                )

            logger.error(
                f"Status Code: 400 | Edit Region Page | Validation Error | {form.errors}"
            )

            messages.error(
                request,
                "Please correct the errors in the form."
            )

        return render(
            request,
            'region_form.html',
            {'form': form}
        )

    except Http404:

        logger.error(
            f"Status Code: 404 | Edit Region Page | Region {pk} not found"
        )

        messages.error(
            request,
            "Region not found."
        )

        return redirect(
            'region_list'
        )

    except IntegrityError as e:

        logger.error(
            f"Status Code: 400 | Edit Region Page | Integrity Error | {str(e)}"
        )

        messages.error(
            request,
            "Unable to update region."
        )

        return redirect(
            'region_list'
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Edit Region Page | {str(e)}"
        )

        messages.error(
            request,
            "Unable to update region."
        )

        return redirect(
            'region_list'
        )


def delete_region(request, pk):

    try:

        region = get_object_or_404(
            Region,
            pk=pk
        )

        if Lead.objects.filter(
            regionid=region
        ).exists():

            logger.error(
                f"Status Code: 400 | Delete Region Page | Region {pk} is used by leads"
            )

            messages.error(
                request,
                "Cannot delete this region because it is being used by one or more leads."
            )

            return redirect(
                'region_list'
            )

        region.delete()

        messages.success(
            request,
            "Region deleted successfully."
        )

        return redirect(
            'region_list'
        )

    except Http404:

        logger.error(
            f"Status Code: 404 | Delete Region Page | Region {pk} not found"
        )

        messages.error(
            request,
            "Region not found."
        )

        return redirect(
            'region_list'
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Delete Region Page | {str(e)}"
        )

        messages.error(
            request,
            "Unable to delete region."
        )

        return redirect(
            'region_list'
        )

def lead_list(request):
    search = request.GET.get('search')

    if search:
        leads = Lead.objects.filter(
            personname__icontains=search
        )
    else:
        leads = Lead.objects.all()
    return render(request, 'lead_list.html', {'leads': leads})

def add_lead(request):
    form = LeadForm(request.POST or None)

    try:
        x=10/0
        if request.method == 'POST':

            if form.is_valid():

                lead = form.save(commit=False)

                max_id = Lead.objects.aggregate(
                    Max('leadid')
                )['leadid__max']

                lead.leadid = (
                    1 if max_id is None else max_id + 1
                )

                lead.added_by = request.user.username
                lead.added_dts = datetime.now().time()

                lead.save()

                messages.success(
                    request,
                    "Lead added successfully."
                )

                return redirect('lead_list')

            logger.error(
                f"Status Code: 400 | Add Lead Page | Validation Error | {form.errors}"
            )

            messages.error(
                request,
                "Please correct the errors in the form."
            )

    except IntegrityError as e:

        logger.error(
            f"Status Code: 400 | Add Lead Page | Integrity Error | {str(e)}"
        )

        messages.error(
            request,
            "Unable to add lead."
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Add Lead Page | {str(e)}"
        )

        messages.error(
            request,
            "An unexpected error occurred."
        )

    return render(
        request,
        'lead_form.html',
        {'form': form}
    )


def edit_lead(request, pk):

    try:

        lead = get_object_or_404(
            Lead,
            pk=pk
        )

        form = LeadForm(
            request.POST or None,
            instance=lead
        )

        if request.method == 'POST':

            if form.is_valid():

                form.save()

                messages.success(
                    request,
                    "Lead updated successfully."
                )

                return redirect(
                    'lead_list'
                )

            logger.error(
                f"Status Code: 400 | Edit Lead Page | Validation Error | {form.errors}"
            )

            messages.error(
                request,
                "Please correct the errors in the form."
            )

        return render(
            request,
            'edit_lead.html',
            {'form': form}
        )

    except Http404:

        logger.error(
            f"Status Code: 404 | Edit Lead Page | Lead {pk} not found"
        )

        messages.error(
            request,
            "Lead not found."
        )

        return redirect(
            'lead_list'
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Edit Lead Page | {str(e)}"
        )

        messages.error(
            request,
            "Unable to update lead."
        )

        return redirect(
            'lead_list'
        )


def delete_lead(request, pk):

    try:

        lead = Lead.objects.get(
            leadid=pk
        )

        lead.delete()

        messages.success(
            request,
            "Lead deleted successfully."
        )

    except Lead.DoesNotExist:

        logger.error(
            f"Status Code: 404 | Delete Lead Page | Lead {pk} not found"
        )

        messages.error(
            request,
            "Lead not found."
        )

    except Exception as e:

        logger.exception(
            f"Status Code: 500 | Delete Lead Page | {str(e)}"
        )

        messages.error(
            request,
            "Unable to delete lead."
        )

    return redirect('lead_list')

