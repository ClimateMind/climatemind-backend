/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";

let session_Id;
const uuid_Format = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;

describe("'/scores' endpoint", () => {

    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        })
    });

    it("should post one set of scores", () => {
        cy.scoresEndpoint(scores, session_Id).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("quizId");
            expect(response.body.quizId).to.be.a("string");
            expect(response.body.quizId).to.match(uuid_Format);
        });
    });

    it("should post both sets of scores", () => {
        cy.scoresEndpoint(scoresSetTwo, session_Id).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("quizId");
            expect(response.body.quizId).to.be.a("string");
            expect(response.body.quizId).to.match(uuid_Format);
        });
    });
});
