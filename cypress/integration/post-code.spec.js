/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";
import scoresAllTheSame from "../fixtures/postScoresAllSameAnswer.json";

let session_Id
let set_one_quizId;
let set_two_quizId;
let radomPostCode = Math.floor(Math.random() * 90000) + 10000;

describe(" '/post-code' endpoint", () => {
    it('response of /post-code endpoint should have a quizId', function () {
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
                }).then((response) => {
                    expect(response.status).to.equal(200);
                    cy.request({
                        method: 'POST',
                        url: "http://localhost:5000/post-code",
                        body: {
                            postCode: scores.zipCode,
                            quizId: set_one_quizId
                        }
                    }).should((response) => {
                        expect(response.status).to.equal(201);
                        expect(response.headers["content-type"]).to.equal("application/json");
                        expect(response.headers["access-control-allow-origin"])
                            .to.equal("*");
                        expect(response.body).to.be.a("object");
                        expect(response.body).to.have.property("message");
                        expect(response.body).to.have.property("postCode");
                        expect(response.body).to.have.property("quizId");
                        expect(response.body.quizId).to.be.a("string");
                    });

                });
            });
        });
    });
});
