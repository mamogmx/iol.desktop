$.fn.serializePGQuery = function() {
    var query = {};
    var form = this;
    var info;
    /* Checkboxes become arrays (Zope by default ORs them) */
    $('#' + $(this).attr('id') + ' input[type=checkbox]:checked:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).attr('checked')){
            info = $(this).data();
	        query[this.name] = query[this.name] || {value:[],op:null,type:null};
            query[this.name].value.push(this.value);
	        query[this.name].op=$("#" + this.name + "_op").val();
	        query[this.name].type=$("#" + this.name + "_searchtype").val();
	        query[this.name].name = info['name'];
	        query[this.name].subname = info['subname'];
	        query[this.name].value.push(this.value);
        }
    });
    /* Input */
    $('#' + $(this).attr('id') + ' input[type=text]:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).val() && $(this).attr('name')){
            info = $(this).data();
            query[this.name] = query[this.name] || {value:[],op:null,type:null};
            query[this.name].value.push($(this).val());
	        query[this.name].op=$("#" + this.name + "_op").val();
            query[this.name].type=$("#" + this.name + "_searchtype").val();
            query[this.name].name = info['name'];
	        query[this.name].subname = info['subname'];
        }
    });
    /*Hidden Fields*/
    $('#' + $(this).attr('id') + ' input[type=hidden]:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).val() && $(this).attr('name')){
            info = $(this).data();
            query[this.name] = query[this.name] || {value:[],op:null,type:null};
            query[this.name].value.push($(this).val());
	        query[this.name].op=$("#" + this.name + "_op").val();
            query[this.name].type=$("#" + this.name + "_searchtype").val();
            query[this.name].name = info['name'];
	        query[this.name].subname = info['subname'];
        }
    });
    /*TODO SELECT FIELDS*/

    return query;
};

$(document).ready(function(){
    $('.dynamicsearch').bind('click',function(event){
        table.fnDraw()
    });
    $('[data-plugin="search"]').bind('click',function(event){
        event.preventDefault();
        table.fnDraw()
    });

});