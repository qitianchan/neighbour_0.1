/**
 * Created by Administrator on 2015/10/2.
 */

(function(win,$){

    var OPT_SUCCESS = "0000",
        OPT_UNLOGIN = "1000",
        OPT_UNAUTH = "2000";

    var G = {},
        _ajaxOpt = {
            dataType:"json",
            type:"GET",
            timeout:6000,
            handleError:true
        };

    G.ajax = function(opt,succFun,errorFun){
        var _opt = $.extend(_ajaxOpt,opt);

        _opt.success = function(data, textStatus, jqXHR){
            // 不进行错误处理
            if(!opt.handleError){
                if(succFun){
                    succFun(data);
                }
                return;
            }
            if(data.retCode && data.retCode == OPT_SUCCESS){
                succFun(data);
            }else if(data.retCode && data.retCode == OPT_UNLOGIN){

            }else if(data.retCode && data.retCode == OPT_UNAUTH){

            }else{
                toast(data.retMsg);
                if (errorFun) {
                    errorFun();
                }
            }
        };

        $.ajax(_opt);
    };


    /**
     * 吐司
     * @param msg 提示信息
     * @param callback 回调函数
     */
    var toast = function(msg, callback) {
        $("<div style='position: fixed;width: 80%;min-height: 40px;line-height: 40px;left: 10%;top: 50px; border:1px solid #939393;background-color: #f1f1f1;text-align: center;color:#939393;z-index: 999;'>")
            .text(msg)
            .appendTo($("body"))
            .delay(1500)
            .fadeOut(500, function () {
                this.remove();
                if (callback) {
                    callback();
                }
            });
    };

    /**
     * 浮层小气泡报错(3秒后自动消失)
     *
     * @param target 指示对象
     * @param error_text 错误信息
     * @param notAutoFocus 设置为非自动获得焦点
     *
     * modify by wujunxi 2015-07-23
     */
    var tipError = function (target, error_text, notAutoFocus) {
        var $target = $(target),
            w = $target.innerWidth(),
            p = $target.offset(),
            htmlStr = "";
        htmlStr += '<div style="position:absolute; background-color:#fd6868; color:#fff; font-size: 1rem; letter-spacing: 1px;' +
            'width:' + w + 'px;padding:7px;left:' + p.left + 'px;top:' + (p.top + $target.outerHeight() + 6) + 'px;">';
        htmlStr += '<div style="position:absolute;top:-11px;left:17px;width:0;height:0;border-width:6px;border-style:solid;' +
            'border-color:transparent transparent #fd6868 transparent;"></div>';
        htmlStr += '<p>' + error_text + '</p>';
        htmlStr += '</div>';
        var $tip = $(htmlStr).appendTo($("body"));
        (function ($tip) {
            setTimeout(function () {
                $tip.remove();
            }, 3000);
        })($tip);
        if (!notAutoFocus) {
            $target.focus();
        }
    };


    /**
     * 报错/提示
     * @param errorInfo 提示信息
     * @param callback 回掉函数
     */
    var alertError = function(errorInfo, callback) {
        var mask = document.createElement("div");
        mask.className = "mask";
        var pop_up = document.createElement("div");
        pop_up.className = "pop-up";
        pop_up.innerHTML = '<h3>提示</h3><p>' + errorInfo + '</p><div class="btn">确定</div>';
        var bodyNode = document.getElementsByTagName("body")[0];
        bodyNode.appendChild(mask);
        bodyNode.appendChild(pop_up);
        //显示
        $(mask).fadeIn(400);
        $(pop_up).animate({top: $(document).scrollTop() + 140}, 0);
        $(pop_up).fadeIn(400);
        $(window).bind("scroll", function () {
            $(pop_up).css({top: $(document).scrollTop() + 140});
            $(mask).css({top: $(document).scrollTop()});
        });
        //隐藏并删除
        $(pop_up).find(".btn").click(function () {
            $(pop_up).fadeOut(400, function () {
                $(pop_up).remove();
            });
            $(mask).fadeOut(400, function () {
                $(mask).remove();
                if (callback) {
                    callback();
                }
            });
        })
    };


    /**
     * 清除输入框
     */
    G.TouchClear = (function () {
        var opt = {
            attrName: "touch-clear",
            iconClass: "touch-clear-icon",
            off: function () {
                $("body").undelegate(namespace);
            }
        }, namespace = ".touch_clear";
        var obj = {};
        obj["focus" + namespace] = function () {
            var $input = $(this),
                $icon = $input.next("." + opt.iconClass);
            if ($icon.length > 0) {
                $icon.css("display", "inline-block");
            } else {
                $("<span class='" + opt.iconClass + "'>").insertAfter($input)
                    .on({
                        "mouseover": function () {
                            $(this).data("isHover",true);
                        }, "mouseout": function () {
                            $(this).data("isHover",false);
                        }, "click": function () {
                            $input.val("");
                            $(this).hide();
                        }
                    });
            }
        };
        obj["blur" + namespace] = function () {
            var $this = $(this),
                $icon = $this.next("." + opt.iconClass);
            if($icon.length > 0){
                if(!$icon.data("isHover")){
                    $icon.hide();
                }
            }
        };
        //
        $(function () {
            $("body").delegate("input[" + opt.attrName + "]", obj);
        });
        return opt;
    })();

    G.findByAttr = function (list, attrName, val) {
        for (var i = 0, len = list.length; i < len; i++) {
            if (list[i][attrName] == val) {
                return list[i];
            }
        }
        return null;
    };


    /**
     * 将当前页面URL地址参数串转化成Object(decodeURI)
     * @returns {{}}
     */
    G.getQueryStrObj = function () {
        var obj = {},
            url = window.location.href;
        if (url.indexOf("?") == -1) {
            return obj;
        }
        var params = decodeURIComponent(url.substring(url.indexOf("?") + 1));
        if (params != null && params != undefined && params != "") {
            params = params.replace(/\?/, "");
            var arr = params.split('&');
            for (var index = 0; index < arr.length; index++) {
                var pair = arr[index];
                var indexOf = pair.indexOf('=');
                if (indexOf != -1) {
                    var name = pair.substring(0, indexOf);
                    var val = "";
                    if (indexOf != pair.length - 1) {
                        val = pair.substring(indexOf + 1);
                    }
                    obj[name] = val;
                } else {
                    obj[pair] = "";
                }
            }
        }
        return obj;
    };


    G.PopList = (function(){
        var initFlag = false,
            $popWrap,
            $ul,
            callback;
        var obj = {
            init:function(){
                var htmlStr = "<div style='display:block;width:100%;height:100%;position:absolute;top:0;left:0;background-color: #efeff4;'>"+
                    "<ul style='list-style: none;margin:0;padding:0;'></ul></div>";
                $popWrap = $(htmlStr).appendTo("body");
                $ul = $popWrap.children("ul");
                $ul.delegate("li","click",function(){
                    var $this = $(this),
                        k = $this.attr("key"),
                        v = $this.text();
                    if(k != ""){
                        callback(k,v);
                    }
                    obj.hide();
                });
                initFlag = true;
                return obj;
            },
            addList:function(list){
                !initFlag && obj.init();
                var keyName,valName;
                if(arguments.length == 2){
                    callback = arguments[1];
                }else{
                    keyName = arguments[1];
                    valName = arguments[2];
                    callback = arguments[3];
                }
                // clear
                $ul.empty();
                obj.addItem("","< 返回");
                if(keyName && valName){
                    for(var i = 0,len = list.length; i < len; i++){
                        obj.addItem(list[i][keyName],list[i][valName]);
                    }
                }else{
                    for(var k in list){
                        obj.addItem(k,list[k]);
                    }
                }
                return obj;
            },
            addItem:function(k,v){
                !initFlag && obj.init();
                var htmlStr = "<li key='"+k+"' style='line-height:40px;height:40px;margin:5px 0 0 0;padding:0 0 0 10px;background-color:#fff;'>"+v+"</li>";
                $ul.append(htmlStr);
                return obj;
            },
            show:function(){
                $popWrap.show();
            },
            hide:function(){
                $popWrap.hide();
            }
        };

        return obj;
    })();

    /**
     * 加法函数，用来得到精确的加法结果
     * @param arg1
     * @param arg2
     * @returns {number} arg1加上arg2的精确结果
     */
    G.accAdd = function(arg1,arg2){
        var r1,r2,m;
        try{r1=arg1.toString().split(".")[1].length}catch(e){r1=0}
        try{r2=arg2.toString().split(".")[1].length}catch(e){r2=0}
        m=Math.pow(10,Math.max(r1,r2));
        return (arg1*m+arg2*m)/m;
    };
    //给Number类型增加一个add方法，调用起来更加方便，以下类似
    Number.prototype.add = function (arg){
        return $Common.accAdd(arg,this);
    };

    /**
     * 乘法函数，用来得到精确的乘法结果
     * @param arg1
     * @param arg2
     * @returns {number} arg1乘以arg2的精确结果
     */
    G.accMul = function(arg1,arg2)
    {
        var m=0,s1=arg1.toString(),s2=arg2.toString();
        try{m+=s1.split(".")[1].length}catch(e){}
        try{m+=s2.split(".")[1].length}catch(e){}
        return Number(s1.replace(".",""))*Number(s2.replace(".",""))/Math.pow(10,m);
    };
    Number.prototype.mul = function (arg){
        return $Common.accMul(arg,this);
    };

    /**
     * 除法函数，用来得到精确的除法结果
     * @param arg1
     * @param arg2
     * @returns {number} arg1除以arg2的精确结果
     */
    G.accDiv = function(arg1,arg2){
        var t1=0,t2=0,r1,r2;
        try{t1=arg1.toString().split(".")[1].length}catch(e){}
        try{t2=arg2.toString().split(".")[1].length}catch(e){}
        with(Math){
            r1=Number(arg1.toString().replace(".",""));
            r2=Number(arg2.toString().replace(".",""));
            return (r1/r2)*pow(10,t2-t1);
        }
    };
    Number.prototype.div = function (arg){
        return $Common.accDiv(arg,this);
    };

    win.G = G;
    win.toast = toast;
    win.tipError = tipError;
    win.alertError = alertError;


    /**
     * 沙盒
     * @type {Function}
     */
    var Sandbox = win.Sandbox = function () {
        var args = Array.prototype.slice.call(arguments),
            callback = args.pop(),
            modules = (args[0] && typeof args[0] === "string") ? args : args[0],
            i;

        if (!(this instanceof Sandbox)) {
            return new Sandbox(modules, callback);
        }

        if (!modules || modules[0] === "*") {
            for (i in Sandbox.modules) {
                if (Sandbox.modules.hasOwnProperty(i)) {
                    modules.push(i);
                }
            }
        }

        for (i = 0; i < modules.length; i++) {
            try {
                Sandbox.modules[modules[i]](this);
            } catch (e) {
                console.dir(modules[i] + ",," + i);
            }
        }

        callback(this);
    };

    Sandbox.modules = {};

    // 用户模块
    Sandbox.modules.user = function(box){

        /**
         * 获得区域及小区信息
         * @param callback
         */
        box.getAreas = function(callback){
            G.ajax({
                url:GET_AREAS_URL
            },callback);
        };

        /**
         * 获得小区楼宇房号信息
         * @param code
         * @param callback
         */
        box.getAreaByCode = function(code,callback){
            G.ajax({
                url:GET_AREA_BY_CODE_URL,
                data:{code:code}
            },callback);
        };

        /**
         * 获得用户房产信息
         * @param callback
         */
        box.getUserHouseInfo = function(callback){
            G.ajax({
                url:GET_USER_HOSE_INFO_URL
            },callback);
        };
    };

    // 小区服务模块
    Sandbox.modules.server = function(box){

        /**
         * 获得水煤表抄送状态
         * @param callback
         */
        box.getUploadBillStatus = function(callback){
            G.ajax({
                url:GET_UPLOAD_BILL_STATUS_URL
            },callback);
        };

        /**
         * 获得报修记录列表
         * @param callback
         */
        box.getRepairOrders = function(callback){
            G.ajax({
                url:GET_REPAIR_ORDERS_URL
            },callback);
        }

    };

    var GET_AREAS_URL = "/wechat_front/get_areas",
        GET_AREA_BY_CODE_URL = "/wechat_front/get_area_by_code",
        GET_USER_HOSE_INFO_URL = "/wechat_front/get_user_house_info",
        UPDATE_HOSE_INFO_URL = "/wechat_front/update_house_info",
        DELETE_HOSE_INFO_URL = "/wechat_front/delete_house_info",
        GET_UPLOAD_BILL_STATUS_URL = "/wechat_front/getUploadBillDataStatus",
        UPLOAD_BILL_DATA_URL = "/wechat_front/upload_bill_data",
        GET_MONTH_BILL_STATUS_URL = "/wechat_front/get_month_bill_status",
        GET_BILL_URL = "/wechat_front/get_bill",
        UPLOAD_REPAIR_ORDER_URL = "/wechat_front/upload_repair_order",
        GET_REPAIR_ORDERS_URL = "/wechat_front/get_repair_orders",
        GET_REPAIR_ORDER_DETAIL = "/wechat_front/getRepairOrderDetail";

})(window,jQuery);

var TRUE="1",FALSE="0",
    ROLE_TYPE = {0:"业主",1:"家属",2:"房客"},
    FEE_STATUS_TYPE = {0:"未出",1:"已出未缴",2:"已缴"},
    ORDER_STATUS_TYPE = {0:"失效",1:"新建",2:"提交",3:"已受理",4:"已发货",5:"已收货",6:"已评价"};

var FEE_STATUS = {UNKNOWN:"0",UNPAID:"1",PAID:"2"},
    REPAIRS_STATUS = {UNHANDLED:0,ACTIVE:1,FINISH:2},
    ORDER_STATUS = {INVALID:"0",NEW:"1",SUBMIT:"2",ACCEPT:"3",DELIVERY:"4",RECEIPT:"5",EVALUATED:"6"};