var csrftoken;
// {% load static %}
$( document ).ready(function() {
    csrftoken = $('input[name=csrfmiddlewaretoken]').attr('value');
    // alert("{% url 'Music:record' %}");
    // console.log(csrftoken);
    
    $(".result").on("click",".song",function(){
      var src = $(this).attr('value');
      var song_id = $(this).attr('song_id');
      record(song_id);
      console.log(" playing id="+song_id);
      window.location = ''+song_id
    });

    console.log( "ready!" );
    $( window ).unload(function() {
      next_song = $('source').attr('next_song_id');
      record(next_song); 
    });

    $("audio").on('ended', function(){
      // done playing
      next_song = $('source').attr('next_song_id');
      console.log("Playing next Song "+ next_song);
      record(next_song);
      window.location = './'+next_song
    });
});

function record(next_song){
    var csrftoken = $('input[name=csrfmiddlewaretoken]').attr('value');
    // var url = "{% url 'Music:record' %}";
    var url= "/Music/record/";
    var song_id = $('source' ).attr('song_id');
    var per = ($(".audiotrack").prop("currentTime") / $("audio")[0].duration)*100;
    console.log("sending to record next_song "+next_song)
    var data = { 'csrfmiddlewaretoken' : csrftoken, 'song_id':song_id, 'per':per, 'next_song':next_song}
    console.log("\n");
    console.log(data);
    console.log("\n");
    $.post( url, data).done(function(data){console.log(data);});
}

