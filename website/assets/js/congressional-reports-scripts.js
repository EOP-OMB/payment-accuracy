function isGovernmentReportSelected() {
    const reportTypeElement = document.getElementById("report-type");
    const selectedReport = reportTypeElement.options[reportTypeElement.selectedIndex];
    return selectedReport.dataset.governmentWide === "true";

}

function reportChanged() {
    document.getElementById("agency-code").selectedIndex = 0;
    document.getElementById("year").selectedIndex = 0;
    enableGenerateReportsButtonIfPossible();

    if(isGovernmentReportSelected()) {
        document.getElementById("agency-code").value = '_';
        agencyChanged();
    }
}

function agencyChanged() {
    document.getElementById("year").selectedIndex = 0;
    enableGenerateReportsButtonIfPossible();
}

function yearChanged() {
    enableGenerateReportsButtonIfPossible();
}

function enableGenerateReportsButtonIfPossible() {
    const reportTypeElement = document.getElementById("report-type");
    const reportType = reportTypeElement.value;
    const reportIsGovernmentWide = isGovernmentReportSelected();

    const agencyCodeElement = document.getElementById("agency-code");
    const agencyCode = agencyCodeElement.value;

    const yearElement = document.getElementById("year");
    const year = yearElement.value;

    const generateReportButtonElement = document.getElementById("generate-congressional-report-button");
    generateReportButtonElement.disabled = reportType === '' || (!reportIsGovernmentWide && agencyCode === '') || year === '';

    const availableReports = JSON.parse(decodeURIComponent(reportTypeElement.dataset.validOptions));
    agencyCodeElement.disabled = (reportType === '' || !availableReports[reportType]);
    if (!agencyCodeElement.disabled) {
        for (let i = 0; i < agencyCodeElement.options.length; i++) {
            agencyCodeElement.options[i].disabled = !(availableReports[reportType][agencyCodeElement.options[i].value]);
        }
    }

    yearElement.disabled = agencyCodeElement.disabled || (!reportIsGovernmentWide && agencyCode === '') || !availableReports[reportType][agencyCode];
    if (!yearElement.disabled) {
        for (let i = 0; i < yearElement.options.length; i++) {
            yearElement.options[i].disabled = !(availableReports[reportType][agencyCode].includes(parseInt(yearElement.options[i].value, 10)));
        }
    }
}

function generateReport() {
    const reportTypeElement = document.getElementById("report-type");
    const reportType = reportTypeElement.value;
    const reportIsGovernmentWide = isGovernmentReportSelected();

    const agencyCodeElement = document.getElementById("agency-code");
    const agencyCode = agencyCodeElement.value;

    const yearElement = document.getElementById("year");
    const year = yearElement.value;

    let pageName = year + '_' + agencyCode + '_' + reportType;
    if (reportIsGovernmentWide) {
        pageName = year + '_' + reportType;
    }

    window.location.href = '/resources/congressional-reports/' + pageName;
}

document.addEventListener('DOMContentLoaded', () => {
    enableGenerateReportsButtonIfPossible();
});