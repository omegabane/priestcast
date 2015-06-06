var comm = new Icecomm('2iEvwDWztV1TVDx9MRO4NexZaD57FeDfWS4FRaRDjygBMfKFi2');

comm.on('local', function(options) {
  localVideo.src = options.stream;
});

comm.on('connected', function(options) {
    document.body.appendChild(options.getVideo());
    document.getElementById('waiting').remove();
});

comm.on('disconnect', function(options) {
    document.getElementById(options.callerID).remove();
});

comm.connect('Catholic Hackathon');