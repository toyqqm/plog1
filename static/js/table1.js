/*搜索方法*/
function queLog(){
    var logType=$("#logType").val();  //日志类型的值
    var kwdIpt=$("#kwdIpt").val();    //日志关键字的值
    var staDpk=$("#staDpk").val();    //日志开始时间的值
    var endDpk=$("#endDpk").val();    //日志结束时间的值
    var arr=[logType,kwdIpt,staDpk,endDpk];
    var arrName=["日志类型","日志关键字","开始时间","结束时间"];
    var queData=[];
    for(var i=0;i<arrName.length;i++){
        queData.push([arrName[i],arr[i]]);
    }

    Rz_search(queData);
}

/*全选方法*/
$(".ssxAll").click(function(){
    $("#tbody input[type=checkbox]").prop("checked",true);
   var expArr=[];
    $("input[type='checkbox']:checked").each(function(i){//把所有被选中的复选框的值存入数组
        var tdChecked=$(this).parent().siblings("td");
        expArr[i] =tdChecked[0].innerHTML;
    });
    console.log(expArr)
});

/*反选方法*/
$(".ssxBack").click(function(){
    $("#tbody input[type=checkbox]").prop("checked",false);
});

/*调用单选或多选方法*/
function choice(){
    var expArr=[];
    $("input[type='checkbox']:checked").each(function(i){//把所有被选中的复选框的值存入数组
        var tdChecked=$(this).parent().siblings("td");
        expArr[i] = tdChecked[0].innerHTML;
    });
    console.log(expArr)
}



