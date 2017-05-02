function mainInit() {
    
    var dataBundle = {"edges": [], "balls": [], "log": [], "myBallIndex": -1, "myPlane": -1};    
    var mainCanvas = document.createElement('canvas');
    var centerDiv = document.getElementById("baseCenterDiv");
    
    $("#baseCenterDiv").append(mainCanvas);
    mainCanvas.id = "mainCanvas";
    mainCanvas.width = centerDiv.clientWidth;
    mainCanvas.height = centerDiv.clientHeight;
    dataBundle.myPlane = new Plane(mainCanvas);
    
    window.addEventListener("resize", function() {dataBundle.myPlane.defaultResizeListener()});
    
    centerDiv.addEventListener("wheel", function(event) {dataBundle.myPlane.defaultMouseWheelListener(event)});
    centerDiv.addEventListener("click", function(event) {dataBundle.myPlane.defaultMouseClickListener(event)});

    var b = document.createElement('button');
    b.innerHTML = "ADD";
    b.onclick = function() {mainAddBall(dataBundle)};
    $("#baseLeftMarginDiv").append(b);

    var resetButton = document.createElement('button');    
    resetButton.innerHTML = "RESET";
    resetButton.onclick = function() {resetState(dataBundle)};
    $("#baseLeftMarginDiv").append(resetButton);

    var pauseButton = document.createElement('button');    
    pauseButton.innerHTML = "START";
    pauseButton.id = "pauseButton";
    pauseButton.onclick = function() {stopGo(dataBundle)};
    $("#baseRightMarginDiv").append(pauseButton);
    
    //get game edges
    getTheEdges(dataBundle);
    
    //init timers
	setInterval(function() {timerEvent(dataBundle)}, 33);
    setInterval(function() {getTheBalls(dataBundle)}, 50); //41);
}

function timerEvent(dataBundle) {
    
    //get 2d context
    //var c = dataBundle.myPlane.delegateCanvas;
    var c = document.getElementById("mainCanvas");
    var ctx=c.getContext("2d");
    
    //clear plane canvas
    dataBundle.myPlane.clear(ctx);
    
    //draw grid and coordinate axes
    dataBundle.myPlane.drawGrid(ctx);
    dataBundle.myPlane.drawAxes(ctx);
    
    //draw any edges
    for (var i = 0; i < dataBundle.edges.length; i++) {
        dataBundle.myPlane.drawEdge(ctx, dataBundle.edges[i])
    }
    
    //draw any cirlcles
    for (var i = 0; i < dataBundle.balls.length; i++) {
        dataBundle.myPlane.drawBall(ctx, dataBundle.balls[i]);
    }
    
}

function stopGo(dataBundle) {
    $.ajax({
        url: '/togglePause',
        type: 'POST',
        success: function(data) {
            if ($("#pauseButton").html() == "STOP") {
                    $("#pauseButton").html("START");
            } else {
                $("#pauseButton").html("STOP");
            }
        },
        error: function(jqXHR, textStatus, errorThrown) { 
            $("#baseFooterDiv").html(errorThrown);
        }
    });
}

function getTheEdges(dataBundle) {
    $.ajax({
        url: '/uploadEdges',
        type: 'GET',
        success: function(data) {
            dataBundle.edges = JSON.parse(data);
        },
        error: function(jqXHR, textStatus, errorThrown) { 
                $("#baseFooterDiv").html(errorThrown);
        }
    });        
}

function getTheBalls(dataBundle) {
    $.ajax({
        url: '/uploadBalls',
        type: 'GET',
        success: function(data) {
            dataBundle.balls = JSON.parse(data);
        },
        error: function(jqXHR, textStatus, errorThrown) { 
                $("#baseFooterDiv").html(errorThrown);
        }
    });    
}

function mainAddBall(dataBundle) {
    $.ajax({
        url: '/addBall',
        type: 'POST',
        success: function(data) {
        },
        error: function(jqXHR, textStatus, errorThrown) { 
            $("#baseFooterDiv").html(errorThrown);
        }
    });
}

function resetState(dataBundle) {
    $.ajax({
        url: '/reset',
        type: 'GET',
        success: function(data) {
            dataBundle.edges = JSON.parse(data);
        },
        error: function(jqXHR, textStatus, errorThrown) { 
            $("#baseFooterDiv").html(errorThrown);
        }
    });
}