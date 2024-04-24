document.addEventListener('DOMContentLoaded', () => {
    const candlestickDataFormatted = candlestickData.map(item => {
        if (!item || typeof item.t === 'undefined' || typeof item.o === 'undefined') {
            console.error('Invalid item encountered:', item);
            return null;
        }
        return {
            x: new Date(luxon.DateTime.fromISO(item.t).valueOf()),
            y: [item.o, item.h, item.l, item.c]
        };
    }).filter(item => item !== null);

    const lineData = candlestickData.map(item => ({ 
        x: new Date(luxon.DateTime.fromISO(item.t).valueOf()), 
        y: item.c 
    }));

    const volumeDataFormatted = candlestickData.map(item => ({
        x: new Date(luxon.DateTime.fromISO(item.t).valueOf()),
        y: item.v
    }));
    

    const buyPointsFormatted = tradeData.filter(trade => trade.type === 'buy').map(trade => {
        if (!trade.date || !trade.price) {
            console.error('Invalid trade data:', trade);
            return null;
        }
        return {
            x: new Date(luxon.DateTime.fromISO(trade.date).valueOf()),
            y: trade.price
        };
    }).filter(item => item !== null);

    const sellPointsFormatted = tradeData.filter(trade => trade.type === 'sell').map(trade => {
        return {
            x: new Date(luxon.DateTime.fromISO(trade.date).valueOf()),
            y: trade.price
        };
    }).filter(item => item !== null);

    var candlestickChart = new ApexCharts(document.querySelector("#candlestick-chart"), {
        series: [
            {
                name: 'Candlestick',
                type: 'candlestick',
                data: candlestickDataFormatted
            },
            {
                name: 'Close Price',
                type: 'line',
                data: lineData
            }
        ],
        chart: {
            height: 350,
            type: 'candlestick',
            id: 'candlestickChart',
            toolbar: {
                show: true,
                tools: {
                    download: true,
                    selection: true,
                    zoom: false,
                    zoomin: false,
                    zoomout: false,
                    pan: true,
                    reset: true
                },
                autoSelected: 'zoom'
            },
            events: {
                mounted: function(chartContext, config) {
                    console.log("Chart has been successfully mounted.");
                },
                zoomed: function(chartContext, {xaxis, yaxis}) {
                    console.log("Zoom event triggered.");
                    updateYAxisBounds(chartContext, xaxis);
                },
                scrolled: function(chartContext, {xaxis, yaxis}) {
                    console.log("Scroll event triggered.");
                    updateYAxisBounds(chartContext, xaxis);
                }
            }
        },
        xaxis: {
            type: 'datetime'
        },
        yaxis: {
            title: {
                text: 'Price'
            }
        },
        annotations: {
            xaxis: [
                ...buyPointsFormatted.map(point => ({
                    x: new Date(point.x).getTime(),
                    borderColor: '#FF0000',
                    label: {
                        borderColor: '#FF0000',
                        style: {
                            fontSize: '12px',
                            color: '#fff',
                            background: '#FF0000'
                        },
                        orientation: 'horizontal',
                        text: 'Buy'
                    }
                })),
                ...sellPointsFormatted.map(point => ({
                    x: new Date(point.x).getTime(),
                    borderColor: '#00FF00',
                    label: {
                        borderColor: '#00FF00',
                        style: {
                            fontSize: '12px',
                            color: '#fff',
                            background: '#00FF00'
                        },
                        orientation: 'horizontal',
                        text: 'Sell'
                    }
                }))
            ]
        }
    });

    var volumeChart = new ApexCharts(document.querySelector("#volume-chart"), {
        series: [
            {
                name: 'Volume',
                type: 'bar',
                data: volumeDataFormatted
            }
        ],
        chart: {
            height: 200,
            type: 'bar',
            id: 'volumeChart',
            brush: {
                enabled: true,
                target: 'candlestickChart'
            },
            selection: {
                enabled: true,
                xaxis: {
                    min: new Date().getTime() - (30 * 24 * 60 * 60 * 1000),
                    max: new Date().getTime()
                }
            },
            events: {
                selection: function(chartContext, { xaxis }) {
                    console.log("Volume chart selection event triggered.");
                    
                    // 调用函数来更新 candlestickChart
                    if (candlestickChart && xaxis && xaxis.min && xaxis.max) {
                        updateYAxisBounds(candlestickChart, xaxis);
                    }
                }
            }
        },
        xaxis: {
            type: 'datetime',
            tickPlacement: 'on'
        },
        yaxis: {
            title: {
                text: 'Volume'
            },
            opposite: true
        }
    });

    candlestickChart.render();
    volumeChart.render();

    function updateYAxisBounds(candlestickChart, xaxis) {
        if (!xaxis || typeof xaxis.min === 'undefined' || typeof xaxis.max === 'undefined') {
            console.error("xaxis data is missing.");
            return;
        }
    
        let newData = candlestickDataFormatted.filter(d => {
            return new Date(d.x).getTime() >= xaxis.min && new Date(d.x).getTime() <= xaxis.max;
        });
    
        let newMinPrice = Math.min(...newData.map(d => d.y[2]));
        let newMaxPrice = Math.max(...newData.map(d => d.y[1]));

        
        newMinPrice *= 0.99; //  -2%
        newMaxPrice *= 1.01; // +2%
    
        candlestickChart.updateOptions({
            yaxis: {
                min: newMinPrice,
                max: newMaxPrice
            },
            xaxis: {
                min: xaxis.min,
                max: xaxis.max
            }
        }, false, true);
    }
    
    


    
});

