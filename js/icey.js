var comm = new Icecomm('2iEvwDWztV1TVDx9MRO4NexZaD57FeDfWS4FRaRDjygBMfKFi2');

comm.on('local', function(peer) {
  localVideo.src = peer.stream;
});

var addUser = function(peer) {
    document.body.appendChild(peer.getVideo());
    $('#waiting').hide();
}

comm.on('connected', addUser);

comm.on('disconnect', function(peer) {
    document.getElementById(peer.callerID).remove();
    $('#waiting').show();
});

comm.connect('Catholic Hackathon');