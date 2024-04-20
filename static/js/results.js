var chart;


document.addEventListener('DOMContentLoaded', function () {
    console.log("DOMContentLoaded event fired");
    var ctx = document.getElementById('chart').getContext('2d');
    
    if (!ctx) {
        console.error("Failed to get canvas context");
        return;
    }

    if (!candlestickData || candlestickData.length === 0) {
        console.error("No data available for the chart");
        return;
    }

    
    var formattedData = candlestickData.map(item => {
        let dateObject = luxon.DateTime.fromISO(item.t); 
        return {
            x: dateObject.valueOf(), 
            o: parseFloat(item.o),
            h: parseFloat(item.h),
            l: parseFloat(item.l),
            c: parseFloat(item.c),
        };
    });
    

    var lineData = formattedData.map(item => {
        return { x: item.x, y: item.c }; 
    });

    var buyPoints = tradeData.filter(trade => trade.type === 'buy').map(trade => {
        let dateObject = luxon.DateTime.fromISO(trade.date);
        return { x: dateObject.valueOf(), y: trade.price };
    });

    var sellPoints = tradeData.filter(trade => trade.type === 'sell').map(trade => {
        let dateObject = luxon.DateTime.fromISO(trade.date);
        return { x: dateObject.valueOf(), y: trade.price };
    });

    console.log("Formatted Data:", formattedData);
    console.log("Line Data:", lineData);
    console.log("Buy Points:", buyPoints);
    console.log("Sell Points:", sellPoints);
    
    chart = new Chart(ctx, {
        type: 'candlestick',
        data: {
            datasets: [
                {
                    label: 'Candlestick',
                    data: formattedData,
                    hidden: true,
                },
                {
                    label: "Close Price",
                    type: "line",
                    data: lineData,
                    borderColor: "rgba(0, 0, 0, 0.65)",
                    backgroundColor: "rgba(0, 0, 0, 0.2)",
                    fill: false,
                    hidden: false,
                },
                {
                    label: 'Buy Points',
                    type: 'scatter',
                    data: buyPoints,
                    pointStyle: 'triangle',
                    borderColor: "rgba(0, 255, 0, 1)",
                    backgroundColor: "rgba(0, 255, 0, 1)",
                    showLine: false,
                    pointRadius: 8
                },
                {
                    label: 'Sell Points',
                    type: 'scatter',
                    data: sellPoints,
                    pointStyle: 'triangle',
                    backgroundColor: "rgba(255, 0, 0, 1)",
                    borderColor: "rgba(255, 0, 0, 1)",
                    showLine: false,
                    pointRadius: 8
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time', 
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    type: 'linear'
                }
            },
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true, 
                            mode: 'x'      
                        },
                        pinch: {
                            enabled: true, 
                            mode: 'x'
                        },
                        mode: 'x'
                    },
                    pan: {
                        enabled: true, 
                        mode: 'x'
                    }
                }
            }
        }
    });

    if (!chart) {
        console.error("Failed to create chart.");
    }

    
    function update() {
        var colorScheme = document.getElementById('color-scheme').value;
        if (colorScheme === 'neon') {
            chart.config.data.datasets[0].backgroundColors = {
                up: '#fe0000', 
                down: '#01ff01',
                unchanged: '#999'
            };
            chart.config.data.datasets[0].borderColors = {
                up: '#fe0000',
                down: '#01ff01',
                unchanged: '#999'
            };
        } else {
            delete chart.config.data.datasets[0].backgroundColors;
            delete chart.config.data.datasets[0].borderColors;
        }
        chart.update();
    }
    
    document.getElementById('color-scheme').addEventListener('change', update);
    
});

