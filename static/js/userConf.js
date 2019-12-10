/* 添加用户模态框 */
/* 添加用户时，添加时间内容获取当前时间 */
$(".addUser").click(function(){
    var nowTime = new Date();
    $('#addDate')[0].value=(nowTime.toLocaleString('chinese', { hour12: false })).replace(/\//g,'-');
    $("#addSta")[0].value='启用';
});

/* 提交按钮单击事件：提交用户信息 */
// $('.addBtn').click(function(){
//     var userName=$('#addUser')[0].value;
//     var userPwd=$('#addPwd')[0].value;
//     var userType=$('#userType')[0].value;
//     var userDate=$('#addDate')[0].value;
//     var addArr=[userName,userPwd,userType,userDate];
//     return addArr;
// }
// );

/* 表格中三个功能图标 （禁用/启用、编辑、删除）*/
/* 修改提示框样式方法 （禁用/启用、删除）*/
function promBox(){
    /* 提示框样式修改 */
    var boxTle=$("#staModalLabel")[0];
    boxTle.innerHTML="提示";
    var modalDialog=$(".userConf_modal");
    modalDialog.css("width","250px");
    modalDialog.css("margin-top","100px");
    var promText=$(".promText");
    promText.css("display","block");
    $(".edtText").css("display","none");
    var modalBody=$(".modalBody");
    modalBody.css("font-size","15px");
    modalBody.css("margin","35px 0");
    $(".modalFooter ").css("padding","0 20px 10px 0");
}

/* 修改提示框样式方法 （编辑）*/
function edtBox(){
    /* 编辑框样式修改 */
    var boxTle=$("#staModalLabel")[0];
    boxTle.innerHTML="编辑";
    var modalDialog=$(".userConf_modal");
    modalDialog.css("width","400px");
    var edtText=$(".edtText");
    edtText.css("display","block");
    $(".promText").css("display","none");
    edtText.css("margin-right","10px");
    var edtIpt=$(".edtIpt");
    var input=$(".edtIpt input[type='text']");
    input.css("width","200px");
}

/* 1.禁用按钮 */
$(".staBtn").click(function(){
    var userid=($(this).parent().siblings("td"))[0].innerHTML;
    var userSta=($(this).parent().siblings("td"))[3];
    var staVal=(userSta.getElementsByClassName("userSta"))[0].innerText;
    if(staVal  ==="启用"){
        $(this).attr("data-toggle","modal");
        $(this).attr("data-target","#staModal");
        promBox();
        $(".promText")[0].innerHTML="确定要禁用吗？";
    }else{
        $(this).attr("data-toggle","modal");
        $(this).attr("data-target","#staModal");
        promBox();
        $(".promText")[0].innerHTML="确定要启用吗？";
    }
    $(".modalBtn").click(function(){
        modify_states(staVal,userid);
    })
});

/* 2.编辑按钮 */
$(".edtBtn").click(function(){
    $(this).attr("data-toggle","modal");
    $(this).attr("data-target","#staModal");
    edtBox();
    var ths=$("#thead").children();
    var thArr=[ths[0].innerHTML,ths[1].innerHTML,ths[5].innerHTML];
    var tds=$(this).parent().siblings("td");
    var tdArr=[tds[0].innerHTML,tds[1].innerHTML,tds[5].innerHTML];
    var thBox=$(".auto");
    var tdBox=$(".edtText input[readonly='readonly']");
    /*获取模态框label内容*/
    for(var a=0;a<thArr.length;a++){
        for(var b=a;b<thBox.length;b++){
            thBox[b].innerHTML=thArr[a];
        }
    }
    /*获取模态框输入框中的内容*/
    for(var c=0;c<tdArr.length;c++){
        for(var d=c;d<tdBox.length;d++){
            tdBox[d].value=tdArr[c];
            var sysDate=new Date();
            tdBox[tdBox.length-1].value=(sysDate.toLocaleDateString()).replace(/\//g,'-');
        }
    }
});

/* 3.删除用户按钮 */
$(".delBtn").click(function(){
    var userSta=($(this).parent().siblings("td"))[0].innerHTML;
    $(this).attr("data-toggle","modal");
    $(this).attr("data-target","#staModal");
    $(".promText")[0].innerHTML="确定要删除此用户吗？";
    promBox();
    $(".modalBtn").click(function(){
        deleteRow(userSta);
    })
});


