/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";

let session_Id;
let set_one_quizId;
let effectNameValue = "increase in flooding of land and property";

describe("'/get_actions' endpoint", () => {

    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                set_one_quizId = response.body.quizId;
            });
        });
    });

    it("should get actions", () => {
        cy.getActionsEndpoint(effectNameValue).should((response) => {
            expect(response.status).to.equal(200);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("actions");
            expect(response.body.actions).to.not.have.length(0);
        });
    });

    it("should get action with correct data", () => {
        cy.getActionsEndpoint(effectNameValue).should((response) => {
            const actions = response.body.actions;
            actions.forEach((actions) => {
                expect(actions).to.have.property("imageUrl");
                expect(actions).to.have.property("iri");
                expect(actions).to.have.property("longDescription");
                expect(actions).to.have.property("shortDescription");
                expect(actions).to.have.property("solutionSources");
                expect(actions).to.have.property("solutionSpecificMythIRIs");
                expect(actions).to.have.property("solutionTitle");
                expect(actions).to.have.property("solutionType");

                expect(actions.imageUrl).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(actions.iri).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(actions.longDescription).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(actions.shortDescription).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(actions.solutionSources).to.satisfy(function (s) {
                    return s === null || Array.isArray(s)
                });
                expect(actions.solutionSpecificMythIRIs).to.satisfy(function (s) {
                    return s === null || Array.isArray(s)
                });
                expect(actions.solutionTitle).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(actions.solutionType).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
            });
        });
    });
});
