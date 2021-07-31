/// <reference types="cypress" />

describe("/session", () => {
    it("response of session endpoint should have a quizId", () => {
        cy.request("POST", "http://localhost:5000/session").should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("sessionId");
            expect(response.body.sessionId).to.be.a("string");
        });
    });
});
