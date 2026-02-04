function downloadDataset() {
    var selectElement = document.getElementById("fiscal-year");
    var selectedOption = selectElement.options[selectElement.selectedIndex];
    var fileName = selectedOption.getAttribute('data-file-name');
    var filePath = "/assets/files/" + fileName;

    // Create a temporary link to trigger the download
    var a = document.createElement("a");
    a.href = filePath;
    a.download = fileName;

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function selectYear(prefix, val) {
    window.location.href = prefix + val;
}

function selectYearNoReload(prefix, val) {
    const yearlyElements = document.querySelectorAll('[data-year]');
    for (let i = 0; i < yearlyElements.length; ++i) {
        let yearlyValue = yearlyElements[i].getAttribute('data-year');
        if (val === yearlyValue) {
            yearlyElements[i].classList.remove('hide');
        } else {
            yearlyElements[i].classList.add('hide');
        }
    }
}

// makes entire th element trigger uswds sort
function initSortableHeaders() {
    document.querySelectorAll("th[data-sortable]").forEach(
        th => th.addEventListener('click', (e) => {
            // prevent triggering twice when clicking sort button directly
            if (e.target === e.currentTarget) {
                th.querySelector('.usa-table__header__button:first-child').click();
            }
        })
    );
}

// uswds does not currently support tabs
// this uses segmented buttons to act as the tabs
// tab groups should share data-group-id
// every tab should unhide a unique data-show-id
function initTabs() {
    let groupIds = [];
    document.querySelectorAll(".tabbed-button").forEach(
        btn => {
            let isFirstInGroup = false;
            if (!groupIds.includes(btn.getAttribute('data-group-id'))) {
                groupIds.push(btn.getAttribute('data-group-id'));
                isFirstInGroup = true;
            }

            btn.addEventListener('click', (e) => {
                let clickedGroupId = btn.getAttribute('data-group-id');
                let clickedShowId = btn.getAttribute('data-show-id');
                let btns = document.querySelectorAll('[data-group-id="'+ clickedGroupId + '"]');
                for (let i = 0; i < btns.length; i++) {
                    let showId = btns[i].getAttribute('data-show-id');
                    if (showId === clickedShowId) {
                        btns[i].classList.remove('usa-button--outline');
                        document.getElementById(showId).classList.remove('hide');
                    } else {
                        btns[i].classList.add('usa-button--outline');
                        document.getElementById(showId).classList.add('hide');
                    }
                }
            });

            // this clicks the first button in the tab,
            //   because we may be hiding tabs/sections without any data
            if (isFirstInGroup) {
                btn.click();
            }
        }
    );
}

document.addEventListener('DOMContentLoaded', () => {
    initSortableHeaders();
    initTabs();
});