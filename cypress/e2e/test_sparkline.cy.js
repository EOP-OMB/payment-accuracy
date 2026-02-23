describe('Visual Regression: Sparkline Chart', () => {
  const testUrl = 'test/sparkline.html';

  beforeEach(() => {
    cy.visit(testUrl);
    // Wait for the chart to fully render
    cy.get('.spending-trends-cards .usa-card').should('be.visible');
    cy.wait(1000); // Allow time for animations/rendering
  });

  it('page should match', () => {
    cy.compareSnapshot('sparkline');
  });
});
