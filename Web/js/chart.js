// chart
var __eon_pubnub = new PubNub({
    subscribeKey: "sub-c-8f5f0910-5896-11e9-a239-aa8227b65335"
});
chart = eon.chart({
    pubnub: __eon_pubnub,
    channels: ["power"],
    history: false,
    flow: true,
    rate: 3000,
    limit: 5,
    generate: {
        bindto: "#power_chart",
        data: {
            type: "spline"
        },
        transition: {
            duration: 750
        },
        axis: {
            x: {
                label: ""
            },
            y: {
                label: "mW"
            }
        },
        grid: {
            x: {
                show: true
            },
            y: {
                show: true
            }
        },
        tooltip: {
            show: true
        },
        point: {
            show: true
        }
    },
});

var pubnub1 = new PubNub({
    // publishKey: 'demo',
    subscribeKey: 'sub-c-8f5f0910-5896-11e9-a239-aa8227b65335'
});
eon.chart({
    pubnub: pubnub1,
    channels: ['voltage'],
    generate: {
        bindto: '#voltage_chart',
        data: {
            type: 'gauge',
        },
        gauge: {
            min: 0,
            max: 30
        },
        grid: {
            x: {
                show: true
            },
            y: {
                show: true
            }
        },
        tooltip: {
            show: true
        },
        point: {
            show: true
        },
        color: {
            pattern: ['#FF0000', '#F6C600', '#60B044'],
            threshold: {
                values: [5, 10, 15]
            }
        }
    }
});

var pubnub2 = new PubNub({
    // publishKey: 'demo',
    subscribeKey: 'sub-c-8f5f0910-5896-11e9-a239-aa8227b65335'
});
eon.chart({
    pubnub: pubnub2,
    channels: ['current'],
    generate: {
        bindto: '#current_chart',
        data: {
            type: 'gauge',
        },
        gauge: {
            min: 0,
            max: 2
        },
        grid: {
            x: {
                show: true
            },
            y: {
                show: true
            }
        },
        color: {
            pattern: ['#FF0000', '#F6C600', '#60B044'],
            threshold: {
                values: [5, 10, 15]
            }
        }
    }
});

// var count = 0;

// function isConnected() {
//     if (count % 2 === 0) {
//         document.getElementById("connection_id").innerHTML = " Alive";
//         count++;
//     } else {
//         document.getElementById("connection_id").innerHTML = " Dead";
//         count++;
//     }
// }

// // setTimeout('isConnected()', 1000);

// var interval = setInterval('isConnected()', 1000);
// setTimeout(function () {
//     clearInterval(interval)
// }, 10000);

document.getElementById('connection_id').innerHTML = ' Dead';

setTimeout(()=>{
    document.getElementById('connection_id').innerHTML = ' Alive';
}, 5000)