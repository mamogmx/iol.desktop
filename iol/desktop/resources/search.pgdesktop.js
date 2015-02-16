$.fn.serializePGQuery = function() {
    var query = {};
    var form = this;
    var info;
    /* Checkboxes become arrays (Zope by default ORs them) */
    $('#' + $(this).attr('id') + ' input[type=checkbox]:checked:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).attr('checked')){
            info = $(this).data();
	        query[this.name] = query[this.name] || {value:[],op:null,type:null,name:null,subname:null};
            query[this.name]['value'].push(this.value);
	        query[this.name]['op']=$("#" + this.name + "_op").val();
	        query[this.name]['type']=$("#" + this.name + "_searchtype").val();
	        query[this.name]['name'] = info['name'];
	        query[this.name]['subname'] = info['subname'];			
        }
    });
    /* Radios become arrays (Zope by default ORs them) */
    $('#' + $(this).attr('id') + ' input[type=radio]:checked:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).attr('checked')){
            info = $(this).data();
	        query[this.name] = query[this.name] || {value:[],op:null,type:null,name:null,subname:null};
            query[this.name]['value'].push(this.value);
	        query[this.name]['op']=$("#" + this.name + "_op").val();
	        query[this.name]['type']=$("#" + this.name + "_searchtype").val();
	        query[this.name]['name'] = info['name'];
	        query[this.name]['subname'] = info['subname'];
        }
    });
    /* Input */
    $('#' + $(this).attr('id') + ' input[type=text]:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).val() && $(this).attr('name')){
            info = $(this).data();
            query[this.name] = query[this.name] || {value:[],op:null,type:null,name:null,subname:null};
            query[this.name]['value'].push($(this).val());
	        query[this.name]['op'] =$("#" + this.name + "_op").val();
            query[this.name]['type'] =$("#" + this.name + "_searchtype").val();
            query[this.name]['name'] = info['name'];
	        query[this.name]['subname'] = info['subname'];
        }
    });
    /*Hidden Fields*/
    $('#' + $(this).attr('id') + ' input[type=hidden]:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).val() && $(this).attr('name')){
            info = $(this).data();
            query[this.name] = query[this.name] || {value:[],op:null,type:null,name:null,subname:null};
            query[this.name]['value'].push($(this).val());
	        query[this.name]['op'] = $("#" + this.name + "_op").val();
            query[this.name]['type'] = $("#" + this.name + "_searchtype").val();
            query[this.name]['name'] = info['name'];
	        query[this.name]['subname'] = info['subname'];
        }
    });
    /*TODO SELECT FIELDS*/
    return query;
};
$.extend( true, $.fn.dataTable.defaults, {    
    "sDom": "<'row-fluid'<'span12'>r>t<'row-fluid'<'span3'l><'span4'i><'span5'p>>",
    "sPaginationType": "bootstrap",
	"oLanguage": {
        "sUrl": "@@collective.js.datatables.translation"
    },
	fnServerParams: function(aoData){
		var cols = this.fnSettings().aoColumns;
		for(i=0;i < cols.length;i++){
			var t = (cols[i]['sType'] == undefined)?('text'):(cols[i]['sType']);
			aoData.push({name:'mDataType_'+i,value:t});
		}
		var data = $('#desktop-object').serializePGQuery();
		aoData.push({'name':'query','value': JSON.stringify(data)});
	},
	fnDrawCallback: function( oSettings ) {
		$("[data-plugins='gotoIstanza']").bind('click',function(event){
			var data = $(this).data();
			window.open(data['url']);
		});
	}
});

function linkIstanza(data,type,full){
    var url = '';
    if (!('object_path' in full))
        url = full['object_url']
    else{
    	if (location.port){
    		if (full['object_path']!=null  && $.isArray(full['object_path']) && full['object_path'].length > 1){
    			url = '/' + full['object_path'].join('/');
    		}
    		else{
    			var pathArray = window.location.pathname.split( '/' );
    			var portal_name = pathArray[0];
    			url="/" + portal_name + "/" + full['plominodb'] + "/" + full['id'];
    		}
    	}
    	else{
    		if (full['object_path']!=null  && $.isArray(full['object_path']) && full['object_path'].length > 1){
    			full['object_path'].shift();
    			url = '/' + full['object_path'].join('/');
    		}
    		else{
    			url="/" + full['plominodb'] + "/" + full['id'];
    		}
    	}
    }
	return '<i class="icon-search linkable" data-plugins="gotoIstanza" data-url="' + url + '"></i>';
}

$(document).ready(function(){
	$("[data-plugins='operator']").bind('change',function(event){
        var id = this.id.replace('_op','');
		if ($(this).val()=='btw'){
			$('#' + id + '_span2').show();
		}
		else{
			$('#' + id + '_span2').hide();
		}
    });
    $("[data-plugins='dynamicsearch']").bind('click',function(event){
        table.fnDraw()
    });
    $('[data-plugins="desktop-search"]').bind('click',function(event){
        event.preventDefault();
        table.fnDraw()
    });

});
