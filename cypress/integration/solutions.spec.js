/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";

let session_Id;
let set_one_quizId;

describe("'/solutions' endpoint", () => {

    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                set_one_quizId = response.body.quizId;
            });
        });
    });

    it("should retreive the climate solution for scores", () => {
        cy.solutionsEndpoint().should((response) => {
            expect(response.status).to.equal(200);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("solutions");
            expect(response.body.solutions).to.be.an("array");
        });
    });

    it("should retreive correct climate solution data", () => {
        cy.solutionsEndpoint().should((response) => {
            for (var solutionIndex in response.body.solutions) {
                expect(response.body.solutions[solutionIndex]).to.be.an("object");
                expect(response.body.solutions[solutionIndex]).to.have.property("imageUrl");
                expect(response.body.solutions[solutionIndex]).to.have.property("iri");
                expect(response.body.solutions[solutionIndex]).to.have.property("longDescription");
                expect(response.body.solutions[solutionIndex]).to.have.property("shortDescription");
                expect(response.body.solutions[solutionIndex]).to.have.property("solutionCo2EqReduced");
                expect(response.body.solutions[solutionIndex]).to.have.property("solutionSources");
                expect(response.body.solutions[solutionIndex]).to.have.property("solutionSpecificMythIRIs");
                expect(response.body.solutions[solutionIndex]).to.have.property("solutionTitle");
                expect(response.body.solutions[solutionIndex]).to.have.property("solutionType");

                expect(response.body.solutions[solutionIndex].imageUrl).to.be.a("null");
                expect(response.body.solutions[solutionIndex].iri).to.be.a("string");
                expect(response.body.solutions[solutionIndex].longDescription).to.be.a("string");
                expect(response.body.solutions[solutionIndex].shortDescription).to.be.a("string");
                //expect(response.body.solutions[solutionIndex].solutionCo2EqReduced).to.be.a("number");
                expect(response.body.solutions[solutionIndex].solutionSources).to.be.an("array");
                expect(response.body.solutions[solutionIndex].solutionSpecificMythIRIs).to.be.a("array");
                expect(response.body.solutions[solutionIndex].solutionTitle).to.be.a("string");
                expect(response.body.solutions[solutionIndex].solutionType).to.be.a("string");

                for (var solutionSourcesIndex in response.body.solutions[solutionIndex].solutionSources) {
                    expect(response.body.solutions[solutionIndex].solutionSources[solutionSourcesIndex]).to.be.a("string");
                }

                for (var solutionSpecificMythIRIsIndex in response.body.solutions[solutionIndex].solutionSpecificMythIRIs) {
                    expect(response.body.solutions[solutionIndex].solutionSpecificMythIRIs[solutionSpecificMythIRIsIndex]).to.be.a("string");
                }
            }
        });
    });
});
