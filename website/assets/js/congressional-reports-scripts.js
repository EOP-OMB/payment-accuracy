function isGovernmentReportSelected() {
    const reportTypeElement = document.getElementById("report-type");
    const selectedReport = reportTypeElement.options[reportTypeElement.selectedIndex];
    return selectedReport.dataset.governmentWide === "true";

}

function enableGenerateReportsButtonIfPossible() {
    const reportTypeElement = document.getElementById("report-type");
    const reportType = reportTypeElement.value;
    const reportIsGovernmentWide = isGovernmentReportSelected();

    const agencyCodeElement = document.getElementById("agency-code");
    const agencyCode = agencyCodeElement.value;
    const agencyCodeLabelElement = document.querySelector('label[for="agency-code"]');
    agencyCodeElement.parentElement.style.display = reportIsGovernmentWide ? 'none' : 'block';
    agencyCodeLabelElement.parentElement.style.display = reportIsGovernmentWide ? 'none' : 'block';

    const yearElement = document.getElementById("year");
    const year = yearElement.value;

    const generateReportButtonElement = document.getElementById("generate-congressional-report-button");
    generateReportButtonElement.disabled = reportType === '' || (!reportIsGovernmentWide && agencyCode === '') || year === '';
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