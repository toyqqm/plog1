from django.core.exceptions import ObjectDoesNotExist
import json
from django.shortcuts import redirect
from pip._internal.utils import logging
from warehouse.models import *
from django.db.models import Q
from django.shortcuts import render, HttpResponse
import xlwt
from io import StringIO, BytesIO
from django.views.decorators.cache import never_cache
from warehouse.HslCommunication import SiemensS7Net
from warehouse.HslCommunication import SiemensPLCS
import requests


def printReadResult(result):
    if result.IsSuccess:
        print(result.Content)
    else:
        print("failed   " + result.Message)


def printWriteResult(result):
    if result.IsSuccess:
        print("success")
    else:
        print("falied  " + result.Message)


@never_cache
def login(request):
    if request.method == 'GET':

        return render(request, 'page-login.html', locals())
    else:
        uname = request.POST['username']
        print(uname)
        upwd = request.POST['password']
        print(upwd)
        uList = Users.objects.filter(username=uname)
        print(uList)

        if uList:
            for u in uList:
                if u.states == '启用' and u.password == upwd:
                    request.session['uname'] = uname
                    return render(request, 'index.html', )
                print("用户名密码错误")
                return HttpResponse("用户名密码错误")
        else:
            # ptint("用户不存在")
            return HttpResponse("用户不存在")


@never_cache
def index(request):
    all_list_index = SortScanNode.objects.all()
    Sn_Count = SortScanNode.objects.all().count()
    Opcaddr_Count = OpcAddressTb.objects.all().count()
    Rn_Count = RouteNode.objects.all().count()
    rz_count = Rizhibiao.objects.filter(rizhiguanjianzi='报错').count()
    yc_count = Rizhibiao.objects.filter(rizhileixing='异常日志').count()
    listx = []
    listy = []
    print(all_list_index)
    for i in all_list_index:
        listx.append(int(i.scan_node))
        listy.append(str(i.device_zone))
    return render(request, 'index.html', {'all_list_index': all_list_index, 'x': listx,
                                          'y': listy, 'Sn_Count': Sn_Count,
                                          'Opcaddr_Count': Opcaddr_Count,
                                          'Rn_Count': Rn_Count, 'rz_count': rz_count,
                                          'yc_count': yc_count, })


@never_cache
def conveyerLine(request):
    all_list = SortScanNode.objects.all()
    sbids = request.GET.get('sbid')
    print(sbids)
    list_sbid = Ssx.objects.filter(sbid=sbids)
    if list_sbid:
        request.session['sbids'] = sbids
    return render(request, 'conveyerLine.html', {'all_list': all_list})
    # else:
    #     pass


def Search(requset):
    sbids = requset.GET.get('device_name')
    print(sbids)
    list_sbid = SortScanNode.objects.filter(device_name__contains=sbids)
    print(list_sbid)
    if list_sbid:
        requset.session['sbids'] = sbids
        return render(requset, 'conveyerLine.html', {'list_sbid': list_sbid})
    else:
        return render(requset, 'conveyerLine.html', locals())


def login_out(request):
    try:
        if request.session['uname']:
            del request.session['uname']
    except KeyError as e:
        logging.warning(e)
    return redirect('/')


def Add(requset):
    device_name = requset.GET.get('device_name')

    device_zone = requset.GET.get('device_zone')

    node = requset.GET.get('scan_node')
    ip = requset.GET.get('scan_ip')
    port = requset.GET.get('scan_port')
    ssx = SortScanNode()
    ssx.device_name = device_name
    ssx.device_zone = device_zone
    ssx.scan_node = node
    ssx.scan_ip = ip
    ssx.scan_port = port
    try:
        ssx.save()
    except ObjectDoesNotExist as e:
        return HttpResponse(e)

    return redirect('conveyerLine')


def Delete(request):
    serial_nbr = request.GET.get('serial_nbr')
    print(serial_nbr)
    try:
        delsbid = SortScanNode.objects.filter(serial_nbr=serial_nbr)
        print('删除这条数据:', delsbid)
        if delsbid:
            delsbid.delete()
        else:
            delsbid.delete()
    except BaseException as e:
        logging.warning(e)
    return redirect('conveyerLine')


def Midified(request):
    ids = request.GET.get('serial_nbr')
    device_name = request.GET.get('device_name')
    device_zone = request.GET.get('device_zone')
    node = request.GET.get('scan_node')
    ip = request.GET.get('scan_ip')
    port = request.GET.get('scan_port')
    try:
        SortScanNode.objects.filter(serial_nbr=ids).update(device_name=device_name, device_zone=device_zone,
                                                           scan_node=node,
                                                           scan_ip=ip, scan_port=port)
    except BaseException as e:
        logging.warning(e)
    return redirect('conveyerLine')


# address 数据功能展示
@never_cache
def Address(request):
    addr_list = OpcAddressTb.objects.all()
    return render(request, 'address.html', {'addr_list': addr_list})


def Addr_Search(request):
    serial_nbr = request.GET.get('serial_nbr')
    print(serial_nbr)
    list_search = OpcAddressTb.objects.filter(serial_nbr__contains=serial_nbr)
    print(list_search)
    if list_search:
        request.session['serial_nbr'] = serial_nbr
        return render(request, 'address.html', {'list_search': list_search})
    else:
        return render(request, 'address.html', locals())


def Addr_Add(request):
    serial_nbr = request.GET.get('serial_nbr')
    plc_no = request.GET.get('plc_no')
    plc_node = request.GET.get('plc_node')
    route_Addr = request.GET.get('route_addr')
    readflag_Addr = request.GET.get('readflag_addr')
    device_zone = request.GET.get('device_zone')
    oat = OpcAddressTb()
    oat.serial_nbr = serial_nbr
    oat.plc_no = plc_no
    oat.plc_node = plc_node
    oat.route_addr = route_Addr
    oat.readflag_addr = readflag_Addr
    oat.device_zone = device_zone
    try:
        oat.save()
    except ObjectDoesNotExist as e:
        return HttpResponse(e)

    return redirect('Address')


def Addr_Delete(request):
    serial_nbr = request.GET.get('serial_nbr')
    print(serial_nbr)
    try:
        delsbid = OpcAddressTb.objects.filter(serial_nbr=serial_nbr)
        print('删除这条数据:', delsbid)
        if delsbid:
            delsbid.delete()
        else:
            delsbid.delete()
    except BaseException as e:
        logging.warning(e)
    return redirect('Address')


def Addr_Midified(request):
    serial_nbr = request.GET.get('serial_nbr')
    plc_no = request.GET.get('plc_no')
    plc_node = request.GET.get('plc_node')
    print(plc_node)
    route_Addr = request.GET.get('route_Addr')
    readflag_Addr = request.GET.get('readflag_Addr')
    device_zone = request.GET.get('device_zone')
    print(device_zone)
    OpcAddressTb.objects.filter(serial_nbr=serial_nbr).update(plc_no=plc_no, plc_node=plc_node,
                                                              route_addr=route_Addr, readflag_addr=readflag_Addr,
                                                              device_zone=device_zone)

    return redirect('Address')


# Rddress串口表数据功能展示
@never_cache
def Rddress(request):
    route_list = RouteNode.objects.all()
    print('所有数据', route_list)
    return render(request, 'route.html', {'route_list': route_list})


def Route_Search(request):
    serialNo = request.GET.get('serialno')
    print(serialNo)
    list_serialno = RouteNode.objects.filter(serialno__contains=serialNo)
    print(list_serialno)
    if list_serialno:
        request.session['serialNo'] = serialNo
        return render(request, 'route.html', {'list_serialno': list_serialno})
    else:
        return render(request, 'route.html', locals())


def Route_Add(request):
    serialno = request.GET.get('serialno')
    sourceNode = request.GET.get('dextinnode')
    destinNode = request.GET.get('destinnode')
    rounds = RouteNode()
    rounds.serialno = serialno
    rounds.sourcenode = sourceNode
    rounds.destinnode = destinNode
    try:
        rounds.save()
    except ObjectDoesNotExist as e:
        return HttpResponse(e)

    return redirect('Rddress')


def Route_Delete(request):
    serialNo = request.GET.get('serial_nbr')
    print(serialNo)
    try:
        delsbid = RouteNode.objects.filter(serialno=serialNo)
        print('删除这条数据:', delsbid)
        if delsbid:
            delsbid.delete()
        else:
            delsbid.delete()
    except BaseException as e:
        logging.warning(e)
    return redirect('Rddress')


def Route_Midified(request):
    serialNo = request.GET.get('serialno')
    sourceNode = request.GET.get('sourcenode')
    destinNode = request.GET.get('destinnode')
    print('输入的数据', destinNode)
    try:
        RouteNode.objects.filter(serialno=serialNo).update(serialno=serialNo, sourcenode=sourceNode,
                                                           destinnode=destinNode)
    except BaseException as e:
        logging.warning(e)
    return redirect('Rddress')


# 日志数据处理
@never_cache
def lineNomalLog(request):
    name = request.session.get('uname')
    print(name)
    aut_list = Users.objects.filter(username=name)
    for aut in aut_list:

        print('登陆用户', aut.authority)
        if aut.authority == '普通用户':
            return HttpResponse('该用户没有权限访问页面')
        else:
            listrz = Rizhibiao.objects.all()
            return render(request, 'lineNomalLog.html', {'listrz': listrz})


# 多个条件查询日志
def Rizhi_Search(request):
    rz_list = []
    rizhileixing = request.POST.get('dropdown')
    print(rizhileixing)
    rizhiguanjianzi = request.POST.get('rizhiguanjianzi')
    print(rizhiguanjianzi)
    datetime1 = request.POST.get('datetime1')
    print("开始时间", datetime1)
    datetime2 = request.POST.get('datetime2')
    print("结束时间", datetime2)
    if rizhileixing:
        rz_list.append(rizhileixing)
    if rizhiguanjianzi:
        rz_list.append(rizhiguanjianzi)
    if datetime1:
        rz_list.append(datetime1)
    if datetime2:
        rz_list.append(datetime2)
        print(rz_list)
    if len(rz_list) == 4:
        data_list = Rizhibiao.objects.filter(
            Q(datatime__gte=datetime1) & Q(datatime__lte=datetime2) & Q(rizhileixing=rizhileixing) & Q(
                rizhiguanjianzi=rizhiguanjianzi))
        return render(request, 'lineNomalLog.html', {'data_list': data_list})
    elif len(rz_list) == 3:
        if rz_list[0] == rizhileixing and rz_list[1] == datetime1 and rz_list[2] == datetime2:
            data_list = Rizhibiao.objects.filter(
                Q(rizhileixing=rizhileixing) & Q(datatime__gte=datetime1) & Q(datatime__lte=datetime2))
            return render(request, 'lineNomalLog.html', {'data_list': data_list})
        elif rz_list[0] == rizhiguanjianzi and rz_list[1] == datetime1 and rz_list[2] == datetime2:
            data_list = Rizhibiao.objects.filter(
                Q(datatime__gte=datetime1) & Q(datatime__lte=datetime2) & Q(rizhiguanjianzi=rizhiguanjianzi))
            return render(request, 'lineNomalLog.html', {'data_list': data_list})

    elif len(rz_list) == 2:
        if rz_list[0] == rizhileixing and rz_list[1] == rizhiguanjianzi:
            data_list = Rizhibiao.objects.filter(Q(rizhileixing=rizhileixing) & Q(rizhiguanjianzi=rizhiguanjianzi))
            return render(request, 'lineNomalLog.html', {'data_list': data_list})
        elif rz_list[0] == datetime1 and rz_list[1] == datetime2:
            data_list = Rizhibiao.objects.filter(Q(datatime__gte=datetime1) & Q(datatime__lte=datetime2))
            return render(request, 'lineNomalLog.html', {'data_list': data_list})

    elif len(rz_list) == 1:
        print('一个条件：', rz_list)
        if rz_list[0] == rizhileixing:
            data_list = Rizhibiao.objects.filter(rizhileixing=rizhileixing)
            return render(request, 'lineNomalLog.html', {'data_list': data_list})
        elif rz_list[0] == rizhiguanjianzi:
            data_list = Rizhibiao.objects.filter(rizhiguanjianzi=rizhiguanjianzi)
            return render(request, 'lineNomalLog.html', {'data_list': data_list})
        elif rz_list[0] == datetime1:
            data_list = Rizhibiao.objects.filter(datatime=datetime1)
            return render(request, 'lineNomalLog.html', {'data_list': data_list})

    else:
        return render(request, 'lineNomalLog.html', locals())


# 导出excel数据
def output(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')
    # 设置文件头的样式
    # style_heading = xlwt.easyxf("""
    #             font:
    #                 name Arial,
    #                 colour_index white,
    #                 bold on,
    #                 height 0xA0;
    #             align:
    #                 wrap off,
    #                 vert center,
    #                 horiz center;
    #             pattern:
    #                 pattern solid,
    #                 fore-colour 0x19;
    #             borders:
    #                 left THIN,
    #                 top THIN,
    #                 bottom THIN;
    #             """)
    # 1st line
    sheet.write(0, 0, 'id', )
    sheet.write(0, 1, '日志类型', )
    sheet.write(0, 2, '日志关键字', )
    sheet.write(0, 3, '日志编号', )
    sheet.write(0, 4, '日志明细', )
    sheet.write(0, 5, '日志时间', )
    listid = request.POST.getlist('check_box_list')
    print(listid)
    data_row = 1
    for i in listid:
        rz_list = Rizhibiao.objects.filter(id=i)
        print(rz_list)
        for z in rz_list:
            oper_time = z.datatime.strftime('%Y-%m-%d')
            print(oper_time)
            print(z.id)
            sheet.write(data_row, 0, z.id)
            print("id", sheet)
            sheet.write(data_row, 1, z.rizhileixing)
            sheet.write(data_row, 2, z.rizhiguanjianzi)
            sheet.write(data_row, 3, z.rizhibianhao)
            sheet.write(data_row, 4, z.rizhimingxi)
            sheet.write(data_row, 5, oper_time)
            data_row = data_row + 1
    output = BytesIO()
    wb.save(output)
    print('保存成功', wb)
    output.seek(0)
    response.write(output.getvalue())
    print('最后一步')
    return response


# 用户管理
@never_cache
def userConf(request):
    list_user = Users.objects.all()

    return render(request, 'userConf.html', {'list_user': list_user})


def add_user(request):
    print('进入增加用户')
    new_user = Users()
    if request.method == 'POST':
        # 获取用户信息插入到 Users 表中,继续向new_user中增加数据
        new_user.username = request.POST['addUser']
        new_user.password = request.POST['password']
        new_user.authority = request.POST['dropdown']
        new_user.creationtimes = request.POST['addDate']
        new_user.states = request.POST['addSta']
        try:
            new_user.save()
        except ObjectDoesNotExist as e:
            return HttpResponse(e)
    list_user = Users.objects.all()
    return render(request, 'userConf.html', {'list_user': list_user})


def user_Search(request):
    print('进入搜索功能')
    username = request.GET.get('username')
    print(username)
    name_list = Users.objects.filter(username__contains=username)
    print(name_list)
    rejson = []

    for recontent in name_list:
        rejson.append(recontent.username)

    return render(request, 'userConf.html', {'name_list': name_list, 'rejson': rejson})


def Pwd_Midified(request):
    list_user = Users.objects.all()

    name = request.GET.get('userName')
    print(name)
    tdata = request.GET.get('edtDate')
    print(tdata)
    pwd = request.GET.get('password')
    print(pwd)

    try:
        Users.objects.filter(username=name).update(password=pwd, updatetimes=tdata)
    except BaseException as e:
        logging.warning(e)

    return render(request, 'userConf.html', {'list_user': list_user})


def deluser(request):
    userid = request.GET.get('userSta')
    print(userid)
    ids = Users.objects.filter(id=userid)
    try:
        ids = Users.objects.filter(id=userid)
        print('删除这条数据:', ids)
        if ids:
            ids.delete()
        else:
            ids.delete()
    except BaseException as e:
        logging.warning(e)
    list_user = Users.objects.all()

    return render(request, 'userConf.html', {'list_user': list_user})


def user_states(request):
    states = request.GET.get('staVal')
    userid = request.GET.get('userid')
    print(userid)
    if states == '启用':
        state = '禁用'
        try:
            Users.objects.filter(id=userid).update(states=state)
        except BaseException as e:
            logging.warning(e)
    else:
        state = '启用'
        try:
            Users.objects.filter(id=userid).update(states=state)
        except BaseException as e:
            logging.warning(e)
    content = {'status': 'Ok'}
    return HttpResponse(json.dumps(content))
