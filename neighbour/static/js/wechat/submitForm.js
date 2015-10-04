/**
 * Created by Administrator on 2015/10/1.
 */
(function($){

    $(function(){

        var $pSelectVillage = $("#pSelectVillage"),
            $divSelectVillage = $("#divSelectVillage"),
            $divVillage = $("#divVillage"),
            $pVillage = $("#pVillage"),
            $spProject = $("#spProject"),
            $spBuilding = $("#spBuilding"),
            $spRoom = $("#spRoom"),
            $spRole = $("#spRole");

        var paramObj = G.getQueryStrObj();

        if(paramObj.type == "edit"){

        }else{
            $divSelectVillage.show();
        }

        $pSelectVillage.click(function(){
            $divSelectVillage.show();
        });

        $divVillage.delegate("li","click",function(){
            var $this = $(this),
                k = $this.attr("key"),
                v = $this.text();
            $pVillage.text(v).attr("key",k);
            $divSelectVillage.hide();
            //window.location.href = "submitForm.shtml?village_id="+k;
        });

        $("#divRole").click(function(){
            G.PopList.addList(ROLE_TYPE,function(k,v){
                $spRole.attr("key",k).text(v);
            }).show();
        });
    });

})(jQuery);