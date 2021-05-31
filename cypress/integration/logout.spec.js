/// <reference types="cypress" />

describe("/logout", () => {
  it("User can log out", () => {
    cy.request("POST", "http://localhost:5000/logout").should((response) => {
      expect(response.status).to.equal(200);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.headers["access-control-allow-origin"]).to.equal("*");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("message");
    });
  });
});
