const http = require('http');
const express = require('express');
const {createTerminus} = require('@godaddy/terminus');
const path = require('path');
const {exec, spawn} = require('child_process');
const WebSocket = require('ws');

let masBackend = null;

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({server});

///////////////////////////////////// FRONT END ///////////////////////////////////////////////
app.use(express.static('public'));

app.get('/', function (req, res) {
    const f = path.join(__dirname, 'views/index.html');
    res.sendFile(f);
});

///////////////////////////////////// WEBSOCKET ///////////////////////////////////////////////
wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        switch (message) {
            case 'init': {
                const command = path.join(__dirname, 'run_print_structure.sh');
                console.log(command);
                exec(command, function (error, stdout, stderr) {
                    ws.send('>>>>|init|' + stdout)
                });
            }
                break;
            case 'start': {
                if (masBackend) {
                    masBackend.kill();
                }
                masBackend = spawn('./run_mas.sh');

                masBackend.stdout.on('data', (data) => {
                    const str = data.toString();
                    const parts = str.split('\n');

                    for (p of parts) {
                        if (p.startsWith('>>>>')) {
                            ws.send(p);
                        }
                    }
                });

                masBackend.stderr.on('data', (data) => {
                    console.log(`stderr: ${data}`);
                });

                masBackend.on('close', (code) => {
                    console.log(`child process exited with code ${code}`);
                });
            }
                break;
            case 'kill': {
                if (masBackend) {
                    masBackend.kill('SIGKILL');
                }
            }
                break;
            default:
                console.log('received: %s', message);
                break;
        }
    });

    ws.send('WS ON');
});

///////////////////////////////////// SHUT DOWN & CLEAN UP ///////////////////////////////////////////////
function onSignal() {
    console.log('server is starting cleanup');
    const p = new Promise(function (resolve, reject) {
        if (masBackend) {
            resolve(masBackend.kill('SIGKILL'));
        } else {
            resolve(null);
        }
        setTimeout(resolve, 100, 'foo');
    });
    return Promise.all([
        p,
    ]);
}

function onShutdown() {
    console.log('cleanup finished, server is shutting down');
}

const options = {
    signals: ['SIGTERM', 'SIGINT'],
    onSignal,
    onShutdown
};

createTerminus(server, options);

///////////////////////////////////// STARTING THE SERVER ///////////////////////////////////////////////
const port = process.env.port || 8181;
server.listen(port);

console.log('server is running at port ' + port);
