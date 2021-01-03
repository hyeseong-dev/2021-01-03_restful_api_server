import json
from django.http                  import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers       import JSONParser

from addresses.models             import Addresses
from addresses.serializers        import AddressesSerializer

@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        query_set  = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def address_detail(request,pk):
    try:
        address = Addresses.objects.get(pk=pk)
    except Addresses.DoesNotExist as e:
        return JsonResponse({'메시지':'Address를 못 찼습니다.'}, status=404)

    if request.method == 'GET':
        serializer = AddressesSerializer(address)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        print('여기는 들어오니?')
        data = JSONParser().parse(request) # 딕셔너리로 변환시킴
        print(data, type(data), '파싱한 데이터유형')
        serializer = AddressesSerializer(address, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Message': '성공적으로 수정했습니다'}, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        address.delete()
        return JsonResponse({'Message': '삭제를 성공적으로 했습니다.'}, status=200)

@csrf_exempt
def login(request):
    try: 
        if request.method == 'POST':
            data            = json.loads(request.body)
            name            = data['name']
            phone_number    = data['phone_number']

            if not name and phone_number:
                return JsonResponse({'Message':'이름과 전화번호를 입력해주세요.'}, status=400)

            if Addresses.objects.filter(name=name, phone_number=phone_number):
                return JsonResponse({'Message': '성공적으로 로그인했어요'}, status=200)
            return JsonResponse({'Message': '가입 정보와 틀려요.'}, status=400)
            


        return JsonResponse({'Message': '오류가 나타났어요.'}, status=400)
    except KeyError:
        return JsonResponse({"Message":"키에러 입니다."}, status=400)
    except Addresses.DoesNotExist:
        return JsonResponse({"Message":"존재하지 않아요."}, status=400)
