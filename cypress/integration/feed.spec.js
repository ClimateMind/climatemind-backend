/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";
import scoresAllTheSame from "../fixtures/postScoresAllSameAnswer.json";

let session_Id
let set_one_quizId;
let set_two_quizId;


describe(" '/feed' endpoint", () => {
    it('should retreive the climate feed for scores', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: scores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },

            }).then((response) => {
                set_one_quizId = response.body.quizId;
                cy.request({
                    method: 'GET',
                    url: `http://localhost:5000/personal_values?quizId=${set_one_quizId}`,
                }).should((response) => {
                    expect(response.status).to.equal(200);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    //expect(response.body).to.have.property("climateEffects");
                    //expect(response.body.climateEffects).to.be.an("array");
                });
            });
        });
    });
    it('The retreived climate feed should be correct', function () {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/session',
        }).then(function (response) {
            session_Id = response.body.sessionId
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/scores',
                body: scores,
                headers: {
                    'content-type': 'application/json',
                    'X-Session-Id': session_Id
                },

            }).then((response) => {
                set_one_quizId = response.body.quizId;
                cy.request({
                    method: 'GET',
                    url: `http://localhost:5000/personal_values?quizId=${set_one_quizId}`,
                }).should((response) => {
                    for (var climateEffectionsIndex in response.body.climateEffects) {
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.be.an("object");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectDescription");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectId");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectScore");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectShortDescription");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectSolutions");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectSources");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectSpecificMythIRIs");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("effectTitle");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("imageUrl");
                        expect(response.body.climateEffects[climateEffectionsIndex]).to.have.property("isPossiblyLocal");

                        expect(response.body.climateEffects[climateEffectionsIndex].effectDescription).to.be.a("string");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectId).to.be.a("string");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectScore).to.be.a("number");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectShortDescription).to.be.a("string");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions).to.be.a("array");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectSources).to.be.an("array");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectSpecificMythIRIs).to.be.an("array");
                        expect(response.body.climateEffects[climateEffectionsIndex].effectTitle).to.be.a("string");
                        expect(response.body.climateEffects[climateEffectionsIndex].imageUrl).to.be.a("string");
                        expect(response.body.climateEffects[climateEffectionsIndex].isPossiblyLocal).to.be.a("number");


                        for (var effectSolutionsIndex in response.body.climateEffects[climateEffectionsIndex].effectSolutions) {
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("imageUrl");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("iri");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("longDescription");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("shortDescription");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("solutionSources");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("solutionSpecificMythIRIs");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("solutionTitle");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex]).to.have.property("solutionType");

                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].imageUrl).to.be.a("null");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].iri).to.be.a("string");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].longDescription).to.be.a("string");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].shortDescription).to.be.a("string");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].solutionSources).to.be.an("array");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].solutionSpecificMythIRIs).to.be.an("array");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].solutionTitle).to.be.a("string");
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSolutions[effectSolutionsIndex].solutionType).to.be.a("string");

                        }

                        for (var effectSourcesIndex in response.body.climateEffects[climateEffectionsIndex].effectSources) {
                            expect(response.body.climateEffects[climateEffectionsIndex].effectSources[effectSourcesIndex]).to.be.a("string");
                        }
                    }
                });
            });
        });
    });
});
