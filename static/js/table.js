function labelNam(){
    var th=document.getElementById("addTh").getElementsByTagName("th");
    console.log(th);
    var arr=[];
    for(var i=0;i<th.length;i++){
        var thText=th[i].innerHTML;
        //console.log(typeof thText.length);
        /*if(thText.length < 4){
            $(".labTh").css("padding-left","30px");
        }*/
        arr.push(thText);
    }
    var labTh=document.getElementsByClassName("labTh");
    for(var a=0;a<arr.length;a++){
        for(var b=a;b<labTh.length;b++){
            labTh[b].innerHTML=arr[a];
        }

    }
}


$("#opeTb tr").click( function() {
    console.log(this);
    var td=$(this).find("td");
    for(var a=1;a<td.length;a++){
        //console.log(td[a]);
        $(td[a]).attr("data-toggle","modal");
        $(td[a]).attr("data-target","#mdyModal");
        console.log(td);
    }
    var modulBox=$(".mdymodalBody")[0].getElementsByTagName("input");
        for(var j=0;j<td.length;j++){
            for(var i=j;i<modulBox.length;i++){
                modulBox[i].value=td[j+1].innerHTML;
            }
        }
} );






//点击每行复选框，选中当前行的数据
$("#opeTb tr .delChk").click(function(){
    var isChecked = $(this).prop("checked");
    var tdChecked=$(this).parent().siblings("td");
    tdChecked.prop("checked", isChecked);
    serial_nbr=tdChecked[0].innerHTML;
});

//调用删除方法
function delRow() {
    deleteRow(serial_nbr);
}

