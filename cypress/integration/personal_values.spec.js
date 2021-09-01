/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";

let session_Id;
let set_one_quizId;
let set_two_quizId;

describe("'/personal_values' endpoint", () => {

    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                set_one_quizId = response.body.quizId;
            });
            cy.scoresEndpoint(scoresSetTwo, session_Id).should((response) => {
                set_two_quizId = response.body.quizId;
            });
        });
    });

    it("retreive the personal values for set_one_quizId scores", () => {
        cy.personalValuesEndpoint(set_one_quizId).should((response) => {
            expect(response.status).to.equal(200);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("personalValues");
            expect(response.body).to.have.property("valueScores");

            expect(response.body.personalValues).to.be.an("array");
            expect(response.body.valueScores).to.be.an("array");

            expect(response.body.personalValues).to.have.length(3);
            expect(response.body.valueScores).to.have.length(10);

            const { personalValues } = response.body;
            const { valueScores } = response.body;
            // P Values have all the right properties
            personalValues.forEach((value) => {
                expect(value).to.have.property("id");
                expect(value).to.have.property("description");
                expect(value).to.have.property("shortDescription");
                expect(value).to.have.property("name");
            });
            // Scores have all the right properties and valid values
            valueScores.forEach((score) => {
                expect(score).to.have.property("personalValue");
                expect(score).to.satisfy(function (s) {
                    const isValid =
                        typeof s.score === "number" && s.score >= 0 && s.score <= 10;
                    return isValid;
                });
            });
        });
    });

    it("retreive the personal values for set_two_quizId scores", () => {
        cy.personalValuesEndpoint(set_two_quizId).should((response) => {
            expect(response.status).to.equal(200);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("personalValues");
            expect(response.body).to.have.property("valueScores");

            expect(response.body.personalValues).to.be.an("array");
            expect(response.body.valueScores).to.be.an("array");

            expect(response.body.personalValues).to.have.length(3);
            expect(response.body.valueScores).to.have.length(10);

            const { personalValues } = response.body;
            const { valueScores } = response.body;
            // P Values have all the right properties
            personalValues.forEach((value) => {
                expect(value).to.have.property("id");
                expect(value).to.have.property("description");
                expect(value).to.have.property("shortDescription");
                expect(value).to.have.property("name");
            });
            // Scores have all the right properties and valid values
            valueScores.forEach((score) => {
                expect(score).to.have.property("personalValue");
                expect(score).to.satisfy(function (s) {
                    const isValid =
                        typeof s.score === "number" && s.score >= 0 && s.score <= 10;
                    return isValid;
                });
            });
        });
    })
});
