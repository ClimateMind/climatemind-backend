/// <reference types="cypress" />

describe("Solutions", () => {
  it("GET Solutions", () => {
    cy.request("http://localhost:5000/solutions").should((response) => {
      expect(response.status).to.equal(200);
    });
  });
});
