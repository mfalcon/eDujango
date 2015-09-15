$(function() {
    $(".datepicker").datepicker({ 
    dateFormat : 'yy-mm-dd',
    changeMonth : true,
    changeYear : true,
    yearRange: '-100y:c+nn',
    monthNamesShort: [ "Enero", "Febrero", "Marzo", "Abril", "Mayo", 
    "Junio", "Julio", "Agosto", "Septiembre", "Octubre", 
    "Noviembre", "Diciembre" ],
    });
});