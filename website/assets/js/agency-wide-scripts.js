/**
 * Number of agencies per page in agency-wide table.
 */
const Agencies_Per_Page = 20;

/**
 * Column index for improper payment rate within Agency-wide table.
 */
const Improper_Payment_Rate_Col_Num = 5

/**
 * Variable to keep track of current page number in agency-wide table.
 */
let currentPage = 1;

/**
 * Renders program tags within search/filter combobox options.
 * This is needed to override uswds combobox.
 */
function renderProgramTags() {
  const intervalId = setInterval(() => {
    const comboList = document.querySelector('.usa-combo-box__list');
    if (comboList) {
      const observer = new MutationObserver(() => {
        document.querySelectorAll('.usa-combo-box__list li').forEach(item => {
          if (item.textContent.startsWith('PROGRAM:')) {
            item.innerHTML = `<span class="usa-tag">Program</span> ${item.textContent.replace('PROGRAM:', '').trim()}`;
          }
        });
      });

      observer.observe(comboList, { childList: true, subtree: true });
      clearInterval(intervalId); // Stop checking once found
    }
  }, 100);
}

/**
 * Applies alternating row colors to visible agency and program rows.
 */
function applyAlternatingRowColors() {
    const visibleAgencyRows = Array.from(document.querySelectorAll('.agency-row'))
      .filter(row => !row.classList.contains('filter-hidden'));
  
    visibleAgencyRows.forEach((agencyRow, index) => {
        const colorClass = index % 2 === 0 ? 'row-color-1' : 'row-color-2';

        agencyRow.classList.remove('row-color-1', 'row-color-2');
        agencyRow.classList.add(colorClass);

        // Match program rows with parent agency row color
        const agencyName = agencyRow.dataset.agencyName;

        const programRows = document.querySelectorAll(
            `.program-row[data-agency-name="${agencyName}"]`
        )

        programRows.forEach(programRow => {
            if (!programRow.classList.contains('collapsed') || !programRow.classList.contains('filter-hidden')) {
              programRow.classList.remove('row-color-1', 'row-color-2');
              programRow.classList.add(colorClass);
            }
        });
    });
}

/**
 * Toggles the expand/collapse icon and the children programs.
 * 
 * @this {HTMLButtonElement} - The expand button that was clicked.
 */
function toggleCollapsedClass() {
    const icon = this.querySelector('.toggle-icon');
    const isCollapsed = icon.getAttribute('src').includes('expand.svg');

    icon.setAttribute('src', isCollapsed ? '/assets/img/collapse.svg' : '/assets/img/expand.svg');
    icon.setAttribute('alt', isCollapsed ? 'Collapse' : 'Expand');
    this.setAttribute('aria-label', isCollapsed ? 'Collapse Agency' : 'Expand Agency');

    const agencyRow = this.closest('tr');
    let nextRow = agencyRow.nextElementSibling;

    while (nextRow && nextRow.classList.contains('program-row')) {
        if (!nextRow.classList.contains('filter-hidden')) {
            nextRow.classList.toggle('collapsed');
        }
        nextRow = nextRow.nextElementSibling;
    }
}

/**
 * Clears filters and resets table to initial state.
 */
function clearFilter() {
    const allAgencyRows = document.querySelectorAll('.agency-row');
    const allProgramRows = document.querySelectorAll('.program-row');

    // remove filter from rows
    allAgencyRows.forEach(row => {
        row.classList.remove('filter-hidden');
        button = row.querySelector('.expand-btn');
        const icon = button.querySelector('.toggle-icon');
        icon.setAttribute('src', '/assets/img/expand.svg');
        icon.setAttribute('alt', 'Expand');
        button.setAttribute('aria-label', 'Expand Agency');
    });
    allProgramRows.forEach(row => row.classList.remove('filter-hidden'));
    // collapse program rows
    allProgramRows.forEach(row => row.classList.add('collapsed'));

    // Set table back to first page
    currentPage = 1;

    // update pagination
    paginateAgencies();

    // reset striped rows
    applyAlternatingRowColors();
}

/**
 * Applies filter to table based on combobox input
 * 
 * @this {HTMLElement} comboBox
 */
function applyFilter() {
    let selectedValue = this.value.trim();
    if (selectedValue.startsWith("Program ")) {
        selectedValue = selectedValue.replace(/^Program /, "");
    } else if (selectedValue.startsWith("PROGRAM: ")) {
        selectedValue = selectedValue.replace(/^PROGRAM: /, "");
    }
    const comboBox = document.getElementsByName('agencies-programs-combobox')[0];
    const options = Array.from(comboBox.querySelectorAll('option')).map(opt => opt.value);
    const agencyRows = document.querySelectorAll('.agency-row');
    const programRows = document.querySelectorAll('.program-row');

    if (options.includes(selectedValue)) {
        if (selectedValue === "") {
            // Clear filter and collapse programs
            clearFilter();
            return;
        }

        // Hide all rows by default
        agencyRows.forEach(row => row.classList.add('filter-hidden'));
        programRows.forEach(row => row.classList.add('filter-hidden'));

        // Try matching agency first
        let matchedAgency = Array.from(agencyRows).find(row =>
        row.dataset.agencyName === selectedValue
        );

        if (matchedAgency) {
            // Show the agency row and all its program rows
            matchedAgency.classList.remove('filter-hidden');
            const button = matchedAgency.querySelector('.expand-btn');
            const icon = button.querySelector('.toggle-icon');
            icon.setAttribute('src', '/assets/img/collapse.svg');
            icon.setAttribute('alt', 'Collapse');
            button.setAttribute('aria-label', 'Collapse Agency');

            const agencyName = matchedAgency.dataset.agencyName;
            programRows.forEach(row => {
                if (row.dataset.agencyName === agencyName) {
                    row.classList.remove('filter-hidden');
                    row.classList.remove('collapsed');
                }
            });
        } else {
            // Otherwise, try to match a program
            const matchedProgram = Array.from(programRows).find(row =>
                row.dataset.programName === selectedValue
            );

            if (matchedProgram) {
                matchedProgram.classList.remove('filter-hidden');
                matchedProgram.classList.remove('collapsed');

                const agencyName = matchedProgram.dataset.agencyName;
                const parentAgency = Array.from(agencyRows).find(row =>
                    row.dataset.agencyName === agencyName
                );

                if (parentAgency) {
                    parentAgency.classList.remove('filter-hidden');
                    const button = parentAgency.querySelector('.expand-btn');
                    const icon = button.querySelector('.toggle-icon');
                    icon.setAttribute('src', '/assets/img/collapse.svg');
                    icon.setAttribute('alt', 'Collapse');
                    button.setAttribute('aria-label', 'Collapse Agency');
                }
            }
        }
        currentPage = 1;
        // update pagination
        paginateAgencies();
        // apply alternating colors to filtered rows
        applyAlternatingRowColors();
    }
}

/**
 * Update pagination buttons based on Agencies_Per_Page and currentPage.
 */
function updatePaginationButtons() {
    const allAgencyRows = document.querySelectorAll('.agency-row');
    // Get only currently visible (non-filtered) agency rows
    const visibleAgenciesTotal = Array.from(allAgencyRows).filter(
        row => !row.classList.contains('filter-hidden')
    ).length;
    const totalPages = Math.ceil(visibleAgenciesTotal / Agencies_Per_Page);
    const container = document.querySelector('#pagination-container');
    container.innerHTML = '';

    const prev = document.createElement('li');
    prev.className = `usa-pagination__item usa-pagination__arrow ${currentPage === 1 ? 'pagination-hidden' : ''}`;
    prev.innerHTML = '<button id="pagination-prev" class="usa-pagination__link border-0 bg-white" aria-label="Previous page">&lt; Previous</button>';
    container.appendChild(prev);

    // Page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = 'usa-pagination__item';
        li.innerHTML = `
            <button class="usa-pagination__button ${i === currentPage ? 'usa-current' : 'usa-not-current bg-white'}" data-page="${i}">
                ${i}
            </button>`;
        container.appendChild(li);
    }

    // Next button
    const next = document.createElement('li');
    next.className = `usa-pagination__item usa-pagination__arrow ${currentPage === totalPages ? 'pagination-hidden' : ''}`;
    next.innerHTML = '<button id="pagination-next" class="usa-pagination__link border-0 bg-white" aria-label="Next page">Next &gt;</button>';
    container.appendChild(next);

    document.querySelector('#pagination-prev')?.addEventListener('click', e => {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            paginateAgencies();
        }
    });

    document.querySelector('#pagination-next')?.addEventListener('click', e => {
        e.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            paginateAgencies();
        }
    });

    container.querySelectorAll('.usa-pagination__button[data-page]').forEach(button => {
        button.addEventListener('click', () => {
            currentPage = parseInt(button.dataset.page);
            paginateAgencies();
        });
    });
}

/**
 * Shows current page's agency rows and programs.
 */
function paginateAgencies() {
    const allAgencyRows = document.querySelectorAll('.agency-row');
    const allProgramRows = document.querySelectorAll('.program-row');

    // Get only currently visible (non-filtered) agency rows
    const visibleAgencies = Array.from(allAgencyRows).filter(
        row => !row.classList.contains('filter-hidden')
    );

    const totalVisible = visibleAgencies.length;

    // First hide all agency and program rows
    allAgencyRows.forEach(row => row.classList.add('pagination-hidden'));
    allProgramRows.forEach(row => row.classList.add('pagination-hidden'));

    // Determine pagination bounds
    const start = (currentPage - 1) * Agencies_Per_Page;
    const end = start + Agencies_Per_Page;

    for (let i = start; i < end && i < totalVisible; i++) {
        const agencyRow = visibleAgencies[i];
        agencyRow.classList.remove('pagination-hidden');

        // Show only its associated program rows
        const agencyName = agencyRow.dataset.agencyName;
        document.querySelectorAll(`.program-row[data-agency-name="${agencyName}"]`).forEach(
            row => row.classList.remove('pagination-hidden')
        );
    }
    // update pagination buttons
    updatePaginationButtons();
}

/**
 * Get agency rows and child program rows.
 * 
 * @returns Nested array of agency rows and child programs.
 */
function getGroupedRows() {
    const rows = Array.from(document.querySelectorAll("tbody tr"));
    const groups = [];

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];

        if (row.classList.contains("agency-row")) {
            const agencyName = row.dataset.agencyName;
            const group = { agencyRow: row, programRows: [] };

            // Collect matching program rows
            i++;
            while (i < rows.length && rows[i].classList.contains("program-row") && rows[i].dataset.agencyName === agencyName) {
                group.programRows.push(rows[i]);
                i++;
            }

            i--; // adjust for next agency row increment
            groups.push(group);
        }
    }
    return groups;
}

/**
 * Gets the sortValue of a cell within table.
 * @param {HTMLElement} cell with dataset.sortValue property
 * @returns sortValue of a cell
 */
function getSortValue(cell) {
    return cell.dataset.sortValue || cell.textContent.trim();
}

/**
 * Return the compare value based on asc/desc.
 * 
 * @param {HTMLElement} cellA 
 * @param {HTMLElement} cellB 
 * @param {boolean} ascending 
 * @returns compare value of 2 cell sortValues dependent on asc/desc
 */
function compareCells(cellA, cellB, ascending = true) {
    const valA = getSortValue(cellA);
    const valB = getSortValue(cellB);

    const isNumeric = !isNaN(valA) && !isNaN(valB);

    if (isNumeric) {
        return ascending ? valA - valB : valB - valA;
    } else {
        return ascending
            ? valA.localeCompare(valB)
            : valB.localeCompare(valA);
    }
}

/**
 * Sort the agency-wide table based on column and asc/desc order.
 * 
 * @param {number} columnIndex 
 * @param {boolean} ascending 
 */
function sortTable(columnIndex = Improper_Payment_Rate_Col_Num, ascending = false) {
    const agencyProgramGroups = getGroupedRows();
    
    agencyProgramGroups.sort((a, b) =>
        compareCells(a.agencyRow.cells[columnIndex], b.agencyRow.cells[columnIndex], ascending)
    );

    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";

    agencyProgramGroups.forEach(group => {
        tbody.append(group.agencyRow);

        // sort program rows
        group.programRows.sort((a, b) =>
            compareCells(a.cells[columnIndex], b.cells[columnIndex], ascending)
        );

        group.programRows.forEach(row => tbody.appendChild(row));
    })
}

/**
 * Updates aria-sort label on headers then calls sortTable to reorder table.
 * 
 * @param {number} columnIndex 
 */
function triggerSort(columnIndex = Improper_Payment_Rate_Col_Num) {
    const sortState = this.getAttribute('aria-sort');
    let ascending = false;

    // Clear aria-sort from all other column headers
    document.querySelectorAll('th[role="columnheader"]').forEach(otherTh => {
      if (otherTh.textContent !== this.textContent) {
        otherTh.removeAttribute('aria-sort');
      }
    });

    // Set aria-sort for current sort column
    if (sortState === 'descending') {
        this.setAttribute('aria-sort', 'ascending');
        ascending = true;
    } else {
        this.setAttribute('aria-sort', 'descending');
        ascending = false;
    }

    sortTable(columnIndex, ascending);
    applyAlternatingRowColors();
    paginateAgencies();
}

document.addEventListener('DOMContentLoaded', () => {
    renderProgramTags();

    // trigger sort on IP_Rate on page load
    const headers = document.querySelectorAll('th[role="columnheader"]');
    const improperPaymentHeader = headers[Improper_Payment_Rate_Col_Num];

    if (improperPaymentHeader) {
        triggerSort.call(improperPaymentHeader, Improper_Payment_Rate_Col_Num);
    }

    document.querySelectorAll('.expand-btn').forEach(button => {
        button.addEventListener('click', toggleCollapsedClass);
    });

    const comboBox = document.getElementById('agencies-programs-combobox');

    comboBox.addEventListener('change', applyFilter);

    document.querySelectorAll('th[role="columnheader"]').forEach((th, i) => {
        th.addEventListener("click", function () {
            triggerSort.call(this, i);
        });
    });

    // prevent tooltip from sorting on mobile
    const tooltips = document.getElementsByClassName("usa-tooltip");
    for (i = 0; i < tooltips.length; ++i) {
        tooltips[i].addEventListener('click', (event) => {
            event.stopPropagation();
        })
    }
});
