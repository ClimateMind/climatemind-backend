/// <reference types="cypress" />

// Expected error responses
const badLoginMessage = "Wrong email or password. Try again.";
const invalidReqMessage =
  "Email and password must included in the request body";

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
