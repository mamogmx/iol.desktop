$.fn.serializePGQuery = function() {
    var query = {};
    var form = this;

    /* Checkboxes become arrays (Zope by default ORs them) */
    $('#' + $(this).attr('id') + ' input[type=checkbox]:checked:not([name$="_op"]):not([name$="_searchtype"])').each(function(){
        if($(this).attr('checked')){
	        query[this.name] = query[this.name] || {value:[],op:null,type:null};
            query[this.name].value.push(this.value);
	        query[this.name].op=$("#" + this.name + "_op").val();
	        query[this.name].type=$("#" + this.name + "_searchtype").val();
        }
    });
    $('#' + $(this).attr('id') + ' input[type=text]:not([name$="_op"]):not([name$="_searchtype"])').each(function(){

        if($(this).val() && $(this).attr('name')){
            query[this.name] = query[this.name] || {value:[],op:null,type:null};
            query[this.name].value.push($(this).val());
	        query[this.name].op=$("#" + this.name + "_op").val();
            query[this.name].type=$("#" + this.name + "_searchtype").val();
        }
    });
    $('#' + $(this).attr('id') + ' input[type=hidden]:not([name$="_op"]):not([name$="_searchtype"])').each(function(){

        if($(this).val() && $(this).attr('name')){
            query[this.name] = query[this.name] || {value:[],op:null,type:null};
            query[this.name].value.push($(this).val());
	        query[this.name].op=$("#" + this.name + "_op").val();
            query[this.name].type=$("#" + this.name + "_searchtype").val();
        }
    });

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