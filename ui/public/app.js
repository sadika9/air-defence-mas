let _stage = null;
let _socket = null;
let _agents = [];
let _flyingItems = [];

function setup() {
    _stage = new createjs.Stage('mas-canvas');
    _stage.setTransform(0, 0, 1, 1)
}

function init() {
    initCanvas();
    initWebsocket();
}

function kill() {
    if (_socket) {
        _socket.send('kill');
    } else {
        alert('No websocket. initialize first.');
    }
}

function start() {
    if (_socket) {
        _socket.send('start');
    } else {
        alert('No websocket. initialize first.');
    }
}

function clearMessageBox() {
    $('#messages').empty();
}

function initCanvas() {
    _stage.removeAllChildren();
    _stage.clear();

    writeMessage('[i] Canvas initialized');
}

function initWebsocket() {
    if (_socket) {
        _socket.close();
        _socket = null;
    }

    _socket = new WebSocket("ws://" + window.location.host);

    _socket.onopen = function (e) {
        writeMessage('[i] Connection established');
        _socket.send('init');
        writeMessage('[s] init');
    };

    _socket.onmessage = function (event) {
        const message = event.data;
        const payload = message.split('|');

        console.log(message);

        switch (payload[1]) {
            case 'init':
                const data = JSON.parse(payload[2]);
                setupAgents(data);
                break;
            case 'msg':
                processMsg(payload);
                writeMessage(message);
                break;
            case 'fire':
                processFire(payload);
                writeMessage(message);
                break;
            default:
                writeMessage(message);
                break;
        }
    };

    _socket.onclose = function (event) {
        if (event.wasClean) {
            writeMessage(`[i] [close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        } else {
            // e.g. server process killed or network down
            // event.code is usually 1006 in this case
            writeMessage('[i] [close] Connection died');
        }
    };

    _socket.onerror = function (error) {
        console.log(`[error] ${error.message}`);
    };
}

function setupAgents(data) {
    const agents = data;

    for (let property in agents) {
        if (agents.hasOwnProperty(property)) {
            const a = agents[property];
            let item = createAgentItem(property, a.x, a.y, a.range);
            _agents.push(item);

            _stage.addChild(item.g);
        }
    }

    _stage.update();
}

function processMsg(payload) {
    const sender = payload[2];

    if (sender.startsWith('radar')) {
        // >>>>|msg|radar2|hq|plane|102|enemy|152|347
        const item = createEnemyItem(payload[5], payload[4], payload[6], payload[7], payload[8]);
        _flyingItems.push(item);

        _stage.addChild(item.g);

        _stage.update();
    }
}

function processFire(payload) {
    // >>>>|fire|missile1|missile|154|enemy|199|310
    const itemId = payload[4];

    const found = _flyingItems.find(function(i) {
      return i.id === itemId;
    });

    if (found) {
        const idx = _flyingItems.indexOf(found);
        _flyingItems.splice(idx, 1);

        _stage.removeChild(found.g);

        _stage.update();
    }
}

function createAgentItem(name, x, y, range) {
    let rangeColor = 'DeepSkyBlue';
    let strokeColor = 'black';
    const pointSize = 10;
    let pointColor = 'black';
    let labelColor = 'black';
    let type = null;

    if (name === 'hq') {
        type = 'hq';
        range = 0;
        pointColor = 'rgba(123, 239, 178)';
    } else if (name.startsWith('radar')) {
        type = 'radar';
        rangeColor = 'rgba(51, 110, 123, 0.05)';
        strokeColor = 'rgba(51, 110, 123)';
        pointColor = 'rgba(51, 110, 123)';
    } else if (name.startsWith('missile')) {
        type = 'missile';
        rangeColor = 'rgba(240, 20, 252, 0.05)';
        strokeColor = 'rgba(240, 20, 252)';
        pointColor = 'rgba(240, 20, 252)';
    }

    const rangeCircle = new createjs.Shape();
    rangeCircle.graphics.beginFill(rangeColor).beginStroke(strokeColor).drawCircle(0, 0, range);

    const pointCircle = new createjs.Shape();
    pointCircle.graphics.beginFill(pointColor).drawCircle(0, 0, pointSize);

    const label = new createjs.Text(name, "14px Arial", labelColor);
    label.x = 20;
    label.y = 0;

    const container = new createjs.Container();
    container.x = x;
    container.y = y;
    container.addChild(rangeCircle, pointCircle, label);

    return {type, g: container};
}

function createEnemyItem(id, type, side, x, y) {
    const fillColor = 'red';
    let labelColor = 'black';

    const enemy = new createjs.Shape();
    enemy.graphics.beginFill(fillColor).drawPolyStar(0, 0, 20, 3);

    const label = new createjs.Text(`${side}-${type}-${id}`, "14px Arial", labelColor);
    label.x = 20;
    label.y = 0;

    const container = new createjs.Container();
    container.x = x;
    container.y = y;
    container.addChild(enemy, label);

    return {id, type, g: container};
}

function writeMessage(message) {
    const $msgBox = $('#messages');

    let text = message;
    if (message.startsWith('>>>>')) {
        const parts = message.split('|');

        if (parts[1] === 'msg') {
            //>>>>|msg|radar1|hq|plane|10|enemy|-20|-20
            //>>>>|msg|radar1|missile1|plane|10|enemy|-20|-20
            //>>>>|msg|hq|missile2|missile|124|enemy|24|157
            if (parts[2].startsWith('radar') && parts[3] === 'hq') {
                text = parts[2] + ' informing ' + parts[3] + ' about ' + parts[6] + ' ' + parts[4] + ' at (' + parts[7] + ', '  + parts[8] + ')';
            } else if (parts[2].startsWith('radar') && parts[3].startsWith('missile')) {
                text = parts[2] + ' directly informing ' + parts[3] + ' about ' + parts[6] + ' ' + parts[4] + ' at (' + parts[7] + ', '  + parts[8] + ')';
            } else if (parts[2].startsWith('hq') && parts[3].startsWith('missile')) {
                text = parts[2] + ' informing ' + parts[3] + ' about ' + parts[6] + ' ' + parts[4] + ' at (' + parts[7] + ', '  + parts[8] + ')';
            }
        } else if (parts[1] === 'state') {
            //>>>>|state|hq|offline
            //>>>>|state|hq|online
            if (parts[3] === 'offline') {
                text = parts[2] + ' went offline';
            } else {
                text = parts[2] + ' is online';
            }
        } else if (parts[1] === 'fire') {
            //>>>>|fire|missile2|missile|20|enemy|-20|-20
            text = parts[3] + ' fired a missile to ' + parts[5] + ' ' + parts[3] + ' ' + ' at (' + parts[6] + ', '  + parts[7] + ')';
        }
    }

    $msgBox.append(`<p>${text}</p>`);

    // scroll to bottom
    $msgBox.scrollTop($msgBox[0].scrollHeight);
}
