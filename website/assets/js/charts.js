function roundTwoPlaces(num) {
    if (typeof num === 'string') {
        num = parseFloat(num);
    }

    return Math.round(num * 100) / 100;
}

function addThousandsSeparator(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function downloadCsvFromString(csvString, filename = 'data.csv') {
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function renderTable(tableId, columnHeaders, rowHeaders, dataSeries, showPercentages) {
    const table = document.getElementById(tableId);
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');

    const headerRow = document.createElement('tr');
    for (let i = 0; i < columnHeaders.length; i++) {
        const headerCell = document.createElement('th');
        headerCell.textContent = columnHeaders[i];
        headerCell.classList.add('no-wrap');
        headerCell.setAttribute("scope","col");
        headerRow.appendChild(headerCell);
    }
    thead.appendChild(headerRow);

    let totals = new Array(dataSeries.length).fill(0);;
    for (let i = 0; i < dataSeries.length; i++) {
        for (let j = 0; j < dataSeries[i].length; j++) {
            totals[j] += dataSeries[i][j];
        }
    }

    for (let i = 0; i < dataSeries.length; i++) {
        const row = document.createElement('tr');
        const rowHeader = document.createElement('th');
        rowHeader.textContent = rowHeaders[i];
        rowHeader.setAttribute("scope","row");
        row.appendChild(rowHeader);
        for (let j = 0; j < dataSeries[i].length; j++) {
            const cell = document.createElement('td');
            const rate = totals[j] == 0 ? 0 : dataSeries[i][j] / totals[j];
            let textContent = addThousandsSeparator(roundTwoPlaces(dataSeries[i][j])) + ' M';
            if (showPercentages === true) {
                textContent += ' (' + Math.round(rate * 100) + '%)'
            }
            cell.textContent = textContent;
            cell.classList.add('amount-col');
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
}

function getStackedLineSeries(label, series, borderColor, backgroundColor) {
    return {
        label: label,
        data: series,
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        borderWidth: 3,
        pointRadius: 0,
        fill: true
    };
}

function renderStackedLineChart(chartElement, years, datasets, toggleSwitches, downloadCsv) {
    const ctx = chartElement.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years.map(y => 'FY ' + y),
            datasets: datasets
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    mode: 'index'
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            scales: {
                x: {
                    display: true,
                    ticks: {
                        maxRotation: 0,
                        minRotation: 0
                    }
                },
                y: {
                    min: 0,
                    stacked: true,
                    display: true,
                    ticks: {
                        display: false
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

    toggleSwitches.forEach(element => {
        element.addEventListener('change', function(event) {
            const labelToHide = element.getAttribute('data-series');
            chart.data.datasets.forEach(function(ds) {
                if (ds.label === labelToHide) {
                    ds.hidden = !event.target.checked;
                }
            });
            chart.update();
        });
    });

    let csvString = 'Amount ($M),' + years.join(',') + '\n';
    for (let i = datasets.length - 1; i >= 0; i--) {
        csvString += datasets[i].label + ',' + datasets[i].data.join(',') + '\n';
    }
    csvString.trim('\n');

    downloadCsv.addEventListener('click', function() {
        downloadCsvFromString(csvString, filename = 'improper-payment-estimates.csv')
    });

    return chart;
}

function renderDoughnutChart(
    chartElement,
    paymentAccuracyRate,
    improperPaymentRate,
    unknownPaymentRate
) {
    const ctx = chartElement.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Payment Accuracy Rate", "Improper Payment Rate", "Unknown Payment Rate"],
            datasets: [{
                data: [paymentAccuracyRate, improperPaymentRate, unknownPaymentRate],
                backgroundColor: [
                    '#146947',
                    '#EF5E25',
                    '#00BDE3'
                ]
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    return chart;
}

function renderChartTableButtons(
    containerElement,
    showChartSelector,
    showTableSelector,
    legendSelector,
    chartSelector,
    tableSelector
) {
    const showChartButton = containerElement.querySelector(showChartSelector);
    const showTableButton = containerElement.querySelector(showTableSelector);
    showChartButton.addEventListener('click', function() {
        showChartButton.classList.remove('usa-button--outline');
        showTableButton.classList.add('usa-button--outline');

        const legends = containerElement.querySelectorAll(legendSelector);
        legends.forEach(legend => {
            legend.classList.remove('hide');
        });

        const chartElements = containerElement.querySelectorAll(chartSelector);
        chartElements.forEach(chartElement => {
            chartElement.classList.remove('hide');
        });

        const tableElements = containerElement.querySelectorAll(tableSelector);
        tableElements.forEach(tableElement => {
            tableElement.classList.add('hide');
        });
    });

    showTableButton.addEventListener('click', function() {
        showTableButton.classList.remove('usa-button--outline');
        showChartButton.classList.add('usa-button--outline');

        const legends = containerElement.querySelectorAll(legendSelector);
        legends.forEach(legend => {
            legend.classList.add('hide');
        });

        const chartElements = containerElement.querySelectorAll(chartSelector);
        chartElements.forEach(chartElement => {
            chartElement.classList.add('hide');
        });

        const tableElements = containerElement.querySelectorAll(tableSelector);
        tableElements.forEach(tableElement => {
            tableElement.classList.remove('hide');
        });
    });
}

function initSparklines() {
    const sparklinesCharts = document.getElementsByClassName("sparklines-chart");
    for (let i = 0; i < sparklinesCharts.length; i++) {
        const ctx = sparklinesCharts[i].getContext('2d');
        const datapoints = JSON.parse(sparklinesCharts[i].getAttribute('data-series'));
        const years = JSON.parse(sparklinesCharts[i].getAttribute('data-years'));
        let labels = ['FY ' + years[0]]

        // use the min/max as specified in the attributes,
        //   unless a datapoint would fall outside that range
        let max = Math.max(...datapoints);
        max = Math.max(max, parseInt(sparklinesCharts[i].getAttribute('data-max')));
        let min = Math.min(...datapoints);
        min = Math.min(min, parseInt(sparklinesCharts[i].getAttribute('data-min')));

        // fix gaps
        let fixedYears = [];
        for (j = 0; j <= (years[years.length - 1] - years[0]); ++j) {
            fixedYears.push(years[0] + j);

            if (!years.includes(years[0] + j)) {
                datapoints.splice(j, 0, null);
            }
        }

        // set intermediate labels to blank
        if (fixedYears.length > 1) {
            for (let j = 1; j < (fixedYears.length - 1); ++j) {
                labels.push('')
            }
            labels.push('FY ' + fixedYears[fixedYears.length - 1]);
        }

        const color = sparklinesCharts[i].getAttribute('data-color');
        const backgroundColor = sparklinesCharts[i].getAttribute('data-background-color');

        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                    labels: labels,
                    datasets: [{
                        label: '',
                        data: datapoints,
                        borderColor: color,
                        backgroundColor: backgroundColor,
                        borderWidth: 2,
                        pointRadius: 0
                    }]
            },
            options: {
                interaction: {
                    mode: 'index',
                    includeInvisible: true,
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            title: function() {
                                return '';
                            },
                            label: function(context) {
                                if (context.parsed.y === null) {
                                    return 'No data';
                                } else {
                                    return (Math.round(context.parsed.y * 10) / 10) + ' %';
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        min: min,
                        max: max,
                        display: true,
                        ticks: {
                            display: true,
                            count: 2
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}

function initImproperPayments() {
    const chartElement = document.getElementById("improper-payment-estimates-chart");
    const containerElement = document.getElementById("improper-payment-estimates-chart-container");

    if (chartElement === null || containerElement === null) {
        return;
    }

    const paymentAccuracySeries = JSON.parse(chartElement.getAttribute('data-payment-accuracy-series')).map(roundTwoPlaces);
    const overpaymentSeries = JSON.parse(chartElement.getAttribute('data-overpayment-series')).map(roundTwoPlaces);
    const underpaymentSeries = JSON.parse(chartElement.getAttribute('data-underpayment-series')).map(roundTwoPlaces);
    const technicallyImproperSeries = JSON.parse(chartElement.getAttribute('data-technically-improper-series')).map(roundTwoPlaces);
    const unknownSeries = JSON.parse(chartElement.getAttribute('data-unknown-series')).map(roundTwoPlaces);
    const years = JSON.parse(chartElement.getAttribute('data-years'));
    const showPercentages = chartElement.getAttribute('data-show-percentages') === "true";

    let improperPaymentSeries = [];
    for (i = 0; i < overpaymentSeries.length; ++i) {
        improperPaymentSeries.push(
            overpaymentSeries[i] +
            underpaymentSeries[i] +
            technicallyImproperSeries[i] +
            unknownSeries[i]
        )
    }

    const datasets = [
        // light blue
        getStackedLineSeries('Unknown', unknownSeries, '#00BDE3', '#84D6ED'),
        // red
        getStackedLineSeries('Technically Improper', technicallyImproperSeries, '#D72D79', '#DF8EB2'),
        // yellow
        getStackedLineSeries('Underpayment', underpaymentSeries, '#FFBE2E', '#FBDDB3'),
        // purple
        getStackedLineSeries('Overpayment', overpaymentSeries, '#54278F', '#9D87BE'),
        // dark-green
        getStackedLineSeries('Proper Payments', paymentAccuracySeries, '#146947', '#83AA99')
    ];

    const downloadCsv = document.getElementById('download-improper-payment-estimates-chart-csv');
    const toggleSwitches = containerElement.querySelectorAll('.chart-toggle');
    renderStackedLineChart(chartElement, years, datasets, toggleSwitches, downloadCsv);

    renderTable(
        'improper-payment-estimates-table',
        ['', ...years],
        [
            'Proper Payments Total',
            'Improper Payments Total',
            'Overpayment',
            'Underpayment',
            'Technically Improper',
            'Unknown'
        ],
        [
            paymentAccuracySeries,
            improperPaymentSeries,
            overpaymentSeries,
            underpaymentSeries,
            technicallyImproperSeries,
            unknownSeries
        ],
        showPercentages
    );

    renderChartTableButtons(
        containerElement,
        '.show-chart-button',
        '.show-table-button',
        '.legend',
        '.improper-payment-estimates-chart-parent',
        '.improper-payment-estimates-table-parent'
    );

    // chart is not useful with one datapoint
    if (years.length === 1) {
        let tableButton = containerElement.querySelector('.show-table-button');
        let buttonContainer = tableButton.parentElement.parentElement;
        tableButton.click();
        buttonContainer.style.display = 'none';
    }
}

function initImproperPaymentsDoughnut() {
    const doughnutCharts = document.getElementsByClassName("improper-payment-estimates-doughnut-chart");
    for (let i = 0; i < doughnutCharts.length; i++) {
        let chartElement = doughnutCharts[i];

        if (chartElement === null) {
            return;
        }

        const paymentAccuracyRate = roundTwoPlaces(JSON.parse(chartElement.getAttribute('data-accuracy')));
        const improperPaymentRate = roundTwoPlaces(JSON.parse(chartElement.getAttribute('data-improper')));
        const unknownPaymentRate = roundTwoPlaces(JSON.parse(chartElement.getAttribute('data-unknown')));

        renderDoughnutChart(chartElement, paymentAccuracyRate, improperPaymentRate, unknownPaymentRate);
    }
}

function initIdentificationAndRecovery() {
    const chartElement = document.getElementById("identified-and-recovered-chart");
    const containerElement = document.getElementById("identified-and-recovered-chart-container");

    if (chartElement === null || containerElement === null) {
        return;
    }

    const identifiedSeries = JSON.parse(chartElement.getAttribute('data-identified-series')).map(roundTwoPlaces);
    const recoveredSeries = JSON.parse(chartElement.getAttribute('data-recovered-series')).map(roundTwoPlaces);
    const years = JSON.parse(chartElement.getAttribute('data-years'));

    const datasets = [
        // dark green
        getStackedLineSeries('Recovered', recoveredSeries, '#146947', '#83AA99'),
        // purple
        getStackedLineSeries('Identified', identifiedSeries, '#54278F', '#9D87BE')
    ];

    const downloadCsv = document.getElementById('download-identified-and-recovered-chart-csv');
    const toggleSwitches = containerElement.querySelectorAll('.chart-toggle');
    renderStackedLineChart(chartElement, years, datasets, toggleSwitches, downloadCsv);

    renderTable(
        'identified-and-recovered-table',
        ['', ...years],
        [
            'Overpayment Amount Identified for Recapture',
            'Overpayment Amount Recovered'
        ],
        [
            identifiedSeries,
            recoveredSeries
        ],
        false
    );

    renderChartTableButtons(
        containerElement,
        '.show-chart-button',
        '.show-table-button',
        '.legend',
        '.identified-and-recovered-chart-parent',
        '.identified-and-recovered-table-parent'
    );

    // chart is not useful with one datapoint
    if (years.length === 1) {
        let tableButton = containerElement.querySelector('.show-table-button');
        let buttonContainer = tableButton.parentElement.parentElement;
        tableButton.click();
        buttonContainer.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initSparklines();
    initImproperPayments();
    initImproperPaymentsDoughnut();
    initIdentificationAndRecovery();
});