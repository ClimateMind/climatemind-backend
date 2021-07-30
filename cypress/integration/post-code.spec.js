/// <reference types="cypress" />
import scores from "../fixtures/postScores.json";

describe("/post-code", () => {
    it('response of /post-code endpoint should have a quizId', () => {
        cy.request("POST", "/scores", scores).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("quizId");
            expect(response.body.quizId).to.be.a("string");
        });
    });
});
