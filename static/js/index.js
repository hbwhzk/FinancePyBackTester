document.getElementById('strategy').addEventListener('change', function() {
    var strategy = this.value;
    var allParamsDivs = document.querySelectorAll('.strategy_params');

    allParamsDivs.forEach(function(div) {
        div.style.display = 'none';
    });

    var strategyParamsDiv = document.getElementById(strategy + '_params');
    if (strategyParamsDiv) {
        strategyParamsDiv.style.display = 'block';
    }
});

document.querySelector('form').addEventListener('submit', function(event) {
    const startDate = new Date(document.getElementById('start_date').value);
    const endDate = new Date(document.getElementById('end_date').value);
    
    if (startDate > endDate) {
        alert("The end date must be later than the start date.");
        event.preventDefault(); 
        return;
    }

    const diffTime = Math.abs(endDate - startDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 

    if (document.getElementById('strategy').value === 'rsi') {
        const rsiPeriod = parseInt(document.getElementById('rsi_period').value, 10);
        if (diffDays < rsiPeriod) {
            alert(`The date range must be at least ${rsiPeriod} days.`);
            event.preventDefault(); 
        }
    }
});

function toggleDataSourceOptions() {
    var dataSource = document.getElementById('data_source').value;

    document.querySelectorAll('.data_source_option').forEach(function(option) {
        option.style.display = 'none';
    });

    if (dataSource === 'local') {
        document.getElementById('local_file').style.display = 'block';
    } else if (dataSource === 'online') {
        document.getElementById('online_resource').style.display = 'block';
    } else if (dataSource === 'a_stock') {
        document.getElementById('a_stock_resource').style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);  
    const lastYear = new Date(today);
    lastYear.setFullYear(today.getFullYear() - 1);  

    const formatDate = (date) => {
        let d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;

        return [year, month, day].join('-');
    };

    document.getElementById('start_date').value = formatDate(lastYear);
    document.getElementById('end_date').value = formatDate(yesterday);
});



