const fs = require('fs');
const yaml = require('js-yaml');

describe('Test: index', () => {
  const testUrl = 'test/index.html';

  it('should load the test page', () => {
    cy.visit(testUrl);
    cy.get('body').should('be.visible');
    cy.get('#main-content').should('exist');
  });

  it('should render the main header section with correct heading', () => {
    cy.visit(testUrl);
    
    // Check for the index-header-section
    cy.get('.index-header-section').should('exist');
    
    // Assert the main h1 heading from index.html layout
    cy.get('.index-header-text h1')
      .should('contain', 'A gateway to data on the accuracy of federal payments.');
    
    // Assert the h2 subtitle
    cy.get('.index-header-text h2')
      .should('contain', 'PaymentAccuracy.gov compiles and synthesizes');
  });
  
  it('should render the "Government-wide trends" section', () => {
    cy.visit(testUrl);
    
    // Check for spending trends section
    cy.get('.spending-trends-section').should('exist');
    
    // Assert the section header
    cy.get('.spending-trends-header')
      .should('contain', 'Government-wide trends');
    
    // Check for the three sparkline chart cards
    cy.get('.spending-trends-cards .usa-card').should('have.length', 3);
  });

  it('should render payment accuracy rate chart with correct data', () => {
    cy.visit(testUrl);
    
    // Find the card containing "Payment accuracy rate"
    cy.contains('.usa-card', 'Payment accuracy rate').should('exist');
    
    // Verify the chart title
    cy.contains('.usa-card', 'Payment accuracy rate')
      .within(() => {
        cy.contains('Payment accuracy rate').should('exist');
      });
  });

  it('should render improper payments rate chart', () => {
    cy.visit(testUrl);
    
    // Find the card containing "Improper payments rate"
    cy.contains('.usa-card', 'Improper payments rate').should('exist');
  });

  it('should render unknown payments rate chart', () => {
    cy.visit(testUrl);
    
    // Find the card containing "Unknown payments rate"
    cy.contains('.usa-card', 'Unknown payments rate').should('exist');
  });

  it('should render the data-driven insights card', () => {
    cy.visit(testUrl);
    
    // Check for the data-driven-card
    cy.get('.data-driven-card').should('exist');
    
    // Assert the h4 heading
    cy.get('.data-driven-card h4')
      .should('contain', 'Data-driven insights on how federal agencies are spending taxpayers dollars.');
    
    // Assert the h5 description
    cy.get('.data-driven-card h5')
      .should('contain', 'Effective stewardship of taxpayer dollars');
  });

  it('should render "Agency trends" section', () => {
    cy.visit(testUrl);
    
    // Check for agency trends section
    cy.get('.agency-trends-section').should('exist');
    
    // Assert section header
    cy.get('.agency-trends-section h4')
      .should('contain', 'Agency trends');
    
    // Assert description paragraph
    cy.get('.agency-trends-section p')
      .should('contain', 'A look at if federal agencies are meeting targets');
  });

  it('should render highest performing agencies table with correct data from markdown', () => {
    cy.visit(testUrl);
    
    // Check for highest performing agencies section
    cy.contains('h5', 'Highest performing agencies').should('exist');
    
    // Check for the table
    cy.get('.top-performing-table').should('exist');
    
    // Verify table headers
    cy.get('.top-performing-table thead').within(() => {
      cy.contains('th', 'Agency').should('exist');
      cy.contains('th', 'High priority program(s)').should('exist');
      cy.contains('th', 'Improper payment percentage').should('exist');
    });

    // Verify top performing agencies
    cy.get('.top-performing-table tbody tr:nth-child(1)').within(() => {
      cy.contains('.agency-name', 'Test Agency').should('exist');
      cy.contains('.target-met-cell', '0.0%');
    });

    cy.get('.top-performing-table tbody tr:nth-child(2').within(() => {
      cy.contains('.agency-name', 'Demo Department').should('exist');
      cy.contains('.target-met-cell', '0.5%');
    });

    // Verify lowest performing agencies
    cy.get('.declining-table tbody tr:nth-child(1)').within(() => {
      cy.contains('.agency-name', 'Sample Organization').should('exist');
      cy.contains('.target-met-cell', '15.0%');
    });

    cy.get('.declining-table tbody tr:nth-child(2').within(() => {
      cy.contains('.agency-name', 'Example Bureau').should('exist');
      cy.contains('.target-met-cell', '10.5%');
    });
  });

  it('should render "About the data" section', () => {
    cy.visit(testUrl);
    
    // Check for about data section
    cy.get('.about-data-section').should('exist');
    
    // Assert section header
    cy.get('.about-data-section h4')
      .should('contain', 'About the data');
    
    // Assert content paragraph
    cy.get('.about-data-section p')
      .should('contain', 'Payment Integrity Information Act of 2019');
    
    // Check for link to resources
    cy.get('.about-data-section a[href="/resources"]')
      .should('exist')
      .and('contain', 'here');
  });

  it('should have proper page structure and accessibility', () => {
    cy.visit(testUrl);
    
    // Check for main content role
    cy.get('#main-content[role="main"]').should('exist');
    
    // Check for proper heading hierarchy
    cy.get('h1').should('exist');
    cy.get('h2').should('exist');
    cy.get('h3, h4').should('exist');
    
    // Check for proper semantic structure
    cy.get('section').should('have.length.at.least', 2);
  });
});


