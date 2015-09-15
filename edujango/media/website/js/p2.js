/*jQuery.noConflict();*/
jQuery(function($) { 
        
    // Superfish
    $("ul.sf-menu").supersubs({ 
        minWidth:    10,   // minimum width of sub-menus in em units 
        maxWidth:    25,   // maximum width of sub-menus in em units 
        extraWidth:  1     // extra width can ensure lines don't sometimes turn over 
                           // due to slight rounding differences and font-family 
    }).superfish({
        delay:          300,
        dropShadows:    false
    });  // call supersubs first, then superfish, so that subs are 
                     // not display:none when measuring. Call before initialising 
                     // containing tabs for same reason. 
            

    // Full page background
    $.supersized({
        //Background image
        slides  :  [ { image : '../img/bg1.jpg' }, { image : 'img/bg2.jpg' } ]
    });            
    
    // Cufon
    Cufon.replace('.replace,.sidebar-widget h4',{fontFamily: 'Museo 500'} );
    Cufon.replace('.sf-menu a',{fontFamily: 'Museo Sans 500'} );
    
    // ColorBox
    $(".video_modal").colorbox({iframe:true, innerWidth:"50%", innerHeight:"50%"});
    $("a[rel='example1']").colorbox();
    $("a[rel='example2']").colorbox({transition:"fade"});
    $("a[rel='example3']").colorbox({transition:"none"});
    $("a[rel='example4']").colorbox({slideshow:true});

    // Scroll to Top
    $('#toTop').click(function() {
        $('#content-wrapper').animate({scrollTop:0},600);
    }); 
        
    // Google Map
    $("#modalmap").colorbox({iframe:true, innerWidth:"50%", innerHeight:"50%", href:" http://maps.google.com/maps/ms?ie=UTF8&msa=0&msid=212476298631221746799.0004a40673151101aad4d&ll=-34.584377,-58.574377&spn=0.006704,0.013872&z=17&iwloc=0004a406731eb86a404bd" });
});




